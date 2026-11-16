"""Neighbourhoods: ranking by price, growth 2010-2015, and a comparison of up to three (notebook 4.4-4.5)."""

import streamlit as st

from lib import charts, data
from lib.ui import cap, chart, footer, header, insight, section


def render() -> None:
    nb = data.neighborhoods()
    w = data.price_wide()

    header(
        "Neighbourhoods",
        "Neighbourhoods compared",
        "Sale price per square foot is the only figure that varies by neighbourhood in this data, so it carries "
        "the comparison. Not every neighbourhood has sales in every year; filter out thin data where it matters.",
    )

    section("Most and least expensive", "Q4. Average sale price per square foot over the years with sales.")
    a, b, c = st.columns(3)
    order = a.segmented_control("Show", ["Most expensive", "Most affordable"], default="Most expensive",
                                key="order", label_visibility="collapsed") or "Most expensive"
    k = b.slider("How many", 5, 25, 10, key="k")
    min_years = c.slider("Only with at least this many years of data", 1, 7, 5, key="miny")
    r = nb[nb["years"] >= min_years].sort_values("price", ascending=order == "Most affordable").head(k)
    chart(charts.bars(r["neighborhood"].values, r["price"].values, horizontal=True,
                      customdata=r[["years", "first_year", "last_year"]].values,
                      hover="<b>%{y}</b><br>$%{x:,.0f} per sq ft<br>%{customdata[0]} years of data "
                            "(%{customdata[1]}-%{customdata[2]})",
                      xtitle="Average price per sq ft ($)").update_xaxes(tickprefix="$"))
    thin = nb[nb["years"] <= 2]
    insight(f"With the filter at 1 year, neighbourhoods like Merced Heights or Westwood Park jump near the top on "
            f"just two or three sales years. {len(thin)} neighbourhoods have two years of data or fewer; the default "
            "filter of 5 years keeps the ranking trustworthy.")

    section("Price growth, 2010 to 2015", "Change in price per sq ft for neighbourhoods with sales in both years.")
    both = w.dropna(subset=[2010, 2015])
    g = (both[2015] / both[2010] - 1).sort_values(ascending=False)
    chart(charts.bars(g.index, g.values, horizontal=True, highlight=(g < 0).values == False,  # noqa: E712
                      customdata=both.loc[g.index, [2010, 2015]].values,
                      hover="<b>%{y}</b><br>%{x:+.0%}<br>$%{customdata[0]:,.0f} → $%{customdata[1]:,.0f}",
                      xtitle="Change in price per sq ft").update_xaxes(tickformat="+.0%"))
    insight(f"Of {len(g)} neighbourhoods, <b>{(g > 0).sum()} rose</b> and {(g < 0).sum()} fell (grey). The median "
            f"rise was {g.median():.0%}. 2015 is used as the end point because fewer neighbourhoods have 2016 sales.")
    cap("Single-year prices are averages of few sales, so big swings (such as Van Ness/Civic Center) partly "
        "reflect which properties happened to sell.")

    section("Compare neighbourhoods", "Price per sq ft over time, up to three neighbourhoods.")
    default = ["Pacific Heights", "Potrero Hill", "Bayview"]
    pick = st.multiselect("Neighbourhoods", sorted(w.index), default=default, max_selections=3, key="pick")
    if pick:
        years = [str(y) for y in w.columns]
        chart(charts.lines(years, {n: w.loc[n].round(0) for n in pick}, hover_fmt="$,.0f",
                           ytitle="Price per sq ft ($)").update_yaxes(tickprefix="$"))
        cap("Gaps in a line are years without sales in that neighbourhood.")

    footer()
