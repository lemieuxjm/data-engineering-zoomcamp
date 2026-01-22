#!/usr/bin/env python
# coding: utf-8

import click
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm

@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--target-table', default='green_taxi_data', help='Target table name')

def ingest_taxi_data(pg_user, pg_pass, pg_host, pg_port, pg_db, target_table,):
    """Ingest NYC taxi data (parquet file) into PostgreSQL database."""
   
    prefix = 'https://d37ci6vzurychx.cloudfront.net/trip-data'
    url = f'{prefix}/green_tripdata_2025-11.parquet'

    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    df_taxi = pd.read_parquet(url)

    df_taxi.to_sql(name=target_table, con=engine, if_exists='replace')

    print("Data ingestion complete; beginning zones data ingestion")
    
    # Call the zones function here
    ingest_zones_data(pg_user, pg_pass, pg_host, pg_port, pg_db)
    
    print("Zones data ingestion complete")        

def ingest_zones_data(pg_user, pg_pass, pg_host, pg_port, pg_db):
    """Ingest NYC taxi zone data into PostgreSQL database."""
    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc'
    url = f'{prefix}/taxi_zone_lookup.csv'

    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    df_zones = pd.read_csv(url)
    df_zones.to_sql(name='zones', con=engine, if_exists='replace')

if __name__ == '__main__':
    print("Data ingestion beginning")
    ingest_taxi_data()
    print("Data ingestion complete")