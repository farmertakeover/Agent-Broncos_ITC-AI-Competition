import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    return psycopg2.connect(os.environ["DATABASE_URL"])

def init_db():
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