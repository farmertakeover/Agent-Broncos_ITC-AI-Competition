#!/usr/bin/env python3
"""HTTP smoke checks via Flask test client (no running server required).

Run from repo root:

    python3 -m unittest scripts.smoke_test -v
"""
from __future__ import annotations

import os
import sys
import unittest
from unittest.mock import patch

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
            "langbly_configured",
            "openweather_configured",
            "dashboard_default_rss_configured",
            "dashboard_skip_remote",
        ):
            self.assertIn(key, j, f"missing {key}")

    def test_student_pulse(self):
        r = self.client.get("/api/student-pulse")
        self.assertEqual(r.status_code, 200)
        j = r.get_json()
        self.assertEqual(j.get("schema_version"), 1)
        self.assertIn("pulse_source", j)

    @patch.dict(os.environ, {"CPP_DASHBOARD_SKIP_REMOTE": "true"}, clear=False)
    def test_api_dashboard_shape(self):
        r = self.client.get("/api/dashboard")
        self.assertEqual(r.status_code, 200, r.get_data(as_text=True))
        j = r.get_json()
        self.assertEqual(j.get("schema_version"), 1)
        self.assertIn("sections", j)
        self.assertIn("announcements", j["sections"])
        self.assertIn("sources", j)
        self.assertNotIn("google", j)

    @patch.dict(os.environ, {"CPP_DASHBOARD_SKIP_REMOTE": "true"}, clear=False)
    def test_api_dashboard_preferences(self):
        r = self.client.post(
            "/api/dashboard/preferences",
            json={"order": ["news", "events", "announcements"], "hidden": ["news"], "tags": ["clubs"]},
        )
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.get_json().get("ok"))
        r2 = self.client.get("/api/dashboard")
        j = r2.get_json()
        self.assertEqual(j.get("preferences", {}).get("order"), ["news", "events", "announcements"])

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

    @patch("app.routes.run_agent_turn", return_value={"content": "ok", "sources": [], "error": None})
    def test_chat_response_is_json(self, _mock_turn):
        """Regression: /api/chat must return JSON (never HTML tracebacks)."""
        saved_db = os.environ.pop("DATABASE_URL", None)
        try:
            r = self.client.post(
                "/api/chat",
                json={"message": "hello", "history": []},
            )
            self.assertIsNotNone(
                r.get_json(silent=True),
                msg=r.get_data(as_text=True)[:800],
            )
            j = r.get_json()
            self.assertIsInstance(j, dict)
            self.assertIn("session_id", j)
            self.assertEqual(j.get("content"), "ok")
        finally:
            if saved_db is not None:
                os.environ["DATABASE_URL"] = saved_db

    def test_translate_missing_text(self):
        r = self.client.post("/api/translate", json={"target": "es"})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.get_json().get("error"), "missing_text")

    def test_translate_batch_empty_entries(self):
        r = self.client.post("/api/translate/batch", json={"target": "es", "entries": {}})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.get_json().get("error"), "missing_entries")

    def test_translate_batch_english_passthrough(self):
        r = self.client.post(
            "/api/translate/batch",
            json={"target": "en", "entries": {"k1": "Hello there"}},
        )
        self.assertEqual(r.status_code, 200, r.get_data(as_text=True))
        j = r.get_json()
        self.assertEqual(j.get("target"), "en")
        self.assertEqual(j.get("entries", {}).get("k1"), "Hello there")

    def test_weather_not_configured_without_key(self):
        saved = os.environ.pop("Agent_Broncos_Weather_API", None)
        try:
            r = self.client.get("/api/weather")
            self.assertEqual(r.status_code, 503)
            self.assertEqual(r.get_json().get("error"), "weather_not_configured")
        finally:
            if saved is not None:
                os.environ["Agent_Broncos_Weather_API"] = saved

    def test_translate_not_configured_without_key(self):
        saved = os.environ.pop("Agent_Broncos_Language_Translation", None)
        try:
            r = self.client.post(
                "/api/translate",
                json={"text": "Hello", "target": "es"},
            )
            self.assertEqual(r.status_code, 503)
            self.assertEqual(r.get_json().get("error"), "translate_not_configured")
        finally:
            if saved is not None:
                os.environ["Agent_Broncos_Language_Translation"] = saved

    def test_home_page_loads(self):
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)
        self.assertIn(b"ui_i18n.js", r.data)
        self.assertIn(b"dashLang", r.data)
        self.assertIn(b"homeDashboardRoot", r.data)
        self.assertIn(b"btn-ask-bronco", r.data)

    def test_chat_page_loads(self):
        r = self.client.get("/chat")
        self.assertEqual(r.status_code, 200)
        self.assertIn(b"ui_i18n.js", r.data)
        self.assertIn(b"starter-btn", r.data)


if __name__ == "__main__":
    unittest.main(verbosity=2)
