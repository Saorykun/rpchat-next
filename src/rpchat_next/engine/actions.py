from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Action:
    pass

@dataclass(frozen=True)
class SendUser(Action):
    text: str

@dataclass(frozen=True)
class AutoStep(Action):
    pass

@dataclass(frozen=True)
class RegenAutoPlayer(Action):
    pass

@dataclass(frozen=True)
class RegenLastNpc(Action):
    pass

@dataclass(frozen=True)
class EditUserMessage(Action):
    user_index: int
    new_text: str
