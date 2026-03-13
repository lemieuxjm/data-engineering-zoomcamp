# Module 2: Workflow Orchestration

This README.md will provide instructions for reproducing the environment necessary to answer Module 2 homework questions.

---

## Prerequisites

For GCP
 - setup a gcp project, location, and service account
 - identify a storage bucket name

For Kestra
 - set up an .env_encoded file for the gcp service account

Clone the repository at
  [My Zoomcamp Repo](https://github.com/lemieuxjm/data-engineering-zoomcamp).

> [!NOTE]  
> I configured Kestra to my GitHub repo via a sync_to_git flow which pulled the flows into Kestra. See this reference: [Sync flows from Git to Kestra](https://kestra.io/plugins/plugin-git/io.kestra.plugin.git.syncflows)

---
## Contents
```
02-workflow-orchestration/
├── flows/						
│   ├── 06_gcp_kv.yaml					# sets GCP service account, project ID, BQ Dataset, storage bucket & location as KV Store values
│   ├── 07_gcp_setup.yaml				# Creates GCS bucket and BigQuery dataset
│   ├── 09_gcp_taxi_scheduled.yaml	 	# set up scheduled retrieval, backfill, and processing of NYC taxi data
│   ├── q3_results.yaml					# sql and answers to hw Q3
│   ├── q4_results.yaml					# sql and answers to hw Q3
│   └── q5_results.yaml					# sql and answers to hw Q3
├── images/
│   └── homework.png					# image needed for homework
├── .env_encoded
├── README.md							# this file
└── docker-compose.yml					# docker file to run container
```
---

## Instructions

1. **Open Github codespace in VSCode**

2. **In the terminal run:**

```bash
cd 02-workflow-orchestration
docker compose up -d
```

3. **Access Kestra at** [http://localhost:8080](http://localhost:8080).

4. **Set up the secret for the gcp service account** [Add Service Account as a Secret](https://kestra.io/docs/how-to-guides/google-credentials#add-service-account-as-a-secret)

5. **(Optional) Run sync-to-git flow**

5. **Verify these flows are present**

   - 06_gcp_kv
   - 07_gcp_setup
   - 09_gcp_taxi_scheduled
   - q3_results
   - q4_results
   - q5_results

6. **Edit 06_gcp_kv.yaml with your values**

7. **Run the flow for** `06_gcp_kv.yaml`

8. **Run the flow for** `07_gcp_setup.yaml`

   - Verify the dataset is present in BigQuery
   - Verify the storage bucket is present in Storage

9. **Run** `09_gcp_taxi_scheduled.yaml` with a backfill of 2019, 2020, and Jan - June 2021 data for yellow and green datasets

10. **Run** `q3_results.yaml`
    
   - The answer to this question is found by running this SQL
```sql
      SELECT SUM(count) as total_records
      FROM (
        SELECT COUNT(*) as count FROM `de-camp-01.de_hw_02_dataset.yellow_tripdata_2020_01`
          UNION ALL
        SELECT COUNT(*) as count FROM `de-camp-01.de_hw_02_dataset.yellow_tripdata_2020_02`
          UNION ALL
        SELECT COUNT(*) as count FROM `de-camp-01.de_hw_02_dataset.yellow_tripdata_2020_03`
          UNION ALL
        SELECT COUNT(*) as count FROM `de-camp-01.de_hw_02_dataset.yellow_tripdata_2020_04`
          UNION ALL
        SELECT COUNT(*) as count FROM `de-camp-01.de_hw_02_dataset.yellow_tripdata_2020_05`
          UNION ALL
        SELECT COUNT(*) as count FROM `de-camp-01.de_hw_02_dataset.yellow_tripdata_2020_06`
          UNION ALL
        SELECT COUNT(*) as count FROM `de-camp-01.de_hw_02_dataset.yellow_tripdata_2020_07`
          UNION ALL
        SELECT COUNT(*) as count FROM `de-camp-01.de_hw_02_dataset.yellow_tripdata_2020_08`
          UNION ALL
        SELECT COUNT(*) as count FROM `de-camp-01.de_hw_02_dataset.yellow_tripdata_2020_09`
          UNION ALL
        SELECT COUNT(*) as count FROM `de-camp-01.de_hw_02_dataset.yellow_tripdata_2020_10`
          UNION ALL
        SELECT COUNT(*) as count FROM `de-camp-01.de_hw_02_dataset.yellow_tripdata_2020_11`
          UNION ALL
        SELECT COUNT(*) as count FROM `de-camp-01.de_hw_02_dataset.yellow_tripdata_2020_12`
      );
```
   - This flow outputs the answer (24648499 rows) in the flow log message. Review this log message

11. **Run** `q4_results.yaml`
    
   - The answer to this question is found by running this SQL
```sql
      SELECT SUM(count) as total_records
      FROM (
        SELECT COUNT(*) as count FROM `de-camp-01.de_hw_02_dataset.green_tripdata_2020_01`
          UNION ALL
        SELECT COUNT(*) as count FROM `de-camp-01.de_hw_02_dataset.green_tripdata_2020_02`
          UNION ALL
        SELECT COUNT(*) as count FROM `de-camp-01.de_hw_02_dataset.green_tripdata_2020_03`
          UNION ALL
        SELECT COUNT(*) as count FROM `de-camp-01.de_hw_02_dataset.green_tripdata_2020_04`
          UNION ALL
        SELECT COUNT(*) as count FROM `de-camp-01.de_hw_02_dataset.green_tripdata_2020_05`
          UNION ALL
        SELECT COUNT(*) as count FROM `de-camp-01.de_hw_02_dataset.green_tripdata_2020_06`
          UNION ALL
        SELECT COUNT(*) as count FROM `de-camp-01.de_hw_02_dataset.green_tripdata_2020_07`
          UNION ALL
        SELECT COUNT(*) as count FROM `de-camp-01.de_hw_02_dataset.green_tripdata_2020_08`
          UNION ALL
        SELECT COUNT(*) as count FROM `de-camp-01.de_hw_02_dataset.green_tripdata_2020_09`
          UNION ALL
        SELECT COUNT(*) as count FROM `de-camp-01.de_hw_02_dataset.green_tripdata_2020_10`
          UNION ALL
        SELECT COUNT(*) as count FROM `de-camp-01.de_hw_02_dataset.green_tripdata_2020_11`
          UNION ALL
        SELECT COUNT(*) as count FROM `de-camp-01.de_hw_02_dataset.green_tripdata_2020_12`
      );
```
   - This flow outputs the answer (1734051 rows) in the flow log message. Review this log message

12. **Run** `q5_results.yaml`
    
   - The answer to this question is found by running this SQL
```sql
SELECT COUNT(*) as total_records FROM `de-camp-01.de_hw_02_dataset.yellow_tripdata_2021_03`;

```
   - This flow outputs the answer (1925152 rows) in the flow log message. Review this log message

13. **When finished, shut off Kestra:**

```bash
cd 02-workflow-orchestration
docker compose down

```

