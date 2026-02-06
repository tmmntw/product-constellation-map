const graphEl = document.getElementById("graph");
const detailsEl = document.getElementById("details");
const datasetEl = document.getElementById("dataset");
const minWeightEl = document.getElementById("minWeight");
const minWeightValueEl = document.getElementById("minWeightValue");

let rawData = null;
let fg = null;
let currentMaxWeight = 1;

function setDetails(text) {
  detailsEl.textContent = text;
}

function linkColorFn(l) {
  const strength = (l.weight || 1) / currentMaxWeight;
  const r = Math.round(80 + strength * 100);
  const g = Math.round(140 + strength * 80);
  const b = 255;
  const alpha = Math.max(0.35, 0.3 + strength * 0.5);
  return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

function linkWidthFn(l) {
  const strength = (l.weight || 1) / currentMaxWeight;
  return Math.max(1.5, strength * 6);
}

async function loadJSON(path) {
  console.log("Loading dataset:", path);
  const res = await fetch(path, { cache: "no-store" });
  if (!res.ok) {
    throw new Error(`Failed to fetch ${path}: ${res.status} ${res.statusText}`);
  }
  const data = await res.json();
  console.log("Loaded:", { nodes: data?.nodes?.length, edges: data?.edges?.length });

  return {
    nodes: data.nodes || [],
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
    .nodeVal(n => Math.max(4, (n.size || 1) * 1.5))
    .nodeColor(() => "#6ec6ff")
    .nodeCanvasObjectMode(() => "after")
    .nodeCanvasObject((node, ctx, globalScale) => {
      const label = node.label || node.id;
      const fontSize = Math.max(10, 14 / globalScale);
      ctx.font = `${fontSize}px Sans-Serif`;
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillStyle = "rgba(230, 234, 240, 0.9)";
      ctx.fillText(label, node.x, node.y + (Math.max(4, (node.size || 1) * 1.5)) + fontSize);
    })
    .linkColor(linkColorFn)
    .linkWidth(linkWidthFn)
    .linkLabel(l => `Co-occurrence: ${l.weight}`)
    .linkDirectionalParticles(l => Math.min(4, Math.ceil((l.weight || 0) / 8)))
    .linkDirectionalParticleWidth(2)
    .linkDirectionalParticleColor(() => "rgba(120, 200, 255, 0.8)")
    .linkDirectionalParticleSpeed(0.004)
    .onNodeHover(node => {
      if (!node) {
        setDetails("Hover a node or edge to see details.");
        return;
      }
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

  fg.d3Force("charge").strength(-200);
  fg.d3Force("link").distance(120);

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
