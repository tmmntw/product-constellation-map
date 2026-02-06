import pandas as pd

MATRIX_CSV = "strategy_matrix.csv"
META_CSV = "episode_metadata_supabase.csv"
OUT_CSV = "strategy_matrix_with_metadata.csv"

matrix = pd.read_csv(MATRIX_CSV)
meta = pd.read_csv(META_CSV)

merged = meta.merge(matrix, on="episode_id", how="inner")

# sanity checks
print("Matrix rows:", len(matrix))
print("Meta rows:", len(meta))
print("Merged rows:", len(merged))

missing = set(meta["episode_id"]) - set(matrix["episode_id"])
if missing:
    print("\nWARNING: metadata episodes missing from matrix (first 10):")
    print(list(sorted(missing))[:10])

merged.to_csv(OUT_CSV, index=False)
print("\nWrote:", OUT_CSV)
