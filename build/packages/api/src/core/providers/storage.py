"""
Storage provider abstraction.

Global: Cloudflare R2 (S3-compatible)
China: Alibaba OSS

Both are accessed via boto3-compatible interface.
"""

from abc import ABC, abstractmethod
from io import BytesIO
from typing import BinaryIO, Optional

import boto3
from botocore.config import Config

from src.config import settings


class StorageProvider(ABC):
    """Abstract storage provider interface."""

    @abstractmethod
    async def upload_file(
        self,
        bucket: str,
        key: str,
        file: BinaryIO,
        content_type: Optional[str] = None,
    ) -> str:
        """Upload a file and return its URL."""
        pass

    @abstractmethod
    async def download_file(self, bucket: str, key: str) -> bytes:
        """Download a file and return its contents."""
        pass

    @abstractmethod
    async def delete_file(self, bucket: str, key: str) -> bool:
        """Delete a file. Returns True if successful."""
        pass

    @abstractmethod
    async def get_presigned_url(
        self,
        bucket: str,
        key: str,
        expires_in: int = 3600,
    ) -> str:
        """Get a presigned URL for temporary access."""
        pass

    @abstractmethod
    async def list_files(
        self,
        bucket: str,
        prefix: str = "",
        max_keys: int = 1000,
    ) -> list[dict]:
        """List files in a bucket with optional prefix."""
        pass


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


class AlibabaOSSProvider(StorageProvider):
    """
    Alibaba OSS storage provider (China deployment).
    Uses oss2 SDK.
    """

    def __init__(self):
        # Import oss2 only when needed (China deployment)
        try:
            import oss2
            self.oss2 = oss2
        except ImportError:
            raise ImportError("oss2 package required for Alibaba OSS. Install with: pip install oss2")

        auth = oss2.Auth(
            settings.OSS_ACCESS_KEY_ID,
            settings.OSS_SECRET_ACCESS_KEY,
        )
        self.endpoint = settings.OSS_ENDPOINT
        self.auth = auth
        self._buckets: dict = {}

    def _get_bucket(self, bucket_name: str):
        if bucket_name not in self._buckets:
            self._buckets[bucket_name] = self.oss2.Bucket(
                self.auth,
                self.endpoint,
                bucket_name,
            )
        return self._buckets[bucket_name]

    async def upload_file(
        self,
        bucket: str,
        key: str,
        file: BinaryIO,
        content_type: Optional[str] = None,
    ) -> str:
        bucket_obj = self._get_bucket(bucket)
        headers = {}
        if content_type:
            headers["Content-Type"] = content_type

        bucket_obj.put_object(key, file, headers=headers)
        return f"https://{bucket}.{self.endpoint.replace('https://', '')}/{key}"

    async def download_file(self, bucket: str, key: str) -> bytes:
        bucket_obj = self._get_bucket(bucket)
        result = bucket_obj.get_object(key)
        return result.read()

    async def delete_file(self, bucket: str, key: str) -> bool:
        try:
            bucket_obj = self._get_bucket(bucket)
            bucket_obj.delete_object(key)
            return True
        except Exception:
            return False

    async def get_presigned_url(
        self,
        bucket: str,
        key: str,
        expires_in: int = 3600,
    ) -> str:
        bucket_obj = self._get_bucket(bucket)
        return bucket_obj.sign_url("GET", key, expires_in)

    async def list_files(
        self,
        bucket: str,
        prefix: str = "",
        max_keys: int = 1000,
    ) -> list[dict]:
        bucket_obj = self._get_bucket(bucket)
        result = []
        for obj in self.oss2.ObjectIterator(bucket_obj, prefix=prefix, max_keys=max_keys):
            result.append({
                "key": obj.key,
                "size": obj.size,
                "last_modified": obj.last_modified,
            })
        return result


class LocalStorageProvider(StorageProvider):
    """
    Local filesystem storage for development.
    """

    def __init__(self):
        import os
        self.base_path = settings.LOCAL_STORAGE_PATH or "/tmp/process-catalogue-storage"
        os.makedirs(self.base_path, exist_ok=True)

    def _get_path(self, bucket: str, key: str) -> str:
        import os
        bucket_path = os.path.join(self.base_path, bucket)
        os.makedirs(bucket_path, exist_ok=True)
        return os.path.join(bucket_path, key.replace("/", os.sep))

    async def upload_file(
        self,
        bucket: str,
        key: str,
        file: BinaryIO,
        content_type: Optional[str] = None,
    ) -> str:
        import os
        path = self._get_path(bucket, key)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(file.read())
        return f"file://{path}"

    async def download_file(self, bucket: str, key: str) -> bytes:
        path = self._get_path(bucket, key)
        with open(path, "rb") as f:
            return f.read()

    async def delete_file(self, bucket: str, key: str) -> bool:
        import os
        try:
            path = self._get_path(bucket, key)
            os.remove(path)
            return True
        except Exception:
            return False

    async def get_presigned_url(
        self,
        bucket: str,
        key: str,
        expires_in: int = 3600,
    ) -> str:
        # For local dev, just return the file path
        return f"file://{self._get_path(bucket, key)}"

    async def list_files(
        self,
        bucket: str,
        prefix: str = "",
        max_keys: int = 1000,
    ) -> list[dict]:
        import os
        bucket_path = os.path.join(self.base_path, bucket)
        if not os.path.exists(bucket_path):
            return []

        result = []
        for root, _, files in os.walk(bucket_path):
            for file in files:
                full_path = os.path.join(root, file)
                key = os.path.relpath(full_path, bucket_path).replace(os.sep, "/")
                if key.startswith(prefix):
                    stat = os.stat(full_path)
                    result.append({
                        "key": key,
                        "size": stat.st_size,
                        "last_modified": stat.st_mtime,
                    })
                    if len(result) >= max_keys:
                        return result
        return result


def get_storage_provider() -> StorageProvider:
    """
    Factory function to get the configured storage provider.
    """
    provider = getattr(settings, "STORAGE_PROVIDER", "local")

    if provider == "r2":
        return CloudflareR2Provider()
    elif provider == "oss":
        return AlibabaOSSProvider()
    else:
        return LocalStorageProvider()
