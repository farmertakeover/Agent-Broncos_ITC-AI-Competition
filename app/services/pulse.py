"""Student pulse: optional JSON from n8n ingest or remote URL (see integrations/pulse_schema.json)."""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from copy import deepcopy
from typing import Any

from retrieval import config

_SCHEMA_PATH = os.path.join(config.REPO_ROOT, "integrations", "pulse_schema.json")
_TOOL_JSON_MAX = int(os.getenv("CPP_PULSE_TOOL_MAX_CHARS", "8000"))


def _reddit_enabled() -> bool:
    return os.getenv("CPP_PULSE_REDDIT_ENABLED", "true").lower() in ("1", "true", "yes")


def _reddit_live_fetch_enabled() -> bool:
    """When false, skip outbound Reddit JSON; use only file/URL/ingest ``reddit_cpp.items`` (e.g. n8n on a non-blocked IP)."""
    return os.getenv("CPP_PULSE_REDDIT_LIVE_FETCH", "true").lower() in ("1", "true", "yes")


def _default_skeleton() -> dict[str, Any]:
    if os.path.isfile(_SCHEMA_PATH):
        try:
            with open(_SCHEMA_PATH, encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):
            pass
    return {
        "schema_version": 1,
        "generated_at": None,
        "weather": {},
        "reddit_cpp": {"items": []},
        "academic_dates": {"items": []},
        "links": {},
        "disclaimers": [],
    }


def _read_file_payload() -> dict[str, Any] | None:
    path = config.PULSE_FILE
    if not os.path.isfile(path):
        return None
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else None
    except (OSError, json.JSONDecodeError):
        return None


def _fetch_url_payload() -> dict[str, Any] | None:
    url = config.PULSE_URL
    if not url:
        return None
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "AgentBroncos-Pulse/1.0"})
        with urllib.request.urlopen(req, timeout=float(os.getenv("CPP_PULSE_FETCH_TIMEOUT", "8"))) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
        data = json.loads(raw)
        return data if isinstance(data, dict) else None
    except (urllib.error.URLError, OSError, TimeoutError, ValueError, json.JSONDecodeError):
        return None


def _fetch_reddit_via_json() -> tuple[list[dict[str, Any]], str | None]:
    url = (os.getenv("CPP_REDDIT_JSON_URL") or "https://www.reddit.com/r/CalPolyPomona/new.json?limit=10").strip()
    timeout = float(os.getenv("CPP_REDDIT_FETCH_TIMEOUT", "8"))
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": os.getenv("CPP_REDDIT_USER_AGENT", "AgentBroncos-Pulse/1.0"),
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
        data = json.loads(raw)
        children = (((data or {}).get("data") or {}).get("children")) if isinstance(data, dict) else None
        if not isinstance(children, list):
            return [], "invalid_json_shape"
        out: list[dict[str, Any]] = []
        for child in children:
            inner = (child or {}).get("data") if isinstance(child, dict) else None
            if not isinstance(inner, dict):
                continue
            title = str(inner.get("title") or "").strip()
            permalink = str(inner.get("permalink") or "").strip()
            if not title:
                continue
            url_final = (
                ("https://www.reddit.com" + permalink)
                if permalink.startswith("/")
                else str(inner.get("url") or "").strip()
            )
            out.append(
                {
                    "title": title,
                    "url": url_final or None,
                    "subreddit": str(inner.get("subreddit") or "CalPolyPomona"),
                    "created_utc": inner.get("created_utc"),
                }
            )
        return out, None
    except (urllib.error.URLError, OSError, TimeoutError, ValueError, json.JSONDecodeError) as e:
        return [], str(e)


def _merge_reddit_items(base: dict[str, Any]) -> None:
    if not _reddit_enabled():
        return
    if _reddit_live_fetch_enabled():
        fetched, err = _fetch_reddit_via_json()
    else:
        fetched, err = [], None
    existing = ((base.get("reddit_cpp") or {}).get("items")) if isinstance(base.get("reddit_cpp"), dict) else None
    items: list[dict[str, Any]] = []
    if isinstance(existing, list):
        for it in existing:
            if isinstance(it, dict):
                items.append(it)
    seen: set[str] = set()
    merged: list[dict[str, Any]] = []
    for it in fetched + items:
        if not isinstance(it, dict):
            continue
        k = f"{it.get('url') or ''}|{it.get('title') or ''}"
        if k in seen:
            continue
        seen.add(k)
        merged.append(it)
    base.setdefault("reddit_cpp", {})
    if isinstance(base["reddit_cpp"], dict):
        base["reddit_cpp"]["items"] = merged[:20]
        base["reddit_cpp"]["source"] = "ingest_only" if not _reddit_live_fetch_enabled() else "json"
        if err:
            base["reddit_cpp"]["warning"] = err
        else:
            base["reddit_cpp"].pop("warning", None)


def get_pulse_for_api() -> dict[str, Any]:
    """Merged digest for GET /api/student-pulse."""
    base = deepcopy(_default_skeleton())
    disk = _read_file_payload()
    if disk:
        base.update(disk)
        base["pulse_source"] = "file"
        _merge_reddit_items(base)
        return base
    if config.PULSE_URL:
        remote = _fetch_url_payload()
        if remote:
            base.update(remote)
            base["pulse_source"] = "url"
            _merge_reddit_items(base)
            return base
    base["pulse_source"] = "default"
    _merge_reddit_items(base)
    return base


def get_pulse_for_tool() -> dict[str, Any]:
    """Truncated JSON-safe dict for LLM tool output."""
    payload = get_pulse_for_api()
    raw = json.dumps(payload, ensure_ascii=False)
    if len(raw) <= _TOOL_JSON_MAX:
        return payload
    return {
        "truncated": True,
        "schema_version": payload.get("schema_version"),
        "generated_at": payload.get("generated_at"),
        "preview": raw[:_TOOL_JSON_MAX] + "…",
        "disclaimers": payload.get("disclaimers"),
    }


def ingest_payload(data: dict[str, Any]) -> tuple[bool, str | None]:
    """Write merged payload to CPP_PULSE_FILE (atomic replace)."""
    path = config.PULSE_FILE
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, path)
        return True, None
    except OSError as e:
        return False, str(e)
