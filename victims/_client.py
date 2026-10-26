"""Provider-agnostic LLM client for the Gaslighter harnesses.

Reads OpenCode Go / vLLM / Ollama settings from the environment, so the same
experiment can run against a local model or an API model without code changes.

Environment:
  CROWBAR_LLM_PROVIDER   ollama | openai | vllm
  CROWBAR_LLM_BASE_URL   e.g. https://opencode.ai/inference/go/openai
  CROWBAR_LLM_MODEL      e.g. deepseek-v4.1-flash
  CROWBAR_LLM_API_KEY    API key (never commit)
  CROWBAR_LLM_USER_AGENT crowbaraf/0.1
  CROWBAR_LLM_SESSION_ID stable per-conversation id for OpenCode Go
"""
from __future__ import annotations

import os
import sys

CROWBAR = os.environ.get("CROWBAR_HOME", os.path.expanduser("~/Desktop/CrowbarAF"))
if CROWBAR not in sys.path:
    sys.path.insert(0, CROWBAR)

from llm_layer import LLMClient  # noqa: E402


def make_client(model: str | None = None, num_ctx: int = 32768,
                num_predict: int = 900) -> LLMClient:
    provider = os.getenv("CROWBAR_LLM_PROVIDER", "ollama")
    base_url = os.getenv("CROWBAR_LLM_BASE_URL", "http://localhost:11434")
    model = model or os.getenv("CROWBAR_LLM_MODEL", "qwen8:latest")
    return LLMClient(
        provider=provider,
        model=model,
        base_url=base_url,
        api_key=os.getenv("CROWBAR_LLM_API_KEY"),
        num_ctx=num_ctx,
        num_predict=num_predict,
        user_agent=os.getenv("CROWBAR_LLM_USER_AGENT", "crowbaraf/0.1"),
        session_id=os.getenv("CROWBAR_LLM_SESSION_ID"),
    )
