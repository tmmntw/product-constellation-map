import csv
from collections import defaultdict
from pathlib import Path

INPUT_CSV = Path("episode_domains_supabase.csv")
OUTPUT_CSV = Path("strategy_matrix.csv")


def main():
    if not INPUT_CSV.exists():
        raise FileNotFoundError(
            f"Missing {INPUT_CSV}. Rename your Supabase export to this filename."
        )

    # Data structure:
    # episode_id -> domain -> label
    matrix = defaultdict(dict)
    all_domains = set()

    # Read long-format domain data
    with INPUT_CSV.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            episode_id = row["episode_id"].strip()
            domain = row["domain"].strip()
            label = int(row["label"])

            matrix[episode_id][domain] = label
            all_domains.add(domain)

    all_domains = sorted(all_domains)

    # Write wide-format strategy matrix
    with OUTPUT_CSV.open("w", encoding="utf-8", newline="") as f:
        fieldnames = ["episode_id"] + all_domains
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for episode_id, domains in matrix.items():
            row = {"episode_id": episode_id}
            for d in all_domains:
                row[d] = domains.get(d, 0)  # default to 0 if missing
            writer.writerow(row)

    print(f"Strategy matrix written to {OUTPUT_CSV.resolve()}")
    print(f"Rows (episodes): {len(matrix)}")
    print(f"Columns (domains): {len(all_domains)}")


if __name__ == "__main__":
    main()
