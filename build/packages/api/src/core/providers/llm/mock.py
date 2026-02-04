"""Mock LLM provider for testing and development."""

from typing import AsyncGenerator

from .base import LLMConfig, LLMProvider, LLMResponse


class MockLLMProvider(LLMProvider):
    """Mock LLM provider for testing and development."""

    def __init__(self):
        self.models = ["mock-model"]

    async def generate(
        self,
        prompt: str,
        config: LLMConfig,
    ) -> LLMResponse:
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
