"""Loads the prepared data in data/ (built by build_data.py)."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st

DATA = Path(__file__).resolve().parent.parent / "data"


@st.cache_data
def meta() -> dict:
    return json.loads((DATA / "meta.json").read_text(encoding="utf-8"))


@st.cache_data
def table(name: str) -> pd.DataFrame:
    return pd.read_parquet(DATA / f"{name}.parquet")


@st.cache_data
def census() -> pd.DataFrame:
    return table("census")


@st.cache_data
def city() -> pd.DataFrame:
    return table("city")


@st.cache_data
def neighborhoods() -> pd.DataFrame:
    return table("neighborhoods")


@st.cache_data
def price_wide() -> pd.DataFrame:
    """Sale price per sq ft: one row per neighbourhood, one column per year."""
    return census().pivot(index="neighborhood", columns="year", values="sale_price_sqr_foot")
