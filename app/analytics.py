"""Lightweight anonymous counters for the bonus analytics dashboard."""
from __future__ import annotations

import threading

_lock = threading.Lock()
_stats: dict[str, int] = {
    "chat_requests": 0,
    "retrieve_requests": 0,
    "chat_completed_ok": 0,
    "chat_completed_error": 0,
}


def record_chat_start() -> None:
    with _lock:
        _stats["chat_requests"] += 1


def record_retrieve() -> None:
    with _lock:
        _stats["retrieve_requests"] += 1


def record_chat_outcome(ok: bool) -> None:
    with _lock:
        if ok:
            _stats["chat_completed_ok"] += 1
        else:
            _stats["chat_completed_error"] += 1


def snapshot() -> dict[str, int]:
    with _lock:
        return dict(_stats)
