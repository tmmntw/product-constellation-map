import pandas as pd
import json
from itertools import combinations

# Load data WITH metadata
df = pd.read_csv("strategy_matrix_with_metadata.csv")

DOMAIN_COLUMNS = [
    "product_strategy",
    "growth",
    "decision_making",
    "discovery_innovation",
    "career_leadership",
    "gtm",
    "data_ai",
    "org_team",
    "founder_mode",
]

AI_ERAS = df["ai_era"].unique()

for era in AI_ERAS:
    subset = df[df["ai_era"] == era]

    # -----------------------
    # Build NODES
    # -----------------------
    nodes = []
    for domain in DOMAIN_COLUMNS:
        count = subset[domain].sum()
        nodes.append({
            "id": domain,
            "label": domain.replace("_", " ").title(),
            "size": int(count)
        })

    # -----------------------
    # Build EDGES
    # -----------------------
    edges = []
    for d1, d2 in combinations(DOMAIN_COLUMNS, 2):
        weight = ((subset[d1] == 1) & (subset[d2] == 1)).sum()
        if weight > 0:
            edges.append({
                "source": d1,
                "target": d2,
                "weight": int(weight)
            })

    # -----------------------
    # Save constellation
    # -----------------------
    constellation = {
        "ai_era": era,
        "nodes": nodes,
        "edges": edges
    }

    filename = f"domain_constellation_{era}.json"
    with open(filename, "w") as f:
        json.dump(constellation, f, indent=2)

    print(f" Saved {filename} ({len(subset)} episodes)")
