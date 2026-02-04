"""
LLM provider abstraction.

Global: Anthropic Claude / OpenAI GPT
China: Alibaba Qwen / Baidu ERNIE

Provides a unified interface for text generation across providers.
"""

from typing import Optional

from src.config import settings

from .base import LLMConfig, LLMProvider, LLMResponse
from .mock import MockLLMProvider


def get_llm_provider(provider_name: Optional[str] = None) -> LLMProvider:
    """Factory function to get the configured LLM provider."""
    provider = provider_name or getattr(settings, "LLM_PROVIDER", "mock")

    if provider == "anthropic":
        from .anthropic import AnthropicProvider
        return AnthropicProvider()
    elif provider == "openai":
        from .openai import OpenAIProvider
        return OpenAIProvider()
    elif provider == "qwen":
        from .qwen import QwenProvider
        return QwenProvider()
    else:
        return MockLLMProvider()


__all__ = [
    "LLMConfig",
    "LLMProvider",
    "LLMResponse",
    "get_llm_provider",
]
