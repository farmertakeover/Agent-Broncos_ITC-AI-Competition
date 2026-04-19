(function () {
  const messagesEl = document.getElementById("messages");
  const form = document.getElementById("chatForm");
  const composerInputRow = document.getElementById("composerInputRow");
  const input = document.getElementById("msg");
  const sendBtn = document.getElementById("sendBtn");
  const micBtn = document.getElementById("micBtn");
  const micHint = document.getElementById("micHint");
  const speakToggle = document.getElementById("speakToggle");
  const replyNotifyToggle = document.getElementById("replyNotifyToggle");
  const graphPanel = document.getElementById("graphPanel");
  const graphCanvas = document.getElementById("graphCanvas");
  const chatPerfNote = document.getElementById("chatPerfNote");
  const voiceInline = document.getElementById("voiceInline");
  const voiceInlineStatus = document.getElementById("voiceInlineStatus");
  const waveCanvas = document.getElementById("waveCanvas");
  const micConfirm = document.getElementById("micConfirm");
  const micDiscard = document.getElementById("micDiscard");
  const micSpinner = document.getElementById("micSpinner");
  const micDecision = document.getElementById("micDecision");
  const recordingPill = document.getElementById("recordingPill");
  const chatMain = document.getElementById("chatMain");
  const chatBusyOverlay = document.getElementById("chatBusyOverlay");
  const chatBusyText = document.getElementById("chatBusyText");
  const thinkingDots = document.getElementById("thinkingDots");
  const mascotInline = document.getElementById("mascotInline");
  const broncoSpeechBubble = document.getElementById("broncoSpeechBubble");
  const speechPauseBtn = document.getElementById("speechPauseBtn");
  const speechStopBtn = document.getElementById("speechStopBtn");
  const micReviewAudioRow = document.getElementById("micReviewAudioRow");
  const micReviewAudio = document.getElementById("micReviewAudio");
  const micReviewMeta = document.getElementById("micReviewMeta");
  const i18nRoot = document.getElementById("chatI18nStrings");
  const defaultInputPlaceholder = input ? input.getAttribute("placeholder") || "" : "";

  const STORAGE_KEY = "cpp_chat_session_v1";
  /** Mirrors ``cpp_session_id`` (localStorage) for /api/chat/recovery. */
  const CHAT_API_SESSION_KEY = "cpp_chat_api_session_id";
  let sessionId = null;
  try {
    sessionId = localStorage.getItem("cpp_session_id") || null;
  } catch {
    sessionId = null;
  }
  try {
    if (sessionId && !sessionStorage.getItem(CHAT_API_SESSION_KEY)) {
      sessionStorage.setItem(CHAT_API_SESSION_KEY, sessionId);
    }
  } catch {
    /* ignore */
  }
  const chatUiDefaults = {
    sourcesPrefix: "Sources & links (",
    sourcesSuffix: ")",
    sectionLabel: "Section:",
    speakAction: "Speak",
    tokensLabel: "tokens in·out·total:",
    speechPause: "Pause speech",
    speechResume: "Resume speech",
    noVoiceHint: "No matching voice pack for this language on this device.",
  };

  let speechVoices = [];
  let speechVoicesLoaded = false;
  let speechVoicesPromise = null;

  function readI18nSpan(id, fallback) {
    const el = i18nRoot ? i18nRoot.querySelector("#" + id) : null;
    const txt = el ? String(el.textContent || "").trim() : "";
    return txt || fallback;
  }

  function chatUiText() {
    return {
      sourcesPrefix: readI18nSpan("chatStrSourcesPrefix", chatUiDefaults.sourcesPrefix),
      sourcesSuffix: readI18nSpan("chatStrSourcesSuffix", chatUiDefaults.sourcesSuffix),
      sectionLabel: readI18nSpan("chatStrSectionLabel", chatUiDefaults.sectionLabel),
      speakAction: readI18nSpan("chatStrSpeakAction", chatUiDefaults.speakAction),
      tokensLabel: readI18nSpan("chatStrTokensLabel", chatUiDefaults.tokensLabel),
      speechPause: readI18nSpan("chatStrSpeechPause", chatUiDefaults.speechPause),
      speechResume: readI18nSpan("chatStrSpeechResume", chatUiDefaults.speechResume),
      noVoiceHint: readI18nSpan("chatStrNoVoiceHint", chatUiDefaults.noVoiceHint),
    };
  }

  function normalizeLocaleTag(tag) {
    return String(tag || "").replace("_", "-").toLowerCase();
  }

  function sameLanguage(a, b) {
    const aa = normalizeLocaleTag(a).split("-")[0];
    const bb = normalizeLocaleTag(b).split("-")[0];
    return !!aa && aa === bb;
  }

  function refreshSpeechVoices() {
    if (!window.speechSynthesis) return;
    try {
      speechVoices = window.speechSynthesis.getVoices() || [];
      speechVoicesLoaded = speechVoices.length > 0;
    } catch {
      speechVoices = [];
      speechVoicesLoaded = false;
    }
  }

  function ensureSpeechVoicesReady() {
    if (!window.speechSynthesis) return Promise.resolve([]);
    refreshSpeechVoices();
    if (speechVoicesLoaded) return Promise.resolve(speechVoices);
    if (speechVoicesPromise) return speechVoicesPromise;
    speechVoicesPromise = new Promise(function (resolve) {
      const synth = window.speechSynthesis;
      const done = function () {
        synth.removeEventListener("voiceschanged", done);
        refreshSpeechVoices();
        resolve(speechVoices);
      };
      synth.addEventListener("voiceschanged", done, { once: true });
      window.setTimeout(done, 350);
    }).finally(function () {
      speechVoicesPromise = null;
    });
    return speechVoicesPromise;
  }

  function pickVoiceForLocale(localeTag) {
    const target = normalizeLocaleTag(localeTag);
    if (!speechVoices.length) return null;
    let found = speechVoices.find((v) => normalizeLocaleTag(v.lang) === target);
    if (found) return found;
    found = speechVoices.find((v) => sameLanguage(v.lang, target));
    if (found) return found;
    if (target.indexOf("zh") === 0) {
      found = speechVoices.find((v) => normalizeLocaleTag(v.lang).indexOf("zh") === 0);
      if (found) return found;
    }
    return null;
  }

  function getUiApiTarget() {
    try {
      if (window.CPPUiI18n && typeof window.CPPUiI18n.getApiTarget === "function") {
        return window.CPPUiI18n.getApiTarget();
      }
    } catch {
      /* ignore */
    }
    try {
      var loc = String(localStorage.getItem("CPP_UI_LANG") || "en-US")
        .trim()
        .replace(/_/g, "-");
      if (!loc) return "en";
      var lower = loc.toLowerCase();
      if (lower === "en" || lower.indexOf("en-") === 0) return "en";
      if (lower === "zh-cn" || lower === "zh") return "zh-CN";
      return loc.split("-")[0] || "en";
    } catch {
      return "en";
    }
  }

  function speechLocaleTag() {
    try {
      return localStorage.getItem("CPP_UI_LANG") || "en-US";
    } catch {
      return "en-US";
    }
  }

  /**
   * @param {string} text
   * @param {string} target Langbly target code (e.g. es, en)
   */
  async function translateLine(text, target) {
    if (!text || !target || target === "en") return text;
    var ctrl = new AbortController();
    var timer = window.setTimeout(function () {
      ctrl.abort();
    }, 90000);
    try {
      var res = await fetch("/api/translate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: text, target: target }),
        signal: ctrl.signal,
      });
      var data = await res.json().catch(function () {
        return null;
      });
      if (!res.ok || !data || typeof data.translated !== "string") {
        return text;
      }
      try {
        window.__cppLastTranslateMs =
          (data && data.metrics && Number(data.metrics.translate_ms)) ||
          Number((res.headers.get("Server-Timing") || "").match(/dur=([0-9.]+)/)?.[1]) ||
          null;
      } catch {
        /* ignore */
      }
      return data.translated;
    } catch {
      return text;
    } finally {
      window.clearTimeout(timer);
    }
  }
  /** @type {string | null} */
  let reviewObjectUrl = null;

  /** @type {{role: string, content: string, sources?: object[], usage?: object}[]} */
  let history = [];
  let chatThinking = false;
  let thinkingTimer = 0;
  let graphState = null;
  let currentUtterance = null;
  let speechPaused = false;
  let micPrimed = false;

  function persistHistory() {
    try {
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify(history));
    } catch {
      /* ignore */
    }
  }

  function rehydrateFromStorage() {
    try {
      const raw = sessionStorage.getItem(STORAGE_KEY);
      if (!raw) return;
      const arr = JSON.parse(raw);
      if (!Array.isArray(arr)) return;
      history = arr;
      messagesEl.innerHTML = "";
      arr.forEach((item) => {
        if (item.role === "user") appendBubble("user", item.content);
        else
          appendBubble("assistant", item.content, {
            sources: item.sources,
            usage: item.usage,
          });
      });
    } catch {
      /* ignore */
    }
  }

  function getChatApiSessionId() {
    if (sessionId) return sessionId;
    try {
      return sessionStorage.getItem(CHAT_API_SESSION_KEY);
    } catch {
      return null;
    }
  }

  function setChatApiSessionId(id) {
    if (!id) return;
    sessionId = id;
    try {
      localStorage.setItem("cpp_session_id", sessionId);
    } catch {
      /* ignore */
    }
    try {
      sessionStorage.setItem(CHAT_API_SESSION_KEY, sessionId);
    } catch {
      /* ignore */
    }
  }

  async function ackChatRecovery(sessionId, recoveryId) {
    if (!sessionId || !recoveryId) return;
    try {
      await fetch("/api/chat/recovery/ack", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId, recovery_id: recoveryId }),
      });
    } catch {
      /* ignore */
    }
  }

  function isPlaceholderErrorAssistant(item) {
    if (!item || item.role !== "assistant") return false;
    const c = item.content;
    if (c === "Network error" || c === "bad json") return true;
    return typeof c === "string" && c.indexOf("Network error:") === 0;
  }

  /**
   * If the user left the page while /api/chat was still running, merge the
   * completed server reply from chat_recovery (same session_id).
   */
  async function recoverPendingServerReply() {
    const sid = getChatApiSessionId();
    if (!sid || !messagesEl) return;
    let data;
    try {
      const res = await fetch("/api/chat/recovery?session_id=" + encodeURIComponent(sid));
      if (!res.ok) return;
      data = await res.json().catch(function () {
        return null;
      });
    } catch {
      return;
    }
    if (!data || !data.has_recovery || !data.content) {
      return;
    }
    const rid = data.recovery_id;
    const serverUm = String(data.user_message_en || "").trim();
    const last = history[history.length - 1];
    const prev = history[history.length - 2];
    let replaceIdx = -1;
    if (last && last.role === "user") {
      const um =
        last.content_en != null && last.content_en !== "" ? String(last.content_en).trim() : String(last.content || "").trim();
      if (serverUm && um !== serverUm) {
        void ackChatRecovery(sid, rid);
        return;
      }
    } else if (last && isPlaceholderErrorAssistant(last) && prev && prev.role === "user") {
      const um =
        prev.content_en != null && prev.content_en !== ""
          ? String(prev.content_en).trim()
          : String(prev.content || "").trim();
      if (serverUm && um !== serverUm) {
        void ackChatRecovery(sid, rid);
        return;
      }
      replaceIdx = history.length - 1;
    } else {
      void ackChatRecovery(sid, rid);
      return;
    }

    let rawReply = data.content;
    let reply = rawReply;
    if (getUiApiTarget() !== "en" && reply) {
      reply = await translateLine(reply, getUiApiTarget());
    }
    const entry = {
      role: "assistant",
      content: reply,
      content_en: rawReply,
      sources: data.sources,
      usage: data.usage,
    };
    if (replaceIdx >= 0) {
      history[replaceIdx] = entry;
      if (messagesEl.lastElementChild) messagesEl.removeChild(messagesEl.lastElementChild);
      appendBubble("assistant", reply, { sources: data.sources, usage: data.usage });
    } else {
      appendBubble("assistant", reply, { sources: data.sources, usage: data.usage });
      history.push(entry);
    }
    persistHistory();
    void ackChatRecovery(sid, rid);
    const ids = (data.sources || []).map((s) => s.chunk_id).filter(Boolean);
    if (ids.length) fetchGraph(ids);
    triggerMascotCelebrate();
    maybeNotifyReply(reply);
  }

  function showSpeechBubble(show) {
    if (!broncoSpeechBubble) return;
    broncoSpeechBubble.classList.toggle("hidden", !show);
  }

  function updateSpeechPauseUi() {
    if (!speechPauseBtn) return;
    speechPauseBtn.textContent = speechPaused ? "▶" : "II";
    const ui = chatUiText();
    speechPauseBtn.setAttribute("aria-label", speechPaused ? ui.speechResume : ui.speechPause);
  }

  function stopSpeaking(withPop) {
    if (window.speechSynthesis) {
      try {
        window.speechSynthesis.cancel();
      } catch {
        /* ignore */
      }
    }
    currentUtterance = null;
    speechPaused = false;
    updateSpeechPauseUi();
    if (broncoSpeechBubble && withPop) {
      broncoSpeechBubble.classList.add("popping");
      window.setTimeout(function () {
        broncoSpeechBubble.classList.remove("popping");
        showSpeechBubble(false);
      }, 240);
      return;
    }
    showSpeechBubble(false);
  }

  async function speakText(text) {
    if (!window.speechSynthesis || !text) return;
    try {
      stopSpeaking(false);
      await ensureSpeechVoicesReady();
      const locale = speechLocaleTag();
      const selectedVoice = pickVoiceForLocale(locale);
      const u = new SpeechSynthesisUtterance(text);
      if (selectedVoice) {
        u.voice = selectedVoice;
        u.lang = selectedVoice.lang || locale;
      } else {
        u.lang = locale;
      }
      u.onstart = function () {
        currentUtterance = u;
        speechPaused = false;
        updateSpeechPauseUi();
        showSpeechBubble(true);
      };
      u.onend = function () {
        currentUtterance = null;
        speechPaused = false;
        updateSpeechPauseUi();
        showSpeechBubble(false);
      };
      u.onerror = function () {
        currentUtterance = null;
        speechPaused = false;
        updateSpeechPauseUi();
        showSpeechBubble(false);
      };
      window.speechSynthesis.speak(u);
    } catch {
      /* ignore */
    }
  }

  function setThinking(on) {
    chatThinking = !!on;
    if (!thinkingDots) return;
    if (thinkingTimer) {
      clearInterval(thinkingTimer);
      thinkingTimer = 0;
    }
    thinkingDots.classList.toggle("hidden", !chatThinking);
    if (!chatThinking) {
      thinkingDots.textContent = "";
      return;
    }
    let phase = 0;
    const dotHtml = function (count) {
      let out = "";
      for (let i = 0; i < count; i++) out += '<span class="think-dot"></span>';
      return out;
    };
    const render = function () {
      phase = (phase + 1) % 4;
      thinkingDots.innerHTML = dotHtml(phase);
    };
    render();
    thinkingTimer = window.setInterval(render, 300);
  }

  function triggerMascotCelebrate() {
    if (!mascotInline) return;
    const mascot = mascotInline.querySelector(".billy-mascot");
    if (!mascot) return;
    mascot.classList.remove("celebrate");
    void mascot.offsetWidth;
    mascot.classList.add("celebrate");
    window.setTimeout(function () {
      mascot.classList.remove("celebrate");
    }, 950);
  }

  function maybeNotifyReply(replyText) {
    if (!replyNotifyToggle || !replyNotifyToggle.checked || !("Notification" in window)) return;
    if (Notification.permission !== "granted") return;
    const body = String(replyText || "").slice(0, 180) || "Agent Bronco replied.";
    try {
      new Notification("Agent Bronco replied", { body: body });
    } catch {
      /* ignore */
    }
  }

  async function primeMicrophoneOnce() {
    if (micPrimed || !navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) return;
    try {
      const tmp = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: false,
          noiseSuppression: false,
          autoGainControl: false,
          channelCount: 1,
          latency: 0,
        },
      });
      tmp.getTracks().forEach(function (t) {
        try {
          t.stop();
        } catch {
          /* ignore */
        }
      });
      micPrimed = true;
    } catch {
      /* ignore */
    }
  }

  /** @param {Record<number, object>} byN */
  function fillAssistantBody(bodyEl, text, sources) {
    bodyEl.textContent = "";
    const byN = {};
    (sources || []).forEach((s) => {
      if (s.n != null) byN[Number(s.n)] = s;
    });
    const parts = String(text).split(/(\[\d+\])/g);
    for (let i = 0; i < parts.length; i++) {
      const part = parts[i];
      const mm = part.match(/^\[(\d+)\]$/);
      if (mm) {
        const n = Number(mm[1]);
        const src = byN[n];
        if (src && src.source_url) {
          const a = document.createElement("a");
          a.href = src.source_url;
          a.target = "_blank";
          a.rel = "noopener noreferrer";
          a.className = "cite-link";
          a.textContent = part;
          a.title = (src.source_path || "") + (src.heading ? " — " + src.heading : "");
          bodyEl.appendChild(a);
        } else {
          bodyEl.appendChild(document.createTextNode(part));
        }
      } else {
        bodyEl.appendChild(document.createTextNode(part));
      }
    }
  }

  function appendBubble(role, text, extras) {
    const ui = chatUiText();
    const wrap = document.createElement("div");
    wrap.className = "bubble " + role;
    const body = document.createElement("div");
    body.className = "bubble-body";
    if (role === "assistant") {
      fillAssistantBody(body, text, extras && extras.sources);
    } else {
      body.textContent = text;
    }
    wrap.appendChild(body);
    if (extras && extras.usage) {
      const meta = document.createElement("div");
      meta.className = "meta";
      meta.textContent =
        ui.tokensLabel + " " +
        extras.usage.prompt_tokens +
        " · " +
        extras.usage.completion_tokens +
        " · " +
        extras.usage.total_tokens;
      wrap.appendChild(meta);
    }
    if (extras && extras.sources && extras.sources.length) {
      const det = document.createElement("details");
      det.className = "sources";
      det.open = false;
      const sum = document.createElement("summary");
      sum.textContent = ui.sourcesPrefix + extras.sources.length + ui.sourcesSuffix;
      det.appendChild(sum);
      extras.sources.forEach((s) => {
        const p = document.createElement("div");
        p.className = "source-item";
        const label = (s.n != null ? "[" + s.n + "] " : "") + (s.source_path || "");
        if (s.source_url) {
          const a = document.createElement("a");
          a.href = s.source_url;
          a.target = "_blank";
          a.rel = "noopener noreferrer";
          a.textContent = label;
          p.appendChild(a);
        } else {
          p.textContent = label;
        }
        if (s.heading) {
          p.appendChild(document.createElement("br"));
          const h = document.createElement("span");
          h.textContent = ui.sectionLabel + " " + s.heading;
          p.appendChild(h);
        }
        det.appendChild(p);
      });
      wrap.appendChild(det);
    }
    if (role === "assistant" && window.speechSynthesis) {
      const bar = document.createElement("div");
      bar.className = "bubble-actions";
      const sp = document.createElement("button");
      sp.type = "button";
      sp.className = "btn mini";
      sp.textContent = ui.speakAction;
      sp.addEventListener("click", () => speakText(text));
      bar.appendChild(sp);
      wrap.appendChild(bar);
    }
    messagesEl.appendChild(wrap);
    messagesEl.scrollTop = messagesEl.scrollHeight;
    return wrap;
  }

  function graphNodeAt(px, py) {
    if (!graphState || !graphState.nodes) return null;
    for (let i = graphState.nodes.length - 1; i >= 0; i--) {
      const n = graphState.nodes[i];
      const r = n.id === graphState.hoveredId ? n.radius + 5 : n.radius + 2;
      const dx = px - n.x;
      const dy = py - n.y;
      if (dx * dx + dy * dy <= r * r) return n;
    }
    return null;
  }

  function renderGraph() {
    if (!graphCanvas || !graphPanel || !graphState) return;
    const ctx = graphCanvas.getContext("2d");
    const w = graphCanvas.width;
    const h = graphCanvas.height;
    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = "#1a1410";
    ctx.fillRect(0, 0, w, h);

    const byId = {};
    graphState.nodes.forEach((n) => {
      byId[n.id] = n;
    });

    ctx.strokeStyle = "#5c4a3a";
    ctx.lineWidth = 1;
    (graphState.edges || []).forEach((e) => {
      const a = byId[e.source];
      const b = byId[e.target];
      if (!a || !b) return;
      ctx.beginPath();
      ctx.moveTo(a.x, a.y);
      ctx.lineTo(b.x, b.y);
      ctx.stroke();
    });

    ctx.font = "11px 'Segoe UI', sans-serif";
    graphState.nodes.forEach((n) => {
      const hovered = n.id === graphState.hoveredId;
      const radius = hovered ? n.radius + 4 : n.radius;
      ctx.beginPath();
      ctx.fillStyle = hovered ? "#d9a441" : "#6b8f5e";
      ctx.arc(n.x, n.y, radius, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = hovered ? "#f8d28c" : "#95b88a";
      ctx.lineWidth = hovered ? 2 : 1;
      ctx.stroke();

      const label = (n.label || "").trim();
      if (!label) return;
      const displayLabel = hovered ? label : label.length > 24 ? label.slice(0, 24) + "…" : label;
      ctx.font = hovered ? "700 12px 'Segoe UI', sans-serif" : "11px 'Segoe UI', sans-serif";
      const tw = ctx.measureText(displayLabel).width;
      const radial = Math.atan2(n.y - h / 2, n.x - w / 2);
      const lx = n.x + Math.cos(radial) * (radius + 10);
      const ly = n.y + Math.sin(radial) * (radius + 10);
      const textX = lx + (Math.cos(radial) >= 0 ? 4 : -(tw + 4));
      const textY = ly + 4;
      ctx.fillStyle = hovered ? "#fff7e8" : "#f5ebe0";
      ctx.fillText(
        displayLabel,
        Math.max(6, Math.min(w - tw - 6, textX)),
        Math.max(12, Math.min(h - 6, textY))
      );
    });
  }

  function drawGraph(data) {
    if (!graphCanvas || !graphPanel) return;
    const nodesRaw = Array.isArray(data.nodes) ? data.nodes : [];
    const edges = Array.isArray(data.edges) ? data.edges : [];
    if (!nodesRaw.length) {
      graphState = null;
      graphPanel.classList.add("hidden");
      return;
    }
    graphPanel.classList.remove("hidden");
    const w = graphCanvas.width;
    const h = graphCanvas.height;
    const cx = w / 2;
    const cy = h / 2;
    const ring = Math.min(w, h) * 0.35;
    const sorted = nodesRaw
      .slice()
      .sort((a, b) => String(a.label || a.id).localeCompare(String(b.label || b.id)));
    const nodes = sorted.map((n, i) => {
      const ang = (2 * Math.PI * i) / Math.max(sorted.length, 1);
      const jitter = (i % 2 === 0 ? -1 : 1) * 10;
      return {
        id: n.id,
        label: String(n.label || n.id || ""),
        source_url: n.source_url || n.url || null,
        x: cx + (ring + jitter) * Math.cos(ang),
        y: cy + (ring + jitter) * Math.sin(ang),
        radius: 10,
      };
    });
    graphState = { nodes, edges, hoveredId: null };
    renderGraph();
  }

  if (graphCanvas) {
    graphCanvas.addEventListener("mousemove", (ev) => {
      if (!graphState) return;
      const rect = graphCanvas.getBoundingClientRect();
      const scaleX = graphCanvas.width / rect.width;
      const scaleY = graphCanvas.height / rect.height;
      const x = (ev.clientX - rect.left) * scaleX;
      const y = (ev.clientY - rect.top) * scaleY;
      const hit = graphNodeAt(x, y);
      const nextId = hit ? hit.id : null;
      if (graphState.hoveredId !== nextId) {
        graphState.hoveredId = nextId;
        renderGraph();
      }
      graphCanvas.style.cursor = hit && hit.source_url ? "pointer" : "default";
    });
    graphCanvas.addEventListener("mouseleave", () => {
      if (!graphState || graphState.hoveredId == null) return;
      graphState.hoveredId = null;
      graphCanvas.style.cursor = "default";
      renderGraph();
    });
    graphCanvas.addEventListener("click", (ev) => {
      if (!graphState) return;
      const rect = graphCanvas.getBoundingClientRect();
      const scaleX = graphCanvas.width / rect.width;
      const scaleY = graphCanvas.height / rect.height;
      const x = (ev.clientX - rect.left) * scaleX;
      const y = (ev.clientY - rect.top) * scaleY;
      const hit = graphNodeAt(x, y);
      if (hit && hit.source_url) {
        window.open(hit.source_url, "_blank", "noopener,noreferrer");
      }
    });
  }

  async function fetchGraph(chunkIds) {
    try {
      const res = await fetch("/api/graph-context", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ chunk_ids: chunkIds }),
      });
      const data = await res.json();
      drawGraph(data);
    } catch {
      graphPanel && graphPanel.classList.add("hidden");
    }
  }

  if (input) {
    input.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        if (!sendBtn || !sendBtn.disabled) form.requestSubmit();
      }
    });
  }

  rehydrateFromStorage();
  if (sessionId) {
    fetch("/api/history?session_id=" + encodeURIComponent(sessionId))
      .then((r) => r.json())
      .then((msgs) => {
        if (!msgs || !msgs.length) return;
        messagesEl.innerHTML = "";
        history = [];
        msgs.forEach((m) => {
          appendBubble(m.role, m.content);
          history.push({ role: m.role, content: m.content });
        });
        try {
          sessionStorage.setItem(STORAGE_KEY, JSON.stringify(history));
        } catch {
          /* ignore */
        }
      })
      .catch(() => {})
      .finally(() => {
        void recoverPendingServerReply();
      });
  } else {
    void recoverPendingServerReply();
  }
  updateSpeechPauseUi();
  ensureSpeechVoicesReady();

  window.addEventListener("cpp-ui-translated", function () {
    updateSpeechPauseUi();
    if (!history.length || !messagesEl) return;
    messagesEl.innerHTML = "";
    history.forEach((item) => {
      if (item.role === "user") appendBubble("user", item.content);
      else appendBubble("assistant", item.content, { sources: item.sources, usage: item.usage });
    });
  });

  function formatBytes(n) {
    if (n < 1024) return n + " B";
    if (n < 1048576) return (n / 1024).toFixed(1) + " KB";
    return (n / 1048576).toFixed(1) + " MB";
  }

  function showBusyOverlay(show, title, sub) {
    if (!chatBusyOverlay) return;
    if (chatBusyText && title) chatBusyText.textContent = title;
    const subEl = chatBusyOverlay.querySelector(".chat-busy-sub");
    if (subEl && sub !== undefined) subEl.textContent = sub || "";
    chatBusyOverlay.classList.toggle("hidden", !show);
    chatBusyOverlay.setAttribute("aria-hidden", show ? "false" : "true");
    if (chatMain) chatMain.classList.toggle("chat-main--busy", !!show);
  }

  function setComposerLocked(locked) {
    if (input) input.disabled = locked;
    if (micBtn) micBtn.disabled = locked;
    if (micConfirm) micConfirm.disabled = locked;
    if (micDiscard) micDiscard.disabled = locked;
    if (form) form.classList.toggle("is-voice-busy", !!locked);
  }

  function setSendVisible(visible) {
    if (!sendBtn) return;
    sendBtn.classList.toggle("hidden", !visible);
    sendBtn.disabled = !visible;
  }

  let pillRaf = 0;
  let pillLevel = 0;
  function stopRecordingPill() {
    if (pillRaf) cancelAnimationFrame(pillRaf);
    pillRaf = 0;
    if (recordingPill) {
      recordingPill.classList.add("hidden");
      recordingPill.style.width = "0px";
    }
  }

  function startRecordingPill() {
    if (!recordingPill || !input) return;
    stopRecordingPill();
    pillLevel = 0;
    recordingPill.classList.remove("hidden");
    recordingPill.style.width = "24px";
    recordingPill.style.setProperty("--pill-level", "0");
    recordingPill.style.setProperty("--pill-height", "12px");
  }

  function setInputVoiceMode(active) {
    if (!input) return;
    input.readOnly = !!active;
    input.placeholder = active ? "" : defaultInputPlaceholder;
  }

  function clearReviewAudio() {
    if (reviewObjectUrl) {
      try {
        URL.revokeObjectURL(reviewObjectUrl);
      } catch {
        /* ignore */
      }
      reviewObjectUrl = null;
    }
    if (micReviewAudio) {
      micReviewAudio.removeAttribute("src");
      try {
        micReviewAudio.load();
      } catch {
        /* ignore */
      }
    }
    if (micReviewAudioRow) micReviewAudioRow.classList.add("hidden");
    if (micReviewMeta) micReviewMeta.textContent = "";
  }

  function attachReviewAudio(blob) {
    clearReviewAudio();
    if (!micReviewAudio || !blob || !blob.size) return;
    reviewObjectUrl = URL.createObjectURL(blob);
    micReviewAudio.src = reviewObjectUrl;
    if (micReviewMeta) {
      micReviewMeta.textContent =
        formatBytes(blob.size) + (blob.type ? " · " + blob.type : "");
    }
    if (micReviewAudioRow) micReviewAudioRow.classList.remove("hidden");
  }

  /**
   * @param {string} text
   * @param {{ keepSendDisabled?: boolean }} [opts]
   */
  async function submitChatMessage(text, opts) {
    let messageForApi = text;
    const perf = { user_translate_ms: 0, chat_ms: 0, reply_translate_ms: 0, total_ms: 0 };
    const submitT0 = performance.now();
    if (getUiApiTarget() !== "en") {
      const tUser = performance.now();
      messageForApi = await translateLine(text, "en");
      perf.user_translate_ms = Math.round(performance.now() - tUser);
    }
    appendBubble("user", text);
    history.push({ role: "user", content: text, content_en: messageForApi });
    persistHistory();
    sendBtn.disabled = true;
    setThinking(true);
    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: messageForApi,
          history: history.slice(0, -1).map((h) => ({
            role: h.role,
            content: h.content_en != null && h.content_en !== "" ? h.content_en : h.content,
          })),
          session_id: getChatApiSessionId() || undefined,
        }),
      });
      const raw = await res.text();
      let data;
      try {
        data = raw ? JSON.parse(raw) : {};
      } catch {
        const snippet = (raw || "").replace(/\s+/g, " ").trim().slice(0, 400);
        appendBubble(
          "assistant",
          "The server returned a non-JSON response (" +
            res.status +
            "). " +
            (snippet ? "Body: " + snippet : "")
        );
        history.push({ role: "assistant", content: "bad json" });
        persistHistory();
        return;
      }
      if (data && data.session_id) setChatApiSessionId(data.session_id);
      let rawReply = (data && data.content) || "";
      let reply = rawReply;
      perf.chat_ms =
        (data && data.metrics && Number(data.metrics.chat_ms)) ||
        Number((res.headers.get("Server-Timing") || "").match(/dur=([0-9.]+)/)?.[1]) ||
        0;
      if (!res.ok) {
        if (!reply && data && data.detail) reply = String(data.detail);
        if (!reply) reply = "Request failed (HTTP " + res.status + ").";
        if (data && data.error) reply += " [" + data.error + "]";
        if (
          data &&
          data.detail &&
          (data.error === "llm_error" ||
            data.error === "ollama_oom" ||
            reply.indexOf(String(data.detail)) < 0)
        ) {
          reply += "\n\nDetails: " + String(data.detail);
        }
        if (getUiApiTarget() !== "en" && reply) {
          const tReplyErr = performance.now();
          reply = await translateLine(reply, getUiApiTarget());
          perf.reply_translate_ms = Math.round(performance.now() - tReplyErr);
        }
        appendBubble("assistant", reply, { sources: data.sources, usage: data.usage });
        triggerMascotCelebrate();
        maybeNotifyReply(reply);
        history.push({
          role: "assistant",
          content: reply,
          content_en: rawReply || reply,
          sources: data.sources,
          usage: data.usage,
        });
        persistHistory();
        const ids = (data.sources || []).map((s) => s.chunk_id).filter(Boolean);
        fetchGraph(ids);
        return;
      }
      rawReply = rawReply || "(no response)";
      reply = rawReply;
      if (getUiApiTarget() !== "en") {
        const tReply = performance.now();
        reply = await translateLine(rawReply, getUiApiTarget());
        perf.reply_translate_ms = Math.round(performance.now() - tReply);
      }
      appendBubble("assistant", reply, { sources: data.sources, usage: data.usage });
      triggerMascotCelebrate();
      maybeNotifyReply(reply);
      if (speakToggle && speakToggle.checked) speakText(reply);
      history.push({
        role: "assistant",
        content: reply,
        content_en: rawReply,
        sources: data.sources,
        usage: data.usage,
      });
      persistHistory();
      const ids = (data.sources || []).map((s) => s.chunk_id).filter(Boolean);
      fetchGraph(ids);
      perf.total_ms = Math.round(performance.now() - submitT0);
      if (chatPerfNote) {
        chatPerfNote.textContent =
          "Latency — chat: " +
          perf.chat_ms +
          " ms · user translate: " +
          perf.user_translate_ms +
          " ms · reply translate: " +
          perf.reply_translate_ms +
          " ms · total: " +
          perf.total_ms +
          " ms";
      }
    } catch (err) {
      appendBubble("assistant", "Network error: " + err);
      triggerMascotCelebrate();
      history.push({ role: "assistant", content: "Network error" });
      persistHistory();
    } finally {
      setThinking(false);
      if (!opts || !opts.keepSendDisabled) sendBtn.disabled = false;
    }
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;
    input.value = "";
    await submitChatMessage(text);
  });

  document.querySelectorAll(".starter-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const q = (btn.textContent || "").trim() || btn.getAttribute("data-q");
      if (q) {
        input.value = q;
        input.focus();
        form.requestSubmit();
      }
    });
  });

  if (replyNotifyToggle) {
    replyNotifyToggle.addEventListener("change", async function () {
      if (replyNotifyToggle.checked && "Notification" in window && Notification.permission === "default") {
        try {
          await Notification.requestPermission();
        } catch {
          /* ignore */
        }
      }
    });
  }

  if (speechPauseBtn) {
    speechPauseBtn.addEventListener("click", function () {
      if (!window.speechSynthesis || !currentUtterance) return;
      if (speechPaused) {
        try {
          window.speechSynthesis.resume();
          speechPaused = false;
        } catch {
          /* ignore */
        }
      } else {
        try {
          window.speechSynthesis.pause();
          const started = Date.now();
          const nudgePause = function () {
            if (!window.speechSynthesis || window.speechSynthesis.paused) return;
            if (Date.now() - started > 450) return;
            try {
              window.speechSynthesis.pause();
            } catch {
              /* ignore */
            }
            window.setTimeout(nudgePause, 24);
          };
          window.setTimeout(nudgePause, 20);
          speechPaused = true;
        } catch {
          /* ignore */
        }
      }
      updateSpeechPauseUi();
    });
  }

  if (speechStopBtn) {
    speechStopBtn.addEventListener("click", function () {
      stopSpeaking(true);
    });
  }

  var TRANSCRIBE_FETCH_MS = 180000;

  /** Prefer a concrete codec; empty string = let the browser choose (still valid). */
  function pickMimeType() {
    const types = [
      "audio/webm;codecs=opus",
      "audio/webm",
      "audio/mp4",
      "audio/ogg;codecs=opus",
      "audio/ogg",
    ];
    for (let i = 0; i < types.length; i++) {
      if (window.MediaRecorder && MediaRecorder.isTypeSupported(types[i])) return types[i];
    }
    return "";
  }

  function blobAudioFilename(blob) {
    const t = (blob.type || "").toLowerCase();
    if (t.indexOf("mp4") >= 0 || t.indexOf("m4a") >= 0 || t.indexOf("mp3") >= 0) return "recording.m4a";
    if (t.indexOf("ogg") >= 0) return "recording.ogg";
    return "recording.webm";
  }

  let mediaRecorder = null;
  let mediaStream = null;
  let audioChunks = [];
  let recordMime = "";
  let isRecording = false;
  let isTranscribing = false;
  let reviewBlob = null;
  let waveRaf = 0;
  let waveAudioCtx = null;
  let transcribingTicker = 0;
  let transcribingStartedAt = 0;

  function stopTranscribingTicker() {
    if (transcribingTicker) clearInterval(transcribingTicker);
    transcribingTicker = 0;
    transcribingStartedAt = 0;
  }

  function startTranscribingTicker() {
    stopTranscribingTicker();
    transcribingStartedAt = Date.now();
    const update = function () {
      if (!voiceInlineStatus) return;
      const sec = Math.max(0, Math.floor((Date.now() - transcribingStartedAt) / 1000));
      const mm = String(Math.floor(sec / 60)).padStart(2, "0");
      const ss = String(sec % 60).padStart(2, "0");
      voiceInlineStatus.textContent =
        "Transcribing… First run can take several minutes while the Whisper model loads. (" +
        mm +
        ":" +
        ss +
        ")";
    };
    update();
    transcribingTicker = window.setInterval(update, 1000);
  }

  function showVoiceInline(show) {
    if (!voiceInline) return;
    voiceInline.classList.toggle("hidden", !show);
    if (composerInputRow) composerInputRow.classList.toggle("voice-inline-active", !!show);
  }

  function stopWaveform() {
    if (waveRaf) cancelAnimationFrame(waveRaf);
    waveRaf = 0;
    if (waveAudioCtx) {
      try {
        waveAudioCtx.close();
      } catch {
        /* ignore */
      }
      waveAudioCtx = null;
    }
    if (waveCanvas) {
      const ctx = waveCanvas.getContext("2d");
      if (ctx) {
        ctx.fillStyle = "#121a15";
        ctx.fillRect(0, 0, waveCanvas.width, waveCanvas.height);
      }
    }
  }

  async function startWaveform(stream) {
    if (!waveCanvas || !window.AudioContext) return;
    stopWaveform();
    const ac = new AudioContext();
    waveAudioCtx = ac;
    try {
      if (ac.state === "suspended") await ac.resume();
    } catch {
      /* ignore */
    }
    const srcNode = ac.createMediaStreamSource(stream);
    const analyser = ac.createAnalyser();
    analyser.fftSize = 128;
    srcNode.connect(analyser);
    const buf = new Uint8Array(analyser.frequencyBinCount);
    const ctx = waveCanvas.getContext("2d");
    const w = waveCanvas.width;
    const h = waveCanvas.height;
    function tick() {
      if (!isRecording) return;
      analyser.getByteFrequencyData(buf);
      ctx.fillStyle = "#121a15";
      ctx.fillRect(0, 0, w, h);
      const n = buf.length;
      const barW = w / n;
      for (let i = 0; i < n; i++) {
        const bh = (buf[i] / 255) * (h - 4);
        ctx.fillStyle = "#6b8f5e";
        ctx.fillRect(i * barW, h - bh, Math.max(1, barW - 1), bh);
      }
      if (recordingPill && input) {
        let sum = 0;
        for (let i = 0; i < n; i++) sum += buf[i];
        const avg = sum / n / 255; // 0..1
        pillLevel = pillLevel * 0.45 + avg * 0.55; // more dramatic response

        // Peak-to-peak growth around origin (center line):
        // - horizontal width grows/shrinks with amplitude
        // - vertical thickness grows/shrinks with amplitude
        const maxW = Math.max(80, input.getBoundingClientRect().width - 24);
        const minW = 18;
        const ampCurve = Math.pow(pillLevel, 0.68);
        const widthByAmp = minW + ampCurve * (maxW - minW);
        recordingPill.style.width = Math.round(Math.max(minW, Math.min(maxW, widthByAmp))) + "px";
        const maxH = Math.max(18, input.getBoundingClientRect().height - 8);
        const minH = 6;
        const heightByAmp = minH + ampCurve * (maxH - minH);
        recordingPill.style.setProperty("--pill-height", Math.round(heightByAmp) + "px");

        // Vertical "intensity" tracks live amplitude.
        recordingPill.style.setProperty("--pill-level", pillLevel.toFixed(3));
        const hueA = Math.round(35 + pillLevel * 230);
        const hueB = Math.round((hueA + 120) % 360);
        const alpha = (0.55 + pillLevel * 0.4).toFixed(3);
        const bright = (0.92 + pillLevel * 0.5).toFixed(3);
        const sat = (0.95 + pillLevel * 0.55).toFixed(3);
        const glow = (0.18 + pillLevel * 0.34).toFixed(3);
        recordingPill.style.setProperty("--pill-h1", String(hueA));
        recordingPill.style.setProperty("--pill-h2", String(hueB));
        recordingPill.style.setProperty("--pill-a", alpha);
        recordingPill.style.setProperty("--pill-bright", bright);
        recordingPill.style.setProperty("--pill-sat", sat);
        recordingPill.style.setProperty("--pill-glow", glow);
      }
      waveRaf = requestAnimationFrame(tick);
    }
    waveRaf = requestAnimationFrame(tick);
  }

  function setMicUi(mode) {
    if (!micBtn) return;
    const on = mode === "recording";
    micBtn.classList.toggle("mic-on", on);
    micBtn.classList.toggle("mic-busy", mode === "transcribing" || mode === "review");
    micBtn.setAttribute("aria-pressed", on ? "true" : "false");
    if (micSpinner) micSpinner.classList.toggle("hidden", mode !== "transcribing");
    if (micDecision) micDecision.classList.toggle("hidden", mode !== "review");
    micBtn.classList.toggle("hidden", mode === "review" || mode === "transcribing");
    setSendVisible(mode === "idle");
    setInputVoiceMode(mode !== "idle");
    showVoiceInline(mode === "review" || mode === "transcribing");
    if (voiceInlineStatus) {
      if (mode === "transcribing") {
        startTranscribingTicker();
      } else if (mode === "review") {
        stopTranscribingTicker();
        voiceInlineStatus.textContent = "Review your recording, then press ✓ to transcribe and send.";
      } else {
        stopTranscribingTicker();
        voiceInlineStatus.textContent = "";
      }
    }
    if (mode === "idle") stopRecordingPill();
    if (mode === "recording") startRecordingPill();
    if (micHint) {
      micHint.hidden = mode === "idle" || mode === "transcribing";
      if (mode === "idle" && !isTranscribing) micHint.textContent = "";
      else if (mode === "recording")
        micHint.textContent =
          "Recording… click mic again to stop, then use \u2713 transcribe or \u2715 discard below.";
      else if (mode === "review") {
        micHint.textContent =
          "Preview your recording below. \u2713 transcribes and sends to chat; \u2715 discards.";
      }
    }
  }

  function stopStreamTracks() {
    if (mediaStream) {
      mediaStream.getTracks().forEach((t) => t.stop());
      mediaStream = null;
    }
  }

  async function transcribeBlob(blob) {
    const ac = new AbortController();
    const timer = setTimeout(function () {
      ac.abort();
    }, TRANSCRIBE_FETCH_MS);
    try {
      const fd = new FormData();
      fd.append("audio", blob, blobAudioFilename(blob));
      const res = await fetch("/api/transcribe", { method: "POST", body: fd, signal: ac.signal });
      let data = {};
      try {
        data = await res.json();
      } catch {
        throw new Error("bad json");
      }
      if (!res.ok) {
        throw new Error((data && (data.detail || data.error)) || "HTTP " + res.status);
      }
      return ((data && data.text) || "").trim();
    } catch (err) {
      if (err && err.name === "AbortError") {
        throw new Error(
          "Transcribe timed out after " +
            Math.round(TRANSCRIBE_FETCH_MS / 1000) +
            "s (first run downloads Whisper weights; try CPP_WHISPER_MODEL_SIZE=tiny or warmup on server)."
        );
      }
      throw err;
    } finally {
      clearTimeout(timer);
    }
  }

  function resetReview() {
    reviewBlob = null;
    clearReviewAudio();
    showVoiceInline(false);
    setMicUi("idle");
  }

  if (micConfirm) {
    micConfirm.addEventListener("click", async () => {
      if (!reviewBlob || isTranscribing) return;
      const blob = reviewBlob;
      if (!blob.size) return;
      isTranscribing = true;
      reviewBlob = null;
      setComposerLocked(true);
      setMicUi("transcribing");
      clearReviewAudio();
      try {
        const text = await transcribeBlob(blob);
        if (text) {
          // Release voice lock immediately; assistant loading indicator is the dots.
          isTranscribing = false;
          setComposerLocked(false);
          setMicUi("idle");
          void submitChatMessage(text);
          return;
        } else if (micHint) {
          micHint.hidden = false;
          micHint.textContent = "No speech detected; try again.";
        }
      } catch (err) {
        if (micHint) {
          micHint.hidden = false;
          const msg = String(err && err.message ? err.message : err || "");
          micHint.textContent =
            msg.indexOf("Server STT unavailable") >= 0
              ? "Voice transcription is temporarily unavailable. Please type your message."
              : "Transcribe failed: " + msg;
        }
      } finally {
        isTranscribing = false;
        setComposerLocked(false);
        setMicUi("idle");
      }
    });
  }

  if (micDiscard) {
    micDiscard.addEventListener("click", () => {
      resetReview();
      setComposerLocked(false);
    });
  }

  if (micBtn) {
    if (!window.MediaRecorder) {
      micBtn.disabled = true;
      micBtn.title = "MediaRecorder not supported in this browser";
      if (micHint) {
        micHint.hidden = false;
        micHint.textContent = "Update your browser or type your message.";
      }
    } else if (!window.isSecureContext) {
      micBtn.disabled = true;
      micBtn.title = "HTTPS or localhost required for microphone";
      if (micHint) {
        micHint.hidden = false;
        micHint.textContent = "Open the site over HTTPS (or localhost) to use the microphone.";
      }
    } else {
      micBtn.addEventListener("click", async () => {
        if (isTranscribing) return;

        if (isRecording && mediaRecorder && mediaRecorder.state === "recording") {
          isRecording = false;
          stopWaveform();
          stopRecordingPill();
          micBtn.disabled = true;
          setMicUi("review");

          const mr = mediaRecorder;
          const chunks = audioChunks;
          const mime = recordMime;

          await new Promise((resolve) => {
            mr.onstop = resolve;
            try {
              if (typeof mr.requestData === "function") mr.requestData();
            } catch {
              /* ignore */
            }
            try {
              mr.stop();
            } catch {
              resolve();
            }
          });
          stopStreamTracks();
          mediaRecorder = null;

          reviewBlob = new Blob(chunks, { type: mime || "audio/webm" });
          audioChunks = [];
          micBtn.disabled = false;
          if (!reviewBlob.size) {
            if (micHint) {
              micHint.hidden = false;
              micHint.textContent =
                "No audio captured (clip may be too short). Hold the mic a bit longer, then stop.";
            }
            resetReview();
            return;
          }
          if (reviewBlob.size < 256) {
            if (micHint) {
              micHint.hidden = false;
              micHint.textContent =
                "Recording looks very small — speak longer or check your microphone level.";
            }
          }
          attachReviewAudio(reviewBlob);
          showVoiceInline(true);
          return;
        }

        try {
          await primeMicrophoneOnce();
          recordMime = pickMimeType();
          mediaStream = await navigator.mediaDevices.getUserMedia({
            audio: {
              echoCancellation: false,
              noiseSuppression: false,
              autoGainControl: false,
              channelCount: 1,
              latency: 0,
            },
          });
          audioChunks = [];
          try {
            mediaRecorder = recordMime
              ? new MediaRecorder(mediaStream, { mimeType: recordMime })
              : new MediaRecorder(mediaStream);
          } catch {
            mediaRecorder = new MediaRecorder(mediaStream);
          }
          if (mediaRecorder.mimeType) recordMime = mediaRecorder.mimeType;
          mediaRecorder.ondataavailable = (ev) => {
            if (ev.data && ev.data.size > 0) audioChunks.push(ev.data);
          };
          /* No timeslice: one blob on stop — avoids empty chunks when user stops within 250ms. */
          mediaRecorder.start();
          isRecording = true;
          await startWaveform(mediaStream);
          setMicUi("recording");
        } catch (err) {
          stopStreamTracks();
          stopWaveform();
          stopRecordingPill();
          mediaRecorder = null;
          isRecording = false;
          setMicUi("idle");
          setComposerLocked(false);
          if (micHint) {
            micHint.hidden = false;
            micHint.textContent =
              "Microphone blocked or unavailable. Allow mic in the browser bar, then try again.";
          }
        }
      });
    }
  }
})();
