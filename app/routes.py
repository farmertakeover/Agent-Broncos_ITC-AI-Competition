from __future__ import annotations
from flask import Blueprint, jsonify, render_template, request, session
from app.database import (
    ack_chat_recovery,
    get_chat_recovery,
    get_history,
    save_message,
    store_chat_recovery,
)
import uuid
import os
import secrets
import urllib.error
import urllib.request
from datetime import datetime, timezone
from time import perf_counter

from app import analytics
from app.corpus_overview import corpus_prefix_counts
from app.services.chat import run_agent_turn
from app.services import pulse as pulse_service
from app.services import dashboard as dashboard_service
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
from app.translator import (
    LangblyError,
    TranslatorConfigError,
    translate_entries,
    translate_text,
)
from app.weather import WeatherAPIError, WeatherConfigError, get_weather
from retrieval import config
from retrieval.store import get_store

bp = Blueprint("main", __name__)


def _trim_history(history: list, max_msgs: int) -> list:
    if len(history) <= max_msgs:
        return history
    return history[-max_msgs:]


def _slim_chat_sources(raw: object, max_items: int = 16) -> list[dict]:
    if not isinstance(raw, list):
        return []
    keys = ("chunk_id", "source_path", "title", "url", "score")
    out: list[dict] = []
    for s in raw[:max_items]:
        if not isinstance(s, dict):
            continue
        row: dict = {}
        for k in keys:
            if k not in s:
                continue
            v = s.get(k)
            if isinstance(v, (str, int, float, bool)) or v is None:
                row[k] = v
        if row:
            out.append(row)
    return out


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
    key = (os.getenv("OPENAI_API_KEY") or "").strip()
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
        "langbly_configured": bool((os.getenv("Agent_Broncos_Language_Translation") or "").strip()),
        "openweather_configured": bool((os.getenv("Agent_Broncos_Weather_API") or "").strip()),
        "dashboard_default_rss_configured": bool((config.DEFAULT_DASHBOARD_RSS_NEWS or "").strip()),
        "dashboard_default_mybar_ics_configured": bool((getattr(config, "DEFAULT_DASHBOARD_MYBAR_ICS", "") or "").strip()),
        "dashboard_skip_remote": os.getenv("CPP_DASHBOARD_SKIP_REMOTE", "").lower() in ("1", "true", "yes"),
        "pulse_reddit_live_fetch": os.getenv("CPP_PULSE_REDDIT_LIVE_FETCH", "true").lower() in ("1", "true", "yes"),
    }
    if config.WHISPER_WARMUP:
        schedule_whisper_warmup_background()
        body["whisper_warmup_scheduled"] = True
    if config.LLM_BACKEND == "openai" and config.ALLOW_OPENAI:
        placeholder = "replace_with_your_openai_api_key"
        body["openai_configured"] = bool(key) and key != placeholder
        body["openai_key_is_placeholder"] = bool(key) and key == placeholder
    return jsonify(body)


@bp.route("/weather", methods=["GET"])
@bp.route("/api/weather", methods=["GET"])
def weather_route():
    city = (request.args.get("city") or "Pomona").strip() or "Pomona"
    try:
        data = get_weather(city)
        return jsonify(data)
    except WeatherConfigError as e:
        return jsonify({"error": "weather_not_configured", "detail": str(e)}), 503
    except WeatherAPIError as e:
        return jsonify({"error": "weather_failed", "detail": str(e)}), 502


@bp.route("/translate", methods=["POST"])
@bp.route("/api/translate", methods=["POST"])
def translate_route():
    t0 = perf_counter()
    data = request.get_json(silent=True) or {}
    text = data.get("text")
    target = data.get("target", "en")
    if not isinstance(text, str) or not text.strip():
        return jsonify({"error": "missing_text", "detail": "JSON body must include non-empty string field 'text'."}), 400
    if not isinstance(target, str) or not target.strip():
        return jsonify({"error": "invalid_target", "detail": "Field 'target' must be a non-empty language code string."}), 400
    try:
        translated = translate_text(text, target.strip())
        elapsed_ms = int((perf_counter() - t0) * 1000)
        resp = jsonify(
            {
                "original": text,
                "translated": translated,
                "target": target.strip(),
                "metrics": {"translate_ms": elapsed_ms},
            }
        )
        resp.headers["Server-Timing"] = f"translate;dur={elapsed_ms}"
        return resp
    except TranslatorConfigError as e:
        return jsonify({"error": "translate_not_configured", "detail": str(e)}), 503
    except ValueError as e:
        return jsonify({"error": "invalid_input", "detail": str(e)}), 400
    except LangblyError as e:
        return jsonify(
            {
                "error": "langbly_error",
                "detail": str(e),
                "code": getattr(e, "code", "") or "",
                "status_code": getattr(e, "status_code", 0) or 0,
            }
        ), 502


@bp.route("/translate/batch", methods=["POST"])
@bp.route("/api/translate/batch", methods=["POST"])
def translate_batch_route():
    """Batch UI translation: JSON ``{ \"target\": \"es\", \"entries\": { \"key\": \"English…\" } }``."""
    t0 = perf_counter()
    data = request.get_json(silent=True) or {}
    target = (data.get("target") or "en").strip() or "en"
    entries = data.get("entries")
    if not isinstance(entries, dict) or not entries:
        return jsonify({"error": "missing_entries", "detail": "Body must include object field 'entries'."}), 400
    if len(entries) > 80:
        return jsonify({"error": "too_many_entries", "detail": "Maximum 80 keys per request."}), 400
    for k, v in entries.items():
        if not isinstance(k, str) or not isinstance(v, str):
            return jsonify({"error": "invalid_entries", "detail": "All keys and values must be strings."}), 400
    try:
        out = translate_entries(entries, target)
        elapsed_ms = int((perf_counter() - t0) * 1000)
        resp = jsonify({"target": target, "entries": out, "metrics": {"translate_batch_ms": elapsed_ms}})
        resp.headers["Server-Timing"] = f"translate_batch;dur={elapsed_ms}"
        return resp
    except TranslatorConfigError as e:
        return jsonify({"error": "translate_not_configured", "detail": str(e)}), 503
    except ValueError as e:
        return jsonify({"error": "invalid_input", "detail": str(e)}), 400
    except LangblyError as e:
        return jsonify(
            {
                "error": "langbly_error",
                "detail": str(e),
                "code": getattr(e, "code", "") or "",
                "status_code": getattr(e, "status_code", 0) or 0,
            }
        ), 502


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
        rt = transcribe_runtime_status()
        issues = list(rt.get("issues") or [])
        if issues:
            detail = "Server STT unavailable: " + "; ".join(issues)
        else:
            detail = "Transcription failed (audio decode or model error). Check server logs."
        return jsonify({"error": err, "detail": detail}), 502
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


@bp.route("/api/dashboard", methods=["GET"])
def api_dashboard():
    """Unified homepage dashboard: official RSS/ICS and Student Pulse."""
    prefs = session.get("dashboard_prefs")
    if not isinstance(prefs, dict):
        prefs = None
    return jsonify(dashboard_service.build_dashboard(prefs=prefs))


@bp.route("/api/dashboard/preferences", methods=["POST"])
def api_dashboard_preferences():
    """Server-side dashboard widget prefs (session); optional complement to localStorage."""
    data = request.get_json(silent=True) or {}
    if not isinstance(data, dict):
        return jsonify({"error": "invalid_json"}), 400
    cur = session.get("dashboard_prefs")
    base = dict(cur) if isinstance(cur, dict) else {}
    if isinstance(data.get("order"), list):
        base["order"] = [str(x) for x in data["order"][:50] if isinstance(x, str)]
    if isinstance(data.get("hidden"), list):
        base["hidden"] = [str(x) for x in data["hidden"][:50] if isinstance(x, str)]
    if isinstance(data.get("tags"), list):
        base["tags"] = [str(x) for x in data["tags"][:20] if isinstance(x, str)]
    session["dashboard_prefs"] = base
    session.modified = True
    return jsonify({"ok": True, "preferences": base})


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


@bp.route("/api/chat/recovery", methods=["GET"])
def api_chat_recovery():
    """Return the last completed assistant turn for this chat session (peek; ack to clear)."""
    sid = (request.args.get("session_id") or "").strip()
    row = get_chat_recovery(sid) if sid else None
    if not row or not (row.get("content") or "").strip():
        return jsonify({"has_recovery": False})
    return jsonify(
        {
            "has_recovery": True,
            "recovery_id": row.get("recovery_id"),
            "user_message_en": row.get("user_message_en"),
            "content": row.get("content"),
            "sources": row.get("sources") or [],
            "usage": row.get("usage") or {},
            "error": row.get("error"),
        }
    )


@bp.route("/api/chat/recovery/ack", methods=["POST"])
def api_chat_recovery_ack():
    data = request.get_json(silent=True) or {}
    sid = (data.get("session_id") or "").strip()
    rid = (data.get("recovery_id") or "").strip()
    ack_chat_recovery(sid, rid)
    return jsonify({"ok": True})


@bp.route("/api/chat", methods=["POST"])
def api_chat():
    t0 = perf_counter()
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

    session_id = data.get("session_id") or str(uuid.uuid4())
    save_message(session_id, "user", user_msg)

    analytics.record_chat_start()
    out = run_agent_turn(openai_msgs)
    llm_elapsed_ms = int((perf_counter() - t0) * 1000)

    if not out.get("error"):
        save_message(session_id, "assistant", out.get("content", ""))
    if (out.get("content") or "").strip() or not out.get("error"):
        store_chat_recovery(
            session_id,
            user_message_en=user_msg,
            content=str(out.get("content") or ""),
            sources=_slim_chat_sources(out.get("sources")),
            usage=out.get("usage") if isinstance(out.get("usage"), dict) else None,
            error=out.get("error") if isinstance(out.get("error"), str) else None,
        )
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
    out["session_id"] = session_id
    out["metrics"] = {"chat_ms": llm_elapsed_ms}
    resp = jsonify(out)
    resp.status_code = status
    resp.headers["Server-Timing"] = f"chat;dur={llm_elapsed_ms}"
    return resp


@bp.route("/api/history", methods=["GET"])
def api_history():
    sid = request.args.get("session_id")
    if not sid:
        return jsonify([])
    messages = get_history(sid)
    return jsonify([{"role": m["role"], "content": m["content"]} for m in messages])
