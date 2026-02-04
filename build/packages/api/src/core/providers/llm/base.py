"""LLM provider base classes and types."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import AsyncGenerator, Optional


@dataclass
class LLMResponse:
    """Standardized LLM response."""
    content: str
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    finish_reason: str


@dataclass
class LLMConfig:
    """LLM request configuration."""
    model: str
    temperature: float = 0.7
    max_tokens: int = 4000
    system_prompt: Optional[str] = None
    stop_sequences: Optional[list[str]] = None


class LLMProvider(ABC):
    """Abstract LLM provider interface."""

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        config: LLMConfig,
    ) -> LLMResponse:
        """Generate a completion for the given prompt."""
        pass

    @abstractmethod
    async def generate_stream(
        self,
        prompt: str,
        config: LLMConfig,
    ) -> AsyncGenerator[str, None]:
        """Stream a completion for the given prompt."""
        pass

    @abstractmethod
    def get_available_models(self) -> list[str]:
        """Return list of available model IDs."""
        pass
