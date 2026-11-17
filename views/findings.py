"""Landing page: the investor's question, the findings and what they mean."""

import plotly.graph_objects as go
import streamlit as st

from lib import charts, data
from lib.ui import cap, finding, footer, header, method_card, recommendations, spotlight


def render() -> None:
    from nav import MAP, METHOD, NEIGHBORHOODS, TRENDS

    m = data.meta()
    c = data.city().set_index("year")
    w = data.price_wide()
    nb = data.neighborhoods()
    y0, y1 = m["years"]
    rent_g = c.loc[y1, "rent"] / c.loc[y0, "rent"] - 1
    price_g = c.loc[y1, "price_median"] / c.loc[y0, "price_median"] - 1
    units_g = c.loc[y1, "units"] / c.loc[y0, "units"] - 1
    both = w.dropna(subset=[2010, 2015])
    growth = (both[2015] / both[2010] - 1)
    reliable = nb[nb["years"] >= 5].sort_values("price", ascending=False)
    p15 = w[2015].dropna()

    header(
        "Exploratory data analysis · Python, pandas, Plotly",
        "San Francisco housing, 2010-2016: where should a rental investor look?",
        f"Seven years of census figures for {m['neighborhoods']} San Francisco neighbourhoods: sale prices per square "
        "foot, the number of housing units and gross rent. I analysed how the market moved and how neighbourhoods "
        "compare, to help investors choose where to buy rental property.",
        chips=[("code", "Python, pandas"), ("map", "Plotly maps"), ("location_city", f"{m['neighborhoods']} neighbourhoods"),
               ("calendar_month", f"{y0} to {y1}")],
    )

    k = st.columns(4)
    k[0].metric(f"Gross rent, {y1}", f"${c.loc[y1, 'rent']:,.0f}", delta=f"+{rent_g:.0%} since {y0}", border=True)
    k[1].metric(f"Median price per sq ft, {y1}", f"${c.loc[y1, 'price_median']:,.0f}", delta=f"+{price_g:.0%} since {y0}",
                border=True)
    k[2].metric(f"Housing units, {y1}", f"{c.loc[y1, 'units']:,.0f}", delta=f"+{units_g:.1%} since {y0}", border=True)
    k[3].metric("Neighbourhoods", m["neighborhoods"], border=True)

    size = 8 + 22 * (nb["price"] - nb["price"].min()) / max(1, nb["price"].max() - nb["price"].min())
    fig = go.Figure(go.Scattermap(
        lat=nb["lat"], lon=nb["lon"], mode="markers",
        marker=dict(size=size, color=nb["price"], colorscale=charts.SEQUENTIAL, opacity=0.85,
                    colorbar=dict(title=dict(text="$ / sq ft", side="top"), thickness=10, outlinewidth=0)),
        customdata=nb[["neighborhood", "years"]].values,
        hovertemplate="<b>%{customdata[0]}</b><br>$%{marker.color:,.0f} per sq ft<br>%{customdata[1]} years of data"
                      "<extra></extra>",
    ))
    fig.update_layout(map=dict(style="carto-positron", center=dict(lat=37.76, lon=-122.44), zoom=11),
                      height=470, margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor=charts.SURFACE)
    spotlight("Where San Francisco is expensive",
              f"Average sale price per square foot, {y0}-{y1}, one circle per neighbourhood: larger and darker means "
              "dearer. The <b>north</b> holds the priciest established areas; the <b>south-east</b> is the most "
              "affordable. Hover a circle for details.", fig, key="spot")

    st.subheader("Key findings", anchor=False)
    a = st.columns(3)
    finding(a[0], f"+{rent_g:.0%}", f"citywide gross rent, {y0} to {y1}",
            "Rents more than tripled",
            f"From ${c.loc[y0, 'rent']:,.0f} to ${c.loc[y1, 'rent']:,.0f} a month, rising every single year.",
            TRENDS, "Citywide trends", card_icon="trending_up")
    finding(a[1], f"+{price_g:.0%}", "median sale price per square foot",
            "Prices rose too, but much less than rent",
            f"Prices dipped in 2011, then climbed every year. Rent grew about {rent_g / price_g:.0f}x faster, which "
            "favours owners who rent out.", TRENDS, "Prices vs rent", card_icon="real_estate_agent")
    finding(a[2], f"+{units_g:.1%}", "more housing units in seven years",
            "Supply barely moved",
            "About 1,950 new units a year on a stock of about 380,000: far too few to cool demand, which helps explain the rent surge.",
            TRENDS, "Housing supply", card_icon="apartment")
    b = st.columns(3)
    finding(b[0], f"{p15.max() / p15.min():.0f}x", f"price gap between the dearest and cheapest neighbourhood ({2015})",
            "Location dominates price",
            f"In 2015 prices ranged from ${p15.min():,.0f} to ${p15.max():,.0f} per sq ft. Over the whole period the "
            f"highest among neighbourhoods with 5+ years of data is {reliable.iloc[0]['neighborhood']}.",
            NEIGHBORHOODS, "Neighbourhood ranking", card_icon="leaderboard")
    finding(b[1], f"+{growth.median():.0%}", f"median price growth, 2010 to 2015 ({len(both)} neighbourhoods)",
            "Most neighbourhoods rose; a few fell",
            f"{(growth < 0).sum()} neighbourhoods were cheaper in 2015 than in 2010, while the strongest more than "
            "tripled. Neighbourhood choice matters as much as timing.",
            NEIGHBORHOODS, "Price growth", card_icon="stacked_line_chart")
    north = nb["lat"] > nb["lat"].median()
    finding(b[2], "North", "is where the priciest established neighbourhoods are",
            "The map shows a north-south gap",
            f"The five priciest neighbourhoods with 5+ years of data ({', '.join(reliable['neighborhood'].head(5))}) "
            f"are all in the north; Bayview in the south-east is the cheapest. Overall the gap is moderate "
            f"(median ${nb.loc[north, 'price'].median():,.0f} north vs ${nb.loc[~north, 'price'].median():,.0f} south).",
            MAP, "Map", card_icon="explore")

    st.subheader("What this means for an investor", anchor=False)
    recommendations([
        ("savings", "Rental yield has improved",
         "Rent rose much faster than purchase prices, so a dollar invested buys more rent in 2016 than in 2010."),
        ("travel_explore", "Look beyond the prime areas",
         "Affordable neighbourhoods with steady growth have a lower entry price, while citywide rent applies everywhere."),
        ("fact_check", "Check data quality first",
         "Some neighbourhoods have only one or two years of sales; their averages are not reliable (the ranking lets "
         "you filter them out)."),
    ])
    cap("Rent and housing units are citywide figures (one value per year), so rent cannot be compared between "
        "neighbourhoods with this data. See Data & method.")
    method_card("<b>How this was done.</b> The census table was cleaned, summarised per year and per neighbourhood, "
                "and joined with neighbourhood coordinates for the map. This app is an interactive version of the "
                "notebook's Dash dashboard.", METHOD, tools=["pandas", "Plotly", "Maps", "Dash (original dashboard)"])

    footer()
