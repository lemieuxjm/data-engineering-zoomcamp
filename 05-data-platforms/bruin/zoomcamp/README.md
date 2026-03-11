# Module 5: Data Platforms Using Bruin

This README.md recaps how a Bruin pipeline was built as part of Module 5 work and homework.
---

#### Preparation
 - Install Bruin CLI
 - Add VSCode extension
 - Configure environments and connections (.bruin.yml)
 - Configure schedule, interval, backfill start date, user defined variables (pipeline.yml)
---

#### Pipeline Creation
 - Initialize Zoomcamp template
 - Create DAG by: 
    - Ingesting data from public API
    - Staging cleaned, normalized, enriched data
    - Displaying dashboards and analytics
---

##### Pipeline Execution
- Validate syntax, schema, dependencies, and connections by static analysis
- Run pipeline to execute assets and create artifacts
---

#### Deployment
- Review the use of the Bruin MCP to facilitate pipeline generation
- Deploy result to Bruin Cloud with GCP project and BigQuery datasets
---

#### Project Structure
```text
zoomcamp/										# bruin project folder
    ├── miscellaneous/							# miscellaneous folder
    │   └── OriginalREADME.md					# copy of original README.md; can be ignored
    ├── pipeline/								# bruin pipeline folder
    │   ├── assets/								# pipeline assets folder
    │   │   ├── ingestion/						# folder for assets that ingest data in raw format
    │   │   │   ├── __pycache__	/				# cache folder
   	│   │   │   │   └── trips.cpython-311.pyc	# cache file
    │   │   │   ├── payment_lookup.asset.yml	# asset file for payment lookup data
    │   │   │   ├── payment_lookup.csv			# source file for payment_lookup data
    │   │   │   ├── requirements.txt			# identifies and installs dependencies for the pipeline 
    │   │   │   └── trips.py					# asset file for Python for ingesting trips data
    │   │   ├── reports/						# folder for assets related to report creation
    │   │   │   └── trips_report.sql			# asset file for SQL for trips_report
    │   │   └── staging/						# folder for assets to preprocess, clean, transform data
    │   │       └── trips.sql					# asset file for SQL needed in staging environment for trips
    │   └── pipeline.yml						# pipeline definition file, ids name, schedule, connection info, pipeline variables
    ├── .bruin.yml								# project file, ids environments and connections; always added to .gitignore
    └── README.md								# this file
```

#### Homework
- Question 1: In a Bruin project, what are the required files/directories?
  - Answer: .bruin.yml and pipeline/ with pipeline.yml and assets/
- Question 2: Identify the best incremental strategy for processing a specific interval period by deleting and inserting data?
  - Answer: time-interval
- Question 3: How do you override variables set in pipeline.yml?
  - Answer: bruin run --var 'taxi_types=["yellow"]'
- Question 4: What is the command to run an asset and all downstream assets?
  - Answer: bruin run ingestion/trips.py --downstream
- Question 5: What quality checks should be added to an asset defintion to ensure pickup_datetime has no NULLs?
  - Answer: name: not_null
- Question 6: What command is used to visualize a pipeline?
  - Answer: bruin lineage
- Question 7: What flag is used to create a table from scratch?
  - Answer: --full-refresh
