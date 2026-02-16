import os
import sys
import urllib.request
import gzip
import shutil
import argparse
from concurrent.futures import ThreadPoolExecutor
from google.cloud import storage
from google.api_core.exceptions import NotFound, Forbidden
import time


# Change this to your bucket name
BUCKET_NAME = "de-camp-04"

# If you authenticated through the GCP SDK you can comment out these two lines
# CREDENTIALS_FILE = "gcs.json"
# client = storage.Client.from_service_account_json(CREDENTIALS_FILE)
# If commented initialize client with the following
client = storage.Client(project='de-camp-01')

DOWNLOAD_DIR = "."
CHUNK_SIZE = 8 * 1024 * 1024

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

bucket = client.bucket(BUCKET_NAME)


def generate_month_list(start_year, start_month, end_year, end_month):
    """
    Generate a list of (year, month) tuples between start and end dates
    """
    months = []
    current_year = start_year
    current_month = start_month
    
    while (current_year < end_year) or (current_year == end_year and current_month <= end_month):
        months.append((current_year, current_month))
        current_month += 1
        if current_month > 12:
            current_month = 1
            current_year += 1
    
    return months


def download_file(params):
    """
    Download a file given color type and year-month tuple
    params: tuple of (color, year, month)
    """
    color, year, month = params
    url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{color}_tripdata_{year}-{month:02d}.csv.gz"
    file_path = os.path.join(DOWNLOAD_DIR, f"{color}_tripdata_{year}-{month:02d}.csv.gz")

    try:
        print(f"Downloading {url}...")
        urllib.request.urlretrieve(url, file_path)
        print(f"Downloaded: {file_path}")
        return file_path
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None


def uncompress_file(gz_file_path):
    """
    Uncompress a .gz file to .csv
    Returns the path to the uncompressed CSV file
    """
    if not gz_file_path or not os.path.exists(gz_file_path):
        print(f"File does not exist: {gz_file_path}")
        return None
    
    csv_file_path = gz_file_path.replace('.gz', '')
    
    try:
        print(f"Uncompressing {gz_file_path}...")
        with gzip.open(gz_file_path, 'rb') as f_in:
            with open(csv_file_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        print(f"Uncompressed: {csv_file_path}")
        
        # Optionally remove the .gz file after successful decompression
        os.remove(gz_file_path)
        print(f"Removed compressed file: {gz_file_path}")
        
        return csv_file_path
    except Exception as e:
        print(f"Failed to uncompress {gz_file_path}: {e}")
        return None


def create_bucket(bucket_name):
    try:
        # Get bucket details
        bucket = client.get_bucket(bucket_name)

        # Check if the bucket belongs to the current project
        project_bucket_ids = [bckt.id for bckt in client.list_buckets()]
        if bucket_name in project_bucket_ids:
            print(
                f"Bucket '{bucket_name}' exists and belongs to your project. Proceeding..."
            )
        else:
            print(
                f"A bucket with the name '{bucket_name}' already exists, but it does not belong to your project."
            )
            sys.exit(1)

    except NotFound:
        # If the bucket doesn't exist, create it
        bucket = client.create_bucket(bucket_name)
        print(f"Created bucket '{bucket_name}'")
    except Forbidden:
        # If the request is forbidden, it means the bucket exists but you don't have access to see details
        print(
            f"A bucket with the name '{bucket_name}' exists, but it is not accessible. Bucket name is taken. Please try a different bucket name."
        )
        sys.exit(1)


def verify_gcs_upload(blob_name):
    return storage.Blob(bucket=bucket, name=blob_name).exists(client)


def upload_to_gcs(file_path, max_retries=3):
    blob_name = os.path.basename(file_path)
    blob = bucket.blob(blob_name)
    blob.chunk_size = CHUNK_SIZE

    create_bucket(BUCKET_NAME)

    for attempt in range(max_retries):
        try:
            print(f"Uploading {file_path} to {BUCKET_NAME} (Attempt {attempt + 1})...")
            blob.upload_from_filename(file_path)
            print(f"Uploaded: gs://{BUCKET_NAME}/{blob_name}")

            if verify_gcs_upload(blob_name):
                print(f"Verification successful for {blob_name}")
                
                # Remove the CSV file after successful upload and verification
                os.remove(file_path)
                print(f"Removed local file: {file_path}")
                
                return
            else:
                print(f"Verification failed for {blob_name}, retrying...")
        except Exception as e:
            print(f"Failed to upload {file_path} to GCS: {e}")

        time.sleep(5)

    print(f"Giving up on {file_path} after {max_retries} attempts.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download and upload NYC TLC trip data to GCS')
    parser.add_argument('--color', type=str, required=True, choices=['yellow', 'green'],
                        help='Type of taxi data: yellow or green')
    parser.add_argument('--start-year', type=int, required=True,
                        help='Start year (e.g., 2019)')
    parser.add_argument('--start-month', type=int, required=True,
                        help='Start month (1-12)')
    parser.add_argument('--end-year', type=int, required=True,
                        help='End year (e.g., 2020)')
    parser.add_argument('--end-month', type=int, required=True,
                        help='End month (1-12)')
    
    args = parser.parse_args()
    
    # Validate month ranges
    if not (1 <= args.start_month <= 12):
        print("Error: start-month must be between 1 and 12")
        sys.exit(1)
    if not (1 <= args.end_month <= 12):
        print("Error: end-month must be between 1 and 12")
        sys.exit(1)
    
    # Generate list of months to download
    months_to_download = generate_month_list(args.start_year, args.start_month, 
                                             args.end_year, args.end_month)
    
    # Create parameter tuples (color, year, month) for each download
    download_params = [(args.color, year, month) for year, month in months_to_download]
    
    print(f"Processing {args.color} taxi data from {args.start_year}-{args.start_month:02d} to {args.end_year}-{args.end_month:02d}")
    print(f"Total files to process: {len(download_params)}")
    
    create_bucket(BUCKET_NAME)

    # Download all .gz files
    with ThreadPoolExecutor(max_workers=4) as executor:
        file_paths = list(executor.map(download_file, download_params))

    # Uncompress all downloaded files
    with ThreadPoolExecutor(max_workers=4) as executor:
        csv_file_paths = list(executor.map(uncompress_file, filter(None, file_paths)))

    # Upload uncompressed CSV files to GCS
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(upload_to_gcs, filter(None, csv_file_paths))

    print("All files processed and verified.")