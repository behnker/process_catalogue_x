"""Anthropic Claude provider (Global deployment)."""

from typing import AsyncGenerator

from src.config import settings

from .base import LLMConfig, LLMProvider, LLMResponse


class AnthropicProvider(LLMProvider):
    """Anthropic Claude provider (Global deployment)."""

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
