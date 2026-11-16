"""Map: average price per square foot by neighbourhood (notebook 4.6)."""

import plotly.graph_objects as go
import streamlit as st

from lib import charts, data
from lib.ui import cap, chart, footer, header, insight


def render() -> None:
    nb = data.neighborhoods()
    w = data.price_wide()

    header(
        "Map",
        "Prices across the city",
        "Each circle is a neighbourhood; darker and larger means a higher sale price per square foot. Hover for "
        "details, scroll or pinch to zoom.",
    )
    years = ["All years"] + [str(y) for y in w.columns]
    a, b = st.columns(2)
    year = a.select_slider("Year", options=years, value="All years", key="year")
    min_years = b.slider("Only neighbourhoods with at least this many years of data", 1, 7, 1, key="map_miny")

    d = nb[nb["years"] >= min_years].copy()
    if year != "All years":
        d["price"] = d["neighborhood"].map(w[int(year)])
    d = d.dropna(subset=["price"])
    size = 8 + 22 * (d["price"] - d["price"].min()) / max(1, d["price"].max() - d["price"].min())

    fig = go.Figure(go.Scattermap(
        lat=d["lat"], lon=d["lon"], mode="markers",
        marker=dict(size=size, color=d["price"], colorscale=charts.SEQUENTIAL, opacity=0.85,
                    colorbar=dict(title=dict(text="$ / sq ft", side="top"), thickness=10, outlinewidth=0)),
        customdata=d[["neighborhood", "years"]].values,
        hovertemplate="<b>%{customdata[0]}</b><br>$%{marker.color:,.0f} per sq ft<br>%{customdata[1]} years of data"
                      "<extra></extra>",
    ))
    fig.update_layout(
        map=dict(style="carto-positron", center=dict(lat=37.76, lon=-122.44), zoom=11.3),
        height=620, margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor=charts.SURFACE,
    )
    chart(fig, key="map")
    north = d["lat"] > d["lat"].median()
    insight(f"{len(d)} neighbourhoods shown. The priciest established areas (Union Square, Pacific Heights, "
            "Telegraph Hill, Presidio Heights, Cow Hollow) are in the north; the south-east is the most affordable. "
            f"Median for this view: ${d.loc[north, 'price'].median():,.0f} in the northern half against "
            f"${d.loc[~north, 'price'].median():,.0f} in the southern half.")
    cap("Positions are approximate neighbourhood centres from the source file; a few neighbourhoods share the same "
        "point and overlap.")

    footer()
