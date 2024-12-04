from abc import ABC, abstractmethod
import os
import openai
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletion,
)

import ollama
from ollama import AsyncClient


# from anthropic import Anthropic
# import google.generativeai as genai
# from google.generativeai.types import HarmCategory, HarmBlockThreshold
# from fireworks.client import Fireworks, AsyncFireworks

from dotenv import load_dotenv, find_dotenv
from typing import List, Dict, Tuple

from time import time

_ = load_dotenv(find_dotenv())  # read local .env file

openai.api_key = os.getenv("OPENAI_API_KEY")
default_model = "gpt-4o-mini"

load_dotenv()


def get_llm_agent_class(model: str):
    if "gpt" in model:
        return OpenAIAgent
    elif "llama" in model or "ollama" in model:
        print("***OLLAMA***")
        return OllamaAgent

    # elif "claude" in model:
    #     return AnthropicAgent
    # elif "gemini" in model:
    #     return GeminiAgent
    # elif "accounts/fireworks" in model:
    #     return FireworksAgent
    else:
        raise NotImplementedError(f"Agent class not found for {model}")


def print_completion_timing(timings: List[Tuple[str, float]], chunk_count: int):
    """
    Print a detailed breakdown of completion timings.

    Args:
    timings (List[Tuple[str, float]]): A list of tuples, each containing a step name and its end time.
    """
    total_time = timings[-1][1] - timings[0][1]
    print("Completion time breakdown:")
    print(f"  Total time: {total_time:.2f}s")
    print(f"  Total chunks: {chunk_count}")

    for i in range(1, len(timings)):
        step_name, end_time = timings[i]
        start_time = timings[i - 1][1]
        step_time = end_time - start_time
        percentage = (step_time / total_time) * 100
        print(f"  {i}. {step_name}: {step_time:.2f}s ({percentage:.1f}%)")


class LLMAgent(ABC):
    """
    Abstract base class for language models.

    This class defines the common interface for interacting with different language models.
    Concrete implementations should be created for specific models.
    """

    def __init__(self, temperature: float = 0.0, max_tokens: int = 2048):
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.default_outputs = "Sorry, I can not satisfy that request."

    @abstractmethod
    def _completions(self, messages) -> str:
        raise NotImplementedError

    @abstractmethod
    async def _async_completions(self, messages) -> str:
        raise NotImplementedError

    async def _completions_stream(self, messages: List[Dict]) -> str:
        raise NotImplementedError

    async def completions_stream(self, messages: List[Dict]) -> str:
        try:
            response = await self._completions_stream(messages)
            return response
        except Exception as e:
            print(f"Exception for [PENDING] ,self.model", str(e))
            return self.default_outputs

    def completions(self, messages: List[Dict]) -> str:
        try:
            response = self._completions(messages)
            return response
        except Exception as e:
            print(f"Exception for PENDING ,self.model", str(e))
            return self.default_outputs

    async def async_completions(self, messages: List[Dict]) -> str:
        try:
            response = await self._async_completions(messages)
            return response
        except Exception as e:
            print(f"Exception for PENDING ,self.model", str(e))
            return self.default_outputs


class OpenAIAgent(LLMAgent):
    def __init__(
        self,
        temperature: float = 0.0,
        max_tokens: int = 2048,
        model: str = default_model,
    ):
        super().__init__(temperature, max_tokens)
        self.model = model
        openai_api_key = os.getenv("OPENAI_API_KEY")
        self.client = openai.OpenAI(api_key=openai_api_key)
        self.async_client = openai.AsyncOpenAI(api_key=openai_api_key)

    def _completions(
        self,
        messages: list[ChatCompletionMessageParam] = [
            ChatCompletionUserMessageParam(role="user", content="some test message")
        ],
    ) -> str:
        response: ChatCompletion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        final_response: str | None = response.choices[0].message.content
        if final_response is None:
            final_response = self.default_outputs
        return final_response

    async def _async_completions(
        self,
        messages: list[ChatCompletionMessageParam] = [
            ChatCompletionUserMessageParam(role="user", content="some test message")
        ],
    ) -> str:
        response: ChatCompletion = await self.async_client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        final_response: str | None = response.choices[0].message.content

        if final_response is None:
            final_response = self.default_outputs
        return final_response

    async def _completions_stream(self, messages: List):
        # messages = self.system + messages
        timings = [("Start| completions_stream", time())]
        stream = self.client.chat.completions.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=messages,
            stream=True,
        )
        timings.append(("Initial chunk", time()))
        chunks_count = 0
        for chunk in stream:
            if (text := chunk.choices[0].delta.content) is not None:
                chunks_count += 1
                yield text

        timings.append(("End chunk", time()))
        print_completion_timing(timings, chunks_count)


class OllamaAgent(LLMAgent):
    def __init__(
        self,
        temperature: float = 0.0,
        max_tokens: int = 2048,
        model: str = "llama3",  # Default Ollama model
    ):
        super().__init__(temperature, max_tokens)
        self.model = model
        self.client = ollama.Client()
        self.async_client = AsyncClient()
        print("Using llama3!!")

    def _completions(
        self,
        messages: List[Dict] = [{"role": "user", "content": "some test message"}],
    ) -> str:
        try:
            response = self.client.chat(
                model=self.model,
                messages=messages,
                options={
                    "temperature": self.temperature,
                    "num_predict": self.max_tokens,
                },
            )
            return response["message"]["content"]
        except Exception as e:
            print(f"Ollama completion error: {e}")
            return self.default_outputs

    async def _async_completions(
        self,
        messages: List[Dict] = [{"role": "user", "content": "some test message"}],
    ) -> str:
        try:
            response = await self.async_client.chat(
                model=self.model,
                messages=messages,
                options={
                    "temperature": self.temperature,
                    "num_predict": self.max_tokens,
                },
            )
            return response["message"]["content"]
        except Exception as e:
            print(f"Ollama async completion error: {e}")
            return self.default_outputs

    async def _completions_stream(self, messages: List[Dict]):
        timings = [("Start| completions_stream", time())]
        chunks_count = 0
        full_response = ""

        # Use a generator function for streaming
        async def stream_generator():
            nonlocal chunks_count
            async for part in await self.async_client.chat(
                model=self.model,
                messages=messages,
                stream=True,
                options={
                    "temperature": self.temperature,
                    "num_predict": self.max_tokens,
                },
            ):
                if part.get("done", False):
                    break

                if "message" in part and "content" in part["message"]:
                    chunk = part["message"]["content"]
                    chunks_count += 1
                    yield chunk

        # Iterate through the generator
        async for chunk in stream_generator():
            yield chunk

        timings.append(("End chunk", time()))
        print_completion_timing(timings, chunks_count)
