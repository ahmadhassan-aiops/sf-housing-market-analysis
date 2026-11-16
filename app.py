"""
San Francisco housing market 2010-2016: where prices and rents went, neighbourhood by neighbourhood.
An interactive presentation of Ahmad Hassan's analysis (replaces the notebook's Dash dashboard).
"""

import streamlit as st

st.set_page_config(
    page_title="San Francisco housing market | Ahmad Hassan",
    page_icon=":material/home_work:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from lib.ui import inject_css  # noqa: E402
from nav import PAGES  # noqa: E402

inject_css()
st.navigation(PAGES, position="top").run()
