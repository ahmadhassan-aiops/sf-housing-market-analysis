"""Landing page: the investor's question, the findings and what they mean."""

import streamlit as st

from lib import data
from lib.ui import cap, finding, footer, header, md


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
    )

    k = st.columns(4)
    k[0].metric(f"Gross rent, {y1}", f"${c.loc[y1, 'rent']:,.0f}", delta=f"+{rent_g:.0%} since {y0}", border=True)
    k[1].metric(f"Median price per sq ft, {y1}", f"${c.loc[y1, 'price_median']:,.0f}", delta=f"+{price_g:.0%} since {y0}",
                border=True)
    k[2].metric(f"Housing units, {y1}", f"{c.loc[y1, 'units']:,.0f}", delta=f"+{units_g:.1%} since {y0}", border=True)
    k[3].metric("Neighbourhoods", m["neighborhoods"], border=True)

    st.subheader("Key findings", anchor=False)
    a = st.columns(3)
    finding(a[0], f"+{rent_g:.0%}", f"citywide gross rent, {y0} to {y1}",
            "Rents more than tripled",
            f"From ${c.loc[y0, 'rent']:,.0f} to ${c.loc[y1, 'rent']:,.0f} a month, rising every single year.",
            TRENDS, "Citywide trends")
    finding(a[1], f"+{price_g:.0%}", "median sale price per square foot",
            "Prices rose too, but much less than rent",
            f"Prices dipped in 2011, then climbed every year. Rent grew about {rent_g / price_g:.0f}x faster, which "
            "favours owners who rent out.", TRENDS, "Prices vs rent")
    finding(a[2], f"+{units_g:.1%}", "more housing units in seven years",
            "Supply barely moved",
            "About 1,950 new units a year on a stock of about 380,000: far too few to cool demand, which helps explain the rent surge.",
            TRENDS, "Housing supply")
    b = st.columns(3)
    finding(b[0], f"{p15.max() / p15.min():.0f}x", f"price gap between the dearest and cheapest neighbourhood ({2015})",
            "Location dominates price",
            f"In 2015 prices ranged from ${p15.min():,.0f} to ${p15.max():,.0f} per sq ft. Over the whole period the "
            f"highest among neighbourhoods with 5+ years of data is {reliable.iloc[0]['neighborhood']}.",
            NEIGHBORHOODS, "Neighbourhood ranking")
    finding(b[1], f"+{growth.median():.0%}", f"median price growth, 2010 to 2015 ({len(both)} neighbourhoods)",
            "Most neighbourhoods rose; a few fell",
            f"{(growth < 0).sum()} neighbourhoods were cheaper in 2015 than in 2010, while the strongest more than "
            "tripled. Neighbourhood choice matters as much as timing.",
            NEIGHBORHOODS, "Price growth")
    north = nb["lat"] > nb["lat"].median()
    finding(b[2], "North", "is where the priciest established neighbourhoods are",
            "The map shows a north-south gap",
            f"The five priciest neighbourhoods with 5+ years of data ({', '.join(reliable['neighborhood'].head(5))}) "
            f"are all in the north; Bayview in the south-east is the cheapest. Overall the gap is moderate "
            f"(median ${nb.loc[north, 'price'].median():,.0f} north vs ${nb.loc[~north, 'price'].median():,.0f} south).",
            MAP, "Map")

    st.subheader("What this means for an investor", anchor=False)
    md("1. **Rental yield has improved.** Rent rose much faster than purchase prices, so a dollar invested buys "
       "more rent in 2016 than in 2010.\n"
       "2. **Look at affordable neighbourhoods with steady growth**, not only the prime areas: the entry price is "
       "lower while citywide rent applies everywhere.\n"
       "3. **Check neighbourhood data quality before deciding.** Some neighbourhoods have only one or two years of "
       "sales; their averages are not reliable (the ranking lets you filter them out).")
    cap("Rent and housing units are citywide figures (one value per year), so rent cannot be compared between "
        "neighbourhoods with this data. See Data & method.")
    with st.container(border=True):
        md("**How this was done.** The census table was cleaned, summarised per year and per neighbourhood, and "
           "joined with neighbourhood coordinates for the map. This app is an interactive version of the notebook's Dash dashboard.")
        st.page_link(METHOD, label="Data & method", icon=":material/arrow_forward:")

    footer()
