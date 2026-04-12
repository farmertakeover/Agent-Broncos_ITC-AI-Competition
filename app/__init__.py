import os

from flask import Flask

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

    from app.routes import bp

    app.register_blueprint(bp)

    @app.context_processor
    def inject_index_meta():
        return {
            "corpus_dir": config.CORPUS_DIR,
            "index_dir": config.INDEX_DIR,
        }

    return app
