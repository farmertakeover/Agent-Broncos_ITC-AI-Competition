"""HTTP client factory and Ollama daemon helpers (modular surface for chat + health)."""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from typing import Any

import httpx
from openai import OpenAI

from retrieval import config


def ollama_daemon_auth_headers() -> dict[str, str]:
    """Ollama Cloud (and some remotes) require Authorization: Bearer for /api/tags and /api/version."""
    token = (os.getenv("OLLAMA_API_KEY") or "").strip()
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}


# Short-lived cache so chat + health do not hammer /api/tags.
_tag_cache: tuple[float, list[str] | None, str | None] = (0.0, None, None)
_TAG_CACHE_TTL_SEC = float(os.getenv("CPP_OLLAMA_TAGS_CACHE_SEC", "30"))


def get_cached_ollama_model_names() -> tuple[list[str] | None, str | None]:
    """Returns (names, fetch_error). Uses in-memory TTL cache."""
    global _tag_cache
    now = time.monotonic()
    ts, names, err = _tag_cache
    if names is not None and (now - ts) < _TAG_CACHE_TTL_SEC:
        return names, err
    root = config.ollama_daemon_root()
    names, err = fetch_ollama_model_names(root)
    _tag_cache = (now, names, err)
    return names, err


def resolve_ollama_model_for_api(requested: str) -> tuple[str, str | None]:
    """
    Ollama OpenAI API requires an installed tag (e.g. gemma4:e2b), not always the library alias (gemma4).

    Returns (model_name_for_api, resolution_note).
    - Exact match to an installed name -> use it.
    - Exactly one installed model shares the same base name (before ':') -> use that tag (fixes gemma4 vs gemma4:e2b).
    - Zero or multiple base matches without exact match -> return requested unchanged (may 404); note explains.
    """
    req = (requested or "").strip()
    if not req:
        return req, None
    names, _err = get_cached_ollama_model_names()
    if not names:
        return req, None
    if req in names:
        return req, None
    base = req.split(":")[0]
    same_base = [n for n in names if n.split(":")[0] == base]
    if len(same_base) == 1:
        chosen = same_base[0]
        if chosen != req:
            return chosen, f"resolved {req!r} -> {chosen!r} (only installed variant for this base name)"
        return chosen, None
    if len(same_base) > 1:
        return req, (
            f"multiple tags share base {base!r}: {same_base}; set OLLAMA_MODEL to the full tag from `ollama list`"
        )
    return req, None


def llm_http_timeout() -> httpx.Timeout:
    return httpx.Timeout(
        connect=float(os.getenv("CPP_LLM_CONNECT_TIMEOUT", "10")),
        read=float(os.getenv("CPP_LLM_READ_TIMEOUT", "120")),
        write=float(os.getenv("CPP_LLM_WRITE_TIMEOUT", "60")),
        pool=5.0,
    )


def llm_max_retries() -> int:
    return int(os.getenv("CPP_LLM_MAX_RETRIES", "0"))


def openai_client_ollama() -> OpenAI:
    return OpenAI(
        base_url=config.OLLAMA_OPENAI_BASE_URL,
        api_key=os.getenv("OLLAMA_API_KEY", "ollama"),
        timeout=llm_http_timeout(),
        max_retries=llm_max_retries(),
    )


def openai_client_cloud(api_key: str) -> OpenAI:
    return OpenAI(
        api_key=api_key,
        timeout=llm_http_timeout(),
        max_retries=max(llm_max_retries(), 0),
    )


def fetch_ollama_version(root: str, timeout_sec: float = 2.0) -> dict[str, Any] | None:
    """GET /api/version from Ollama daemon (for health / support)."""
    url = f"{root.rstrip('/')}/api/version"
    try:
        req = urllib.request.Request(url, headers=ollama_daemon_auth_headers())
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
        data = json.loads(raw)
        return data if isinstance(data, dict) else None
    except (urllib.error.URLError, OSError, TimeoutError, ValueError, json.JSONDecodeError):
        return None


def fetch_ollama_model_names(root: str, timeout_sec: float = 3.0) -> tuple[list[str] | None, str | None]:
    """Returns (tag_names, error_message)."""
    url = f"{root.rstrip('/')}/api/tags"
    try:
        req = urllib.request.Request(url, headers=ollama_daemon_auth_headers())
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
        data: dict[str, Any] = json.loads(raw)
        models = data.get("models") or []
        names: list[str] = []
        for m in models:
            if isinstance(m, dict):
                n = m.get("name")
                if isinstance(n, str) and n:
                    names.append(n)
        return names, None
    except (urllib.error.URLError, OSError, TimeoutError, ValueError, json.JSONDecodeError) as e:
        return None, str(e)


def ollama_model_tag_present(requested: str, installed: list[str]) -> bool:
    """Match OLLAMA_MODEL to Ollama list names (handles :latest and base name)."""
    req = (requested or "").strip()
    if not req:
        return False
    req_base = req.split(":")[0]
    for n in installed:
        if n == req:
            return True
        if n.split(":")[0] == req_base:
            return True
    return False
