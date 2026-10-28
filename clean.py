"""Practical 3 / Practical 4: clean the IMDb dataset.

Run: python clean.py
Input: imdb_top_1000.csv OR all files in data/batches/
Output: output/clean_movies.csv
"""
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent
OUTPUT = BASE / "output"
SOURCE = BASE / "imdb_top_1000.csv"
BATCH_DIR = BASE / "data" / "batches"


def clean_data():
    batches = sorted(BATCH_DIR.glob("batch_*.csv"))
    if batches:
        print(f"Reading {len(batches)} batch(es).")
        df = pd.concat([pd.read_csv(p) for p in batches], ignore_index=True)
    elif SOURCE.exists():
        print("Reading original IMDb dataset.")
        df = pd.read_csv(SOURCE)
    else:
        raise FileNotFoundError(
            "Missing imdb_top_1000.csv. Download the Kaggle file, "
            "put it next to clean.py, and try again."
        )

    original_rows = len(df)
    required = ["Series_Title", "Released_Year", "Runtime", "Genre", "IMDB_Rating", "Gross"]
    missing_columns = sorted(set(required) - set(df.columns))
    if missing_columns:
        raise ValueError(f"Dataset missing columns: {missing_columns}")

    # Extract a usable year even if a source value is not perfectly formatted.
    df["year"] = pd.to_numeric(
        df["Released_Year"].astype("string").str.extract(r"(\d{4})", expand=False),
        errors="coerce",
    )
    # IMDb runtime is stored as text like '142 min'.
    df["runtime_min"] = pd.to_numeric(
        df["Runtime"].astype("string").str.extract(r"(\d+)", expand=False),
        errors="coerce",
    )
    df["rating"] = pd.to_numeric(df["IMDB_Rating"], errors="coerce")
    # Gross is text like '28,341,469'. Missing gross stays missing.
    df["gross"] = pd.to_numeric(
        df["Gross"].astype("string").str.replace(",", "", regex=False),
        errors="coerce",
    )
    # Keep films missing gross: they can still be used for runtime analysis.
    df = df.dropna(subset=["Series_Title", "Genre", "year", "runtime_min", "rating"])
    df = df[df["rating"].between(0.1, 10) & df["runtime_min"].gt(0)]
    df["Series_Title"] = df["Series_Title"].astype(str).str.strip()
    df["Genre"] = df["Genre"].astype(str).str.strip()
    df = df[(df["Series_Title"] != "") & (df["Genre"] != "")]
    df["year"] = df["year"].astype(int)
    df = df.drop_duplicates(subset=["Series_Title", "year"], keep="first")

    OUTPUT.mkdir(exist_ok=True)
    out = OUTPUT / "clean_movies.csv"
    df.to_csv(out, index=False)
    print(f"Cleaning: {original_rows} input rows -> {len(df)} valid unique movies.")
    print(f"Saved: {out}")
    return df


if __name__ == "__main__":
    clean_data()
