import os
import boto3

def get_s3_client():
    return boto3.client("s3", region_name=os.getenv("AWS_REGION", "ap-south-1"))

def upload_file(file_path, key):
    bucket = os.getenv("AWS_S3_BUCKET")
    if not bucket:
        raise RuntimeError("Set AWS_S3_BUCKET in environment before uploading.")
    get_s3_client().upload_file(file_path, bucket, key)
    return f"s3://{bucket}/{key}"
