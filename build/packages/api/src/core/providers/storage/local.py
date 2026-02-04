"""Local filesystem storage for development."""

import os
from typing import BinaryIO, Optional

from src.config import settings

from .base import StorageProvider


class LocalStorageProvider(StorageProvider):
    """Local filesystem storage for development."""

    def __init__(self):
        self.base_path = settings.LOCAL_STORAGE_PATH or "/tmp/process-catalogue-storage"
        os.makedirs(self.base_path, exist_ok=True)

    def _get_path(self, bucket: str, key: str) -> str:
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
        return f"file://{self._get_path(bucket, key)}"

    async def list_files(
        self,
        bucket: str,
        prefix: str = "",
        max_keys: int = 1000,
    ) -> list[dict]:
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
