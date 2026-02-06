// frontend/app.js

const graphEl = document.getElementById("graph");
const detailsEl = document.getElementById("details");
const datasetEl = document.getElementById("dataset");
const minWeightEl = document.getElementById("minWeight");
const minWeightValueEl = document.getElementById("minWeightValue");

let rawData = null;      // original full graph
let fg = null;           // ForceGraph instance

function setDetails(text) {
  detailsEl.textContent = text;
}

async function loadJSON(path) {
  console.log("Loading dataset:", path);

  const res = await fetch(path, { cache: "no-store" });
  if (!res.ok) {
    throw new Error(`Failed to fetch ${path}: ${res.status} ${res.statusText}`);
  }

  const data = await res.json();
  console.log("Loaded:", {
    nodes: data?.nodes?.length,
    edges: data?.edges?.length
  });

  // Convert your { nodes, edges } format into ForceGraph { nodes, links }
  return {
    nodes: data.nodes || [],
    links: (data.edges || []).map(e => ({
      source: e.source,
      target: e.target,
      weight: e.weight
    }))
  };
}

function applyMinWeight(minW) {
  if (!rawData) return;

  // Filter links by weight threshold
  const filteredLinks = rawData.links.filter(l => (l.weight ?? 0) >= minW);

  // Keep nodes that still appear in remaining links
  const used = new Set();
  filteredLinks.forEach(l => {
    used.add(typeof l.source === "object" ? l.source.id : l.source);
    used.add(typeof l.target === "object" ? l.target.id : l.target);
  });
  const filteredNodes = rawData.nodes.filter(n => used.has(n.id));

  fg.graphData({ nodes: filteredNodes, links: filteredLinks });

  setDetails(
    `Showing ${filteredNodes.length} nodes and ${filteredLinks.length} edges (min weight = ${minW}).`
  );
}

function initGraph(data) {
  // Size the canvas to fill the container
  const width = graphEl.clientWidth;
  const height = graphEl.clientHeight || (window.innerHeight - 60);

  fg = ForceGraph()(graphEl)
    .width(width)
    .height(height)
    .graphData(data)
    .backgroundColor("#0b0d10")
    .nodeId("id")
    .nodeLabel(n => `${n.label} (${n.size})`)
    .nodeVal(n => Math.max(2, n.size || 1))
    .linkLabel(l => `Co-occurrence: ${l.weight}`)
    .linkWidth(l => Math.max(1, (l.weight || 1) / 6))
    .linkDirectionalParticles(l => Math.min(6, Math.floor((l.weight || 1) / 6)))
    .linkDirectionalParticleWidth(1.5)
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
    });

  // Make it responsive
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
    setDetails(
      `ERROR loading graph.\n\n${err.message}\n\nOpen DevTools Console to see details.`
    );
  }
}

// UI events
datasetEl.addEventListener("change", () => boot());

minWeightEl.addEventListener("input", () => {
  minWeightValueEl.textContent = minWeightEl.value;
  applyMinWeight(parseInt(minWeightEl.value, 10));
});

// Start
boot();
