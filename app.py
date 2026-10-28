"""Practical 3: launch with 'python app.py', then open the forwarded 8050 port."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, dash_table, Input, Output
from figures import make_figures

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output"
for filename in ["clean_movies.csv", "genre_metrics.csv", "year_metrics.csv", "studio_metrics.csv"]:
    if not (OUT / filename).exists():
        raise FileNotFoundError(f"Missing output/{filename}. First run: python clean.py, then python process.py")

movies = pd.read_csv(OUT / "clean_movies.csv")
genre = pd.read_csv(OUT / "genre_metrics.csv")
year = pd.read_csv(OUT / "year_metrics.csv")
studio = pd.read_csv(OUT / "studio_metrics.csv")
bar, line, scatter, hit_bar = make_figures(genre, year, studio)

app = Dash(__name__)
app.title = "IMDB 1000"
card = {"background": "white", "padding": "16px", "marginBottom": "18px", "borderRadius": "12px", "boxShadow": "0 1px 4px #d9e2ec"}
app.layout = html.Div(
    style={"maxWidth": "1150px", "margin": "24px auto", "fontFamily": "Arial, sans-serif", "padding": "0 18px", "background": "#f5f8fc"},
    children=[
        html.H1("IMDB 1000"),
        html.P("Movie genres, revenue, ratings, runtime trends, and a studio's commercial-hit question."),
        html.Div([
            html.H3("First five films in the cleaned dataframe (.head())"),
            dash_table.DataTable(
                data=movies[["Series_Title", "year", "Genre", "rating", "gross"]].head().fillna("").to_dict("records"),
                columns=[{"name": v, "id": v} for v in ["Series_Title", "year", "Genre", "rating", "gross"]],
                style_table={"overflowX": "auto"}, style_cell={"textAlign": "left", "padding": "9px", "fontFamily": "Arial"},
                style_header={"backgroundColor": "#eff3f9", "fontWeight": "bold"},
            )
        ], style=card),
        html.Div(dcc.Graph(figure=bar), style=card),
        html.Div(dcc.Graph(figure=line), style=card),
        html.Div(dcc.Graph(figure=scatter), style=card),
        html.Div([
            html.H3("A business question: Which genre has the highest commercial hit rate?"),
            html.P("Here, a commercial hit means reported gross >= 50 million. Select a genre:"),
            dcc.Dropdown(id="genre-choice", options=[{"label": g, "value": g} for g in sorted(studio["genre"])],
                         value=sorted(studio["genre"])[0], clearable=False),
            html.Div(id="genre-answer", style={"marginTop": "14px", "fontSize": "17px"}),
            dcc.Graph(id="genre-detail"),
        ], style=card),
        html.P("Important: the dataset covers top-rated IMDb movies, not all movies, and some gross values are missing.",
               style={"fontSize": "13px", "color": "#596578"}),
    ],
)


@app.callback(Output("genre-answer", "children"), Output("genre-detail", "figure"), Input("genre-choice", "value"))
def choose_genre(chosen):
    record = studio.loc[studio["genre"] == chosen].iloc[0]
    count, hits, percent = int(record["movie_count"]), int(record["hit_count"]), float(record["hit_rate_pct"])
    text = f"{chosen}: {hits} of {count} movies were commercial hits ({percent:.1f}%)."
    graph = go.Figure(go.Bar(x=[hits, count - hits], y=["Gross >= 50m", "Below 50m"], orientation="h"))
    graph.update_layout(title=f"Commercial hits for {chosen}", xaxis_title="Number of movies", height=250,
                        margin=dict(l=20, r=20, t=45, b=35))
    return text, graph


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8050)
