"""OpenAI GPT provider (Global deployment alternative)."""

from typing import AsyncGenerator

from src.config import settings

from .base import LLMConfig, LLMProvider, LLMResponse


class OpenAIProvider(LLMProvider):
    """OpenAI GPT provider (Global deployment alternative)."""

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
