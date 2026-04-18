from app.database import init_db
init_db()
"""Run the Flask development server."""
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(__import__("os").environ.get("PORT", "5000")))
