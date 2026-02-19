from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterator, Optional

# Bridge to legacy: we reuse llm_manager to ensure the exact same runtime behavior initially.
from rpchat import llm_manager

@dataclass
class LLMCallMeta:
    model_path: str
    stream: bool
    gen_params: dict[str, Any]

class LLMGateway:
    """Single entrypoint for all LLM calls.

    During migration:
    - keep caching here
    - keep all llama.cpp kwargs filtering / stop behavior exactly as legacy
    """

    def __init__(self) -> None:
        self._cache: dict[str, Any] = {}  # model_path -> LLM instance

    def get_model(self, model_path: str, *, cfg: Any = None) -> Any:
        # legacy expects a cache dict that Gradio state passes around; we centralize it here
        return llm_manager.get_llm_for_character(
            character_id="__shared__",
            llm_cache=self._cache,
            cfg=cfg,
            model_path=model_path,
        )

    def chat_completion(
        self,
        *,
        model: Any,
        messages: list[dict[str, Any]],
        stream: bool,
        **kwargs: Any,
    ):
        # delegate to legacy wrapper (filters kwargs, normalizes)
        return llm_manager.create_chat_completion(model, messages, stream=stream, **kwargs)
