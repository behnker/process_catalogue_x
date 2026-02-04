"""
Storage provider abstraction.

Global: Cloudflare R2 (S3-compatible)
China: Alibaba OSS
"""

from src.config import settings

from .base import StorageProvider


def get_storage_provider() -> StorageProvider:
    """Factory function to get the configured storage provider."""
    provider = getattr(settings, "STORAGE_PROVIDER", "local")

    if provider == "r2":
        from .cloudflare_r2 import CloudflareR2Provider
        return CloudflareR2Provider()
    elif provider == "oss":
        from .alibaba_oss import AlibabaOSSProvider
        return AlibabaOSSProvider()
    else:
        from .local import LocalStorageProvider
        return LocalStorageProvider()


__all__ = [
    "StorageProvider",
    "get_storage_provider",
]
