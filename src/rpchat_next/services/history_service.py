from __future__ import annotations

from typing import Any
from rpchat_next.domain.models import ChatHistory, ChatMessage

# Bridge to legacy behavior first to avoid regressions
from rpchat import history_utils as legacy_history

def normalize_history(history: ChatHistory) -> ChatHistory:
    """Normalize history for UI/render.

    During migration, keep identical behavior to legacy.
    """
    return legacy_history.normalize_history(history)  # type: ignore

def ensure_prologue(history: ChatHistory, prologue: str) -> ChatHistory:
    # Implement later based on legacy invariants.
    if not history:
        return [{"role":"assistant","content":prologue,"kind":"narrator"}]
    return history
