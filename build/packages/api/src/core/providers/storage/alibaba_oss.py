"""Alibaba OSS storage provider (China deployment)."""

from typing import BinaryIO, Optional

from src.config import settings

from .base import StorageProvider


class AlibabaOSSProvider(StorageProvider):
    """
    Alibaba OSS storage provider (China deployment).
    Uses oss2 SDK.
    """

    def __init__(self):
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
