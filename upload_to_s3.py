import os
import boto3
from config import (
    AWS_ACCESS_KEY,
    AWS_SECRET_KEY,
    AWS_REGION,
    BUCKET_NAME,
)

# Create S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION,
)

LOCAL_FOLDER = "registered_model"

for root, dirs, files in os.walk(LOCAL_FOLDER):
    for file in files:
        local_path = os.path.join(root, file)

        # Preserve folder structure in S3
        s3_key = os.path.relpath(local_path, ".")

        print(f"Uploading {local_path} → s3://{BUCKET_NAME}/{s3_key}")

        s3.upload_file(local_path, BUCKET_NAME, s3_key)

print("\n✅ All registered model artifacts uploaded successfully!")