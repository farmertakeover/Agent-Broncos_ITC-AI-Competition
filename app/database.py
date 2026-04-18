import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    url = os.environ.get("DATABASE_URL") or os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL environment variable not set")
    return psycopg2.connect(url)

def init_db():
    if not os.environ.get("DATABASE_URL"):
        print("[database] DATABASE_URL not set; skipping init_db().")
        return
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id SERIAL PRIMARY KEY,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def save_message(session_id, role, content):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO chat_history (session_id, role, content) VALUES (%s, %s, %s)",
        (session_id, role, content)
    )
    conn.commit()
    cur.close()
    conn.close()

def get_history(session_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        "SELECT role, content, created_at FROM chat_history WHERE session_id = %s ORDER BY created_at ASC",
        (session_id,)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows