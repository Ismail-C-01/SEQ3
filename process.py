"""Practical 3 / Practical 4: compute indicators from cleaned IMDb data.

Run after clean.py: python process.py
"""
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent
OUT = BASE / "output"
HIT_THRESHOLD = 50_000_000  # Example studio business question: gross at least 50 million


def process_data():
    source = OUT / "clean_movies.csv"
    if not source.exists():
        raise FileNotFoundError("Run python clean.py first.")
    df = pd.read_csv(source)

    # A film like 'Drama, Crime' contributes to BOTH genre groups.
    genres = df.assign(genre=df["Genre"].fillna("").str.split(",")).explode("genre")
    genres["genre"] = genres["genre"].str.strip()
    genres = genres[genres["genre"] != ""].copy()

    # We can only compute earnings when the Gross value is present.
    earning = genres.dropna(subset=["gross"]).copy()
    earning = earning[earning["gross"] >= 0]
    earning["gross_m"] = earning["gross"] / 1_000_000
    earning["earning_per_point_m"] = earning["gross_m"] / earning["rating"]
    earning["is_hit"] = earning["gross"] >= HIT_THRESHOLD

    genre_metrics = (earning.groupby("genre", as_index=False)
        .agg(movie_count=("Series_Title", "count"),
             avg_gross_m=("gross_m", "mean"),
             avg_rating=("rating", "mean"),
             avg_earning_per_score_m=("earning_per_point_m", "mean"),
             hit_count=("is_hit", "sum"),
             hit_rate_pct=("is_hit", lambda x: 100 * x.mean()))
        .sort_values("avg_earning_per_score_m", ascending=False))

    year_metrics = (df.groupby("year", as_index=False)
        .agg(avg_runtime_min=("runtime_min", "mean"), movie_count=("Series_Title", "count"))
        .sort_values("year"))

    # Company question: which genres have the highest share of commercially successful movies?
    studio_metrics = genre_metrics[["genre", "movie_count", "hit_count", "hit_rate_pct"]].copy()
    for name, data in [("genre_metrics.csv", genre_metrics),
                       ("year_metrics.csv", year_metrics),
                       ("studio_metrics.csv", studio_metrics)]:
        data.to_csv(OUT / name, index=False)
        print(f"Saved: output/{name} ({len(data)} rows)")

    print("\nGENRES: average gross, average rating, and earning per rating point")
    print(genre_metrics.head(8).round(2).to_string(index=False))
    print("\nSTUDIO QUESTION: share of films with gross >= 50 million")
    print(studio_metrics.sort_values("hit_rate_pct", ascending=False).head(8).round(1).to_string(index=False))
    print("\nNote: This is a top-rated-movies dataset, not all movies ever released.")
    print("Note: Missing Gross values are excluded from money-based indicators.")
    return genre_metrics, year_metrics, studio_metrics


if __name__ == "__main__":
    process_data()
