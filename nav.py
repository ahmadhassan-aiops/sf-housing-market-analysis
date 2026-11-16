"""Page registry, shared by app.py and pages that link to other pages."""

import streamlit as st

from views import findings, map_view, method, neighborhoods, trends

FINDINGS = st.Page(findings.render, title="Key findings", icon=":material/insights:", url_path="findings", default=True)
TRENDS = st.Page(trends.render, title="Citywide trends", icon=":material/trending_up:", url_path="trends")
NEIGHBORHOODS = st.Page(neighborhoods.render, title="Neighbourhoods", icon=":material/location_city:", url_path="neighbourhoods")
MAP = st.Page(map_view.render, title="Map", icon=":material/map:", url_path="map")
METHOD = st.Page(method.render, title="Data & method", icon=":material/dataset:", url_path="method")

PAGES = [FINDINGS, TRENDS, NEIGHBORHOODS, MAP, METHOD]
