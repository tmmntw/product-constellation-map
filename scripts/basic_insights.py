import pandas as pd

# Load your strategy matrix
df = pd.read_csv("strategy_matrix.csv")

# Drop episode_id for numeric analysis
domains = df.drop(columns=["episode_id"])

print("\n=== BASIC INSIGHTS ===\n")

# --------------------------------------------------
# 1. Domain prevalence
# --------------------------------------------------
print("1. DOMAIN PREVALENCE (how often each domain appears):\n")
prevalence = domains.sum().sort_values(ascending=False)
print(prevalence)
print("\n")

# --------------------------------------------------
# 2. Domain prevalence as % of episodes
# --------------------------------------------------
print("2. DOMAIN PREVALENCE (% of episodes):\n")
percentages = (domains.sum() / len(domains) * 100).round(1)
print(percentages)
print("\n")

# --------------------------------------------------
# 3. Domain co-occurrence matrix
# --------------------------------------------------
print("3. DOMAIN CO-OCCURRENCE MATRIX:\n")
co_occurrence = domains.T.dot(domains)
print(co_occurrence)
print("\n")

# --------------------------------------------------
# 4. Correlation matrix (what crowds out what)
# --------------------------------------------------
print("4. DOMAIN CORRELATION MATRIX:\n")
correlations = domains.corr().round(2)
print(correlations)
print("\n")

print("=== END OF INSIGHTS ===")
