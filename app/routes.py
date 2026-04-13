from __future__ import annotations

import os
import secrets
import urllib.error
import urllib.request
from datetime import datetime, timezone

from flask import Blueprint, jsonify, render_template, request

from app import analytics
from app.corpus_overview import corpus_prefix_counts
from app.services.chat import run_agent_turn
from app.services import pulse as pulse_service
from app.services.ollama_client import (
    fetch_ollama_version,
    get_cached_ollama_model_names,
    ollama_daemon_auth_headers,
    ollama_model_tag_present,
    resolve_ollama_model_for_api,
)
from app.services.transcribe import (
    schedule_whisper_warmup_background,
    transcribe_upload,
    transcribe_runtime_status,
    whisper_model_cached,
)
from retrieval import config
from retrieval.store import get_store

bp = Blueprint("main", __name__)


def _trim_history(history: list, max_msgs: int) -> list:
    if len(history) <= max_msgs:
        return history
    return history[-max_msgs:]


@bp.route("/")
def home():
    built = os.path.isfile(config.FAISS_PATH)
    return render_template(
        "index.html",
        index_ready=built,
        index_built_at=datetime.now(timezone.utc).strftime("%Y-%m-%d") if built else None,
    )


@bp.route("/corpus-map")
def corpus_map_page():
    return render_template("corpus_map.html")


@bp.route("/pulse")
def pulse_page():
    return render_template("pulse.html")


@bp.route("/api/corpus-overview", methods=["GET"])
def api_corpus_overview():
    """
    Topic buckets from filenames (file counts per prefix). For UI map only.
    Retrieval uses FAISS vector search, not this graph.
    """
    nodes, edges = corpus_prefix_counts()
    return jsonify(
        {
            "nodes": nodes,
            "edges": edges,
            "retrieval": "faiss_vector_rag",
            "note": (
                "Answers use FAISS + embeddings (vector RAG), not graph RAG. "
                "This map is a structural overview of crawled page filenames."
            ),
        }
    )


@bp.route("/chat")
def chat_page():
    built = os.path.isfile(config.FAISS_PATH)
    return render_template(
        "chat.html",
        index_ready=built,
        starter_questions=[
            "What is Billy Chat and how do I use it?",
            "Where can I find the academic calendar?",
            "How do I contact the Bronco Advising Center?",
            "What are impacted majors for freshmen?",
            "How does parking work for visitors?",
        ],
    )


def _ollama_reachable() -> bool:
    root = config.ollama_daemon_root()
    try:
        req = urllib.request.Request(
            f"{root.rstrip('/')}/api/tags",
            headers=ollama_daemon_auth_headers(),
        )
        with urllib.request.urlopen(req, timeout=2) as resp:
            code = getattr(resp, "status", None) or resp.getcode()
            return 200 <= int(code) < 300
    except (urllib.error.URLError, OSError, TimeoutError, ValueError):
        return False


@bp.route("/api/health", methods=["GET"])
def api_health():
    ollama_ok = _ollama_reachable()
    key = os.getenv("Agent_Broncos_API_Key") or os.getenv("OPENAI_API_KEY")
    ollama_names: list[str] | None = None
    ollama_tags_error: str | None = None
    ollama_model_present: bool | None = None
    ollama_model_for_api: str | None = None
    ollama_model_resolution_note: str | None = None
    ollama_version: dict | None = None
    if config.LLM_BACKEND == "ollama" and ollama_ok:
        ollama_names, ollama_tags_error = get_cached_ollama_model_names()
        if ollama_names is not None:
            ollama_model_present = ollama_model_tag_present(config.OLLAMA_MODEL, ollama_names)
        resolved, res_note = resolve_ollama_model_for_api(config.OLLAMA_MODEL)
        ollama_model_for_api = resolved
        ollama_model_resolution_note = res_note
        ollama_version = fetch_ollama_version(config.ollama_daemon_root())

    body = {
        "ok": True,
        "index_ready": os.path.isfile(config.FAISS_PATH),
        "llm_backend": config.LLM_BACKEND,
        "ollama_model": config.OLLAMA_MODEL if config.LLM_BACKEND == "ollama" else None,
        "ollama_model_for_api": ollama_model_for_api,
        "ollama_model_resolution_note": ollama_model_resolution_note,
        "ollama_openai_base_url": config.OLLAMA_OPENAI_BASE_URL if config.LLM_BACKEND == "ollama" else None,
        "ollama_reachable": ollama_ok,
        "ollama_model_present": ollama_model_present,
        "ollama_tags_error": ollama_tags_error,
        "ollama_version": ollama_version,
        "ollama_host_is_cloud": "ollama.com" in config.ollama_daemon_root().lower(),
        "whisper_model_cached": whisper_model_cached(),
        "transcribe_runtime": transcribe_runtime_status(),
        "pulse_tool_enabled": config.PULSE_ENABLED,
    }
    if config.WHISPER_WARMUP:
        schedule_whisper_warmup_background()
        body["whisper_warmup_scheduled"] = True
    if config.LLM_BACKEND == "openai" and config.ALLOW_OPENAI:
        body["openai_configured"] = bool(key)
    return jsonify(body)


@bp.route("/api/transcribe", methods=["POST"])
def api_transcribe():
    """Multipart field `audio`: recorded webm/wav/etc. Returns JSON { text }."""
    f = request.files.get("audio")
    text, err = transcribe_upload(f)
    if err == "missing_file":
        return jsonify({"error": err, "detail": "Expected multipart file field 'audio'."}), 400
    if err == "empty_file":
        return jsonify({"error": err}), 400
    if err == "transcribe_failed":
        return jsonify({"error": err, "detail": "faster-whisper or ffmpeg may be missing; see README."}), 502
    return jsonify({"text": text or ""})


def _pulse_ingest_authorized() -> bool:
    expected = (config.PULSE_INGEST_SECRET or "").strip()
    if not expected:
        return False
    header = (request.headers.get("X-CPP-Pulse-Secret") or "").strip()
    auth = request.headers.get("Authorization") or ""
    token = header
    if auth.lower().startswith("bearer "):
        token = auth[7:].strip()
    if len(token) != len(expected):
        return False
    return secrets.compare_digest(token, expected)


@bp.route("/api/student-pulse", methods=["GET"])
def api_student_pulse():
    return jsonify(pulse_service.get_pulse_for_api())


@bp.route("/api/student-pulse/ingest", methods=["POST"])
def api_student_pulse_ingest():
    if not (config.PULSE_INGEST_SECRET or "").strip():
        return jsonify(
            {
                "error": "ingest_disabled",
                "detail": "Set CPP_PULSE_INGEST_SECRET in the environment to enable n8n ingest.",
            }
        ), 503
    if not _pulse_ingest_authorized():
        return jsonify(
            {
                "error": "unauthorized",
                "detail": "Send CPP_PULSE_INGEST_SECRET via Authorization: Bearer … or X-CPP-Pulse-Secret.",
            }
        ), 401
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "invalid_json"}), 400
    ok, err = pulse_service.ingest_payload(data)
    if not ok:
        return jsonify({"error": "write_failed", "detail": err}), 500
    return jsonify({"ok": True})


@bp.route("/api/stats", methods=["GET"])
def api_stats():
    """Anonymous usage counters (bonus analytics)."""
    return jsonify(analytics.snapshot())


@bp.route("/api/retrieve", methods=["GET"])
def api_retrieve():
    q = (request.args.get("q") or "").strip()
    if not q:
        return jsonify({"error": "missing q"}), 400
    top_k = request.args.get("top_k", type=int)
    analytics.record_retrieve()
    try:
        store = get_store()
        hits = store.search(q, top_k=top_k)
    except FileNotFoundError as e:
        return jsonify({"error": "index_missing", "detail": str(e)}), 503
    return jsonify(
        {
            "results": [
                {
                    "chunk_id": h.chunk_id,
                    "score": h.score,
                    "source_path": h.source_path,
                    "source_url": h.source_url,
                    "heading": h.heading,
                    "snippet": h.text,
                    "start_line": h.start_line,
                }
                for h in hits
            ]
        }
    )


@bp.route("/api/graph-context", methods=["POST"])
def api_graph_context():
    """Co-retrieved document graph for visualization (Phase 2)."""
    data = request.get_json(silent=True) or {}
    chunk_ids = data.get("chunk_ids") or []
    if not isinstance(chunk_ids, list) or not chunk_ids:
        return jsonify({"nodes": [], "edges": []})
    store = get_store()
    try:
        store.ensure_loaded()
    except FileNotFoundError:
        return jsonify({"error": "index_missing"}), 503
    hits = []
    for cid in chunk_ids[:20]:
        h = store.get_chunk_by_id(str(cid))
        if h:
            hits.append(h)
    g = store.graph_neighbors_for_hits(hits)
    return jsonify(g)


@bp.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json(silent=True) or {}
    user_msg = (data.get("message") or "").strip()
    history = data.get("history") or []
    if not user_msg:
        return jsonify({"error": "empty message"}), 400
    if not isinstance(history, list):
        return jsonify({"error": "invalid history"}), 400

    openai_msgs = []
    for item in _trim_history(history, config.MAX_CONVERSATION_MESSAGES):
        role = item.get("role")
        content = (item.get("content") or "").strip()
        if role not in ("user", "assistant") or not content:
            continue
        openai_msgs.append({"role": role, "content": content})
    openai_msgs.append({"role": "user", "content": user_msg})

    analytics.record_chat_start()
    out = run_agent_turn(openai_msgs)
    err = out.get("error")
    if err:
        # Always use an error-class status when `error` is set; body may still include `content`.
        if err in ("missing_api_key", "index_missing", "openai_disabled"):
            status = 503
        elif err in ("llm_error", "ollama_oom"):
            status = 502
        else:
            status = 500
        analytics.record_chat_outcome(ok=False)
    else:
        status = 200
        analytics.record_chat_outcome(ok=True)
    return jsonify(out), status
