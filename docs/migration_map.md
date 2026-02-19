# Migration map (legacy -> new)

## Entry
- legacy `app.py` -> keep temporarily, later replace by `src/rpchat_next/app.py` (thin UI wiring)

## UI
- legacy `rpchat/ui/*` -> `src/rpchat_next/ui/*`
  - Goal: UI only renders and sends Actions, does not call LLM directly.

## Prompts (MUST remain the same)
- legacy `rpchat/prompts.py` -> `src/rpchat_next/domain/prompts.py` (copy verbatim)

## Models
- legacy `rpchat/models.py` -> `src/rpchat_next/domain/models.py` (types + dataclasses only)

## Single LLM entrypoint
- legacy `rpchat/llm_manager.py` -> `src/rpchat_next/infra/llm_gateway.py`
  - Keep caching logic here; all model calls go through gateway.

## Engine (new)
- new `src/rpchat_next/engine/actions.py` : Action dataclasses
- new `src/rpchat_next/engine/events.py`  : EngineEvent types for UI
- new `src/rpchat_next/engine/engine.py`  : ActionEngine (orchestrator)

## History / helpers
- legacy `rpchat/history_utils.py` -> `src/rpchat_next/services/history_service.py` (normalize + invariants)
- legacy `rpchat/ui/chat_render.py` -> stays UI, but should call history_service for normalization.

## Regen / edits / pipeline
- legacy `rpchat/chat_edit.py` + `rpchat/core/pipeline.py` -> migrate into ActionEngine
  - Keep behavior: regen-from-user-index, edit-like-chatgpt, regen last NPC, regen auto-player.

## Memory updater (later)
- legacy `rpchat/memory_updater.py` -> `src/rpchat_next/engine/post_steps/memory_updater.py`
  - For now, can remain legacy and called as a post-step from engine.

## Sessions / Events storage
- legacy `rpchat/storage/session_store.py` -> `src/rpchat_next/infra/storage/session_store.py`
- legacy `rpchat/events_store.py` -> `src/rpchat_next/infra/storage/events_store.py`
