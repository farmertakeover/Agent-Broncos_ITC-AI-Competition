"""OpenWeatherMap current weather helper."""

from __future__ import annotations

import os
from typing import Any

import httpx


class WeatherConfigError(RuntimeError):
    """Raised when the OpenWeatherMap API key is missing."""


class WeatherAPIError(RuntimeError):
    """Raised when OpenWeatherMap returns an error payload."""


def get_weather(city: str = "Pomona") -> dict[str, Any]:
    """
    Fetch current weather for ``city`` (metric units).

    Requires env ``Agent_Broncos_Weather_API`` (OpenWeatherMap API key).
    """
    api_key = (os.getenv("Agent_Broncos_Weather_API") or "").strip()
    if not api_key:
        raise WeatherConfigError(
            "Set Agent_Broncos_Weather_API in the environment (see .env.example)."
        )
    city = (city or "Pomona").strip() or "Pomona"
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}
    with httpx.Client(timeout=15.0) as client:
        resp = client.get(url, params=params)
        try:
            data = resp.json()
        except ValueError as e:
            raise WeatherAPIError(f"Invalid JSON from OpenWeatherMap: {e}") from e

    if resp.status_code != 200:
        msg = data.get("message") if isinstance(data, dict) else str(data)
        raise WeatherAPIError(msg or f"HTTP {resp.status_code}")

    try:
        return {
            "city": city,
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
        }
    except (KeyError, IndexError, TypeError) as e:
        raise WeatherAPIError(f"Unexpected OpenWeatherMap payload: {e}") from e


__all__ = ["WeatherAPIError", "WeatherConfigError", "get_weather"]
