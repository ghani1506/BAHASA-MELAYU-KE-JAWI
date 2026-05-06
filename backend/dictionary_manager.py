import csv
from pathlib import Path
import pandas as pd


def ensure_dictionary(path):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    if not p.exists():
        with p.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["rumi", "jawi", "kategori"])


def append_dictionary_entry(path, rumi, jawi, kategori="pengguna"):
    ensure_dictionary(path)
    p = Path(path)

    rows = []
    found = False
    rumi_key = rumi.strip().lower()

    with p.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if (row.get("rumi") or "").strip().lower() == rumi_key:
                row["jawi"] = jawi.strip()
                row["kategori"] = kategori.strip() or "pengguna"
                found = True
            rows.append(row)

    if not found:
        rows.append({
            "rumi": rumi_key,
            "jawi": jawi.strip(),
            "kategori": kategori.strip() or "pengguna"
        })

    with p.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["rumi", "jawi", "kategori"])
        writer.writeheader()
        writer.writerows(rows)


def load_dictionary_frame(path):
    ensure_dictionary(path)
    return pd.read_csv(path)
