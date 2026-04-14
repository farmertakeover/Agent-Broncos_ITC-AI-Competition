"""LLM chat with tool calling (search_corpus, get_source_excerpt).

Default backend: Ollama via OpenAI-compatible /v1 API (no API key).
Optional: OpenAI cloud when CPP_ALLOW_OPENAI=true and CPP_LLM_BACKEND=openai.
"""
from __future__ import annotations

import json
import os
import re
from typing import Any

from openai import OpenAI

from app.services.ollama_client import (
    openai_client_cloud,
    openai_client_ollama,
    resolve_ollama_model_for_api,
)
from app.services import pulse as pulse_service
from retrieval import config
from retrieval.store import CorpusIndex, get_store

SYSTEM_PROMPT = """You are Agent Bronco, a Cal Poly Pomona campus assistant.
Rules:
- Answer using ONLY information from tool results (the markdown corpus). If tools return no relevant chunks or scores are weak, say clearly that the corpus does not contain enough information—do not guess dates, policies, or contacts.
- Use inline citations like [1], [2] only when search_corpus (or get_source_excerpt) tool results include those numbers in the same turn. If you did not receive tool results with chunks, do not use bracket citations.
- Be concise. Prefer bullet lists for multi-part answers.
- For follow-ups, stay consistent with prior user messages in the provided history."""


def _openai_api_key() -> str | None:
    k = (os.getenv("OPENAI_API_KEY") or "").strip()
    return k or None


def _resolve_client_and_model() -> tuple[OpenAI | None, str | None, str | None]:
    """
    Returns (client, model_name, error_code).
    error_code set => do not call the API.
    """
    if config.LLM_BACKEND == "openai":
        if not config.ALLOW_OPENAI:
            return None, None, "openai_disabled"
        key = _openai_api_key()
        if not key:
            return None, None, "missing_api_key"
        return openai_client_cloud(key), config.OPENAI_MODEL, None

    # Ollama (default): use exact installed tag (e.g. gemma3:4b), not bare gemma3 when only one variant is pulled.
    model, _note = resolve_ollama_model_for_api(config.OLLAMA_MODEL)
    return openai_client_ollama(), model, None


def _tools_schema() -> list[dict[str, Any]]:
    tools: list[dict[str, Any]] = [
        {
            "type": "function",
            "function": {
                "name": "search_corpus",
                "description": (
                    "Semantic search over Cal Poly Pomona official website content (markdown corpus). "
                    "Call this before answering factual questions about CPP."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query in natural language."},
                        "top_k": {
                            "type": "integer",
                            "description": f"Optional number of chunks (default {config.DEFAULT_TOP_K}, max {config.MAX_TOP_K}).",
                        },
                    },
                    "required": ["query"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_source_excerpt",
                "description": (
                    "Fetch a slightly larger excerpt for a chunk_id returned by search_corpus "
                    "when the snippet is insufficient."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "chunk_id": {"type": "string"},
                    },
                    "required": ["chunk_id"],
                },
            },
        },
    ]
    if config.PULSE_ENABLED:
        tools.append(
            {
                "type": "function",
                "function": {
                    "name": "get_student_pulse",
                    "description": (
                        "Read-only campus digest: weather snippet, public Reddit titles, academic dates, "
                        "and link-outs (not the official CPP corpus). Use for 'what's happening' questions; "
                        "still use search_corpus for policies and official CPP web content."
                    ),
                    "parameters": {"type": "object", "properties": {}, "required": []},
                },
            }
        )
    return tools


def _strip_orphan_citations(text: str, sources: list[dict[str, Any]]) -> str:
    """Remove [n] tokens when there are no sources (model hallucination) or trim extra spaces."""
    if sources:
        return text
    return re.sub(r"\s*\[\d+\]\s*", " ", text).strip()


def _execute_tool(
    name: str,
    arguments: dict[str, Any],
    store: CorpusIndex,
    source_state: dict[str, Any],
) -> tuple[str, list[dict[str, Any]]]:
    """Returns (json_string_for_tool_message, source_records_for_UI).

    source_state: {"seen_ids": set[str], "next_n": list[int]} — one global citation counter per turn
    so model-facing [n] matches the final sources list after dedupe.
    """
    seen_ids: set[str] = source_state["seen_ids"]
    next_n: list[int] = source_state["next_n"]

    def take_n() -> int:
        n = next_n[0]
        next_n[0] += 1
        return n

    sources: list[dict[str, Any]] = []
    if name == "search_corpus":
        q = (arguments.get("query") or "").strip()
        if not q:
            return json.dumps({"error": "empty query"}), []
        top_k = arguments.get("top_k")
        if top_k is not None:
            try:
                top_k = int(top_k)
            except (TypeError, ValueError):
                top_k = None
        hits = store.search(q, top_k=top_k)
        payload = []
        for h in hits:
            cid = h.chunk_id
            if cid in seen_ids:
                continue
            seen_ids.add(cid)
            n = take_n()
            rec = {
                "n": n,
                "chunk_id": cid,
                "score": round(h.score, 4),
                "source_path": h.source_path,
                "source_url": h.source_url,
                "heading": h.heading,
                "snippet": h.text,
                "start_line": h.start_line,
            }
            payload.append(rec)
            sources.append(rec)
        return json.dumps({"results": payload}, ensure_ascii=False), sources
    if name == "get_source_excerpt":
        cid = (arguments.get("chunk_id") or "").strip()
        ex = store.excerpt_around_chunk(cid)
        if not ex:
            return json.dumps({"error": "chunk not found"}), []
        if cid in seen_ids:
            return json.dumps(ex, ensure_ascii=False), []
        seen_ids.add(cid)
        sources.append(
            {
                "n": take_n(),
                "chunk_id": cid,
                "source_path": ex["source_path"],
                "source_url": ex.get("source_url"),
                "heading": ex.get("heading", ""),
                "snippet": ex["excerpt"],
                "start_line": ex.get("start_line", 0),
            }
        )
        return json.dumps(ex, ensure_ascii=False), sources
    if name == "get_student_pulse":
        payload = pulse_service.get_pulse_for_tool()
        return json.dumps(payload, ensure_ascii=False), []
    return json.dumps({"error": f"unknown tool {name}"}), []


def run_agent_turn(
    messages: list[dict[str, Any]],
    store: CorpusIndex | None = None,
) -> dict[str, Any]:
    """
    messages: OpenAI-style roles user/assistant/system (no tools in history from client).
    Returns dict with keys: content, sources, error, usage (optional), raw_finish_reason.
    """
    client, model, setup_err = _resolve_client_and_model()
    if setup_err == "openai_disabled":
        return {
            "content": (
                "Server misconfiguration: OpenAI backend is disabled. "
                "Set CPP_ALLOW_OPENAI=true only if you intend to use CPP_LLM_BACKEND=openai."
            ),
            "sources": [],
            "error": "openai_disabled",
        }
    if setup_err == "missing_api_key":
        return {
            "content": (
                "Server misconfiguration: CPP_LLM_BACKEND=openai requires OPENAI_API_KEY in `.env`."
            ),
            "sources": [],
            "error": "missing_api_key",
        }
    assert client is not None and model is not None

    store = store or get_store()
    try:
        store.ensure_loaded()
    except FileNotFoundError as e:
        return {
            "content": (
                "Search index is not built yet. Ask the operator to run "
                "`python scripts/build_index.py` from the repository root."
            ),
            "sources": [],
            "error": "index_missing",
            "detail": str(e),
        }

    sys = SYSTEM_PROMPT
    if config.PULSE_ENABLED:
        sys += (
            "\n- Optional tool get_student_pulse returns an unofficial digest (e.g. weather, public Reddit "
            "titles). Prefer search_corpus for official CPP policies and website facts."
        )
    api_messages: list[dict[str, Any]] = [
        {"role": "system", "content": sys},
        *messages,
    ]

    all_sources: list[dict[str, Any]] = []
    source_state: dict[str, Any] = {"seen_ids": set(), "next_n": [1]}
    usage_total: dict[str, int] = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

    tool_waves = 0
    max_waves = config.MAX_TOOL_ROUNDS

    def _record_usage(completion) -> None:
        u = completion.usage
        if u:
            usage_total["prompt_tokens"] += u.prompt_tokens or 0
            usage_total["completion_tokens"] += u.completion_tokens or 0
            usage_total["total_tokens"] += u.total_tokens or 0

    def _finalize(msg, completion) -> dict[str, Any]:
        text = _strip_orphan_citations((msg.content or "").strip(), all_sources)
        return {
            "content": text,
            "sources": list(all_sources),
            "usage": usage_total,
            "finish_reason": completion.choices[0].finish_reason,
        }

    try:
        while True:
            force_no_tools = tool_waves >= max_waves
            create_kw: dict[str, Any] = {
                "model": model,
                "messages": api_messages,
                "tools": _tools_schema(),
                "tool_choice": "none" if force_no_tools else "auto",
            }
            if config.LLM_BACKEND == "ollama":
                create_kw["temperature"] = 0.2
            elif config.OPENAI_CHAT_TEMPERATURE is not None:
                create_kw["temperature"] = config.OPENAI_CHAT_TEMPERATURE
            if config.LLM_BACKEND == "ollama" and config.OLLAMA_CHAT_NUM_CTX is not None:
                # Ollama-specific; lowers KV cache vs server default (helps tight-RAM hosts).
                create_kw["extra_body"] = {"num_ctx": config.OLLAMA_CHAT_NUM_CTX}
            completion = client.chat.completions.create(**create_kw)
            msg = completion.choices[0].message
            _record_usage(completion)

            if not msg.tool_calls:
                return _finalize(msg, completion)

            tool_waves += 1
            if tool_waves > max_waves:
                return {
                    "content": (
                        "The model tried to run more tools than allowed. "
                        "Please ask a narrower question or try again."
                    ),
                    "sources": all_sources,
                    "usage": usage_total,
                    "error": "max_tool_rounds",
                }

            api_messages.append(
                {
                    "role": "assistant",
                    "content": msg.content or "",
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {"name": tc.function.name, "arguments": tc.function.arguments},
                        }
                        for tc in msg.tool_calls
                    ],
                }
            )

            for tc in msg.tool_calls:
                name = tc.function.name
                try:
                    args = json.loads(tc.function.arguments or "{}")
                except json.JSONDecodeError:
                    args = {}
                out_json, srcs = _execute_tool(name, args, store, source_state)
                all_sources.extend(srcs)
                api_messages.append({"role": "tool", "tool_call_id": tc.id, "content": out_json})
    except Exception as e:
        detail = str(e)
        low = detail.lower()
        content = "The assistant could not complete this request. Please try again later."
        err_kind = "llm_error"
        if "connection error" in low or "connecterror" in low:
            if config.LLM_BACKEND == "ollama":
                content = (
                    "Could not connect to Ollama. Check OLLAMA_BASE_URL, confirm the Ollama server is reachable, "
                    "and if using Ollama Cloud ensure OLLAMA_API_KEY is set. See README 'Connection error' checks."
                )
            else:
                content = (
                    "Could not reach OpenAI. Check internet egress and verify OPENAI_API_KEY for CPP_LLM_BACKEND=openai."
                )
        if "system memory" in low or "more system memory" in low or "requires more system memory" in low:
            err_kind = "ollama_oom"
            content = (
                "Ollama refused to load the model: not enough free RAM for this tag. "
                "Restarting Flask does not fix this—you need a smaller model/quant, more memory, or swap. "
                "See README “Ollama out of memory”. Technical detail below."
            )
        return {
            "content": content,
            "sources": all_sources,
            "usage": usage_total,
            "error": err_kind,
            "detail": detail,
        }
