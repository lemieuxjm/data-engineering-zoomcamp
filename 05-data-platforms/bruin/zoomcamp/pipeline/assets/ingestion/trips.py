"""@bruin

name: ingestion.trips

type: python

image: python:3.11

connection: duckdb-default

materialization:
  type: table
  strategy: append

columns:
  - name: taxi_type
    type: string
    description: "Type of taxi (yellow or green)"
    checks:
      - name: not_null
  - name: extracted_at
    type: timestamp
    description: "Timestamp when the record was extracted"
    checks:
      - name: not_null

@bruin"""

import os
import json
import io
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

import pandas as pd
import requests


BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/"


def get_months_in_range(start_date: date, end_date: date) -> list[tuple[int, int]]:
    """Return list of (year, month) tuples covering [start_date, end_date)."""
    months = []
    current = date(start_date.year, start_date.month, 1)
    end = date(end_date.year, end_date.month, 1)
    while current <= end:
        months.append((current.year, current.month))
        current += relativedelta(months=1)
    return months


def fetch_parquet(taxi_type: str, year: int, month: int) -> pd.DataFrame | None:
    url = f"{BASE_URL}{taxi_type}_tripdata_{year}-{month:02d}.parquet"
    print(f"Fetching: {url}")
    response = requests.get(url, timeout=120)
    if response.status_code == 404:
        print(f"  Not found (404), skipping.")
        return None
    response.raise_for_status()
    return pd.read_parquet(io.BytesIO(response.content))


def normalize_columns(df: pd.DataFrame, taxi_type: str) -> pd.DataFrame:
    """Rename taxi-type-specific columns to a unified schema."""
    col_map = {}
    # Yellow taxi uses tpep_, green uses lpep_
    for prefix in ("tpep_", "lpep_"):
        if f"{prefix}pickup_datetime" in df.columns:
            col_map[f"{prefix}pickup_datetime"] = "pickup_datetime"
        if f"{prefix}dropoff_datetime" in df.columns:
            col_map[f"{prefix}dropoff_datetime"] = "dropoff_datetime"
    if col_map:
        df = df.rename(columns=col_map)
    df["taxi_type"] = taxi_type
    df["extracted_at"] = datetime.utcnow()
    return df


def materialize():
    start_date = date.fromisoformat(os.environ["BRUIN_START_DATE"])
    end_date = date.fromisoformat(os.environ["BRUIN_END_DATE"])

    bruin_vars = json.loads(os.environ.get("BRUIN_VARS", "{}"))
    taxi_types = bruin_vars.get("taxi_types", ["yellow", "green"])

    months = get_months_in_range(start_date, end_date)
    frames = []

    for taxi_type in taxi_types:
        for year, month in months:
            df = fetch_parquet(taxi_type, year, month)
            if df is not None and not df.empty:
                df = normalize_columns(df, taxi_type)
                frames.append(df)

    if not frames:
        print("No data fetched for the given date range and taxi types.")
        return pd.DataFrame()

    result = pd.concat(frames, ignore_index=True)
    print(f"Total rows fetched: {len(result)}")
    return result


