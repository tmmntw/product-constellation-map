import pandas as pd

df = pd.read_csv("strategy_matrix_with_metadata_v2.csv")

# -----------------------
# CONFIG: change this only
# -----------------------
SPLIT_COLUMN = "prior_founder"  # e.g., woman_leader, prior_founder, prior_big_tech, ai_depth

NON_DOMAIN_COLUMNS = {
    "episode_id",
    "year",
    "ai_era",
    "ai_depth",
    "woman_leader",
    "guest_role",
    "company_at_time",
    "prior_founder",
    "prior_big_tech",
    "career_stage"
}

# Domain columns = everything else
DOMAIN_COLUMNS = [c for c in df.columns if c not in NON_DOMAIN_COLUMNS]

# Force domains to numeric 0/1 (handles "0", "1", blanks, weird strings)
for c in DOMAIN_COLUMNS:
    df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0).astype(int)

print(f"\n=== SPLIT INSIGHTS: {SPLIT_COLUMN} ===\n")

values = sorted(df[SPLIT_COLUMN].dropna().unique())

for value in values:
    subset = df[df[SPLIT_COLUMN] == value]

    print(f"\n--- {SPLIT_COLUMN} = {value} ---")
    print(f"Episodes: {len(subset)}\n")

    prevalence = subset[DOMAIN_COLUMNS].sum().sort_values(ascending=False)
    percentages = (prevalence / len(subset) * 100).round(1)

    print("Domain prevalence (count):")
    print(prevalence)
    print("\nDomain prevalence (% of episodes):")
    print(percentages)
    print("\n")
