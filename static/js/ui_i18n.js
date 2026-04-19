/**
 * Site-wide UI language: reads CPP_UI_LANG (same key as home dashboard),
 * translates static labels via POST /api/translate/batch (Langbly).
 * English originals are captured once on first DOMContentLoaded (server HTML).
 */
(function () {
  var LANG_KEY = "CPP_UI_LANG";
  var CACHE_PREFIX = "CPP_I18N_CACHE_v2_";
  var BUNDLE_PREFIX = "CPP_I18N_BUNDLE_v1_";
  var PREFETCH_KEY_PREFIX = "CPP_I18N_PREFETCH_v1_";
  var BUNDLE_LOCALES = ["en", "es", "zh-CN", "vi", "ko", "ja", "ar", "fr", "de", "hi"];

  /** @type {{ text: Record<string, string>, placeholder: Record<string, string>, aria: Record<string, string>, title: Record<string, string> } | null} */
  var originals = null;
  /** @type {Record<string, string>} */
  var resolvedEntries = {};

  function readLocale() {
    try {
      return localStorage.getItem(LANG_KEY) || "en-US";
    } catch {
      return "en-US";
    }
  }

  function localeToTarget(locale) {
    if (!locale || String(locale).toLowerCase().indexOf("en") === 0) return "en";
    var lower = String(locale).toLowerCase();
    if (lower === "zh-cn") return "zh-CN";
    return String(locale).split("-")[0] || "en";
  }

  function getApiTarget() {
    return localeToTarget(readLocale());
  }

  function shortHash(str) {
    var h = 5381;
    for (var i = 0; i < str.length; i++) {
      h = ((h << 5) + h + str.charCodeAt(i)) | 0;
    }
    return (h >>> 0).toString(36);
  }

  function setLangStatus(msg, isError) {
    var el = document.getElementById("dashLangTranslateNote") || document.getElementById("langTranslateNote");
    if (!el) return;
    if (!msg) {
      el.textContent = "";
      el.hidden = true;
      el.style.color = "";
      return;
    }
    el.textContent = msg;
    el.hidden = false;
    el.style.color = isError ? "#f0a8a8" : "";
  }

  function clearCache() {
    try {
      var keys = [];
      for (var i = 0; i < sessionStorage.length; i++) {
        var k = sessionStorage.key(i);
        if (k && k.indexOf(CACHE_PREFIX) === 0) keys.push(k);
      }
      keys.forEach(function (k) {
        sessionStorage.removeItem(k);
      });
    } catch {
      /* ignore */
    }
  }

  function readCachedBundle(target) {
    try {
      var raw = localStorage.getItem(BUNDLE_PREFIX + target);
      if (!raw) return null;
      var parsed = JSON.parse(raw);
      if (!parsed || !parsed.entries || typeof parsed.entries !== "object") return null;
      return parsed.entries;
    } catch {
      return null;
    }
  }

  function writeCachedBundle(target, entries) {
    try {
      localStorage.setItem(BUNDLE_PREFIX + target, JSON.stringify({ entries: entries, ts: Date.now() }));
    } catch {
      /* ignore */
    }
  }

  async function fetchLocaleBundle(target) {
    if (!target || BUNDLE_LOCALES.indexOf(target) < 0) return null;
    var cached = readCachedBundle(target);
    if (cached) return cached;
    try {
      var res = await fetch("/static/i18n/" + encodeURIComponent(target) + ".json", { cache: "force-cache" });
      if (!res.ok) return null;
      var data = await res.json().catch(function () {
        return null;
      });
      if (!data || !data.entries || typeof data.entries !== "object") return null;
      writeCachedBundle(target, data.entries);
      return data.entries;
    } catch {
      return null;
    }
  }

  function subsetMap(full, keys, sourceEntries) {
    var out = {};
    var missing = {};
    keys.forEach(function (k) {
      if (full && full[k] != null) out[k] = full[k];
      else if (sourceEntries && sourceEntries[k] != null) missing[k] = sourceEntries[k];
    });
    return { out: out, missing: missing };
  }

  function parseEntriesFromDocument(doc) {
    var out = {};
    if (!doc || !doc.querySelectorAll) return out;
    doc.querySelectorAll("[data-i18n]").forEach(function (el) {
      var k = el.getAttribute("data-i18n");
      var v = (el.textContent || "").trim();
      if (k && v) out[k] = v;
    });
    doc.querySelectorAll("[data-i18n-placeholder]").forEach(function (el) {
      var k = el.getAttribute("data-i18n-placeholder");
      var v = (el.getAttribute("placeholder") || "").trim();
      if (k && v) out["ph." + k] = v;
    });
    doc.querySelectorAll("[data-i18n-aria]").forEach(function (el) {
      var k = el.getAttribute("data-i18n-aria");
      var v = (el.getAttribute("aria-label") || "").trim();
      if (k && v) out["aria." + k] = v;
    });
    doc.querySelectorAll("[data-i18n-title]").forEach(function (el) {
      var k = el.getAttribute("data-i18n-title");
      var v = (el.getAttribute("title") || "").trim();
      if (k && v) out["title." + k] = v;
    });
    return out;
  }

  async function prefetchSiteI18n(locale) {
    var target = localeToTarget(locale || readLocale());
    if (!target || target === "en") return;
    var already = false;
    try {
      already = sessionStorage.getItem(PREFETCH_KEY_PREFIX + target) === "1";
    } catch {
      already = false;
    }
    if (already) return;
    var routes = ["/", "/chat", "/corpus-map", "/pulse"];
    var entries = {};
    for (var i = 0; i < routes.length; i++) {
      try {
        var res = await fetch(routes[i], { cache: "force-cache" });
        if (!res.ok) continue;
        var html = await res.text();
        var doc = new DOMParser().parseFromString(html, "text/html");
        entries = Object.assign(entries, parseEntriesFromDocument(doc));
      } catch {
        /* ignore individual route fetch failure */
      }
    }
    var keys = Object.keys(entries);
    if (!keys.length) return;
    var bundle = readCachedBundle(target) || {};
    var missing = {};
    keys.forEach(function (k) {
      if (bundle[k] == null && entries[k] != null) missing[k] = entries[k];
    });
    var missingKeys = Object.keys(missing);
    if (missingKeys.length) {
      try {
        var translated = await translateViaApi(target, missing);
        bundle = Object.assign({}, bundle, translated);
        writeCachedBundle(target, bundle);
      } catch {
        /* keep moving; this is a background optimization */
      }
    }
    try {
      sessionStorage.setItem(PREFETCH_KEY_PREFIX + target, "1");
    } catch {
      /* ignore */
    }
  }

  function captureOriginals() {
    var o = { text: {}, placeholder: {}, aria: {}, title: {} };
    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      var k = el.getAttribute("data-i18n");
      if (k) o.text[k] = el.textContent;
    });
    document.querySelectorAll("[data-i18n-placeholder]").forEach(function (el) {
      var k = el.getAttribute("data-i18n-placeholder");
      if (k) o.placeholder[k] = el.getAttribute("placeholder") || "";
    });
    document.querySelectorAll("[data-i18n-aria]").forEach(function (el) {
      var k = el.getAttribute("data-i18n-aria");
      if (k) o.aria[k] = el.getAttribute("aria-label") || "";
    });
    document.querySelectorAll("[data-i18n-title]").forEach(function (el) {
      var k = el.getAttribute("data-i18n-title");
      if (k) o.title[k] = el.getAttribute("title") || "";
    });
    originals = o;
  }

  function buildEntries() {
    if (!originals) return {};
    var entries = {};
    Object.keys(originals.text).forEach(function (k) {
      var v = originals.text[k];
      if (v && String(v).trim()) entries[k] = String(v).trim();
    });
    Object.keys(originals.placeholder).forEach(function (k) {
      var v = originals.placeholder[k];
      if (v && String(v).trim()) entries["ph." + k] = String(v).trim();
    });
    Object.keys(originals.aria).forEach(function (k) {
      var v = originals.aria[k];
      if (v && String(v).trim()) entries["aria." + k] = String(v).trim();
    });
    Object.keys(originals.title).forEach(function (k) {
      var v = originals.title[k];
      if (v && String(v).trim()) entries["title." + k] = String(v).trim();
    });
    return entries;
  }

  function applyTranslations(map) {
    resolvedEntries = Object.assign({}, resolvedEntries, map || {});
    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      var k = el.getAttribute("data-i18n");
      if (k && map[k] != null) el.textContent = map[k];
    });
    document.querySelectorAll("[data-i18n-placeholder]").forEach(function (el) {
      var k = el.getAttribute("data-i18n-placeholder");
      if (k && map["ph." + k] != null) el.setAttribute("placeholder", map["ph." + k]);
    });
    document.querySelectorAll("[data-i18n-aria]").forEach(function (el) {
      var k = el.getAttribute("data-i18n-aria");
      if (k && map["aria." + k] != null) el.setAttribute("aria-label", map["aria." + k]);
    });
    document.querySelectorAll("[data-i18n-title]").forEach(function (el) {
      var k = el.getAttribute("data-i18n-title");
      if (k && map["title." + k] != null) el.setAttribute("title", map["title." + k]);
    });
  }

  function restoreEnglish() {
    if (!originals) return;
    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      var k = el.getAttribute("data-i18n");
      if (k && originals.text[k] != null) el.textContent = originals.text[k];
    });
    document.querySelectorAll("[data-i18n-placeholder]").forEach(function (el) {
      var k = el.getAttribute("data-i18n-placeholder");
      if (k && originals.placeholder[k] != null) el.setAttribute("placeholder", originals.placeholder[k]);
    });
    document.querySelectorAll("[data-i18n-aria]").forEach(function (el) {
      var k = el.getAttribute("data-i18n-aria");
      if (k && originals.aria[k] != null) el.setAttribute("aria-label", originals.aria[k]);
    });
    document.querySelectorAll("[data-i18n-title]").forEach(function (el) {
      var k = el.getAttribute("data-i18n-title");
      if (k && originals.title[k] != null) el.setAttribute("title", originals.title[k]);
    });
    resolvedEntries = buildEntries();
    setLangStatus("", false);
  }

  async function translateViaApi(target, entries) {
    var res = await fetch("/api/translate/batch", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ target: target, entries: entries }),
    });
    var data = await res.json().catch(function () {
      return null;
    });
    if (!res.ok || !data || !data.entries) {
      var detail = (data && (data.detail || data.error)) || res.statusText || String(res.status);
      throw new Error(detail);
    }
    return data.entries;
  }

  /** @param {string} locale BCP-47 */
  async function applyLocale(locale) {
    var target = localeToTarget(locale);
    document.documentElement.lang = locale || "en";

    if (target === "en") {
      restoreEnglish();
      window.dispatchEvent(new CustomEvent("cpp-ui-translated", { detail: { locale: locale, target: "en" } }));
      return;
    }

    if (!originals) captureOriginals();
    var entries = buildEntries();
    var keys = Object.keys(entries);
    if (!keys.length) {
      window.dispatchEvent(new CustomEvent("cpp-ui-translated", { detail: { locale: locale, target: target } }));
      return;
    }

    var pathKey = String(location.pathname || "/").replace(/[^a-z0-9/_-]/gi, "_");
    var cacheKey = CACHE_PREFIX + target + "_" + pathKey + "_" + shortHash(keys.sort().join("|"));
    try {
      var cached = sessionStorage.getItem(cacheKey);
      if (cached) {
        var parsed = JSON.parse(cached);
        if (parsed && parsed.entries) {
          applyTranslations(parsed.entries);
          setLangStatus("", false);
          window.dispatchEvent(new CustomEvent("cpp-ui-translated", { detail: { locale: locale, target: target } }));
          return;
        }
      }
    } catch {
      /* ignore */
    }

    setLangStatus("Translating interface…", false);
    var t0 = performance.now();
    try {
      var merged = {};
      var bundleEntries = await fetchLocaleBundle(target);
      if (bundleEntries) {
        var picked = subsetMap(bundleEntries, keys, entries);
        merged = Object.assign({}, merged, picked.out);
        var missingKeys = Object.keys(picked.missing);
        if (missingKeys.length) {
          var fromApiMissing = await translateViaApi(target, picked.missing);
          merged = Object.assign({}, merged, fromApiMissing);
        }
      } else {
        merged = await translateViaApi(target, entries);
      }
      applyTranslations(merged);
      setLangStatus("", false);
      var translateMs = Math.round(performance.now() - t0);
      try {
        sessionStorage.setItem(cacheKey, JSON.stringify({ entries: merged }));
      } catch {
        /* ignore */
      }
      window.dispatchEvent(
        new CustomEvent("cpp-ui-translated", {
          detail: { locale: locale, target: target, metrics: { translate_batch_ms: translateMs } },
        })
      );
      prefetchSiteI18n(locale);
    } catch (e) {
      setLangStatus("", false);
      console.warn("[ui_i18n] translate batch error", e);
      window.dispatchEvent(
        new CustomEvent("cpp-ui-translate-failed", { detail: { error: "translation_unavailable" } })
      );
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    captureOriginals();
    applyLocale(readLocale());
    prefetchSiteI18n(readLocale());
  });

  window.addEventListener("cpp-ui-lang-changed", function (ev) {
    var loc = (ev && ev.detail && ev.detail.locale) || readLocale();
    clearCache();
    if (localeToTarget(loc) === "en") {
      restoreEnglish();
      document.documentElement.lang = loc || "en";
      window.dispatchEvent(new CustomEvent("cpp-ui-translated", { detail: { locale: loc, target: "en" } }));
      return;
    }
    applyLocale(loc);
  });

  window.addEventListener("cpp-ui-lang-changed", function (ev) {
    var loc = (ev && ev.detail && ev.detail.locale) || readLocale();
    var target = localeToTarget(loc);
    if (!target || target === "en") return;
    fetchLocaleBundle(target).catch(function () {
      /* ignore */
    });
  });

  window.CPPUiI18n = {
    applyLocale: applyLocale,
    readLocale: readLocale,
    clearCache: clearCache,
    localeToTarget: localeToTarget,
    getApiTarget: getApiTarget,
    getResolvedText: function (key, fallback) {
      if (key && resolvedEntries[key] != null) return resolvedEntries[key];
      return fallback != null ? fallback : "";
    },
    prefetchLocaleBundle: function (locale) {
      var target = localeToTarget(locale || readLocale());
      if (!target || target === "en") return Promise.resolve(null);
      return fetchLocaleBundle(target);
    },
  };
})();
