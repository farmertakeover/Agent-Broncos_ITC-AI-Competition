"""Central limits for retrieval, tool payloads, and chat (token-saving)."""
import os

# --- LLM (default: Ollama + OpenAI-compatible /v1; optional OpenAI cloud) ---


def _normalize_ollama_openai_base() -> str:
    raw = (
        os.getenv("OLLAMA_BASE_URL")
        or os.getenv("CPP_OLLAMA_BASE_URL")
        or "http://127.0.0.1:11434"
    ).rstrip("/")
    if raw.endswith("/v1"):
        return raw
    return raw + "/v1"


OLLAMA_OPENAI_BASE_URL = _normalize_ollama_openai_base()


def ollama_daemon_root() -> str:
    """Ollama HTTP root (no /v1) for /api/tags health checks."""
    u = OLLAMA_OPENAI_BASE_URL.rstrip("/")
    return u[:-3] if u.endswith("/v1") else u


LLM_BACKEND = os.getenv("CPP_LLM_BACKEND", "ollama").strip().lower()
if LLM_BACKEND not in ("ollama", "openai"):
    LLM_BACKEND = "ollama"

ALLOW_OPENAI = os.getenv("CPP_ALLOW_OPENAI", "false").lower() in ("1", "true", "yes")

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL") or os.getenv("CPP_OLLAMA_MODEL") or "gemma3:4b"

WHISPER_MODEL_SIZE = os.getenv("CPP_WHISPER_MODEL_SIZE", "base")

WHISPER_WARMUP = os.getenv("CPP_WHISPER_WARMUP", "false").lower() in ("1", "true", "yes")

# Student pulse (n8n / static JSON); see integrations/pulse_schema.json
PULSE_ENABLED = os.getenv("CPP_ENABLE_PULSE_TOOL", "false").lower() in ("1", "true", "yes")
PULSE_URL = (os.getenv("CPP_PULSE_URL") or "").strip()
PULSE_INGEST_SECRET = os.getenv("CPP_PULSE_INGEST_SECRET", "")

# Embedding model (local, no per-query API cost)
EMBEDDING_MODEL = os.getenv("CPP_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# Optional cross-encoder rerank (Phase 2)
RERANKER_MODEL = os.getenv("CPP_RERANKER_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2")
USE_RERANKER = os.getenv("CPP_USE_RERANKER", "true").lower() in ("1", "true", "yes")

# FAISS retrieval widens before rerank
FAISS_PREFETCH_K = int(os.getenv("CPP_FAISS_PREFETCH_K", "24"))
# After rerank (or raw FAISS if rerank off)
DEFAULT_TOP_K = int(os.getenv("CPP_DEFAULT_TOP_K", "6"))
MAX_TOP_K = int(os.getenv("CPP_MAX_TOP_K", "10"))

# Chunks returned to the LLM (truncate body)
MAX_CHUNK_CHARS = int(os.getenv("CPP_MAX_CHUNK_CHARS", "800"))
EXCERPT_WINDOW_CHARS = int(os.getenv("CPP_EXCERPT_WINDOW_CHARS", "1200"))

# Index paths (built by scripts/build_index.py)
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PULSE_FILE = os.path.abspath(
    os.getenv("CPP_PULSE_FILE", os.path.join(REPO_ROOT, "_data", "pulse", "latest.json"))
)
# Underscore prefix avoids a top-level `data/` folder (confusing vs cpp.edu /data/... URLs in the corpus).
DEFAULT_CORPUS_DIR = os.path.join(REPO_ROOT, "_data", "Corpus", "itc2026_ai_corpus")
CORPUS_DIR = os.path.abspath(os.getenv("CPP_CORPUS_DIR", DEFAULT_CORPUS_DIR))
INDEX_DIR = os.path.abspath(os.getenv("CPP_INDEX_DIR", os.path.join(REPO_ROOT, "_data", "index")))

INDEX_NAME = "cpp_corpus"
FAISS_PATH = os.path.join(INDEX_DIR, f"{INDEX_NAME}.faiss")
META_PATH = os.path.join(INDEX_DIR, f"{INDEX_NAME}.meta.jsonl")
URL_MAP_PATH = os.path.join(INDEX_DIR, "url_map.json")

# OpenAI (only when CPP_LLM_BACKEND=openai and CPP_ALLOW_OPENAI=true)
OPENAI_MODEL = os.getenv("CPP_OPENAI_MODEL", "gpt-5-mini")
# Many newer OpenAI models reject non-default temperature; leave unset to omit the param (API default).
_ot = (os.getenv("CPP_OPENAI_TEMPERATURE") or "").strip()
OPENAI_CHAT_TEMPERATURE: float | None
try:
    OPENAI_CHAT_TEMPERATURE = float(_ot) if _ot else None
except ValueError:
    OPENAI_CHAT_TEMPERATURE = None
MAX_TOOL_ROUNDS = int(os.getenv("CPP_MAX_TOOL_ROUNDS", "2"))
MAX_CONVERSATION_MESSAGES = int(os.getenv("CPP_MAX_CONVERSATION_MESSAGES", "10"))

# Ollama OpenAI-compat: caps KV cache RAM (lower = less peak RAM during long prompts). Unset = server default.
# See https://github.com/ollama/ollama — num_ctx / context_length on chat completions.
_ctx = (os.getenv("CPP_OLLAMA_NUM_CTX") or os.getenv("CPP_LLM_NUM_CTX") or "").strip()
OLLAMA_CHAT_NUM_CTX: int | None
if _ctx.isdigit() and int(_ctx) > 0:
    OLLAMA_CHAT_NUM_CTX = int(_ctx)
else:
    OLLAMA_CHAT_NUM_CTX = None

# --- Homepage dashboard (/api/dashboard): RSS/ICS + pulse ---
# If CPP_DASHBOARD_RSS_NEWS is unset, app/services/dashboard.py falls back to this public CPP news feed.
DEFAULT_DASHBOARD_RSS_NEWS = "https://polycentric.cpp.edu/feed/"
# Public MyBar ICS (student org / campus events). Override with CPP_DASHBOARD_MYBAR_ICS="" to disable.
DEFAULT_DASHBOARD_MYBAR_ICS = "https://mybar.cpp.edu/events.ics"
