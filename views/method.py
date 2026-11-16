"""Data & method: sources, cleaning decisions, what the data can and cannot answer."""

import pandas as pd
import streamlit as st

from lib import data
from lib.site import NOTEBOOK_URL
from lib.ui import footer, header, md, section


def render() -> None:
    m = data.meta()

    header(
        "Data & method",
        "How the analysis was done",
        "The data, the cleaning decisions and what the data can and cannot answer. The full Python work, "
        f'including the original Dash dashboard, is in the <a href="{NOTEBOOK_URL}" target="_blank">original notebook</a>.',
    )

    section("The data")
    md(f"Two files. A census summary with **{m['raw_shape'][0]} rows** (one per neighbourhood and year, "
       f"{m['years'][0]}-{m['years'][1]}) and a list of {m['neighborhoods']} neighbourhood coordinates. The analysis "
       "follows the first three CRISP-DM stages: business understanding, data understanding, data preparation.")
    st.table(pd.DataFrame([
        ("year", "Year of the record"),
        ("neighborhood", "San Francisco neighbourhood"),
        ("sale_price_sqr_foot", "Average sale price per square foot (varies by neighbourhood)"),
        ("housing_units", "Number of housing units (one citywide value per year)"),
        ("gross_rent", "Average monthly gross rent (one citywide value per year)"),
    ], columns=["Column", "Meaning"]), hide_index=True, border="horizontal")
    with st.expander("Look at the raw data (50 random rows)"):
        st.dataframe(data.table("sample_census"), hide_index=True, height=320)

    section("Cleaning decisions")
    st.table(pd.DataFrame([
        ("Missing prices", f"{m['missing_price_rows']} rows without a sale price", "Dropped (too few to matter)"),
        ("Neighbourhood names", f"{m['names_with_trailing_space']} names had a trailing space "
         "(\"Downtown \"), so they did not match the coordinates file", "Spaces removed"),
        ("Joining coordinates", "The notebook placed the two tables side by side by row position",
         "Joined by neighbourhood name, so a missing or extra neighbourhood can never shift the rows. (On this data "
         "the positional join happened to line up.)"),
        ("Outliers", "Some very high prices (up to $2,259 per sq ft)", "Kept: they are real sales, and the median is "
         "shown next to the mean"),
        ("Duplicates", f"{m['duplicates']} in this version of the file", "Removed if present"),
    ], columns=["Item", "What was found", "How it was handled"]), hide_index=True, border="horizontal")

    section("What this data can't answer")
    md("- **Rent by neighbourhood.** Gross rent and housing units are a single citywide number per year, repeated "
       "on every row, so rent yields can't be compared between neighbourhoods.\n"
       "- **Reliable prices for thin neighbourhoods.** Some neighbourhoods have sales in only one or two years; "
       "their averages depend on which properties happened to sell.\n"
       f"- **Exact supply.** Housing units rise by exactly {m['units_step'][0]:,.0f} every year, which looks "
       "interpolated rather than counted.\n"
       "- **Precise locations.** Coordinates are approximate centres, and a few neighbourhoods share one point.\n"
       "- **After 2016.** The data ends in 2016; the market has changed since.")

    section("How this app is built")
    md("Python, pandas and Plotly in a Streamlit app; the map uses Plotly's MapLibre maps with CARTO tiles (no API "
       "key). The notebook's Dash dashboard (tabs for units, rent, prices and the map) is replaced by these pages. "
       f"`build_data.py` cleans the CSVs once into Parquet files that ship with the app. Data built on {m['built']}.")

    footer()
