# Data Warehouse and BigQuery

This README.md will provide instructions for reproducing the environment necessary to answer Module 3 homework questions.

---

## Prerequisites

### Authentication
I added the authentication key .json file to my codespace project and then ran (details changed for security):
```bash
    gcloud auth activate-service-account xxxxxx@de-camp-01.iam.gserviceaccount.com   --key-file=<name of service account json file>
```
---

### Environment
For my work, I used my github codespace. I did the following to setup my environment:
 - install Google SDK:
 ```bash
    curl https://sdk.cloud.google.com | bash
 ```
 - install libraries for GCP bucket and BigQuery:
 ```bash
    pip3 install google-cloud-storage google-cloud-bigquery
 ```
  - install Terraform:
```bash
    # Download the latest Terraform binary
    wget https://releases.hashicorp.com/terraform/1.9.8/terraform_1.9.8_linux_amd64.zip

    # Unzip it
    unzip terraform_1.9.8_linux_amd64.zip

    # Move to a directory in your PATH
    sudo mv terraform /usr/local/bin/

    # Clean up
    rm terraform_1.9.8_linux_amd64.zip

    # Verify installation
    terraform --version
 ```
 To setup the Google Bucket and BigQuery dataset, I created the following Terraform files:
  - main.tf
  - variables.tf
  - terraform.tfvars (updated with desired values)

I also created an outputs.tfvars file
```bash
# Create outputs.tf in your Terraform directory
    cat > outputs.tf << EOF
    output "bucket_name" {
        description = "The name of the GCS bucket"
        value       = var.bucket_name
    }

    output "project_id" {
        description = "The GCP project ID"
        value       = var.project_id
    }
    EOF
```
---
## To pull parquet files from source to the Google bucket:
```bash
    # One-liner to set vars and run script
    BUCKET_NAME=$(terraform output -raw bucket_name) \
    PROJECT_ID=$(terraform output -raw project_id) \
    python3 load_yellow_taxi_data.py
```

## To verify what files are present in the bucket:
```bash
    gsutil ls gs://de-camp-03-dw
```
---

### BigQuery 
 - Reference the Wk3_HW_Scripts.sql file for questions, answers and SQL queries related to Wk3 Homework.
