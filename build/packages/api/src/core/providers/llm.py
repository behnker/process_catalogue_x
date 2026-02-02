"""
LLM provider abstraction.

Global: Anthropic Claude / OpenAI GPT
China: Alibaba Qwen / Baidu ERNIE

Provides a unified interface for text generation across providers.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import AsyncGenerator, Optional

from src.config import settings


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


class AnthropicProvider(LLMProvider):
    """
    Anthropic Claude provider (Global deployment).
    """

    def __init__(self):
        try:
            from anthropic import AsyncAnthropic
            self.client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
        except ImportError:
            raise ImportError("anthropic package required. Install with: pip install anthropic")

        self.models = [
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307",
            "claude-3-5-sonnet-20241022",
        ]

    async def generate(
        self,
        prompt: str,
        config: LLMConfig,
    ) -> LLMResponse:
        messages = [{"role": "user", "content": prompt}]

        kwargs = {
            "model": config.model,
            "max_tokens": config.max_tokens,
            "messages": messages,
        }

        if config.system_prompt:
            kwargs["system"] = config.system_prompt
        if config.temperature is not None:
            kwargs["temperature"] = config.temperature
        if config.stop_sequences:
            kwargs["stop_sequences"] = config.stop_sequences

        response = await self.client.messages.create(**kwargs)

        return LLMResponse(
            content=response.content[0].text,
            model=response.model,
            prompt_tokens=response.usage.input_tokens,
            completion_tokens=response.usage.output_tokens,
            total_tokens=response.usage.input_tokens + response.usage.output_tokens,
            finish_reason=response.stop_reason or "stop",
        )

    async def generate_stream(
        self,
        prompt: str,
        config: LLMConfig,
    ) -> AsyncGenerator[str, None]:
        messages = [{"role": "user", "content": prompt}]

        kwargs = {
            "model": config.model,
            "max_tokens": config.max_tokens,
            "messages": messages,
        }

        if config.system_prompt:
            kwargs["system"] = config.system_prompt
        if config.temperature is not None:
            kwargs["temperature"] = config.temperature

        async with self.client.messages.stream(**kwargs) as stream:
            async for text in stream.text_stream:
                yield text

    def get_available_models(self) -> list[str]:
        return self.models


class OpenAIProvider(LLMProvider):
    """
    OpenAI GPT provider (Global deployment alternative).
    """

    def __init__(self):
        try:
            from openai import AsyncOpenAI
            self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        except ImportError:
            raise ImportError("openai package required. Install with: pip install openai")

        self.models = [
            "gpt-4-turbo-preview",
            "gpt-4",
            "gpt-3.5-turbo",
        ]

    async def generate(
        self,
        prompt: str,
        config: LLMConfig,
    ) -> LLMResponse:
        messages = []
        if config.system_prompt:
            messages.append({"role": "system", "content": config.system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = await self.client.chat.completions.create(
            model=config.model,
            messages=messages,
            max_tokens=config.max_tokens,
            temperature=config.temperature,
            stop=config.stop_sequences,
        )

        choice = response.choices[0]
        return LLMResponse(
            content=choice.message.content or "",
            model=response.model,
            prompt_tokens=response.usage.prompt_tokens,
            completion_tokens=response.usage.completion_tokens,
            total_tokens=response.usage.total_tokens,
            finish_reason=choice.finish_reason or "stop",
        )

    async def generate_stream(
        self,
        prompt: str,
        config: LLMConfig,
    ) -> AsyncGenerator[str, None]:
        messages = []
        if config.system_prompt:
            messages.append({"role": "system", "content": config.system_prompt})
        messages.append({"role": "user", "content": prompt})

        stream = await self.client.chat.completions.create(
            model=config.model,
            messages=messages,
            max_tokens=config.max_tokens,
            temperature=config.temperature,
            stream=True,
        )

        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    def get_available_models(self) -> list[str]:
        return self.models


class QwenProvider(LLMProvider):
    """
    Alibaba Qwen provider (China deployment).
    Uses DashScope API.
    """

    def __init__(self):
        try:
            import dashscope
            dashscope.api_key = settings.DASHSCOPE_API_KEY
            self.dashscope = dashscope
        except ImportError:
            raise ImportError("dashscope package required. Install with: pip install dashscope")

        self.models = [
            "qwen-turbo",
            "qwen-plus",
            "qwen-max",
        ]

    async def generate(
        self,
        prompt: str,
        config: LLMConfig,
    ) -> LLMResponse:
        from dashscope import Generation

        messages = []
        if config.system_prompt:
            messages.append({"role": "system", "content": config.system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = Generation.call(
            model=config.model,
            messages=messages,
            max_tokens=config.max_tokens,
            temperature=config.temperature,
            result_format="message",
        )

        output = response.output
        usage = response.usage

        return LLMResponse(
            content=output.choices[0].message.content,
            model=config.model,
            prompt_tokens=usage.input_tokens,
            completion_tokens=usage.output_tokens,
            total_tokens=usage.total_tokens,
            finish_reason=output.choices[0].finish_reason,
        )

    async def generate_stream(
        self,
        prompt: str,
        config: LLMConfig,
    ) -> AsyncGenerator[str, None]:
        from dashscope import Generation

        messages = []
        if config.system_prompt:
            messages.append({"role": "system", "content": config.system_prompt})
        messages.append({"role": "user", "content": prompt})

        responses = Generation.call(
            model=config.model,
            messages=messages,
            max_tokens=config.max_tokens,
            temperature=config.temperature,
            result_format="message",
            stream=True,
            incremental_output=True,
        )

        for response in responses:
            if response.output and response.output.choices:
                content = response.output.choices[0].message.content
                if content:
                    yield content

    def get_available_models(self) -> list[str]:
        return self.models


class MockLLMProvider(LLMProvider):
    """
    Mock LLM provider for testing and development.
    """

    def __init__(self):
        self.models = ["mock-model"]

    async def generate(
        self,
        prompt: str,
        config: LLMConfig,
    ) -> LLMResponse:
        # Simple mock response
        response = f"[Mock Response] Received prompt with {len(prompt)} characters."

        return LLMResponse(
            content=response,
            model="mock-model",
            prompt_tokens=len(prompt) // 4,
            completion_tokens=len(response) // 4,
            total_tokens=(len(prompt) + len(response)) // 4,
            finish_reason="stop",
        )

    async def generate_stream(
        self,
        prompt: str,
        config: LLMConfig,
    ) -> AsyncGenerator[str, None]:
        response = f"[Mock Response] Received prompt with {len(prompt)} characters."
        for word in response.split():
            yield word + " "

    def get_available_models(self) -> list[str]:
        return self.models


def get_llm_provider(provider_name: Optional[str] = None) -> LLMProvider:
    """
    Factory function to get the configured LLM provider.
    """
    provider = provider_name or getattr(settings, "LLM_PROVIDER", "mock")

    if provider == "anthropic":
        return AnthropicProvider()
    elif provider == "openai":
        return OpenAIProvider()
    elif provider == "qwen":
        return QwenProvider()
    else:
        return MockLLMProvider()
