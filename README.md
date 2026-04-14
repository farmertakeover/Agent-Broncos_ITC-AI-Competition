# Agent Broncos — CPP ITC AI Competition

Agent Broncos is a Flask app that answers Cal Poly Pomona questions using:
- tool-calling chat (`/api/chat`)
- local FAISS retrieval over the CPP markdown corpus
- optional local speech-to-text (`/api/transcribe`) via `faster-whisper`

Default backend in `.env.example` is OpenAI. Ollama is also supported.

## What Is In Use

| Area | Implementation |
|---|---|
| Web app | Flask + Jinja templates (`/chat`, `/corpus-map`, `/pulse`) |
| Chat orchestration | `app/services/chat.py` with tools `search_corpus`, `get_source_excerpt` (+ optional `get_student_pulse`) |
| Retrieval | FAISS (`faiss-cpu`) + sentence-transformers embeddings |
| Corpus source | `_data/Corpus/itc2026_ai_corpus/*.md` + `_data/Corpus/itc2026_ai_corpus/index.json` |
| Index artifacts | `_data/index/cpp_corpus.faiss`, `_data/index/cpp_corpus.meta.jsonl`, `_data/index/url_map.json` |
| STT | `faster-whisper` + `ffmpeg` |
| Optional pulse feed | JSON ingest/read via `/api/student-pulse` and `/api/student-pulse/ingest` |

## Architecture Diagram

```mermaid
flowchart LR
    U[Browser UI<br/>/chat /corpus-map /pulse] --> F[Flask Routes<br/>app/routes.py]

    F --> C[Chat Service<br/>run_agent_turn]
    C --> T1[Tool: search_corpus]
    C --> T2[Tool: get_source_excerpt]
    C --> T3[Optional Tool:<br/>get_student_pulse]

    T1 --> R[Retrieval Store]
    T2 --> R
    R --> I[_data/index<br/>FAISS + metadata]
    I --> M[_data/Corpus<br/>CPP markdown corpus]

    C -->|CPP_LLM_BACKEND=openai| OAI[OpenAI Chat API]
    C -->|CPP_LLM_BACKEND=ollama| OLL[Ollama OpenAI-compatible API]

    F --> STT[/api/transcribe]
    STT --> W[faster-whisper model]
    STT --> FF[ffmpeg]

    F --> P[/api/student-pulse]
    P --> PF[_data/pulse/latest.json<br/>or CPP_PULSE_URL]
```

## Quick Start

```bash
cd /workspaces/Brono-Agents-ITC-AI-Competition
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Build the index:

```bash
python scripts/build_index.py
```

Run the app:

```bash
python run.py
```

Open:
- `http://127.0.0.1:5000/chat`
- `http://127.0.0.1:5000/api/health`

## LLM Backend Configuration

### OpenAI (default)

In `.env`:
- `CPP_LLM_BACKEND=openai`
- `CPP_ALLOW_OPENAI=true`
- `OPENAI_API_KEY=...`
- optional `CPP_OPENAI_MODEL` (default: `gpt-5-mini`)

### Ollama

In `.env`:
- `CPP_LLM_BACKEND=ollama`
- `CPP_ALLOW_OPENAI=false`
- `OLLAMA_BASE_URL=http://127.0.0.1:11434` (or your remote/cloud endpoint)
- `OLLAMA_MODEL=<installed tag>` (example `gemma3:4b`)
- `OLLAMA_API_KEY` only when your Ollama endpoint requires auth

## Speech-to-Text (Optional, Implemented)

`POST /api/transcribe` is enabled in code. Requirements:
- Python package `faster-whisper` (already in `requirements.txt`)
- system `ffmpeg` on PATH

Useful env vars:
- `CPP_WHISPER_MODEL_SIZE` (default `base`, use `tiny` for lighter dev)
- `CPP_WHISPER_DEVICE` (`cpu` or `cuda`)
- `CPP_WHISPER_COMPUTE_TYPE` (default `int8`)
- `CPP_WHISPER_WARMUP=true` to preload on health check

## Pulse Feed (Optional, Implemented)

Supported and wired:
- `GET /api/student-pulse`
- `POST /api/student-pulse/ingest` (requires `CPP_PULSE_INGEST_SECRET`)
- `CPP_ENABLE_PULSE_TOOL=true` to expose `get_student_pulse` to chat

Primary schema: `integrations/pulse_schema.json`.

## Retrieval Evaluation

After index build:

```bash
python scripts/golden_eval.py
```

Writes `_data/eval_results.json` from `_data/golden_questions.json`.

## Key Endpoints

| Path | Purpose |
|---|---|
| `GET /api/health` | backend/index/STT/pulse readiness details |
| `POST /api/chat` | chat with tool-calling over corpus |
| `GET /api/retrieve?q=...` | direct retrieval debugging |
| `POST /api/transcribe` | audio to text |
| `GET /api/student-pulse` | pulse JSON |
| `POST /api/student-pulse/ingest` | authenticated pulse ingest |
| `GET /api/stats` | anonymous usage counters |

## Project Data Layout

| Path | Contents |
|---|---|
| `_data/Corpus/itc2026_ai_corpus/` | source markdown corpus + `index.json` |
| `_data/index/` | generated FAISS + metadata files |
| `_data/golden_questions.json` | retrieval eval fixtures |
| `_data/eval_results.json` | eval output |
