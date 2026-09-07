import os
import uuid
import hashlib
from datetime import datetime, timedelta

import boto3
from botocore.exceptions import ClientError


def get_s3_client():
    """Create S3 client from environment variables"""
    return boto3.client(
        "s3",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )


def upload_file_local_to_s3(local_path, s3_key):
    """Upload a local file to S3 bucket"""
    s3 = get_s3_client()
    bucket = os.getenv("AWS_S3_BUCKET")

    try:
        s3.upload_file(Filename=local_path, Bucket=bucket, Key=s3_key)
        return True
    except ClientError as e:
        print(f"S3 upload error: {e}")
        return False


def upload_file_bytes_to_s3(file_bytes, s3_key, content_type="audio/wav"):
    """Upload bytes to S3 bucket"""
    s3 = get_s3_client()
    bucket = os.getenv("AWS_S3_BUCKET")

    try:
        s3.put_object(
            Bucket=bucket,
            Key=s3_key,
            Body=file_bytes,
            ContentType=content_type,
        )
        return True
    except ClientError as e:
        print(f"S3 upload error: {e}")
        return False


def generate_presigned_url(s3_key, expiration_hours=24):
    """Generate a presigned URL for file access"""
    s3 = get_s3_client()
    bucket = os.getenv("AWS_S3_BUCKET")

    try:
        url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": s3_key},
            ExpiresIn=expiration_hours * 3600,
        )
        return url
    except ClientError as e:
        print(f"Presigned URL error: {e}")
        return None


def delete_from_s3(s3_key):
    """Delete a file from S3 bucket"""
    s3 = get_s3_client()
    bucket = os.getenv("AWS_S3_BUCKET")

    try:
        s3.delete_object(Bucket=bucket, Key=s3_key)
        return True
    except ClientError as e:
        print(f"S3 delete error: {e}")
        return False


def get_s3_file_size(s3_key):
    """Get file size from S3"""
    s3 = get_s3_client()
    bucket = os.getenv("AWS_S3_BUCKET")

    try:
        response = s3.head_object(Bucket=bucket, Key=s3_key)
        return response["ContentLength"]
    except ClientError as e:
        print(f"S3 head error: {e}")
        return None