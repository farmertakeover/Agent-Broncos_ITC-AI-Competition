(function () {
  const canvas = document.getElementById("corpusCanvas");
  const noteEl = document.getElementById("ragNote");
  const countEl = document.getElementById("ragNoteCount");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  let graph = null;
  let view = { x: 0, y: 0, scale: 1 };
  let dragNode = null;
  let dragCanvas = false;
  let hoverNode = null;
  let startMouse = null;
  let startView = null;

  function getPos(ev) {
    const rect = canvas.getBoundingClientRect();
    const sx = canvas.width / rect.width;
    const sy = canvas.height / rect.height;
    return { x: (ev.clientX - rect.left) * sx, y: (ev.clientY - rect.top) * sy };
  }

  function toWorld(p) {
    return {
      x: (p.x - view.x) / view.scale,
      y: (p.y - view.y) / view.scale,
    };
  }

  function nodeAt(worldPoint) {
    if (!graph || !graph.nodes) return null;
    for (let i = graph.nodes.length - 1; i >= 0; i--) {
      const n = graph.nodes[i];
      const r = (n.radius || 10) + 3;
      const dx = worldPoint.x - n.x;
      const dy = worldPoint.y - n.y;
      if (dx * dx + dy * dy <= r * r) return n;
    }
    return null;
  }

  function physicsTick() {
    if (!graph || !graph.nodes) return;
    const nodes = graph.nodes;
    const center = nodes.find((n) => n.type === "center");
    if (!center) return;
    for (let i = 0; i < nodes.length; i++) {
      const a = nodes[i];
      if (a === center || a === dragNode) continue;
      for (let j = i + 1; j < nodes.length; j++) {
        const b = nodes[j];
        if (b === center) continue;
        const dx = b.x - a.x;
        const dy = b.y - a.y;
        const d2 = Math.max(1, dx * dx + dy * dy);
        const force = 4200 / d2;
        const fx = (dx / Math.sqrt(d2)) * force;
        const fy = (dy / Math.sqrt(d2)) * force;
        if (a !== dragNode) {
          a.vx -= fx;
          a.vy -= fy;
        }
        if (b !== dragNode) {
          b.vx += fx;
          b.vy += fy;
        }
      }
      if (a !== dragNode) {
        const cx = center.x - a.x;
        const cy = center.y - a.y;
        a.vx += cx * 0.0009;
        a.vy += cy * 0.0009;
      }
    }
    nodes.forEach((n) => {
      if (n === dragNode || n.type === "center") return;
      n.vx *= 0.9;
      n.vy *= 0.9;
      n.x += n.vx;
      n.y += n.vy;
    });
  }

  function draw() {
    const w = canvas.width;
    const h = canvas.height;
    ctx.fillStyle = "#0f1410";
    ctx.fillRect(0, 0, w, h);
    if (!graph || !graph.nodes || !graph.nodes.length) {
      ctx.fillStyle = "#9aaa9a";
      ctx.font = "16px system-ui";
      ctx.fillText("No corpus files found at configured path.", 24, h / 2);
      return;
    }

    ctx.save();
    ctx.translate(view.x, view.y);
    ctx.scale(view.scale, view.scale);

    const center = graph.nodes.find((n) => n.type === "center");
    graph.nodes.forEach((n) => {
      if (!center || n.type === "center") return;
      ctx.strokeStyle = "#355045";
      ctx.lineWidth = 1 / view.scale;
      ctx.beginPath();
      ctx.moveTo(center.x, center.y);
      ctx.lineTo(n.x, n.y);
      ctx.stroke();
    });

    graph.nodes.forEach((n) => {
      const hovered = hoverNode && hoverNode.id === n.id;
      const r = hovered ? n.radius + 3 : n.radius;
      ctx.beginPath();
      ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
      if (n.type === "center") {
        ctx.fillStyle = "#1e4d2b";
        ctx.strokeStyle = "#c99700";
      } else {
        ctx.fillStyle = hovered ? "#3cb878" : "rgba(42, 106, 61, 0.85)";
        ctx.strokeStyle = "#3cb878";
      }
      ctx.lineWidth = hovered ? 2 / view.scale : 1 / view.scale;
      ctx.fill();
      ctx.stroke();

      const label = n.type === "center" ? "CPP crawl" : (n.label || n.id || "").slice(0, 18);
      ctx.fillStyle = "#e8f0e8";
      ctx.font = `${Math.max(9, Math.min(12, r * 0.48))}px system-ui`;
      ctx.textAlign = "center";
      ctx.fillText(label, n.x, n.y + 3);
      if (n.type !== "center") {
        ctx.font = "8px system-ui";
        ctx.fillStyle = "#9aaa9a";
        ctx.fillText(String(n.count || ""), n.x, n.y + r + 11);
      }
    });
    ctx.restore();
  }

  function animate() {
    physicsTick();
    draw();
    window.requestAnimationFrame(animate);
  }

  function buildGraph(data) {
    const nodes = (data.nodes || []).slice();
    const centerRaw = nodes.find((n) => n.type === "center");
    const leaves = nodes.filter((n) => n.type !== "center");
    const center = {
      id: (centerRaw && centerRaw.id) || "center",
      label: "CPP crawl",
      type: "center",
      count: centerRaw ? centerRaw.count : 0,
      x: canvas.width * 0.44,
      y: canvas.height * 0.52,
      radius: 30,
      vx: 0,
      vy: 0,
    };
    const maxCount = Math.max(1, ...leaves.map((n) => Number(n.count) || 0));
    const ring = Math.min(canvas.width, canvas.height) * 0.34;
    const leafNodes = leaves.map((n, i) => {
      const ang = (2 * Math.PI * i) / Math.max(1, leaves.length) - Math.PI / 2;
      return {
        id: n.id,
        label: n.label || n.id,
        type: "leaf",
        count: Number(n.count) || 0,
        x: center.x + ring * Math.cos(ang),
        y: center.y + ring * Math.sin(ang),
        radius: 8 + 22 * Math.sqrt((Number(n.count) || 0) / maxCount),
        vx: 0,
        vy: 0,
      };
    });
    graph = { nodes: [center].concat(leafNodes), note: data.note || "" };
    if (noteEl) noteEl.textContent = data.note || "";
    if (countEl) {
      countEl.textContent = center.count
        ? " · " + Number(center.count).toLocaleString() + " markdown files indexed in buckets below."
        : "";
    }
    view = { x: 0, y: 0, scale: 1 };
    draw();
  }

  canvas.addEventListener("mousedown", (ev) => {
    const p = getPos(ev);
    const world = toWorld(p);
    const hit = nodeAt(world);
    hoverNode = hit;
    if (hit && hit.type !== "center") {
      dragNode = hit;
      canvas.style.cursor = "grabbing";
    } else {
      dragCanvas = true;
      startMouse = p;
      startView = { x: view.x, y: view.y };
      canvas.style.cursor = "grabbing";
    }
  });
  canvas.addEventListener("mousemove", (ev) => {
    const p = getPos(ev);
    const world = toWorld(p);
    if (dragNode) {
      dragNode.x = world.x;
      dragNode.y = world.y;
      dragNode.vx = 0;
      dragNode.vy = 0;
      return;
    }
    if (dragCanvas && startMouse && startView) {
      view.x = startView.x + (p.x - startMouse.x);
      view.y = startView.y + (p.y - startMouse.y);
      return;
    }
    hoverNode = nodeAt(world);
    canvas.style.cursor = hoverNode ? "pointer" : "grab";
  });
  function endDrag() {
    dragNode = null;
    dragCanvas = false;
    startMouse = null;
    startView = null;
    canvas.style.cursor = hoverNode ? "pointer" : "grab";
  }
  canvas.addEventListener("mouseup", endDrag);
  canvas.addEventListener("mouseleave", endDrag);
  canvas.addEventListener("wheel", (ev) => {
    ev.preventDefault();
    const p = getPos(ev);
    const before = toWorld(p);
    const factor = ev.deltaY < 0 ? 1.12 : 0.88;
    view.scale = Math.max(0.45, Math.min(2.75, view.scale * factor));
    const after = toWorld(p);
    view.x += (after.x - before.x) * view.scale;
    view.y += (after.y - before.y) * view.scale;
  });

  fetch("/api/corpus-overview")
    .then((r) => r.json())
    .then(buildGraph)
    .catch(() => {
      if (noteEl) noteEl.textContent = "Could not load corpus overview.";
      if (countEl) countEl.textContent = "";
    });
  canvas.style.cursor = "grab";
  animate();
})();
