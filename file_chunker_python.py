import pandas as pd

input_path = "s3://big-file-chunks/input_files/annual-enterprise-survey-2025-financial-year-provisional-size-bands.csv"
output_dir = "s3://big-file-chunks/output_files"

print(f"Reading from: {input_path}")

# Reads input directly from S3 in 5000 row chunks and uploads to output directory
for i, chunk in enumerate(pd.read_csv(input_path, chunksize=5000, dtype=str)):
    target_file = f"{output_dir}/chunk_{i + 1}.csv"
    chunk.to_csv(target_file, index=False)
    print(f"Uploaded: {target_file}")

print("Done!")
