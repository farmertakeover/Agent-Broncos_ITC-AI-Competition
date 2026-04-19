#!/usr/bin/env python3
"""Build static UI i18n bundles for supported locales.

Usage:
  python3 scripts/build_ui_i18n_bundles.py
"""

from __future__ import annotations

import json
import os
from html.parser import HTMLParser
from pathlib import Path

from app import create_app
from app.translator import translate_entries


SUPPORTED_LOCALES = [
    "en-US",
    "es-MX",
    "zh-CN",
    "vi-VN",
    "ko-KR",
    "ja-JP",
    "ar-SA",
    "fr-FR",
    "de-DE",
    "hi-IN",
]

ROUTES = ["/", "/chat", "/corpus-map", "/pulse"]


def locale_to_target(locale: str) -> str:
    low = locale.lower()
    if low.startswith("en"):
        return "en"
    if low == "zh-cn":
        return "zh-CN"
    return locale.split("-")[0] or "en"


class I18nExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.entries: dict[str, str] = {}
        self._stack: list[tuple[str, list[str]]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        amap = {k: (v or "") for k, v in attrs}
        data_i18n = amap.get("data-i18n")
        if data_i18n:
            self._stack.append((data_i18n, []))
        for attr_key, pref_key in (
            ("data-i18n-placeholder", "ph."),
            ("data-i18n-aria", "aria."),
            ("data-i18n-title", "title."),
        ):
            key = amap.get(attr_key)
            if not key:
                continue
            src_attr = (
                "placeholder"
                if pref_key == "ph."
                else "aria-label"
                if pref_key == "aria."
                else "title"
            )
            text = (amap.get(src_attr) or "").strip()
            if text:
                self.entries[pref_key + key] = text

    def handle_endtag(self, tag: str) -> None:
        if not self._stack:
            return
        key, chunks = self._stack.pop()
        txt = " ".join(" ".join(chunks).split())
        if txt:
            self.entries[key] = txt

    def handle_data(self, data: str) -> None:
        if not self._stack:
            return
        self._stack[-1][1].append(data)


def collect_source_entries() -> dict[str, str]:
    app = create_app()
    found: dict[str, str] = {}
    with app.test_client() as client:
        for route in ROUTES:
            resp = client.get(route)
            if resp.status_code != 200:
                raise RuntimeError(f"Failed route {route}: {resp.status_code}")
            parser = I18nExtractor()
            parser.feed(resp.get_data(as_text=True))
            found.update(parser.entries)
    return dict(sorted(found.items()))


def build_bundles(output_dir: Path) -> None:
    source_entries = collect_source_entries()
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "source_en.json").write_text(
        json.dumps({"entries": source_entries}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    for locale in SUPPORTED_LOCALES:
        target = locale_to_target(locale)
        translated = translate_entries(source_entries, target)
        payload = {
            "locale": locale,
            "target": target,
            "entries": translated,
        }
        out_file = output_dir / f"{target}.json"
        out_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {out_file}")


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    output_dir = repo_root / "static" / "i18n"
    if not (os.getenv("Agent_Broncos_Language_Translation") or "").strip():
        raise SystemExit("Missing Agent_Broncos_Language_Translation environment variable")
    build_bundles(output_dir)


if __name__ == "__main__":
    main()
