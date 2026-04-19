(function () {
  var PREF_KEY = "cpp_dashboard_prefs";
  var TODO_KEY = "cpp_dashboard_todos";
  var FEED_SECTIONS = ["news", "events", "announcements"];
  var PREF_SHOW_KEYS = {
    announcements: "home.dashPrefShowAnnouncements",
    events: "home.dashPrefShowEvents",
    news: "home.dashPrefShowNews",
  };
  var PREF_SHOW_FALLBACKS = {
    announcements: "Show announcements",
    events: "Show events",
    news: "Show news",
  };

  var lastDashPayload = null;

  function readJson(key, fallback) {
    try {
      var raw = localStorage.getItem(key);
      if (!raw) return fallback;
      var o = JSON.parse(raw);
      return o && typeof o === "object" ? o : fallback;
    } catch {
      return fallback;
    }
  }

  function writeJson(key, val) {
    try {
      localStorage.setItem(key, JSON.stringify(val));
    } catch {
      /* ignore */
    }
  }

  function defaultPrefs() {
    return { order: ["news", "events", "announcements"], hidden: [], tags: [] };
  }

  function loadPrefs() {
    var p = readJson(PREF_KEY, {});
    var d = defaultPrefs();
    if (!Array.isArray(p.order) || !p.order.length) p.order = d.order;
    if (!Array.isArray(p.hidden)) p.hidden = [];
    if (!Array.isArray(p.tags)) p.tags = [];
    return p;
  }

  function savePrefs(prefs) {
    writeJson(PREF_KEY, prefs);
    syncPrefsToServer(prefs);
  }

  function syncPrefsToServer(prefs) {
    fetch("/api/dashboard/preferences", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        order: prefs.order,
        hidden: prefs.hidden,
        tags: prefs.tags,
      }),
    }).catch(function () {});
  }

  function tStr(key, fallback) {
    var pool = document.getElementById("dashJsI18nPool");
    if (pool) {
      try {
        var el = pool.querySelector('[data-i18n="' + key + '"]');
        if (el) {
          var tx = (el.textContent || "").trim();
          if (tx) return tx;
        }
      } catch {
        /* ignore */
      }
    }
    if (window.CPPUiI18n && typeof window.CPPUiI18n.getResolvedText === "function") {
      var r = window.CPPUiI18n.getResolvedText(key, fallback);
      if (r) return r;
    }
    return fallback;
  }

  function applyPanelOrder(prefs) {
    var col = document.getElementById("dashColFeeds");
    if (!col) return;
    var panels = {};
    col.querySelectorAll(".dash-panel").forEach(function (el) {
      var s = el.getAttribute("data-section");
      if (s) panels[s] = el;
    });
    var order = prefs.order.filter(function (s) {
      return FEED_SECTIONS.indexOf(s) >= 0;
    });
    FEED_SECTIONS.forEach(function (s) {
      if (order.indexOf(s) < 0) order.push(s);
    });
    order.forEach(function (sec) {
      var n = panels[sec];
      if (n) col.appendChild(n);
    });
  }

  function applyHidden(prefs) {
    var col = document.getElementById("dashColFeeds");
    if (!col) return;
    col.querySelectorAll(".dash-panel").forEach(function (el) {
      var sec = el.getAttribute("data-section");
      if (!sec) return;
      if (prefs.hidden.indexOf(sec) >= 0) el.classList.add("hidden");
      else el.classList.remove("hidden");
    });
  }

  function buildPrefsUi(prefs) {
    var fs = document.getElementById("dashPrefsFieldset");
    if (!fs) return;
    fs.innerHTML = "";
    FEED_SECTIONS.forEach(function (sec) {
      var id = "dashPrefHide_" + sec;
      var label = document.createElement("label");
      var cb = document.createElement("input");
      cb.type = "checkbox";
      cb.id = id;
      cb.checked = prefs.hidden.indexOf(sec) < 0;
      cb.setAttribute("data-section", sec);
      cb.addEventListener("change", function () {
        var p = loadPrefs();
        if (cb.checked) {
          p.hidden = p.hidden.filter(function (x) {
            return x !== sec;
          });
        } else if (p.hidden.indexOf(sec) < 0) p.hidden.push(sec);
        savePrefs(p);
        applyHidden(p);
      });
      var span = document.createElement("span");
      var ik = PREF_SHOW_KEYS[sec] || "";
      span.textContent = ik ? tStr(ik, PREF_SHOW_FALLBACKS[sec] || "Show " + sec) : "Show " + sec;
      label.appendChild(cb);
      label.appendChild(span);
      fs.appendChild(label);
    });
  }

  function formatWhen(iso) {
    if (!iso) return "";
    try {
      var d = new Date(iso);
      if (isNaN(d.getTime())) return "";
      return new Intl.DateTimeFormat("en-US", {
        timeZone: "America/Los_Angeles",
        month: "short",
        day: "numeric",
        hour: "numeric",
        minute: "2-digit",
      }).format(d);
    } catch {
      return "";
    }
  }

  function formatEventRange(c) {
    var s = c.start_at ? formatWhen(c.start_at) : "";
    var e = c.end_at ? formatWhen(c.end_at) : "";
    if (s && e && s !== e) return s + " – " + e;
    if (s) return s;
    if (e) return "Until " + e;
    return "";
  }

  function renderCardList(ul, cards) {
    if (!ul) return;
    var itemFb = tStr("home.dashCardFallback", "Item");
    ul.innerHTML = "";
    (cards || []).slice(0, 12).forEach(function (c) {
      var li = document.createElement("li");
      var title = document.createElement("p");
      title.className = "dash-card-title";
      if (c.url) {
        var a = document.createElement("a");
        a.href = c.url;
        a.rel = "noopener noreferrer";
        a.target = "_blank";
        a.textContent = c.title || itemFb;
        title.appendChild(a);
      } else {
        title.textContent = c.title || itemFb;
      }
      li.appendChild(title);
      if (c.summary) {
        var sm = document.createElement("p");
        sm.className = "dash-card-summary";
        sm.textContent = c.summary;
        li.appendChild(sm);
      }
      var meta = document.createElement("p");
      meta.className = "dash-meta";
      var bits = [];
      var range = formatEventRange(c);
      if (range) bits.push(range);
      if (c.repeat_label) bits.push(String(c.repeat_label));
      if (c.source) bits.push(String(c.source).replace(/_/g, " "));
      meta.textContent = bits.join(" · ");
      li.appendChild(meta);
      ul.appendChild(li);
    });
  }

  function setPanelState(panel, state, msg) {
    if (!panel) return;
    var st = panel.querySelector(".dash-panel-status");
    var list = panel.querySelector(".dash-card-list");
    if (st) {
      st.setAttribute("data-state", state);
      st.textContent = msg || "";
    }
    if (list) {
      if (state === "ready") list.hidden = list.children.length === 0;
      else list.hidden = true;
    }
  }

  function showBannerFromQuery() {
    var params = new URLSearchParams(window.location.search || "");
    var err = params.get("dash_error");
    var el = document.getElementById("dashBanner");
    if (!el) return;
    if (err) {
      el.textContent = err.replace(/\+/g, " ");
      el.classList.remove("hidden");
    } else {
      el.classList.add("hidden");
    }
  }

  function renderCampusLinks(rows) {
    var sec = document.getElementById("dashCampusLinksSection");
    var ul = document.getElementById("dashCampusLinksList");
    if (!sec || !ul) return;
    if (!rows || !rows.length) {
      sec.hidden = true;
      ul.innerHTML = "";
      return;
    }
    sec.hidden = false;
    ul.innerHTML = "";
    rows.forEach(function (row) {
      var li = document.createElement("li");
      li.className = "dash-campus-link-tile";
      var a = document.createElement("a");
      a.href = row.url;
      a.className = "dash-campus-link-a";
      a.rel = "noopener noreferrer";
      a.target = "_blank";
      var thumb = document.createElement("span");
      thumb.className = "dash-campus-link-thumb";
      if (row.icon) {
        var img = document.createElement("img");
        img.className = "dash-campus-link-icon";
        img.src = row.icon;
        img.width = 28;
        img.height = 28;
        img.alt = "";
        img.loading = "lazy";
        img.decoding = "async";
        img.addEventListener("error", function () {
          img.remove();
          var ph = document.createElement("span");
          ph.className = "dash-campus-link-icon-fallback";
          ph.setAttribute("aria-hidden", "true");
          ph.textContent = ((row.title || row.url || "?").trim().charAt(0) || "?").toUpperCase();
          thumb.appendChild(ph);
        });
        thumb.appendChild(img);
      } else {
        var ph0 = document.createElement("span");
        ph0.className = "dash-campus-link-icon-fallback";
        ph0.setAttribute("aria-hidden", "true");
        ph0.textContent = ((row.title || row.url || "?").trim().charAt(0) || "?").toUpperCase();
        thumb.appendChild(ph0);
      }
      var cap = document.createElement("span");
      cap.className = "dash-campus-link-label";
      cap.textContent = row.title || row.url;
      a.appendChild(thumb);
      a.appendChild(cap);
      li.appendChild(a);
      ul.appendChild(li);
    });
  }

  function applyDashboardPayload(data) {
    if (!data || typeof data !== "object") return;
    var mapping = {
      announcements: { ul: "dashListAnnouncements", panelSel: '[data-section="announcements"]' },
      events: { ul: "dashListEvents", panelSel: '[data-section="events"]' },
      news: { ul: "dashListNews", panelSel: '[data-section="news"]' },
    };
    var emptyMsg = tStr("home.dashEmptyGeneric", "No items right now.");
    if (data.preferences && typeof data.preferences === "object") {
      var sp = data.preferences;
      var merged = loadPrefs();
      if (Array.isArray(sp.order) && sp.order.length) {
        merged.order = sp.order.filter(function (s) {
          return FEED_SECTIONS.indexOf(s) >= 0;
        });
        FEED_SECTIONS.forEach(function (s) {
          if (merged.order.indexOf(s) < 0) merged.order.push(s);
        });
      }
      if (Array.isArray(sp.hidden)) merged.hidden = sp.hidden.slice();
      writeJson(PREF_KEY, merged);
      applyPanelOrder(merged);
      applyHidden(merged);
      buildPrefsUi(merged);
    }
    var sections = data.sections || {};
    Object.keys(mapping).forEach(function (key) {
      var m = mapping[key];
      var ul = document.getElementById(m.ul);
      var panel = document.querySelector(m.panelSel);
      var cards = sections[key] || [];
      renderCardList(ul, cards);
      if (!cards.length) {
        if (ul) {
          ul.innerHTML = "";
          ul.hidden = true;
        }
        setPanelState(panel, "empty", emptyMsg);
      } else {
        setPanelState(panel, "ready", "");
      }
    });
    renderCampusLinks(data.campus_links || []);
  }

  function loadTodos() {
    var list = document.getElementById("dashTodoList");
    if (!list) return;
    var removeLbl = tStr("home.dashTodoRemoveAria", "Remove to-do");
    var items = readJson(TODO_KEY, []);
    if (!Array.isArray(items)) items = [];
    list.innerHTML = "";
    items.forEach(function (text, idx) {
      var li = document.createElement("li");
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "btn ghost";
      btn.textContent = "✕";
      btn.setAttribute("aria-label", removeLbl);
      btn.addEventListener("click", function () {
        items.splice(idx, 1);
        writeJson(TODO_KEY, items);
        loadTodos();
      });
      var span = document.createElement("span");
      span.textContent = text;
      li.appendChild(btn);
      li.appendChild(span);
      list.appendChild(li);
    });
  }

  function bindTodoForm() {
    var form = document.getElementById("dashTodoForm");
    var input = document.getElementById("dashTodoInput");
    if (!form || !input) return;
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var t = (input.value || "").trim();
      if (!t) return;
      var items = readJson(TODO_KEY, []);
      if (!Array.isArray(items)) items = [];
      items.push(t);
      writeJson(TODO_KEY, items);
      input.value = "";
      loadTodos();
    });
  }

  /* --- Clock & weather (client) --- */
  var weatherEl = document.getElementById("dashWeather");
  var timeEl = document.getElementById("dashTime");

  function tickClock() {
    if (!timeEl) return;
    try {
      var fmt = new Intl.DateTimeFormat("en-US", {
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
    var statusEl = document.getElementById("dashWeatherStatus");
    var unavail = tStr("home.dashWeatherUnavailable", "Unavailable");
    var retryHint = tStr("home.dashWeatherRetry", "Check network or try again later");
    var lat = 34.0576;
    var lon = -117.8203;
    try {
      var url =
        "https://api.open-meteo.com/v1/forecast?latitude=" +
        lat +
        "&longitude=" +
        lon +
        "&current=temperature_2m,weather_code&temperature_unit=fahrenheit&timezone=America%2FLos_Angeles";
      var res = await fetch(url);
      var data = await res.json();
      var t = data && data.current && data.current.temperature_2m;
      if (typeof t === "number") {
        weatherEl.textContent = Math.round(t) + "°F";
        if (statusEl) statusEl.textContent = "";
      } else {
        weatherEl.textContent = unavail;
        if (statusEl) statusEl.textContent = "";
      }
    } catch {
      weatherEl.textContent = unavail;
      if (statusEl) statusEl.textContent = retryHint;
    }
  }

  async function loadDashboard() {
    var mapping = {
      announcements: { ul: "dashListAnnouncements", panelSel: '[data-section="announcements"]' },
      events: { ul: "dashListEvents", panelSel: '[data-section="events"]' },
      news: { ul: "dashListNews", panelSel: '[data-section="news"]' },
    };
    var loadErr = tStr("home.dashLoadError", "Could not load dashboard. Try again later.");
    try {
      var res = await fetch("/api/dashboard", { credentials: "same-origin" });
      var data = await res.json();
      if (!data || typeof data !== "object") throw new Error("bad_json");
      lastDashPayload = data;
      applyDashboardPayload(data);
    } catch (e) {
      lastDashPayload = null;
      Object.keys(mapping).forEach(function (key) {
        var m = mapping[key];
        var panel = document.querySelector(m.panelSel);
        setPanelState(panel, "error", loadErr);
      });
    }
  }

  function refreshAfterUiLang() {
    if (lastDashPayload) applyDashboardPayload(lastDashPayload);
    else loadDashboard();
    buildPrefsUi(loadPrefs());
    loadTodos();
    loadWeather();
  }

  window.addEventListener("cpp-ui-translated", function () {
    refreshAfterUiLang();
  });
  window.addEventListener("cpp-ui-translate-failed", function () {
    refreshAfterUiLang();
  });
  window.addEventListener("cpp-ui-lang-changed", function () {
    /* Translation runs async; cpp-ui-translated (or -failed) will follow for non-English. */
  });

  var prefs = loadPrefs();
  applyPanelOrder(prefs);
  applyHidden(prefs);
  buildPrefsUi(prefs);
  showBannerFromQuery();
  bindTodoForm();
  loadTodos();

  tickClock();
  setInterval(tickClock, 1000);
  loadWeather();
  loadDashboard();
})();
