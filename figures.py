"""Reusable charts for both the Dash app and exported offline HTML."""
import plotly.express as px
import plotly.graph_objects as go


def make_figures(genre, year, studio):
    bar = px.bar(
        genre.sort_values("avg_earning_per_score_m"),
        x="avg_earning_per_score_m", y="genre", orientation="h",
        title="Average gross earned per IMDb rating point, by genre",
        labels={"avg_earning_per_score_m": "Gross per rating point (millions)", "genre": "Genre"},
    )
    bar.update_layout(height=660, margin=dict(l=25, r=25, t=65, b=45))

    line = px.line(
        year, x="year", y="avg_runtime_min", markers=True,
        title="How average movie runtime changes over release years",
        labels={"year": "Release year", "avg_runtime_min": "Average runtime (minutes)"},
        hover_data=["movie_count"],
    )
    line.update_layout(height=430, margin=dict(l=25, r=25, t=65, b=45))

    scatter = px.scatter(
        genre, x="avg_rating", y="avg_gross_m", size="movie_count",
        hover_name="genre", text="genre",
        title="Do higher-earning genres always have higher IMDb ratings?",
        labels={"avg_rating": "Average IMDb rating", "avg_gross_m": "Average reported gross (millions)"},
    )
    scatter.update_traces(textposition="top center")
    scatter.update_layout(height=510, margin=dict(l=25, r=25, t=65, b=45))

    hit_bar = px.bar(
        studio.sort_values("hit_rate_pct"),
        x="hit_rate_pct", y="genre", orientation="h",
        title="Studio indicator: share of movies with gross >= 50 million",
        labels={"hit_rate_pct": "Commercial hit rate (%)", "genre": "Genre"},
        hover_data=["hit_count", "movie_count"],
    )
    hit_bar.update_layout(height=660, margin=dict(l=25, r=25, t=65, b=45))
    return bar, line, scatter, hit_bar


def offline_interactive_hit_chart(studio):
    """Make a genuine, browser-only genre dropdown using Plotly (no Dash server needed)."""
    s = studio.sort_values("hit_rate_pct")
    names = s["genre"].tolist()
    f = go.Figure()
    f.add_bar(x=s["hit_rate_pct"], y=s["genre"], orientation="h", name="All genres", visible=True)
    for _, r in s.iterrows():
        f.add_bar(x=[r["hit_rate_pct"]], y=[r["genre"]], orientation="h", name=r["genre"], visible=False)
    buttons = [dict(label="All genres", method="update", args=[{"visible": [True] + [False] * len(names)}, {"title": "Studio commercial hit rate — All genres"}])]
    for idx, name in enumerate(names):
        visible = [False] * (1 + len(names))
        visible[idx + 1] = True
        buttons.append(dict(label=name, method="update", args=[{"visible": visible}, {"title": f"Studio commercial hit rate — {name}"}]))
    f.update_layout(
        title="Studio commercial hit rate — All genres",
        xaxis_title="Share of movies with gross >= 50 million (%)",
        yaxis_title="Genre", xaxis_range=[0, 105], height=660,
        updatemenus=[dict(buttons=buttons, active=0, direction="down", x=1, y=1.13,
                          xanchor="right", yanchor="top", showactive=True)],
        margin=dict(l=25, r=25, t=110, b=45), showlegend=False,
    )
    return f
