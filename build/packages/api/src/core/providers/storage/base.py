"""Storage provider base class."""

from abc import ABC, abstractmethod
from typing import BinaryIO, Optional


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
