# Agent Broncos — Cal Poly Pomona ITC AI Competition

Flask web app with **local Ollama** (OpenAI-compatible `/v1` API) for tool calling, plus a **local FAISS** index over the CPP markdown corpus. Optional **OpenAI** cloud is off unless you explicitly enable it.

Everything lives under **`_data/`** (underscore avoids a bare `data/` folder, which is easy to confuse with CPP site paths like `/data/...` in the crawl):

| Path | Contents |
|------|----------|
| `_data/Corpus/itc2026_ai_corpus/` | Source markdown + `index.json` (tracked) |
| `_data/index/` | Generated FAISS index (gitignored; large binaries) |
| `_data/golden_questions.json` | Retrieval eval questions (tracked) |
| `_data/eval_results.json` | Output of `golden_eval.py` (gitignored) |

## Setup

```bash
cd /workspaces/Brono-Agents-ITC-AI-Competition
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### Ollama (default)

1. Install and start [Ollama](https://ollama.com).
2. Pull **Gemma 4** (good tool-use / agent workflows per [Google’s Gemma 4 line](https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/)). Ollama’s library is [`gemma4`](https://ollama.com/library/gemma4); tags include `gemma4`, `gemma4:e2b`, `gemma4:e4b`, `gemma4:26b`, `gemma4:31b`—pick one that fits RAM/VRAM, then confirm with `ollama list`:

   ```bash
   ollama pull gemma4
   ```

   For running or quantizing GGUFs outside Ollama, see [Unsloth — Gemma 4 (local + fine-tuning)](https://unsloth.ai/docs/models/gemma-4).

3. Optional env (see `.env.example`):

   - `OLLAMA_BASE_URL` — default `http://127.0.0.1:11434` (the app appends `/v1` for the OpenAI client).
   - `OLLAMA_MODEL` — default `gemma4` (must match the tag you pulled, e.g. `gemma4:e4b`).

**TurboQuant / KV cache:** Configure on the **Ollama server process** (not in Flask). See current Ollama release notes for variables such as `OLLAMA_KV_CACHE_TYPE` and supported modes on your engine build.

### Speech-to-text (optional)

Chat can **record audio in the browser** and send it to **`POST /api/transcribe`**, which runs **faster-whisper** on the server. Install **ffmpeg** on the host so decoding WebM/Opus works. Tune with `CPP_WHISPER_MODEL_SIZE` (default `base`; use `tiny` for faster dev), `CPP_WHISPER_DEVICE`, `CPP_WHISPER_COMPUTE_TYPE`. Set **`CPP_WHISPER_WARMUP=true`** to load the Whisper model in a background thread when **`GET /api/health`** is hit (reduces “stuck transcribing” on first mic use).

Browser-side transcribe requests **abort after 180 seconds**; extend the limit in `static/js/chat.js` (`TRANSCRIBE_FETCH_MS`) if needed.

### OpenAI cloud (optional)

Only if you set **`CPP_ALLOW_OPENAI=true`** and **`CPP_LLM_BACKEND=openai`**, provide **`Agent_Broncos_API_Key`** or **`OPENAI_API_KEY`**.

### Build the index

```bash
# Full corpus (can take a long time)
python scripts/build_index.py

# Optional: only first N files while developing
python scripts/build_index.py --limit-files 200
```

The script prints resolved **corpus** and **index** paths first; confirm they point at `_data/...` before waiting on embeddings.

If Hugging Face downloads fail, set a token (`HF_TOKEN`) or use an environment where `huggingface_hub` can reach the hub; after the embedding model is cached, rebuilds are mostly offline-friendly.

Override paths with `CPP_CORPUS_DIR` / `CPP_INDEX_DIR` if needed (see `retrieval/config.py`).

Run the app:

```bash
python run.py
```

Open `http://127.0.0.1:5000/chat`. Browse **`/corpus-map`** for a topic overview of the crawl; retrieval itself is **FAISS vector RAG**, not graph RAG.

## Retrieval evaluation

After the index exists:

```bash
python scripts/golden_eval.py
```

Writes `_data/eval_results.json` with match rate against `_data/golden_questions.json`.

## Configuration

See `retrieval/config.py` for defaults: `CPP_DEFAULT_TOP_K`, `CPP_MAX_CHUNK_CHARS`, `CPP_MAX_TOOL_ROUNDS`, `CPP_USE_RERANKER`, `CPP_LLM_BACKEND`, Ollama URL/model, whisper size, `CPP_LLM_READ_TIMEOUT` / `CPP_LLM_CONNECT_TIMEOUT`, optional **pulse** (`CPP_ENABLE_PULSE_TOOL`, `CPP_PULSE_INGEST_SECRET`, `CPP_PULSE_URL`).

## Verification (Ollama + Gemma 4 + STT)

Run these from the machine where **Flask and Ollama** run (or fix `OLLAMA_BASE_URL`).

| Step | Command / check | Pass |
|------|-------------------|------|
| V1 | `curl -sS http://127.0.0.1:11434/api/tags` | HTTP 200, JSON includes your model name |
| V2 | `curl -sS …/v1/chat/completions` with minimal `messages` (no tools) | 200, assistant content |
| V3 | Same with a minimal `tools` array | 200 (tool_calls or content) |
| V4 | `curl -sS http://127.0.0.1:5000/api/health` | `ollama_reachable: true`, `ollama_model_present: true` |
| V5 | Send a short message via **`POST /api/chat`** | HTTP 200, answer text, tokens or tool usage |
| V6 | **`POST /api/transcribe`** with a short audio clip | JSON `text` within timeout |

Example health check:

```bash
curl -sS http://127.0.0.1:5000/api/health | python3 -m json.tool
```

Chat errors with **`llm_error`** now include a **Details** line in the UI (server `detail` field). Typical fixes: start Ollama, `ollama pull <tag>`, align `OLLAMA_MODEL` with `ollama list`.

## Campus pulse (optional)

- UI: **`/pulse`** and **`GET /api/student-pulse`** — JSON digest ([`integrations/pulse_schema.json`](integrations/pulse_schema.json)).
- n8n: [`docs/n8n/README.md`](docs/n8n/README.md) — **`POST /api/student-pulse/ingest`** with `CPP_PULSE_INGEST_SECRET`.
- LLM: set **`CPP_ENABLE_PULSE_TOOL=true`** for tool **`get_student_pulse`** (unofficial digest only; corpus search remains authoritative for CPP policy).

## Optional fine-tuning (Unsloth → Ollama)

See [`scripts/finetune/README.md`](scripts/finetune/README.md) for a Phase-2 checklist (offline LoRA, export, `ollama create`, then set `OLLAMA_MODEL`).

## Optional browser extension

See `extension/README.txt` (consent-first spike, no portal scraping).

## API endpoints

| Path | Purpose |
|------|---------|
| `GET /api/health` | `index_ready`, `llm_backend`, `ollama_reachable`, `ollama_model_present`, `whisper_model_cached`, etc. (no secrets) |
| `GET /api/student-pulse` | Optional campus digest JSON |
| `POST /api/student-pulse/ingest` | n8n / automation push (requires `CPP_PULSE_INGEST_SECRET`) |
| `POST /api/transcribe` | Multipart field `audio` → JSON `{ "text": "..." }` |
| `GET /api/stats` | Anonymous counters: chat/retrieve requests and outcomes |
| `GET /api/retrieve?q=…` | Direct FAISS search (debugging / tools) |
| `POST /api/chat` | Chat with tool calling; errors use 4xx/5xx with JSON `error` field |

If `/api/chat` returns **502** with `llm_error`, read the **Details** line in the chat bubble (and JSON `detail`). Check Ollama, model tag, and network/timeouts (`CPP_LLM_READ_TIMEOUT`).

## Smaller installs (CPU-only PyTorch)

Default `pip install -r requirements.txt` may pull a large CUDA build of `torch`. For CPU-only servers, install PyTorch from the [PyTorch get-started page](https://pytorch.org/get-started/locally/) first, then install the rest of the requirements without re-pulling torch.
