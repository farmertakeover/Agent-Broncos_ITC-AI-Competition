import json
import os
import uuid
from typing import Any

import psycopg2
from psycopg2.extras import RealDictCursor

# In-process fallback when DATABASE_URL is unset (dev / smoke).
_MEMORY_CHAT_RECOVERY: dict[str, dict[str, Any]] = {}
_MEMORY_RECOVERY_MAX = 512


def _database_url() -> str | None:
    url = (os.environ.get("DATABASE_URL") or "").strip()
    return url or None


def get_connection():
    url = _database_url()
    if not url:
        raise RuntimeError("DATABASE_URL is not set")
    return psycopg2.connect(url)


def init_db():
    if not _database_url():
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
    cur.execute("""
        CREATE TABLE IF NOT EXISTS chat_recovery (
            session_id TEXT PRIMARY KEY,
            recovery_id TEXT NOT NULL,
            user_message_en TEXT NOT NULL,
            content TEXT NOT NULL,
            sources_json TEXT,
            usage_json TEXT,
            error TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def save_message(session_id, role, content):
    if not _database_url():
        return
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
    if not _database_url():
        return []
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


def _ensure_chat_recovery_table(cur) -> None:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS chat_recovery (
            session_id TEXT PRIMARY KEY,
            recovery_id TEXT NOT NULL,
            user_message_en TEXT NOT NULL,
            content TEXT NOT NULL,
            sources_json TEXT,
            usage_json TEXT,
            error TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)


def store_chat_recovery(
    session_id: str,
    *,
    user_message_en: str,
    content: str,
    sources: list[dict[str, Any]] | None,
    usage: dict[str, Any] | None,
    error: str | None,
) -> str:
    """Persist last completed chat turn for client recovery after navigation (peek until ack)."""
    recovery_id = str(uuid.uuid4())
    um = (user_message_en or "")[:4000]
    body = (content or "")[:120000]
    sj = json.dumps(sources or [], separators=(",", ":"))[:500000]
    uj = json.dumps(usage or {}, separators=(",", ":"))[:32000] if usage else None
    err = (error or "")[:500] if error else None
    blob: dict[str, Any] = {
        "recovery_id": recovery_id,
        "user_message_en": um,
        "content": body,
        "sources": sources or [],
        "usage": usage or {},
        "error": err,
    }
    if not _database_url():
        if len(_MEMORY_CHAT_RECOVERY) >= _MEMORY_RECOVERY_MAX:
            for k in list(_MEMORY_CHAT_RECOVERY.keys())[: _MEMORY_RECOVERY_MAX // 4]:
                _MEMORY_CHAT_RECOVERY.pop(k, None)
        _MEMORY_CHAT_RECOVERY[session_id] = blob
        return recovery_id
    conn = get_connection()
    cur = conn.cursor()
    try:
        _ensure_chat_recovery_table(cur)
        cur.execute(
            """
            INSERT INTO chat_recovery (
                session_id, recovery_id, user_message_en, content, sources_json, usage_json, error
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (session_id) DO UPDATE SET
                recovery_id = EXCLUDED.recovery_id,
                user_message_en = EXCLUDED.user_message_en,
                content = EXCLUDED.content,
                sources_json = EXCLUDED.sources_json,
                usage_json = EXCLUDED.usage_json,
                error = EXCLUDED.error,
                updated_at = CURRENT_TIMESTAMP
            """,
            (session_id, recovery_id, um, body, sj, uj, err),
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()
    return recovery_id


def get_chat_recovery(session_id: str) -> dict[str, Any] | None:
    if not session_id:
        return None
    if not _database_url():
        row = _MEMORY_CHAT_RECOVERY.get(session_id)
        return dict(row) if row else None
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        _ensure_chat_recovery_table(cur)
        cur.execute(
            "SELECT recovery_id, user_message_en, content, sources_json, usage_json, error "
            "FROM chat_recovery WHERE session_id = %s",
            (session_id,),
        )
        row = cur.fetchone()
    finally:
        cur.close()
        conn.close()
    if not row:
        return None
    out: dict[str, Any] = {
        "recovery_id": row["recovery_id"],
        "user_message_en": row["user_message_en"],
        "content": row["content"],
        "error": row["error"],
    }
    try:
        out["sources"] = json.loads(row["sources_json"] or "[]")
    except (TypeError, json.JSONDecodeError):
        out["sources"] = []
    try:
        out["usage"] = json.loads(row["usage_json"] or "{}")
    except (TypeError, json.JSONDecodeError):
        out["usage"] = {}
    return out


def ack_chat_recovery(session_id: str, recovery_id: str) -> None:
    if not session_id or not recovery_id:
        return
    if not _database_url():
        cur = _MEMORY_CHAT_RECOVERY.get(session_id)
        if cur and cur.get("recovery_id") == recovery_id:
            _MEMORY_CHAT_RECOVERY.pop(session_id, None)
        return
    conn = get_connection()
    cur = conn.cursor()
    try:
        _ensure_chat_recovery_table(cur)
        cur.execute(
            "DELETE FROM chat_recovery WHERE session_id = %s AND recovery_id = %s",
            (session_id, recovery_id),
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()