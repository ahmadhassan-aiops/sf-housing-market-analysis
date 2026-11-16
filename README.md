# San Francisco housing, 2010-2016: where should a rental investor look?

An interactive presentation of an exploratory data analysis by **Ahmad Hassan** (AI Engineer), replacing the
notebook's Dash dashboard. Seven years of San Francisco census figures: sale price per square foot by
neighbourhood, citywide housing units and gross rent.

- **Key findings**: rents tripled while prices rose about 90% and supply barely moved; what it means for investors.
- **Citywide trends**: rent, prices and housing units, indexed and in absolute terms.
- **Neighbourhoods**: ranking with a data-quality filter, price growth 2010-2015, compare up to three.
- **Map**: price per square foot by neighbourhood, per year.
- **Data & method**: cleaning decisions and what the data can't answer.

Notebook (updated with the corrections described in the app): [AIOPS-Portfolio-Projects / San Francisco housing rental analysis](https://github.com/ahmadhassan-aiops/AIOPS-Portfolio-Projects/tree/main/1.%20Data-analysis-with-python-Projects/San%20Francisco%20housing%20rental%20analysis)

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Rebuild the data: `python build_data.py "path/to/San Francisco housing rental analysis"`.

Structure: `app.py` (entry), `nav.py` (pages), `views/` (one module per page), `lib/` (data loading, charts, UI),
`build_data.py` (CSVs to Parquet), `data/` (prepared data shipped with the app), `Dockerfile` (port 7860).
Map tiles © CARTO, © OpenStreetMap contributors.
