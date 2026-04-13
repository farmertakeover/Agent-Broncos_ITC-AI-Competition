(function () {
  const messagesEl = document.getElementById("messages");
  const form = document.getElementById("chatForm");
  const input = document.getElementById("msg");
  const sendBtn = document.getElementById("sendBtn");
  const micBtn = document.getElementById("micBtn");
  const micHint = document.getElementById("micHint");
  const speakToggle = document.getElementById("speakToggle");
  const graphPanel = document.getElementById("graphPanel");
  const graphCanvas = document.getElementById("graphCanvas");

  /** @type {{role: string, content: string}[]} */
  let history = [];

  function speakText(text) {
    if (!window.speechSynthesis || !text) return;
    try {
      window.speechSynthesis.cancel();
      const u = new SpeechSynthesisUtterance(text);
      u.lang = "en-US";
      window.speechSynthesis.speak(u);
    } catch {
      /* ignore */
    }
  }

  function appendBubble(role, text, extras) {
    const wrap = document.createElement("div");
    wrap.className = "bubble " + role;
    const body = document.createElement("div");
    body.className = "bubble-body";
    body.textContent = text;
    wrap.appendChild(body);
    if (extras && extras.usage) {
      const meta = document.createElement("div");
      meta.className = "meta";
      meta.textContent =
        "tokens in·out·total: " +
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
      const sum = document.createElement("summary");
      sum.textContent = "Sources (" + extras.sources.length + ")";
      det.appendChild(sum);
      extras.sources.forEach((s) => {
        const p = document.createElement("div");
        p.className = "source-item";
        const label = (s.n != null ? "[" + s.n + "] " : "") + (s.source_path || "");
        if (s.source_url) {
          const a = document.createElement("a");
          a.href = s.source_url;
          a.target = "_blank";
          a.rel = "noopener";
          a.textContent = label;
          p.appendChild(a);
        } else {
          p.textContent = label;
        }
        if (s.heading) {
          p.appendChild(document.createElement("br"));
          const h = document.createElement("span");
          h.textContent = "Section: " + s.heading;
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
      sp.textContent = "Speak";
      sp.addEventListener("click", () => speakText(text));
      bar.appendChild(sp);
      wrap.appendChild(bar);
    }
    messagesEl.appendChild(wrap);
    messagesEl.scrollTop = messagesEl.scrollHeight;
    return wrap;
  }

  function drawGraph(data) {
    if (!graphCanvas || !graphPanel) return;
    const nodes = data.nodes || [];
    const edges = data.edges || [];
    if (!nodes.length) {
      graphPanel.classList.add("hidden");
      return;
    }
    graphPanel.classList.remove("hidden");
    const ctx = graphCanvas.getContext("2d");
    const w = graphCanvas.width;
    const h = graphCanvas.height;
    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = "#1a1410";
    ctx.fillRect(0, 0, w, h);
    const cx = w / 2;
    const cy = h / 2;
    const r = Math.min(w, h) * 0.32;
    const positions = {};
    nodes.forEach((n, i) => {
      const ang = (2 * Math.PI * i) / Math.max(nodes.length, 1);
      positions[n.id] = { x: cx + r * Math.cos(ang), y: cy + r * Math.sin(ang) };
    });
    ctx.strokeStyle = "#5c4a3a";
    ctx.lineWidth = 1;
    edges.forEach((e) => {
      const a = positions[e.source];
      const b = positions[e.target];
      if (a && b) {
        ctx.beginPath();
        ctx.moveTo(a.x, a.y);
        ctx.lineTo(b.x, b.y);
        ctx.stroke();
      }
    });
    nodes.forEach((n) => {
      const p = positions[n.id];
      if (!p) return;
      ctx.beginPath();
      ctx.fillStyle = "#6b8f5e";
      ctx.arc(p.x, p.y, 10, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = "#f5ebe0";
      ctx.font = "10px sans-serif";
      const lbl = (n.label || "").slice(0, 18);
      ctx.fillText(lbl, p.x - 24, p.y + 22);
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

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;
    input.value = "";
    appendBubble("user", text);
    history.push({ role: "user", content: text });
    sendBtn.disabled = true;
    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text, history: history.slice(0, -1) }),
      });
      let data;
      try {
        data = await res.json();
      } catch {
        appendBubble("assistant", "The server returned a non-JSON response (" + res.status + ").");
        history.push({ role: "assistant", content: "bad json" });
        return;
      }
      let reply = (data && data.content) || "";
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
        appendBubble("assistant", reply, { sources: data.sources, usage: data.usage });
        history.push({ role: "assistant", content: reply });
        const ids = (data.sources || []).map((s) => s.chunk_id).filter(Boolean);
        fetchGraph(ids);
        return;
      }
      reply = reply || "(no response)";
      appendBubble("assistant", reply, { sources: data.sources, usage: data.usage });
      if (speakToggle && speakToggle.checked) speakText(reply);
      history.push({ role: "assistant", content: reply });
      const ids = (data.sources || []).map((s) => s.chunk_id).filter(Boolean);
      fetchGraph(ids);
    } catch (err) {
      appendBubble("assistant", "Network error: " + err);
      history.push({ role: "assistant", content: "Network error" });
    } finally {
      sendBtn.disabled = false;
    }
  });

  document.querySelectorAll(".starter-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const q = btn.getAttribute("data-q");
      if (q) {
        input.value = q;
        input.focus();
      }
    });
  });

  /* Record → upload → /api/transcribe → paste (faster-whisper on server) */
  var TRANSCRIBE_FETCH_MS = 180000;

  function pickMimeType() {
    const types = ["audio/webm;codecs=opus", "audio/webm", "audio/mp4"];
    for (let i = 0; i < types.length; i++) {
      if (window.MediaRecorder && MediaRecorder.isTypeSupported(types[i])) return types[i];
    }
    return "";
  }

  let mediaRecorder = null;
  let mediaStream = null;
  let audioChunks = [];
  let recordMime = "";
  let isRecording = false;
  let isTranscribing = false;

  function setMicUi(mode) {
    if (!micBtn) return;
    const on = mode === "recording";
    micBtn.classList.toggle("mic-on", on);
    micBtn.classList.toggle("mic-busy", mode === "transcribing");
    micBtn.setAttribute("aria-pressed", on ? "true" : "false");
    if (micHint) {
      micHint.hidden = mode === "idle";
      if (mode === "idle") micHint.textContent = "";
      else if (mode === "recording") micHint.textContent = "Recording… click again to stop and transcribe.";
      else if (mode === "transcribing") {
        micHint.textContent =
          "Transcribing… First run can take several minutes while the Whisper model loads. ";
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
      const name = blob.type && blob.type.indexOf("mp4") >= 0 ? "recording.m4a" : "recording.webm";
      fd.append("audio", blob, name);
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
          isTranscribing = true;
          setMicUi("transcribing");
          micBtn.disabled = true;

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

          const blob = new Blob(chunks, { type: mime || "audio/webm" });
          audioChunks = [];

          try {
            const text = await transcribeBlob(blob);
            if (text) {
              const cur = input.value.trim();
              input.value = cur ? cur + " " + text : text;
              input.focus();
            } else if (micHint) {
              micHint.hidden = false;
              micHint.textContent = "No speech detected; try again.";
            }
          } catch (err) {
            if (micHint) {
              micHint.hidden = false;
              micHint.textContent = "Transcribe failed: " + (err && err.message ? err.message : err);
            }
          } finally {
            isTranscribing = false;
            micBtn.disabled = false;
            setMicUi("idle");
          }
          return;
        }

        try {
          recordMime = pickMimeType();
          if (!recordMime && micHint) {
            micHint.hidden = false;
            micHint.textContent = "No supported audio codec; try Chrome or Edge.";
            return;
          }
          mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
          audioChunks = [];
          mediaRecorder = new MediaRecorder(mediaStream, recordMime ? { mimeType: recordMime } : undefined);
          if (mediaRecorder.mimeType) recordMime = mediaRecorder.mimeType;
          mediaRecorder.ondataavailable = (ev) => {
            if (ev.data && ev.data.size > 0) audioChunks.push(ev.data);
          };
          mediaRecorder.start(250);
          isRecording = true;
          setMicUi("recording");
        } catch (err) {
          stopStreamTracks();
          mediaRecorder = null;
          isRecording = false;
          setMicUi("idle");
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
