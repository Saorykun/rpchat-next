from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, TypedDict, NotRequired

Role = Literal["system", "user", "assistant"]

class ChatMessage(TypedDict, total=False):
    role: Role
    content: str
    # semantic fields (legacy compatible)
    kind: str
    speaker_id: str
    speaker: str

ChatHistory = list[ChatMessage]


@dataclass
class SceneState:
    # keep fields aligned with legacy SceneState (extend as needed)
    situation: str = ""
    hero_state: str = ""
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class CharacterSpec:
    id: str
    name: str
    description: str = ""
    speech_style: str = ""
    goals: str = ""
    limits: str = ""
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class RPConfig:
    # keep aligned with legacy RPConfig (add fields during migration)
    model_path: str = ""
    max_tokens: int = 256
    temperature: float = 0.7
    top_p: float = 0.95
    repeat_penalty: float = 1.05
    stop: list[str] = field(default_factory=list)
    extra: dict[str, Any] = field(default_factory=dict)
