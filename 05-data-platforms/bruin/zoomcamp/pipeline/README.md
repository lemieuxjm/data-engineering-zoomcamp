# Data Platforms

This README.md recaps how the NYC Taxi data pipeline was generated using Bruin as part of Module 5 work and homework.
---

## Preparation
 - Install Bruin CLI
 - Add VSCode extension
 - Configure environments and connections (.bruin.yml)
 - Configure schedule, interval, backfill start date, user defined variables (pipeline.yml)
---

## Pipeline Creation
 - Initialize Zoomcamp template
 - Create DAG by: 
    - Ingesting data from public API
    - Staging cleaned, normalized, enriched data
    - Displaying dashboards and analytics
---

## Pipeline Execution
- Validate syntax, schema, dependencies, and connections by static analysis
- Run pipeline to execute assets and create artifacts
---

## Deployment
- Review the use of the Bruin MCP to facilitate pipeline generation
- Deploy result to Bruin Cloud with GCP project and BigQuery datasets
---