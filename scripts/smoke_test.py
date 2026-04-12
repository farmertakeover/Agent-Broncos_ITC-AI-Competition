#!/usr/bin/env python3
"""HTTP smoke checks via Flask test client (no running server required)."""
from __future__ import annotations

import os
import sys
import unittest

# Repo root on path
_REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _REPO not in sys.path:
    sys.path.insert(0, _REPO)


class TestSmoke(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ.setdefault("FLASK_DEBUG", "0")
        from app import create_app

        cls.app = create_app()
        cls.client = cls.app.test_client()

    def test_health_shape(self):
        r = self.client.get("/api/health")
        self.assertEqual(r.status_code, 200, r.get_data(as_text=True))
        j = r.get_json()
        self.assertIsInstance(j, dict)
        for key in (
            "ok",
            "index_ready",
            "llm_backend",
            "ollama_reachable",
            "ollama_model_present",
            "ollama_tags_error",
            "whisper_model_cached",
            "pulse_tool_enabled",
        ):
            self.assertIn(key, j, f"missing {key}")

    def test_student_pulse(self):
        r = self.client.get("/api/student-pulse")
        self.assertEqual(r.status_code, 200)
        j = r.get_json()
        self.assertEqual(j.get("schema_version"), 1)
        self.assertIn("pulse_source", j)

    def test_pulse_page(self):
        r = self.client.get("/pulse")
        self.assertEqual(r.status_code, 200)
        self.assertIn(b"Campus pulse", r.data)

    def test_transcribe_missing_file(self):
        r = self.client.post("/api/transcribe")
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.get_json().get("error"), "missing_file")

    def test_pulse_ingest_disabled_without_secret(self):
        r = self.client.post("/api/student-pulse/ingest", json={"schema_version": 1})
        self.assertEqual(r.status_code, 503)
        self.assertEqual(r.get_json().get("error"), "ingest_disabled")

    def test_chat_empty_message(self):
        r = self.client.post("/api/chat", json={"message": "   ", "history": []})
        self.assertEqual(r.status_code, 400)


if __name__ == "__main__":
    unittest.main(verbosity=2)
