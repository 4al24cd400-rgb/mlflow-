import os
import boto3
from config import (
    AWS_ACCESS_KEY,
    AWS_SECRET_KEY,
    AWS_REGION,
    BUCKET_NAME,
)

s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION,
)

LOCAL_FOLDER = "registered_model"


def download_folder():
    os.makedirs(LOCAL_FOLDER, exist_ok=True)

    response = s3.list_objects_v2(
        Bucket=BUCKET_NAME,
        Prefix="registered_model/"
    )

    if "Contents" not in response:
        print("No model found in S3.")
        return

    for obj in response["Contents"]:
        key = obj["Key"]

        if key.endswith("/"):
            continue

        local_file = key

        os.makedirs(os.path.dirname(local_file), exist_ok=True)

        print(f"Downloading {key}")

        s3.download_file(
            BUCKET_NAME,
            key,
            local_file
        )

    print("✅ Model downloaded successfully!")