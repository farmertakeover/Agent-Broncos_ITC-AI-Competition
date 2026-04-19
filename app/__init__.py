import os

from dotenv import load_dotenv

_REPO_ROOT_EARLY = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_DOTENV_PATH = os.path.join(_REPO_ROOT_EARLY, ".env")

# Apply `.env` before `retrieval.config` reads env. `override=True` so repo `.env` wins over stale
# shell exports (e.g. OPENAI_API_KEY=replace_with_your_openai_api_key from an old `export` / CI default).
load_dotenv(_DOTENV_PATH, override=True)

from flask import Flask

from app.services.transcribe import transcribe_runtime_status
from retrieval import config

_REPO_ROOT = _REPO_ROOT_EARLY


def create_app() -> Flask:
    load_dotenv(_DOTENV_PATH, override=True)
    app = Flask(
        __name__,
        template_folder=os.path.join(_REPO_ROOT, "templates"),
        static_folder=os.path.join(_REPO_ROOT, "static"),
        static_url_path="/static",
    )
    app.secret_key = os.getenv("FLASK_SECRET_KEY") or os.getenv("SECRET_KEY") or "dev-insecure-change-me"
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    # Room for short voice memos to /api/transcribe (webm/opus).
    app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024
    app.config["CPP_INDEX_BUILT_AT"] = None
    app.config["TRANSCRIBE_RUNTIME_STATUS"] = transcribe_runtime_status()
    if not app.config["TRANSCRIBE_RUNTIME_STATUS"]["ok"]:
        print(
            "WARNING: STT runtime preflight failed:",
            "; ".join(app.config["TRANSCRIBE_RUNTIME_STATUS"]["issues"]),
        )

    from app.routes import bp

    app.register_blueprint(bp)

    @app.context_processor
    def inject_index_meta():
        return {
            "corpus_dir": config.CORPUS_DIR,
            "index_dir": config.INDEX_DIR,
        }

    return app
