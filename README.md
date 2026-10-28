# IMDB 1000 — Practical sequence 3.1 and 4

This project follows the two course practicals using the Kaggle dataset:
https://www.kaggle.com/datasets/harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows

## Before starting

Download and extract `imdb_top_1000.csv` from Kaggle. Place it in the same folder as `clean.py`. The CSV is intentionally not included in this ZIP.

The easiest environment for beginners is **GitHub Codespaces**, which runs Python inside your browser. Create a GitHub repository, upload the project files (including hidden `.github/workflows/imdb.yml`), and create a Codespace from the repository.

## Practical 3.1 — analysis and Dash

Open a terminal in your project's folder. Type each command separately:

```bash
python -m pip install -r requirements.txt
python clean.py
python process.py
python app.py
```

Open the port 8050 link that Codespaces offers. The dashboard shows:

1. Title `IMDB 1000` and first five rows of the cleaned DataFrame.
2. Average gross per IMDb score point, grouped by genre.
3. Average runtime by release year.
4. Gross vs. rating by genre to address the profitability/quality question.
5. Commercial hit rate by genre, with an interactive dropdown (studio question).

Stop the Dash server by clicking in the terminal and pressing Ctrl+C.

## Practical 4 — automation

The project already includes `.github/workflows/imdb.yml`. It triggers when you push to `main`, and can also be started manually under the GitHub **Actions** tab with **Run workflow**.

GitHub Actions runs two jobs: `cleaning`, then `processing`. The second job creates a self-contained HTML dashboard and uploads it as the artifact `imdb-dashboard`. Download that artifact ZIP from the run summary and open `imdb_dashboard.html` in a browser.

## Batch simulation

Your teacher mentions a file from Moodle called `batch_simulator.py`. That file was not attached to the conversation, so this kit cannot claim to reproduce its exact expected arguments or behavior. A clearly labeled demonstration substitute is included:

```bash
python batch_simulator_example.py --batches 3 --interval 15
```

Run this ONLY inside a GitHub Codespace that already has the project committed on `main` and permission to `git push`. The program writes a new `data/batches/batch_NNN.csv` and pushes a commit for each batch. Every push starts the GitHub workflow. If you just want to simulate locally without pushing, add `--no-push`.

Once batch files exist, `clean.py` uses the combined batches instead of the original full CSV. This shows growing aggregated indicators. The `data/batches` files are included in the final project through Git commits.

## How indicators are calculated

- IMDb quality score: `IMDB_Rating` (0–10).
- Gross: `Gross` stripped of commas and converted to a number; rows missing it stay usable for the runtime trend but cannot be included in gross calculations.
- **Average gross per rating point by genre:** for each movie with gross data, `Gross / IMDB_Rating`; take the average by genre.
- **Mean runtime by year:** extract minutes from `Runtime`, extract year from `Released_Year`, then take mean by release year.
- **Quality vs earnings:** average gross and average IMDb rating per genre.
- **Studio business question:** which genre has the highest share of movies with gross >= 50 million? Numerator = hits; denominator = movies with known gross.
- Movies with multiple genres count in every listed genre.
- IMDb top-1000 is a **selected sample**, so results should not be described as representing all films.

## Files

| File | Why it exists |
|---|---|
| `clean.py` | Reads data, handles missing values and duplicates, saves `output/clean_movies.csv` |
| `process.py` | Computes genre, year and company metrics |
| `figures.py` | Reusable Plotly figures |
| `app.py` | Interactive Dash dashboard for Practical 3 |
| `export_report.py` | Writes an interactive offline HTML dashboard for Practical 4 |
| `.github/workflows/imdb.yml` | GitHub Actions pipeline on push to main |
| `batch_simulator_example.py` | Demonstration substitute for unavailable Moodle file |
| `requirements.txt` | Python dependencies |

Data source: Kaggle IMDb Dataset of Top 1000 Movies and TV Shows by harshitshankhdhar, shown with CC0 license on Kaggle. This is an educational exercise.
