# Deployment notes

This app is a **Flask** server with **local FAISS**, optional **faster-whisper**, and filesystem-backed assets. That does **not** map cleanly to **Vercel serverless** without a major refactor (cold starts, read-only/ephemeral disk, dependency size).

## Recommended: split stack

- **Frontend / marketing**: host static pages on Vercel (or keep everything on one host below).
- **API + RAG**: run the Flask app on a **long-lived** host with disk or object storage for `_data/index` and the corpus:
  - [Render](https://render.com), [Railway](https://railway.app), [Fly.io](https://fly.io), a small VM, or **Google Cloud Run** with a volume or GCS sync for the index.

Point the browser at your Flask `ORIGIN` (single deployment is simplest: Flask serves templates + static as it does today).

## Manual steps (operator)

1. Build the index in CI or locally: `python scripts/build_index.py`
2. Ship `_data/index/` (and corpus if not baked into the image) to the runtime.
3. Set environment variables (see `.env.example`): `OLLAMA_*` or OpenAI keys, `CPP_*` paths, optional Whisper and pulse settings.
4. Run with a production WSGI server (e.g. gunicorn) behind HTTPS — **not** `run.py` in production.

## If you still want Vercel-only

You must slim the app: external vector DB, no local whisper in the function, no file-based pulse writes, and a `vercel.json` + serverless entry wrapping Flask. Expect significant engineering; the split stack above is faster and safer for this codebase.
