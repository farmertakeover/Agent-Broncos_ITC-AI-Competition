"""Local speech-to-text via faster-whisper (lazy-loaded)."""
from __future__ import annotations

import os
import tempfile
import threading
from functools import lru_cache

from werkzeug.datastructures import FileStorage

from retrieval import config

_warmup_lock = threading.Lock()
_warmup_thread_started = False


@lru_cache(maxsize=1)
def _model():
    from faster_whisper import WhisperModel

    size = config.WHISPER_MODEL_SIZE
    device = os.getenv("CPP_WHISPER_DEVICE", "cpu")
    compute_type = os.getenv("CPP_WHISPER_COMPUTE_TYPE", "int8")
    return WhisperModel(size, device=device, compute_type=compute_type)


def schedule_whisper_warmup_background() -> None:
    """Load Whisper model once in a daemon thread (CPP_WHISPER_WARMUP=1 on /api/health)."""
    global _warmup_thread_started
    with _warmup_lock:
        if _warmup_thread_started:
            return
        _warmup_thread_started = True

    def _run() -> None:
        try:
            _model()
        except Exception:
            pass

    threading.Thread(target=_run, daemon=True).start()


def whisper_model_cached() -> bool:
    return _model.cache_info().currsize > 0


def transcribe_upload(file: FileStorage | None) -> tuple[str | None, str | None]:
    """
    Returns (text, error_code). error_code is one of missing_file, empty_file, transcribe_failed.
    """
    if file is None or file.filename is None or file.filename == "":
        return None, "missing_file"
    raw = file.read()
    if not raw:
        return None, "empty_file"

    suffix = ".webm"
    fn = (file.filename or "").lower()
    if fn.endswith(".wav"):
        suffix = ".wav"
    elif fn.endswith(".mp3"):
        suffix = ".mp3"
    elif fn.endswith(".ogg"):
        suffix = ".ogg"
    elif fn.endswith(".m4a"):
        suffix = ".m4a"

    try:
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=True) as tmp:
            tmp.write(raw)
            tmp.flush()
            model = _model()
            segments, _info = model.transcribe(tmp.name)
            parts = [s.text for s in segments]
        text = " ".join(p.strip() for p in parts if p).strip()
        return (text if text else None), None
    except Exception:
        return None, "transcribe_failed"
