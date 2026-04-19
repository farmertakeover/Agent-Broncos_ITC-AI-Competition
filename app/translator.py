"""Langbly-backed language detection and translation."""

from __future__ import annotations

import os
from typing import Optional

from langbly import Langbly, LangblyError

_client: Optional[Langbly] = None


class TranslatorConfigError(RuntimeError):
    """Raised when the Langbly API key is missing."""


def _translator() -> Langbly:
    global _client
    if _client is not None:
        return _client
    key = (os.getenv("Agent_Broncos_Language_Translation") or "").strip()
    if not key:
        raise TranslatorConfigError(
            "Set Agent_Broncos_Language_Translation in the environment (see .env.example)."
        )
    _client = Langbly(api_key=key)
    return _client


def detect_language(text: str) -> str:
    """Return a BCP-47 style language code for the given text."""
    if not (text or "").strip():
        raise ValueError("empty text")
    return _translator().detect(text).language


def translate_text(text: str, target_language: str = "en") -> str:
    """Translate text to ``target_language`` (default English)."""
    if not (text or "").strip():
        raise ValueError("empty text")
    result = _translator().translate(text, target=target_language)
    return result.text


def translate_entries(entries: dict[str, str], target_language: str) -> dict[str, str]:
    """
    Translate many UI strings in one Langbly call (list translate).

    ``entries`` maps stable keys to source text. Returns the same keys with translated text.
    If ``target_language`` is English (or empty), returns a copy of ``entries`` without calling the API.
    """
    if not isinstance(entries, dict):
        raise ValueError("entries must be a dict")
    tgt = (target_language or "en").strip() or "en"
    if tgt.lower().startswith("en"):
        return dict(entries)

    keys = [k for k, v in entries.items() if isinstance(k, str) and isinstance(v, str) and v.strip()]
    if not keys:
        return {}
    values = [entries[k].strip() for k in keys]
    results = _translator().translate(values, target=tgt)
    if not isinstance(results, list) or len(results) != len(keys):
        raise RuntimeError("unexpected Langbly batch translate response shape")
    return {keys[i]: results[i].text for i in range(len(keys))}


__all__ = [
    "LangblyError",
    "TranslatorConfigError",
    "detect_language",
    "translate_entries",
    "translate_text",
]
