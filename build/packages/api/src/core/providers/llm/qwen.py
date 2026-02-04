"""Alibaba Qwen provider (China deployment)."""

from typing import AsyncGenerator

from src.config import settings

from .base import LLMConfig, LLMProvider, LLMResponse


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
