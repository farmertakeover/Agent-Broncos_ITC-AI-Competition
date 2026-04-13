# Agent Broncos — Cal Poly Pomona ITC AI Competition

Flask web app with **Ollama** (local or **[Ollama Cloud](https://docs.ollama.com/cloud)**) via the OpenAI-compatible `/v1` API for tool calling, plus a **local FAISS** index over the CPP markdown corpus. Optional **OpenAI** cloud is off unless you explicitly enable it.

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

### Ollama Cloud (recommended if you want to save laptop RAM)

Use this when **local GGUFs** (e.g. `gemma4:e2b`) do not fit in free RAM but you still want an Ollama-compatible stack.

1. Create an API key at [ollama.com/settings/keys](https://ollama.com/settings/keys).
2. In `.env` (see [`.env.example`](.env.example)):

   - `OLLAMA_BASE_URL=https://ollama.com` (no `/v1`; the app appends it).
   - `OLLAMA_API_KEY=<your key>` (**required** for cloud; health and `/api/tags` use the same Bearer token).
   - `OLLAMA_MODEL=<a [cloud model](https://ollama.com/search?c=cloud)>` (example in `.env.example`: `gpt-oss:120b-cloud`).

3. Confirm:

   ```bash
   curl -sS -H "Authorization: Bearer $OLLAMA_API_KEY" https://ollama.com/api/tags | head
   curl -sS http://127.0.0.1:5000/api/health | python3 -m json.tool
   ```

   Expect **`ollama_reachable`**, **`ollama_host_is_cloud`**, and **`ollama_model_present`** to be true. Corpus + **faster-whisper** still run **locally**; only the **chat LLM** hits the cloud.

**Tool calling:** depends on the cloud model you pick—verify with a real question in **`/chat`**.

### Local Ollama (optional)

1. Install and start [Ollama](https://ollama.com).
2. Pull a model, e.g. **Gemma 4** ([library](https://ollama.com/library/gemma4)):

   ```bash
   ollama pull gemma4:e2b
   ollama list
   ```

   The app can **auto-resolve** a short name like `gemma4` to the only installed `gemma4:*` tag. **`GET /api/health`** includes `ollama_model_for_api` and optional `ollama_model_resolution_note`.

3. Env: `OLLAMA_BASE_URL=http://127.0.0.1:11434`, `OLLAMA_MODEL=<exact tag>`. Leave **`OLLAMA_API_KEY`** unset for typical local installs.

For GGUFs outside Ollama, see [Unsloth — Gemma 4](https://unsloth.ai/docs/models/gemma-4).

**TurboQuant / KV cache:** Only affect **local** (or self-hosted) Ollama; set on the **Ollama process** (e.g. `OLLAMA_KV_CACHE_TYPE`). Not applicable to weights hosted on Ollama Cloud.

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

Chat errors with **`llm_error`** now include a **Details** line in the UI (server `detail` field). Typical fixes: start Ollama, `ollama pull <tag>`, set **`OLLAMA_MODEL`** to the **exact** tag (or rely on auto-resolve when only one `gemma4:*` variant is installed).

### Why `404 model 'gemma4' not found`?

Ollama often only has **`gemma4:e2b`** (or another variant) installed. The OpenAI-compatible endpoint must receive that **full** name. **`ollama_model_present`** could still be true when the app treated `gemma4` as matching the same *family* as `gemma4:e2b`, while the API rejected the short name. Chat now resolves **one** matching variant automatically; use **`ollama_model_for_api`** from **`/api/health`** to see what will be called.

### Gemma 4 “native” audio vs faster-whisper

Neither is automatically “better” for every use case. **faster-whisper** is specialized STT; **`CPP_WHISPER_MODEL_SIZE=tiny`** can run in hundreds of MB while your **chat** model is separate. **Gemma 4 E2B/E4B** can handle audio in some **native** multimodal stacks (Unsloth / llama.cpp, etc.), but **this app** only sends **text** to Ollama after transcription. Doing ASR **inside** Gemma as well as chat usually needs **more** total memory, not less—your current error is the **LLM** load failing RAM checks, not Whisper.

**Rewriting for Gemma-only audio** would mean sending **audio** through an API that your Ollama tag actually supports (check Ollama’s current multimodal docs; plain text `chat.completions` may not be enough). That is separate from fixing out-of-memory on the chat model.

### Ollama out of memory (`model requires more system memory …`)

If you see **`ollama_oom`** or **Details** with **more system memory than is available**, **Flask is not broken**—**Ollama** will not load that GGUF because **free RAM** is too low (e.g. 7.2 GiB needed vs 4.8 GiB available). **Restarting or “reopening” Flask does not add RAM.**

Mitigations: use a **smaller** Ollama tag/quant, **free memory** (close apps, unload other models), add **swap**, use a **beefier machine** or **GPU**, or use one of the **workarounds** below.

### Laptop RAM too small: workarounds (no local GGUF load)

1. **Remote Ollama (your own PC / server)**  
   Install Ollama on a machine with enough RAM. Bind or tunnel it safely (VPN, Tailscale, SSH `-L 11434:127.0.0.1:11434`, or a private network). On the laptop, in `.env`:
   - `OLLAMA_BASE_URL=http://<that-host>:11434` (no `/v1`; the app adds it)
   - `OLLAMA_MODEL=<exact tag on that host>`  
   Flask and the browser can stay on the laptop; only LLM traffic goes to the remote host. **Do not** expose `11434` to the public internet without auth.

2. **Ollama Cloud (hosted inference)**  
   Ollama can run **cloud** models on their side so your laptop does not hold the full weight in RAM. See [Ollama Cloud](https://docs.ollama.com/cloud): create an API key at [ollama.com/settings/keys](https://ollama.com/settings/keys), then in `.env`:
   - `OLLAMA_BASE_URL=https://ollama.com`
   - `OLLAMA_API_KEY=<your key>` (required; not the dummy `ollama` placeholder)
   - `OLLAMA_MODEL=<a cloud-capable model name from the [model library](https://ollama.com/search?c=cloud)>`  
   This app uses the same OpenAI-compatible `/v1` client as for local Ollama. **Tool calling** must be supported by the cloud model you pick—verify with a short chat test.

3. **Hosted OpenAI-style API (competition / backup)**  
   Enable **`CPP_ALLOW_OPENAI=true`**, **`CPP_LLM_BACKEND=openai`**, and set **`OPENAI_API_KEY`** (or `Agent_Broncos_API_Key`). Uses your cloud provider instead of Ollama.

**Fine-tuning (Unsloth)** does not replace any of the above for “I have 4.8 GiB and E2B wants 7.2 GiB”—it changes behavior after you can already run a model somewhere.

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
| `GET /api/health` | `index_ready`, `llm_backend`, `ollama_reachable`, `ollama_host_is_cloud`, `ollama_model_present`, `ollama_version`, `whisper_model_cached`, etc. (no secrets) |
| `GET /api/student-pulse` | Optional campus digest JSON |
| `POST /api/student-pulse/ingest` | n8n / automation push (requires `CPP_PULSE_INGEST_SECRET`) |
| `POST /api/transcribe` | Multipart field `audio` → JSON `{ "text": "..." }` |
| `GET /api/stats` | Anonymous counters: chat/retrieve requests and outcomes |
| `GET /api/retrieve?q=…` | Direct FAISS search (debugging / tools) |
| `POST /api/chat` | Chat with tool calling; errors use 4xx/5xx with JSON `error` field |

If `/api/chat` returns **502** with `llm_error` or **`ollama_oom`**, read the **Details** line (JSON `detail`). For **`ollama_oom`**, fix RAM or model size (see “Ollama out of memory” above). Otherwise check Ollama, model tag, and timeouts (`CPP_LLM_READ_TIMEOUT`).

## Smaller installs (CPU-only PyTorch)

Default `pip install -r requirements.txt` may pull a large CUDA build of `torch`. For CPU-only servers, install PyTorch from the [PyTorch get-started page](https://pytorch.org/get-started/locally/) first, then install the rest of the requirements without re-pulling torch.
