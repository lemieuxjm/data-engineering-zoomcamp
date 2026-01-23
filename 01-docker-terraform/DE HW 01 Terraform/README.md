# GCP Terraform Configuration to create a GCP Storage Bucket and a BQ DataSet
# To be used with DataEngineering ZoomCamp Mod 01 HW Question 7

This Terraform configuration creates:
- A GCS bucket named `de-camp-01-terra-bucket`
- A BigQuery dataset named `de_hw_01_dataset`

## Prerequisites

1. **Install Terraform**: Download from [terraform.io](https://www.terraform.io/downloads)
2. **Install gcloud CLI**: Follow instructions at [cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install)

## Service Account

There is one service account:

### terraform-de-runner@de-camp-01.iam.gserviceaccount.com
Roles:
- BigQuery Admin
- Compute Admin
- Storage Admin

## Setup Instructions

### 1. Authenticate with GCP

```bash
# Authenticate with user account
gcloud auth application-default login

# OR authenticate with the terraform-de-runner service account
gcloud auth activate-service-account terraform-de-runner@de-camp-01.iam.gserviceaccount.com \
  --key-file=/path/to/terraform-de-runner-key.json

# Set project
gcloud config set project de-camp-01
```

### 2. Configure Variables

Copy the example file and update with your values:

```bash
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars`:
```hcl
project_id            = "de-camp-01"  # The actual project ID
region                = "us-central1"
location              = "US"
bucket_name           = "de-camp-01-terra-bucket"
dataset_id            = "de_hw_01_dataset"
service_account_email = "gcpsvc-de-camp@de-camp-01.iam.gserviceaccount.com"
```

### 3. Initialize Terraform

```bash
terraform init
```

### 4. Review the Plan

```bash
terraform plan
```

### 5. Apply the Configuration

```bash
terraform apply
```

Type `yes` when prompted to create the resources.

## Important Notes

### Bucket Naming
- GCS bucket names must be globally unique
- If `de-camp-01-terra-bucket` is taken, modify the `bucket_name` in `terraform.tfvars`
- Consider using: `de-camp-01-terra-bucket-<your-initials>` or add a random suffix

### Location Settings
- `location = "US"` is a multi-region location
- For single region, use: `location = "us-central1"`
- BigQuery dataset and GCS bucket should typically be in the same location

## Cleanup

To destroy all resources created by Terraform:

```bash
terraform destroy
```

## File Structure

```
.
├── main.tf                    # Main Terraform configuration
├── variables.tf               # Variable definitions
├── terraform.tfvars           # Variables file
└── README.md                  # This file
```

