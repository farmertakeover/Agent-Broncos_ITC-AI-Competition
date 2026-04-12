"""HTTP client factory and Ollama daemon helpers (modular surface for chat + health)."""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

import httpx
from openai import OpenAI

from retrieval import config


def llm_http_timeout() -> httpx.Timeout:
    return httpx.Timeout(
        connect=float(os.getenv("CPP_LLM_CONNECT_TIMEOUT", "10")),
        read=float(os.getenv("CPP_LLM_READ_TIMEOUT", "120")),
        write=float(os.getenv("CPP_LLM_WRITE_TIMEOUT", "60")),
        pool=5.0,
    )


def llm_max_retries() -> int:
    return int(os.getenv("CPP_LLM_MAX_RETRIES", "0"))


def openai_client_ollama() -> OpenAI:
    return OpenAI(
        base_url=config.OLLAMA_OPENAI_BASE_URL,
        api_key=os.getenv("OLLAMA_API_KEY", "ollama"),
        timeout=llm_http_timeout(),
        max_retries=llm_max_retries(),
    )


def openai_client_cloud(api_key: str) -> OpenAI:
    return OpenAI(
        api_key=api_key,
        timeout=llm_http_timeout(),
        max_retries=max(llm_max_retries(), 0),
    )


def fetch_ollama_model_names(root: str, timeout_sec: float = 3.0) -> tuple[list[str] | None, str | None]:
    """Returns (tag_names, error_message)."""
    url = f"{root.rstrip('/')}/api/tags"
    try:
        with urllib.request.urlopen(url, timeout=timeout_sec) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
        data: dict[str, Any] = json.loads(raw)
        models = data.get("models") or []
        names: list[str] = []
        for m in models:
            if isinstance(m, dict):
                n = m.get("name")
                if isinstance(n, str) and n:
                    names.append(n)
        return names, None
    except (urllib.error.URLError, OSError, TimeoutError, ValueError, json.JSONDecodeError) as e:
        return None, str(e)


def ollama_model_tag_present(requested: str, installed: list[str]) -> bool:
    """Match OLLAMA_MODEL to Ollama list names (handles :latest and base name)."""
    req = (requested or "").strip()
    if not req:
        return False
    req_base = req.split(":")[0]
    for n in installed:
        if n == req:
            return True
        if n.split(":")[0] == req_base:
            return True
    return False
