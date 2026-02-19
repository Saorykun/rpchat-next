from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal, Optional

Stage = Literal[
    "idle",
    "prepare",
    "generating_player",
    "generating_npc",
    "updating_scene",
    "updating_lore",
    "done",
    "error",
]

@dataclass(frozen=True)
class EngineEvent:
    pass

@dataclass(frozen=True)
class StageChanged(EngineEvent):
    stage: Stage
    text: str = ""

@dataclass(frozen=True)
class PromptPreviewUpdated(EngineEvent):
    preview_text: str
    meta: dict[str, Any]

@dataclass(frozen=True)
class HistoryUpdated(EngineEvent):
    history: Any  # ChatHistory, kept Any to bridge to legacy dicts during migration

@dataclass(frozen=True)
class ErrorEvent(EngineEvent):
    message: str
    details: str = ""
