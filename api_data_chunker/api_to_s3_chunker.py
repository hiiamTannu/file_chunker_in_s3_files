import json
import pandas as pd
import requests
import s3fs

# Configuration Settings
API_URL = "https://jsonplaceholder.typicode.com/photos"  # 5,000 sample records
BUCKET_NAME = "big-file-chunks"
RAW_S3_PATH = f"s3://{BUCKET_NAME}/raw_api_data/photos_raw.json"
CHUNK_S3_DIR = f"s3://{BUCKET_NAME}/chunked_api_data"
CHUNK_SIZE = 1000


def fetch_and_stage_raw_api():
    """Fetch JSON data from REST API and save raw payload directly to S3."""
    print(f"1. Fetching data from API: {API_URL}")
    response = requests.get(API_URL)
    response.raise_for_status()
    data = response.json()
    print(f"   Successfully fetched {len(data)} records.")

    print(f"2. Uploading raw JSON to S3: {RAW_S3_PATH}")
    fs = s3fs.S3FileSystem()
    with fs.open(RAW_S3_PATH, "w") as f:
        json.dump(data, f, indent=2)
    print("   Raw JSON staging complete.")


def process_and_chunk_s3_json():
    """Read raw JSON from S3, split into chunks, and save as JSON files in output S3 folder."""
    print(f"3. Reading raw JSON from S3: {RAW_S3_PATH}")
    df = pd.read_json(RAW_S3_PATH)

    total_records = len(df)
    print(f"   Total records loaded into DataFrame: {total_records}")

    print(
        f"4. Chunking data (Size: {CHUNK_SIZE}) and uploading to:"
        f" {CHUNK_S3_DIR}"
    )

    for i in range(0, total_records, CHUNK_SIZE):
        chunk = df.iloc[i : i + CHUNK_SIZE]
        chunk_num = (i // CHUNK_SIZE) + 1
        target_file = f"{CHUNK_S3_DIR}/chunk_{chunk_num}.json"

        # Export DataFrame chunk directly to S3 as JSON array [citing: 1.1.1, 1.2.2]
        chunk.to_json(target_file, orient="records", indent=2)
        print(f"   Uploaded: {target_file} ({len(chunk)} records)")

    print("Pipeline Execution Completed Successfully!")


if __name__ == "__main__":
    fetch_and_stage_raw_api()
    process_and_chunk_s3_json()
