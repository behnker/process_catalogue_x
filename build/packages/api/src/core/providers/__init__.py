"""
Provider abstractions for Global and China deployments.

Blueprint Environment Parity Rules:
- Infrastructure abstraction: Storage, auth, cache, and LLM access go through
  service interfaces - never call Cloudflare R2 or Alibaba OSS directly.
- Provider adapters live in this directory. Services depend on interfaces,
  not implementations.

Global Stack:
- Storage: Cloudflare R2
- LLM: Anthropic Claude / OpenAI
- Cache: Upstash Redis

China Stack:
- Storage: Alibaba OSS
- LLM: Alibaba Qwen / Baidu ERNIE
- Cache: Alibaba Redis
"""

from src.core.providers.storage import StorageProvider, get_storage_provider
from src.core.providers.llm import LLMProvider, get_llm_provider
from src.core.providers.cache import CacheProvider, get_cache_provider

__all__ = [
    "StorageProvider",
    "get_storage_provider",
    "LLMProvider",
    "get_llm_provider",
    "CacheProvider",
    "get_cache_provider",
]
