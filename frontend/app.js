const graphEl = document.getElementById("graph");
const detailsEl = document.getElementById("details");
const datasetEl = document.getElementById("dataset");
const minWeightEl = document.getElementById("minWeight");
const minWeightValueEl = document.getElementById("minWeightValue");

let rawData = null;
let fg = null;
let currentMaxWeight = 1;

const NODE_COLORS = [
  "#e06c75", "#e5c07b", "#61afef", "#c678dd", "#56b6c2",
  "#98c379", "#d19a66", "#be5046", "#7ec8e3", "#c8a2c8",
  "#f0e68c", "#ff8c69", "#87ceeb", "#dda0dd", "#90ee90",
  "#ffa07a", "#20b2aa", "#b0c4de"
];

function setDetails(text) {
  detailsEl.textContent = text;
}

function getNodeColor(node) {
  if (node.__colorIdx === undefined) return NODE_COLORS[0];
  return NODE_COLORS[node.__colorIdx % NODE_COLORS.length];
}

function linkColorFn(l) {
  const strength = (l.weight || 1) / currentMaxWeight;
  const alpha = Math.max(0.12, 0.08 + strength * 0.35);
  return `rgba(150, 180, 220, ${alpha})`;
}

function linkWidthFn(l) {
  const strength = (l.weight || 1) / currentMaxWeight;
  return Math.max(0.5, strength * 4);
}

async function loadJSON(path) {
  console.log("Loading dataset:", path);
  const res = await fetch(path, { cache: "no-store" });
  if (!res.ok) {
    throw new Error(`Failed to fetch ${path}: ${res.status} ${res.statusText}`);
  }
  const data = await res.json();
  console.log("Loaded:", { nodes: data?.nodes?.length, edges: data?.edges?.length });

  const nodes = (data.nodes || []).map((n, i) => ({ ...n, __colorIdx: i }));

  return {
    nodes,
    links: (data.edges || [])
      .filter(e => (e.weight || 0) > 0)
      .map(e => ({ source: e.source, target: e.target, weight: e.weight }))
  };
}

function applyMinWeight(minW) {
  if (!rawData) return;

  const filteredLinks = rawData.links.filter(l => (l.weight ?? 0) >= minW);

  const used = new Set();
  filteredLinks.forEach(l => {
    used.add(typeof l.source === "object" ? l.source.id : l.source);
    used.add(typeof l.target === "object" ? l.target.id : l.target);
  });
  const filteredNodes = rawData.nodes.filter(n => used.has(n.id));

  currentMaxWeight = Math.max(...filteredLinks.map(l => l.weight || 0), 1);

  fg.graphData({ nodes: filteredNodes, links: filteredLinks });

  setDetails(
    `Showing ${filteredNodes.length} nodes and ${filteredLinks.length} edges (min weight = ${minW}).`
  );
}

function initGraph(data) {
  const width = graphEl.clientWidth;
  const height = graphEl.clientHeight || (window.innerHeight - 60);

  currentMaxWeight = Math.max(...data.links.map(l => l.weight || 0), 1);

  fg = ForceGraph()(graphEl)
    .width(width)
    .height(height)
    .graphData(data)
    .backgroundColor("#0b0d10")
    .nodeId("id")
    .nodeLabel(n => `${n.label} (${n.size})`)
    .nodeVal(n => Math.max(5, (n.size || 1) * 1.2))
    .nodeCanvasObjectMode(() => "replace")
    .nodeCanvasObject((node, ctx, globalScale) => {
      const r = Math.sqrt(Math.max(5, (node.size || 1) * 1.2)) * 2.5;
      const color = getNodeColor(node);

      ctx.beginPath();
      ctx.arc(node.x, node.y, r, 0, 2 * Math.PI);
      ctx.fillStyle = color;
      ctx.fill();

      ctx.strokeStyle = "rgba(255,255,255,0.3)";
      ctx.lineWidth = 1;
      ctx.stroke();

      const label = node.label || node.id;
      const fontSize = Math.max(10, 12 / globalScale);
      ctx.font = `600 ${fontSize}px Sans-Serif`;
      ctx.textAlign = "center";
      ctx.textBaseline = "top";
      ctx.fillStyle = "#e6eaf0";
      ctx.fillText(label, node.x, node.y + r + 4);
    })
    .linkColor(linkColorFn)
    .linkWidth(linkWidthFn)
    .linkLabel(l => `Co-occurrence: ${l.weight}`)
    .linkDirectionalParticles(l => l.weight > 5 ? Math.min(3, Math.ceil(l.weight / 10)) : 0)
    .linkDirectionalParticleWidth(1.5)
    .linkDirectionalParticleColor(() => "rgba(200, 220, 255, 0.6)")
    .linkDirectionalParticleSpeed(0.003)
    .linkCurvature(0)
    .onNodeHover(node => {
      if (!node) {
        setDetails("Hover a node or edge to see details.");
        graphEl.style.cursor = "default";
        return;
      }
      graphEl.style.cursor = "pointer";
      setDetails(`${node.label}\n\nEpisodes tagged with this domain: ${node.size}`);
    })
    .onLinkHover(link => {
      if (!link) return;
      const s = typeof link.source === "object" ? link.source.id : link.source;
      const t = typeof link.target === "object" ? link.target.id : link.target;
      setDetails(`Edge: ${s} ↔ ${t}\n\nShared episodes: ${link.weight}`);
    })
    .cooldownTicks(100)
    .warmupTicks(50);

  fg.d3Force("charge").strength(-300);
  fg.d3Force("link").distance(150);

  window.addEventListener("resize", () => {
    fg.width(graphEl.clientWidth);
    fg.height(graphEl.clientHeight || (window.innerHeight - 60));
  });
}

async function boot() {
  try {
    minWeightValueEl.textContent = minWeightEl.value;
    const path = datasetEl.value;
    const data = await loadJSON(path);
    rawData = data;
    if (!fg) initGraph(rawData);
    applyMinWeight(parseInt(minWeightEl.value, 10));
  } catch (err) {
    console.error(err);
    setDetails(`ERROR loading graph.\n\n${err.message}\n\nOpen DevTools Console to see details.`);
  }
}

datasetEl.addEventListener("change", () => boot());

minWeightEl.addEventListener("input", () => {
  minWeightValueEl.textContent = minWeightEl.value;
  applyMinWeight(parseInt(minWeightEl.value, 10));
});

boot();
