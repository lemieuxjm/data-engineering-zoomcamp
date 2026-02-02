# Workflow Orchestration

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
> I configured Kestra to my GitHub repo via a sync_to_git flow which pulled the flows into Kestra
> [Sync flows from Git to Kestra](https://kestra.io/plugins/plugin-git/io.kestra.plugin.git.syncflows)

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

   - Look in log for answer to Q3

11. **Run** `q4_results.yaml`

   - Look in log for answer to Q4

12. **Run** `q5_results.yaml`

   - Look in log for answer to Q5

13. **When finished, shut off Kestra:**

```bash
cd 02-workflow-orchestration
docker compose down
```