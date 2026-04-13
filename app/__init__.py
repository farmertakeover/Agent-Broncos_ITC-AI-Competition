import os

from dotenv import load_dotenv

# Apply `.env` before `retrieval.config` reads OLLAMA_* (otherwise URLs/model stay at import-time defaults).
load_dotenv()

from flask import Flask

from app.services.transcribe import transcribe_runtime_status
from retrieval import config

_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def create_app() -> Flask:
    from dotenv import load_dotenv

    load_dotenv()
    app = Flask(
        __name__,
        template_folder=os.path.join(_REPO_ROOT, "templates"),
        static_folder=os.path.join(_REPO_ROOT, "static"),
        static_url_path="/static",
    )
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
