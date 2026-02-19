from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Generator, Iterable, Optional

from rpchat_next.engine.actions import (
    Action, SendUser, AutoStep, RegenAutoPlayer, RegenLastNpc, EditUserMessage
)
from rpchat_next.engine.events import (
    EngineEvent, StageChanged, HistoryUpdated, PromptPreviewUpdated, ErrorEvent
)
from rpchat_next.infra.llm_gateway import LLMGateway

# Bridge to legacy behavior for v0 (safe migration)
from rpchat import chat_ui_adapter
from rpchat import chat_edit
from rpchat import core

@dataclass
class EngineState:
    # Keep these fields aligned with what UI currently stores in gr.State
    history: Any
    cfg: Any
    characters: Any
    order: Any
    llm_cache: Any
    scene_summary: Any
    scene_state: Any
    prompt_preview: str = ""
    debug_trace: Any = None
    last_auto_user_text: str = ""

class ActionEngine:
    def __init__(self, gateway: Optional[LLMGateway] = None) -> None:
        self.gateway = gateway or LLMGateway()

    def run(self, st: EngineState, action: Action) -> Generator[EngineEvent, None, EngineState]:
        """Run an action and emit events.

        v0: delegates to legacy functions (no behavioral change).
        v1+: migrate logic inside this engine and delete legacy calls.
        """
        try:
            if isinstance(action, SendUser):
                yield StageChanged("prepare", "⏳ Готовлю запрос…")
                # Delegate to legacy streaming generator
                gen = chat_ui_adapter.on_send_all_sequential(
                    history=st.history,
                    user_line=action.text,
                    cfg=st.cfg,
                    characters=st.characters,
                    order=st.order,
                    llm_cache=st.llm_cache,
                    scene_summary=st.scene_summary,
                    scene_state=st.scene_state,
                    prompt_preview_state=st.prompt_preview,
                    debug_trace=st.debug_trace,
                )
                # Legacy generator yields tuples; UI adapters should translate.
                # Here we only provide a placeholder event model; actual binding happens in UI.
                for item in gen:
                    # item typically contains updated history and UI fields; we at least pass history
                    try:
                        new_hist = item[0]
                    except Exception:
                        new_hist = st.history
                    st.history = new_hist
                    yield HistoryUpdated(st.history)
                yield StageChanged("done", "✅ Готово")
                return st

            if isinstance(action, RegenLastNpc):
                yield StageChanged("prepare", "🔄 Перегенерирую последний ответ…")
                out = chat_edit.on_regen_last(
                    history=st.history,
                    cfg=st.cfg,
                    characters=st.characters,
                    order=st.order,
                    llm_cache=st.llm_cache,
                    scene_summary=st.scene_summary,
                    scene_state=st.scene_state,
                    prompt_preview_state=st.prompt_preview,
                    debug_trace=st.debug_trace,
                )
                # out is typically a tuple with history + ui fields
                st.history = out[0] if isinstance(out, (list, tuple)) and out else st.history
                yield HistoryUpdated(st.history)
                yield StageChanged("done", "✅ Готово")
                return st

            if isinstance(action, EditUserMessage):
                yield StageChanged("prepare", "✏️ Применяю правку и пересобираю диалог…")
                out = chat_edit.apply_edit_like_chatgpt(
                    history=st.history,
                    user_index=action.user_index,
                    new_user_text=action.new_text,
                    cfg=st.cfg,
                    characters=st.characters,
                    order=st.order,
                    llm_cache=st.llm_cache,
                    scene_summary=st.scene_summary,
                    scene_state=st.scene_state,
                    prompt_preview_state=st.prompt_preview,
                    debug_trace=st.debug_trace,
                )
                st.history = out[0] if isinstance(out, (list, tuple)) and out else st.history
                yield HistoryUpdated(st.history)
                yield StageChanged("done", "✅ Готово")
                return st

            # Auto-step and regen-auto-player are migrated later;
            # keep placeholders to avoid breaking skeleton.
            if isinstance(action, AutoStep):
                yield ErrorEvent("AutoStep not wired in skeleton yet")
                return st

            if isinstance(action, RegenAutoPlayer):
                yield ErrorEvent("RegenAutoPlayer not wired in skeleton yet")
                return st

            yield ErrorEvent(f"Unknown action: {action!r}")
            return st

        except Exception as e:
            yield StageChanged("error", "⚠️ Ошибка")
            yield ErrorEvent(str(e))
            return st
