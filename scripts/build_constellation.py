import sys
from pathlib import Path
import json
import pandas as pd

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from scripts.paths import OUTPUTS_DIR

# ---- INPUT / OUTPUT ----
IN_MATRIX = OUTPUTS_DIR / "strategy_matrix_with_metadata_v2.csv"  # episodes x domains (0/1)
OUT_JSON = OUTPUTS_DIR / "domain_constellation.json"  # nodes + edges

# Map internal column names -> nicer labels
DOMAIN_LABELS = {
    "product_strategy": "Product Strategy",
    "growth": "Growth",
    "decision_making": "Decision Making",
    "discovery_innovation": "Discovery & Innovation",
    "career_leadership": "Career & Leadership Growth",
    "gtm": "Go-to-Market",
    "data_ai": "AI & Data",
    "org_team": "Org Design & Team Dynamics",
    "founder_mode": "Founder Mode",
}


def main():
    df = pd.read_csv(IN_MATRIX)

    # Expect: episode_id + 9 domain columns
    if "episode_id" not in df.columns:
        raise ValueError("Expected 'episode_id' column in strategy_matrix.csv")

    domain_cols = [c for c in df.columns if c != "episode_id"]

    # Force numeric (protects against strings)
    for c in domain_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0).astype(int)

    # ---- Nodes: size = how many episodes include the domain ----
    nodes = []
    for c in domain_cols:
        nodes.append({
            "id": c,
            "label": DOMAIN_LABELS.get(c,
                                       c.replace("_", " ").title()),
            "size": int(df[c].sum())
        })

    # ---- Edges: weight = how many episodes include BOTH domains ----
    edges = []
    for i, d1 in enumerate(domain_cols):
        for d2 in domain_cols[i + 1:]:
            weight = int(((df[d1] == 1) & (df[d2] == 1)).sum())
            edges.append({"source": d1, "target": d2, "weight": weight})

    out = {"nodes": nodes, "edges": edges}

    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)

    print("Wrote:", OUT_JSON)
    print("Nodes:", len(nodes), "| Edges:", len(edges))


if __name__ == "__main__":
    main()
