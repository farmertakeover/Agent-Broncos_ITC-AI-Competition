/**
 * Populates every select[data-cpp-ui-lang], syncs with localStorage (CPP_UI_LANG),
 * and dispatches cpp-ui-lang-changed on change (same contract as the home dashboard).
 */
(function () {
  var LANG_KEY = "CPP_UI_LANG";
  var locales = [
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

  function readSaved() {
    try {
      return localStorage.getItem(LANG_KEY);
    } catch {
      return null;
    }
  }

  /** BCP-47-ish: collapse legacy underscores so es_MX matches option es-MX. */
  function canonUiLang(raw) {
    if (!raw) return null;
    return String(raw).trim().replace(/_/g, "-");
  }

  function clearLegacyI18nCaches() {
    try {
      for (var i = sessionStorage.length - 1; i >= 0; i--) {
        var k = sessionStorage.key(i);
        if (!k) continue;
        if (k.indexOf("CPP_I18N_CACHE_v1_") === 0 || k.indexOf("CPP_I18N_CACHE_v2_") === 0) {
          sessionStorage.removeItem(k);
        }
      }
    } catch {
      /* ignore */
    }
  }

  function populateSelect(sel) {
    if (!sel || sel.getAttribute("data-cpp-ui-lang-populated") === "1") return;
    sel.setAttribute("data-cpp-ui-lang-populated", "1");
    sel.innerHTML = "";
    locales.forEach(function (L) {
      var o = document.createElement("option");
      o.value = L.code;
      o.textContent = L.label;
      sel.appendChild(o);
    });
  }

  function syncAllSelects(value) {
    document.querySelectorAll("select[data-cpp-ui-lang]").forEach(function (sel) {
      populateSelect(sel);
      if (locales.some(function (x) { return x.code === value; })) sel.value = value;
      else sel.value = "en-US";
    });
  }

  function onLocaleChange(nextLocale) {
    try {
      localStorage.setItem(LANG_KEY, nextLocale);
    } catch {
      /* ignore */
    }
    clearLegacyI18nCaches();
    try {
      if (window.CPPUiI18n && typeof window.CPPUiI18n.clearCache === "function") {
        window.CPPUiI18n.clearCache();
      }
    } catch {
      /* ignore */
    }
    try {
      window.dispatchEvent(new CustomEvent("cpp-ui-lang-changed", { detail: { locale: nextLocale } }));
    } catch {
      /* ignore */
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    var saved = readSaved();
    var canon = canonUiLang(saved);
    var inList = canon && locales.some(function (x) { return x.code === canon; });
    if (inList && canon && saved && canon !== saved) {
      try {
        localStorage.setItem(LANG_KEY, canon);
      } catch {
        /* ignore */
      }
    }
    var value = inList ? canon : "en-US";
    document.querySelectorAll("select[data-cpp-ui-lang]").forEach(function (sel) {
      populateSelect(sel);
    });
    syncAllSelects(value);
    document.querySelectorAll("select[data-cpp-ui-lang]").forEach(function (sel) {
      sel.addEventListener("change", function () {
        syncAllSelects(sel.value);
        onLocaleChange(sel.value);
      });
    });
  });

  window.addEventListener("cpp-ui-lang-changed", function (ev) {
    var loc = (ev && ev.detail && ev.detail.locale) || readSaved() || "en-US";
    syncAllSelects(loc);
  });
})();
