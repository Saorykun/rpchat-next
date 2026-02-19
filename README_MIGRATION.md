# RPChat Next — skeleton for architectural refactor

This repo is a *starting point* for migrating the current RPChat project into a cleaner, scalable architecture
while preserving the same external behavior and *the same prompts*.

## Goals / invariants
- Keep all user-visible functionality: chat, auto-step, regen last NPC, regen auto-player, edit past message.
- Debug must show the *actual prompt(s) sent to the model* for every action.
- Single model instance in memory (unified gateway / cache).
- Prompts remain unchanged (ported as-is from legacy rpchat/prompts.py).

## Suggested target architecture (layers)
- **domain/**: pure data models, prompt builders, rules (no I/O, no llama.cpp, no Gradio).
- **engine/**: action orchestration (Send/AutoStep/Regen/Edit), emits events for UI.
- **services/**: history operations, progress computation, parsing helpers.
- **infra/**: llama.cpp gateway, persistence adapters (sessions/events), logging.
- **ui/**: Gradio tabs renderers that are *thin* and react to engine events.

## Migration strategy (safe, step-by-step)
1. Introduce the ActionEngine and LLMGateway *inside legacy project* first (bridge mode).
2. Make **Game tab** call ActionEngine for the 5 actions, but internally engine can still call legacy functions.
3. Once stable, move legacy logic into new modules:
   - move "NPC sequential streaming" core out of `chat_ui_adapter.py` into `engine/engine.py`
   - move regen/edit core out of `core/pipeline.py` into engine
   - keep prompts identical (copy file, no edits)
4. Add a small test harness to replay button sequences.

See `docs/migration_map.md` for an exact module mapping.
