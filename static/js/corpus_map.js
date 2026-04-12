(function () {
  const canvas = document.getElementById("corpusCanvas");
  const noteEl = document.getElementById("ragNote");
  if (!canvas) return;

  function draw(data) {
    const ctx = canvas.getContext("2d");
    const w = canvas.width;
    const h = canvas.height;
    ctx.fillStyle = "#0f1410";
    ctx.fillRect(0, 0, w, h);

    const nodes = (data.nodes || []).filter((n) => n.type !== "center");
    const center = (data.nodes || []).find((n) => n.type === "center");
    const total = center ? center.count : 0;
    if (noteEl) {
      noteEl.textContent =
        (data.note || "") +
        (total ? " · " + total.toLocaleString() + " markdown files indexed in buckets below." : "");
    }
    if (!nodes.length) {
      ctx.fillStyle = "#9aaa9a";
      ctx.font = "16px system-ui";
      ctx.fillText("No corpus files found at configured path.", 24, h / 2);
      return;
    }

    const cx = w * 0.42;
    const cy = h * 0.5;
    const maxC = Math.max(...nodes.map((n) => n.count), 1);
    const rOrbit = Math.min(w, h) * 0.38;

    /* Center */
    ctx.strokeStyle = "#c99700";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(cx, cy, 28, 0, Math.PI * 2);
    ctx.fillStyle = "#1e4d2b";
    ctx.fill();
    ctx.stroke();
    ctx.fillStyle = "#e8f0e8";
    ctx.font = "11px system-ui";
    ctx.textAlign = "center";
    ctx.fillText("CPP", cx, cy - 4);
    ctx.fillText("crawl", cx, cy + 8);

    nodes.forEach((n, i) => {
      const ang = (2 * Math.PI * i) / nodes.length - Math.PI / 2;
      const px = cx + rOrbit * Math.cos(ang);
      const py = cy + rOrbit * Math.sin(ang);
      const br = 8 + 22 * Math.sqrt(n.count / maxC);

      ctx.strokeStyle = "#355045";
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.lineTo(px, py);
      ctx.stroke();

      ctx.beginPath();
      ctx.arc(px, py, br, 0, Math.PI * 2);
      ctx.fillStyle = "rgba(42, 106, 61, 0.85)";
      ctx.fill();
      ctx.strokeStyle = "#3cb878";
      ctx.stroke();

      ctx.fillStyle = "#cfe8d4";
      ctx.font = Math.max(9, Math.min(11, br * 0.45)) + "px system-ui";
      ctx.textAlign = "center";
      const label = (n.label || n.id || "").slice(0, 14);
      ctx.fillText(label, px, py + 3);
      ctx.font = "8px system-ui";
      ctx.fillStyle = "#9aaa9a";
      ctx.fillText(String(n.count), px, py + br + 12);
    });
  }

  fetch("/api/corpus-overview")
    .then((r) => r.json())
    .then(draw)
    .catch(() => {
      if (noteEl) noteEl.textContent = "Could not load corpus overview.";
    });
})();
