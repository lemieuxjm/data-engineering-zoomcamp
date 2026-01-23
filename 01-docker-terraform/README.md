# Docker, posgres, pgAdmin Configuration to create three Docker containers 
# To be used with DataEngineering ZoomCamp Mod 01 Homework

# These are the instructions to reproduce the environment necessary to answer Q3 - Q6

Follow these instructions to create three Docker images that will be combined in 
one docker-compose. 

## Prerequisite

1. **Retrieve Docker Image for ingestion pipeline**: Download from [Docker Hub](https://hub.docker.com/repositories/jmlemieux)

## Setup Instructions

### 1. Start up docker-compose

```bash
docker-compose up -d
```
### 2. Start pgcli

```bash
uv run pgcli -h localhost -p 5432 -u root -d ny_taxi
```
### 3. Run query for Q3

```sql
SELECT COUNT(*) FROM green_taxi_data WHERE lpep_pickup_datetime BETWEEN '2025-11-01' AND '2025-12-01' AND trip_distance <= 1;
```

### 4. Run query for Q4

```sql
SELECT CAST(lpep_pickup_datetime AS DATE), trip_distance FROM green_taxi_data WHERE trip_distance < 100 ORDER BY trip_distance DESC;
```

### 5. Run query for Q5

```sql
SELECT z."Zone", SUM(g.total_amount) AS total_amount
 FROM green_taxi_data g
 JOIN zones z ON z."LocationID" = g."PULocationID"
 WHERE g.lpep_pickup_datetime BETWEEN '2025-11-18' AND '2025-11-19'
 GROUP BY z."Zone" ORDER BY 2 DESC;
```

### 6. Run query for Q6

```sql
SELECT z2."Zone" AS drop_off_zone, g.tip_amount
  FROM green_taxi_data g
  JOIN zones z ON z."LocationID" = g."PULocationID"
 JOIN zones z2 ON z2."LocationID" = g."DOLocationID"
 WHERE z."Zone" = 'East Harlem North'
 ORDER BY g.tip_amount DESC; 
```

### 7. Quit pgcli

```
\q
```
## Clean up

[Git Hub](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/docker-sql/11-cleanup.md)

# For Q7:

## Prerequisite

1. **Retrieve source files**: 
Download from [Git Hub](https://github.com/lemieuxjm/data-engineering-zoomcamp/tree/main/01-docker-terraform/DE%20HW%2001%20Terraform)

## Follow instructions in the README.md
at /01-docker-terraform/DE HW 01 Terraform/README.md


