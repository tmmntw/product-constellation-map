import csv
from pathlib import Path

INPUT_CSV = Path("Wide_EPISODES METADATA_Anthropic.csv")          # your Google Sheets export
OUT_EPISODES = Path("episodes.csv")            # metadata table
OUT_DOMAINS = Path("episode_domains.csv")      # long-format domains table

DOMAIN_PREFIX = "domain_"   # columns that start with this become domain rows


def normalize_bool(value: str):
    """
    Converts common Sheets boolean-ish values into standardized outputs.
    - Returns True/False for boolean-like strings
    - Returns the original string if not boolean-like
    """
    if value is None:
        return value
    v = str(value).strip().lower()
    if v in ("true", "t", "yes", "y", "1"):
        return True
    if v in ("false", "f", "no", "n", "0"):
        return False
    return value


def to_int01(value: str) -> int:
    """
    Converts a cell value into 0 or 1.
    Treats blank as 0.
    Accepts: 1, "1", true/yes, etc.
    """
    if value is None:
        return 0
    s = str(value).strip().lower()
    if s == "":
        return 0
    if s in ("1", "true", "t", "yes", "y"):
        return 1
    return 0


def main():
    if not INPUT_CSV.exists():
        raise FileNotFoundError(
            f"Missing {INPUT_CSV}. Upload your Google Sheets export as 'Wide_EPISODES METADATA_Anthropic.csv'."
        )

    # Read input
    with INPUT_CSV.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        raise RuntimeError("Input CSV has no rows.")

    # Identify columns
    all_columns = list(rows[0].keys())
    domain_columns = [c for c in all_columns if c and c.startswith(DOMAIN_PREFIX)]
    non_domain_columns = [c for c in all_columns if c not in domain_columns]

    if "episode_id" not in all_columns:
        raise RuntimeError("Input CSV must contain an 'episode_id' column.")

    print(f"Found {len(rows)} episodes")
    print(f"Found {len(domain_columns)} domain columns: {domain_columns}")

    # Build episodes.csv (metadata only)
    with OUT_EPISODES.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=non_domain_columns)
        writer.writeheader()

        for r in rows:
            out = {}
            for c in non_domain_columns:
                out[c] = normalize_bool(r.get(c, ""))
            writer.writerow(out)

    # Build episode_domains.csv (long format)
    domain_rows = []
    for r in rows:
        eid = str(r.get("episode_id", "")).strip()
        if not eid:
            continue

        for dc in domain_columns:
            # Convert "domain_growth" -> "growth"
            domain_name = dc[len(DOMAIN_PREFIX):].strip()
            label = to_int01(r.get(dc, ""))
            domain_rows.append(
                {
                    "episode_id": eid,
                    "domain": domain_name,
                    "label": label,
                }
            )

    with OUT_DOMAINS.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["episode_id", "domain", "label"])
        writer.writeheader()
        writer.writerows(domain_rows)

    print(f"\nWrote: {OUT_EPISODES.resolve()}")
    print(f"Wrote: {OUT_DOMAINS.resolve()}")
    print("\nNext: import episodes.csv into Supabase table 'episodes', and episode_domains.csv into 'episode_domains'.")


if __name__ == "__main__":
    main()
