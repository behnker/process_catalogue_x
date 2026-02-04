"""Cloudflare R2 storage provider (Global deployment)."""

from io import BytesIO
from typing import BinaryIO, Optional

import boto3
from botocore.config import Config

from src.config import settings

from .base import StorageProvider


class CloudflareR2Provider(StorageProvider):
    """
    Cloudflare R2 storage provider (Global deployment).
    S3-compatible API.
    """

    def __init__(self):
        self.client = boto3.client(
            "s3",
            endpoint_url=settings.R2_ENDPOINT_URL,
            aws_access_key_id=settings.R2_ACCESS_KEY_ID,
            aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
            config=Config(
                signature_version="s3v4",
                s3={"addressing_style": "path"},
            ),
        )
        self.public_url_base = settings.R2_PUBLIC_URL

    async def upload_file(
        self,
        bucket: str,
        key: str,
        file: BinaryIO,
        content_type: Optional[str] = None,
    ) -> str:
        extra_args = {}
        if content_type:
            extra_args["ContentType"] = content_type

        self.client.upload_fileobj(file, bucket, key, ExtraArgs=extra_args)
        return f"{self.public_url_base}/{bucket}/{key}"

    async def download_file(self, bucket: str, key: str) -> bytes:
        buffer = BytesIO()
        self.client.download_fileobj(bucket, key, buffer)
        buffer.seek(0)
        return buffer.read()

    async def delete_file(self, bucket: str, key: str) -> bool:
        try:
            self.client.delete_object(Bucket=bucket, Key=key)
            return True
        except Exception:
            return False

    async def get_presigned_url(
        self,
        bucket: str,
        key: str,
        expires_in: int = 3600,
    ) -> str:
        return self.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=expires_in,
        )

    async def list_files(
        self,
        bucket: str,
        prefix: str = "",
        max_keys: int = 1000,
    ) -> list[dict]:
        response = self.client.list_objects_v2(
            Bucket=bucket,
            Prefix=prefix,
            MaxKeys=max_keys,
        )
        return [
            {
                "key": obj["Key"],
                "size": obj["Size"],
                "last_modified": obj["LastModified"],
            }
            for obj in response.get("Contents", [])
        ]
