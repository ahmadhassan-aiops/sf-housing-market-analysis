"""Citywide trends: housing units, gross rent and sale price per year (notebook 4.1-4.3)."""

import streamlit as st

from lib import charts, data
from lib.ui import chart, footer, header, insight, note, section


def render() -> None:
    c = data.city()
    years = c["year"].astype(str).tolist()

    header(
        "Market trends",
        "Citywide trends",
        "How the whole San Francisco market moved from 2010 to 2016: supply, rent and purchase prices.",
    )

    section("Rent vs price, indexed", "Each series set to 100 in 2010, so growth can be compared on one axis.")
    idx = {
        "Gross rent": (c["rent"] / c["rent"].iloc[0] * 100).round(1),
        "Median price per sq ft": (c["price_median"] / c["price_median"].iloc[0] * 100).round(1),
        "Housing units": (c["units"] / c["units"].iloc[0] * 100).round(1),
    }
    chart(charts.lines(years, idx, hover_fmt=".0f", ytitle="Index (2010 = 100)"))
    insight(
        f"By 2016 rent stood at <b>{idx['Gross rent'].iloc[-1]:.0f}</b> (3.5 times its 2010 level), prices at "
        f"<b>{idx['Median price per sq ft'].iloc[-1]:.0f}</b> and housing units at "
        f"{idx['Housing units'].iloc[-1]:.0f}. Rent outran prices every year from 2011."
    )

    left, right = st.columns(2, gap="large")
    with left:
        section("Gross rent", "Q3. Average monthly rent, citywide.")
        chart(charts.bars(years, c["rent"].values, text=[f"${v:,.0f}" for v in c["rent"]],
                          hover="%{x}<br><b>$%{y:,.0f}</b> a month", ytitle="Monthly rent ($)")
              .update_yaxes(tickprefix="$"))
        insight(f"Rent rose every year, fastest in 2012 (+{c['rent'].pct_change().iloc[2]:.0%}).")
    with right:
        section("Sale price per square foot", "Q1. Mean and median across neighbourhoods.")
        fig = charts.lines(years, {"Median": c["price_median"].round(0), "Mean": c["price_mean"].round(0)},
                           hover_fmt="$,.0f", ytitle="Price per sq ft ($)")
        chart(fig.update_yaxes(tickprefix="$"))
        insight("Prices fell slightly in 2011, then rose every year. The mean sits above the median because a few "
                "very expensive neighbourhood-years pull it up.")

    section("Housing units", "Q2. Number of housing units in the city.")
    chart(charts.bars(years, c["units"].values, hover="%{x}<br><b>%{y:,}</b> units", ytitle="Housing units")
          .update_yaxes(range=[365000, 386000]))
    insight("Units grew by <b>exactly 1,947 a year</b>, about 0.5% a year. The axis starts at 365,000 so the change "
            "is visible; from zero the bars would look identical.")
    note("Exactly the same increase every year suggests this column was interpolated between census counts rather "
         "than measured each year. Treat it as a rough trend.")

    section("The data behind these charts")
    st.dataframe(c.rename(columns={"year": "Year", "units": "Housing units", "rent": "Gross rent",
                                   "price_mean": "Mean price/sq ft", "price_median": "Median price/sq ft",
                                   "neighborhoods": "Neighbourhoods with sales"}),
                 hide_index=True,
                 column_config={"Year": st.column_config.NumberColumn(format="%d"),
                                "Housing units": st.column_config.NumberColumn(format="localized"),
                                "Gross rent": st.column_config.NumberColumn(format="dollar"),
                                "Mean price/sq ft": st.column_config.NumberColumn(format="dollar"),
                                "Median price/sq ft": st.column_config.NumberColumn(format="dollar")})

    footer()
