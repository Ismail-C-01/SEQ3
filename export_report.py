"""Practical 4: generate a self-contained interactive HTML dashboard artifact."""
from pathlib import Path
import pandas as pd
from figures import make_figures, offline_interactive_hit_chart

OUT = Path(__file__).resolve().parent / "output"


def export_report():
    movies = pd.read_csv(OUT / "clean_movies.csv")
    genre = pd.read_csv(OUT / "genre_metrics.csv")
    year = pd.read_csv(OUT / "year_metrics.csv")
    studio = pd.read_csv(OUT / "studio_metrics.csv")
    bar, line, scatter, _ = make_figures(genre, year, studio)
    interactive = offline_interactive_hit_chart(studio)

    table = movies[["Series_Title", "year", "Genre", "rating", "gross"]].head(5).to_html(index=False, classes="movie-table", border=0, na_rep="—", escape=True)
    charts = "\n".join(fig.to_html(full_html=False, include_plotlyjs=True if i == 0 else False)
                        for i, fig in enumerate([bar, line, scatter, interactive]))
    html_page = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>IMDB 1000 — Automated Report</title><style>
body{{font:16px Arial,sans-serif;background:#f3f6fa;color:#1c2a3a;max-width:1200px;margin:26px auto;padding:0 20px}}
header{{background:#142b48;color:white;padding:26px;border-radius:12px}}
section{{background:white;border-radius:12px;padding:18px;margin:19px 0;box-shadow:0 1px 5px #d5dfea}}
.movie-table{{border-collapse:collapse;width:100%;font-size:13px}}th,td{{padding:9px;text-align:left;border-bottom:1px solid #ddd}}
.small{{color:#607083;font-size:13px}}</style></head><body>
<header><h1>IMDB 1000</h1><p>Automated movie indicators and interactive charts</p></header>
<section><h2>First five films (.head())</h2>{table}</section>
<section>{charts}</section>
<section class="small"><p>Studio indicator: gross >= 50 million; only movies with a reported gross are counted.</p>
<p>Each multi-genre movie is included in every listed genre. The IMDb top-1000 sample is not representative of every movie.</p>
<p>The genre selector is inside the final chart. Unlike the Dash app, this HTML works without a Python server.</p></section>
</body></html>'''
    path = OUT / "imdb_dashboard.html"
    path.write_text(html_page, encoding="utf-8")
    print(f"Exported independent interactive HTML dashboard: {path}")
    return path


if __name__ == "__main__":
    export_report()
