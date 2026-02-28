/* @bruin

name: staging.trips

type: duckdb.sql

depends:
  - ingestion.trips
  - ingestion.payment_lookup

materialization:
  type: table
  strategy: time_interval
  incremental_key: pickup_datetime
  time_granularity: timestamp

columns:
  - name: trip_id
    type: bigint
    description: "Surrogate row number used as a deduplication key within each time window"
    primary_key: true
    checks:
      - name: not_null
  - name: pickup_datetime
    type: timestamp
    description: "Datetime when the trip started"
    checks:
      - name: not_null
  - name: dropoff_datetime
    type: timestamp
    description: "Datetime when the trip ended"
    checks:
      - name: not_null
  - name: taxi_type
    type: string
    description: "Type of taxi (yellow or green)"
    checks:
      - name: not_null
  - name: passenger_count
    type: double
    description: "Number of passengers"
  - name: trip_distance
    type: double
    description: "Trip distance in miles"
    checks:
      - name: non_negative
  - name: fare_amount
    type: double
    description: "Fare amount in dollars"
  - name: total_amount
    type: double
    description: "Total charged amount including tips and fees"
  - name: payment_type_id
    type: integer
    description: "Numeric payment type code"
  - name: payment_type_name
    type: string
    description: "Human-readable payment type from lookup table"

custom_checks:
  - name: no_duplicate_trips_in_window
    description: "Ensures no duplicate rows exist within the processed time window"
    query: |
      SELECT COUNT(*) - COUNT(DISTINCT trip_id)
      FROM staging.trips
      WHERE pickup_datetime >= '{{ start_datetime }}'
        AND pickup_datetime < '{{ end_datetime }}'
    value: 0

@bruin */

WITH raw AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY taxi_type, pickup_datetime, dropoff_datetime, total_amount
            ORDER BY extracted_at DESC
        ) AS rn
    FROM ingestion.trips
    WHERE pickup_datetime >= '{{ start_datetime }}'
      AND pickup_datetime < '{{ end_datetime }}'
      AND pickup_datetime IS NOT NULL
      AND dropoff_datetime IS NOT NULL
      AND dropoff_datetime > pickup_datetime
),

deduped AS (
    SELECT * FROM raw WHERE rn = 1
),

enriched AS (
    SELECT
        ROW_NUMBER() OVER (ORDER BY d.pickup_datetime, d.taxi_type) AS trip_id,
        d.pickup_datetime,
        d.dropoff_datetime,
        d.taxi_type,
        d.passenger_count,
        d.trip_distance,
        d.fare_amount,
        d.total_amount,
        CAST(d.payment_type AS INTEGER)    AS payment_type_id,
        p.payment_type_name,
        d.extracted_at
    FROM deduped d
    LEFT JOIN ingestion.payment_lookup p
        ON CAST(d.payment_type AS INTEGER) = p.payment_type_id
)

SELECT * FROM enriched
