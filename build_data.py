"""
Offline build step: the two SF CSVs -> data/*.parquet + data/meta.json.

    python build_data.py "W:/Portfolio Projects/1. Data-analysis-with-python-Projects/San Francisco housing rental analysis"

Cleaning: trailing spaces removed from neighbourhood names (4 names had them); the 5 rows without a sale price
dropped; duplicates dropped; neighbourhood averages joined to coordinates BY NAME (not by row position).
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

import pandas as pd

DEFAULT_RAW = Path("W:/Portfolio Projects/1. Data-analysis-with-python-Projects/San Francisco housing rental analysis")
OUT = Path(__file__).parent / "data"


def main(raw: Path) -> None:
    OUT.mkdir(exist_ok=True)
    d = pd.read_csv(raw / "sfo_neighborhoods_census_data.csv")
    coords = pd.read_csv(raw / "neighborhoods_coordinates.csv").rename(
        columns={"Neighborhood": "neighborhood", "Lat": "lat", "Lon": "lon"})
    d.sample(50, random_state=7).to_parquet(OUT / "sample_census.parquet", index=False)
    raw_shape = list(d.shape)

    spaced = int((d["neighborhood"] != d["neighborhood"].str.strip()).groupby(d["neighborhood"].str.strip()).any().sum())
    d["neighborhood"] = d["neighborhood"].str.strip()
    coords["neighborhood"] = coords["neighborhood"].str.strip()
    missing = int(d["sale_price_sqr_foot"].isna().sum())
    d = d.dropna(subset=["sale_price_sqr_foot"])
    dups = int(d.duplicated().sum())
    d = d.drop_duplicates().reset_index(drop=True)
    d.to_parquet(OUT / "census.parquet", index=False)

    nb = (d.groupby("neighborhood")
          .agg(price=("sale_price_sqr_foot", "mean"), years=("year", "nunique"),
               first_year=("year", "min"), last_year=("year", "max"))
          .reset_index())
    nb = coords.merge(nb, on="neighborhood", how="left", validate="one_to_one")
    nb.to_parquet(OUT / "neighborhoods.parquet", index=False)

    city = d.groupby("year").agg(units=("housing_units", "first"), rent=("gross_rent", "first"),
                                 price_mean=("sale_price_sqr_foot", "mean"),
                                 price_median=("sale_price_sqr_foot", "median"),
                                 neighborhoods=("neighborhood", "nunique")).reset_index()
    city.to_parquet(OUT / "city.parquet", index=False)

    meta = {
        "built": date.today().isoformat(),
        "raw_shape": raw_shape,
        "rows": int(len(d)),
        "neighborhoods": int(d["neighborhood"].nunique()),
        "years": [int(d["year"].min()), int(d["year"].max())],
        "names_with_trailing_space": spaced,
        "missing_price_rows": missing,
        "duplicates": dups,
        "citywide_constant_per_year": bool(d.groupby("year")[["housing_units", "gross_rent"]].nunique().eq(1).all().all()),
        "units_step": sorted(city["units"].diff().dropna().unique().tolist()),
        "coords_without_data": int(nb["price"].isna().sum()),
    }
    (OUT / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_RAW)
