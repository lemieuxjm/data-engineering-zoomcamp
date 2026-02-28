/* @bruin

name: reports.trips_report

type: duckdb.sql

depends:
  - staging.trips

materialization:
  type: table
  strategy: time_interval
  incremental_key: pickup_date
  time_granularity: date

columns:
  - name: pickup_date
    type: date
    description: "Date of trip pickup (truncated from timestamp)"
    primary_key: true
    checks:
      - name: not_null
  - name: taxi_type
    type: string
    description: "Type of taxi (yellow or green)"
    primary_key: true
    checks:
      - name: not_null
  - name: payment_type_name
    type: string
    description: "Human-readable payment type"
    primary_key: true
    checks:
      - name: not_null
  - name: trip_count
    type: bigint
    description: "Total number of trips"
    checks:
      - name: non_negative
  - name: total_revenue
    type: double
    description: "Total revenue from all trips on this day/type/payment"
    checks:
      - name: non_negative
  - name: avg_fare
    type: double
    description: "Average fare amount"
    checks:
      - name: non_negative
  - name: avg_distance
    type: double
    description: "Average trip distance"
    checks:
      - name: non_negative

custom_checks:
  - name: aggregate_totals_non_negative
    description: "Ensures all aggregate measures are non-negative"
    query: |
      SELECT COUNT(*) AS invalid_rows
      FROM reports.trips_report
      WHERE pickup_date >= '{{ start_date }}'
        AND pickup_date < '{{ end_date }}'
        AND (trip_count < 0 OR total_revenue < 0 OR avg_fare < 0 OR avg_distance < 0)
    value: 0

@bruin */

SELECT
    CAST(pickup_datetime AS DATE) AS pickup_date,
    taxi_type,
    COALESCE(payment_type_name, 'unknown') AS payment_type_name,
    COUNT(*) AS trip_count,
    SUM(GREATEST(total_amount, 0)) AS total_revenue,
    AVG(CASE WHEN fare_amount >= 0 THEN fare_amount ELSE NULL END) AS avg_fare,
    AVG(GREATEST(trip_distance, 0)) AS avg_distance
FROM staging.trips
WHERE pickup_datetime >= '{{ start_datetime }}'
  AND pickup_datetime < '{{ end_datetime }}'
GROUP BY
    CAST(pickup_datetime AS DATE),
    taxi_type,
    payment_type_name
