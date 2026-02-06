import pandas as pd
from pathlib import Path

# --- Base paths ---
ROOT = Path(__file__).resolve().parents[1] # /workspace
DATA_DIR = ROOT / "data"
OUTPUTS_DIR = ROOT / "outputs"

# --- File paths ---
BASE_FILE = OUTPUTS_DIR /"strategy_matrix_with_metadata.csv"
CAREER_FILE = DATA_DIR / "career_stage_supabase.csv"
OUT_FILE = OUTPUTS_DIR / "strategy_matrix_with_metadata_v2.csv"

# --- Load data ---
base = pd.read_csv(BASE_FILE)
career = pd.read_csv(CAREER_FILE)

# Join on episode_id
merged = base.merge(career, on="episode_id", how="left")

# Sanity checks
print("Base rows:", len(base))
print("Career rows:", len(career))
print("Merged rows:", len(merged))

missing = merged[merged["career_stage"].isna()]
if not missing.empty:
    print("\nWARNING: Missing career_stage for episodes:")
    print(missing["episode_id"].tolist())

merged.to_csv(OUT_FILE, index=False)
print("\nWrote:", OUT_FILE)
