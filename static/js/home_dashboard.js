(function () {
  const LANG_KEY = "CPP_UI_LANG";
  const locales = [
    { code: "en-US", label: "English (US)" },
    { code: "es-MX", label: "Español (México)" },
    { code: "zh-CN", label: "中文 (简体)" },
    { code: "vi-VN", label: "Tiếng Việt" },
    { code: "ko-KR", label: "한국어" },
    { code: "ja-JP", label: "日本語" },
    { code: "ar-SA", label: "العربية" },
    { code: "fr-FR", label: "Français" },
    { code: "de-DE", label: "Deutsch" },
    { code: "hi-IN", label: "हिन्दी" },
  ];

  const weatherEl = document.getElementById("dashWeather");
  const weatherSub = document.getElementById("dashWeatherSub");
  const timeEl = document.getElementById("dashTime");
  const langEl = document.getElementById("dashLang");

  function tickClock() {
    if (!timeEl) return;
    try {
      const fmt = new Intl.DateTimeFormat("en-US", {
        timeZone: "America/Los_Angeles",
        weekday: "short",
        hour: "numeric",
        minute: "2-digit",
        second: "2-digit",
        hour12: true,
      });
      timeEl.textContent = fmt.format(new Date());
    } catch {
      timeEl.textContent = new Date().toLocaleString();
    }
  }

  async function loadWeather() {
    if (!weatherEl) return;
    const lat = 34.0576;
    const lon = -117.8203;
    try {
      const url =
        "https://api.open-meteo.com/v1/forecast?latitude=" +
        lat +
        "&longitude=" +
        lon +
        "&current=temperature_2m,weather_code&temperature_unit=fahrenheit&timezone=America%2FLos_Angeles";
      const res = await fetch(url);
      const data = await res.json();
      const t = data && data.current && data.current.temperature_2m;
      if (typeof t === "number") {
        weatherEl.textContent = Math.round(t) + "°F";
        if (weatherSub) weatherSub.textContent = "Open-Meteo · Pomona area";
      } else {
        weatherEl.textContent = "Unavailable";
      }
    } catch {
      weatherEl.textContent = "Unavailable";
      if (weatherSub) weatherSub.textContent = "Check network or try again later";
    }
  }

  function initLang() {
    if (!langEl) return;
    const saved = (function () {
      try {
        return localStorage.getItem(LANG_KEY);
      } catch {
        return null;
      }
    })();
    locales.forEach((L) => {
      const o = document.createElement("option");
      o.value = L.code;
      o.textContent = L.label;
      langEl.appendChild(o);
    });
    langEl.value = locales.some((x) => x.code === saved) ? saved : "en-US";
    langEl.addEventListener("change", () => {
      try {
        localStorage.setItem(LANG_KEY, langEl.value);
      } catch {
        /* ignore */
      }
    });
  }

  initLang();
  tickClock();
  setInterval(tickClock, 1000);
  loadWeather();
})();
