# Legacy project file index (from XXX.zip)

Этот документ — «паспорт» текущего (legacy) проекта RPChat: список файлов и кратко за что они отвечают.
Нужен, чтобы при миграции ничего не потерять и сохранить весь функционал и внешнее поведение.

## Entry / runtime
- `app.py` — entrypoint Gradio: Blocks, gr.State, вкладки, CSS/JS/overlay.
- `rpchat/runtime.py` — рантайм и дефолтная модель, lazy LLM, shared-кэш.

## Models / config
- `rpchat/models.py` — dataclasses: `RPConfig`, `CharacterSpec`, `SceneState`, типы истории, сериализация SceneState, константы (`MAIN_HERO_ID`).
- `rpchat/settings.py` — небольшие настройки/константы.

## Prompts / formatting
- `rpchat/prompts.py` — все промпты и сборка системного промпта (MUST stay unchanged during migration).
- `rpchat/utils_text.py` — текстовые утилиты.
- `rpchat/history_utils.py` — нормализация истории, чистка/префиксы, подготовка текста.

## Characters / events
- `rpchat/characters.py` — инициализация персонажей из cfg, структура и порядок.
- `rpchat/characters_manage.py` — операции управления персонажами для UI.
- `rpchat/events_store.py` — хранилище событий: список/загрузка/путь.

## LLM layer / tracing
- `rpchat/llm_manager.py` — кеш модели, `create_chat_completion`, фильтрация kwargs, backend info. Критично для “одна модель в памяти”.
- `rpchat/debug_trace.py` — трассировка/события дебага.

## Chat engine (legacy)
- `rpchat/chat_ui_adapter.py` — стриминговая генерация NPC: `on_send_all_sequential`, ретраи, обновление истории, prompt preview.
- `rpchat/chat_edit.py` — редактирование/регенерации: `apply_edit_like_chatgpt`, `on_regen_last`, связь с `core/pipeline`.
- `rpchat/chat_core.py` — общий “клей” для чат-логики.
- `rpchat/editor_ai.py` — AI-редактор (вспомогательные сценарии).

## Core (scene / memory / pipeline)
- `rpchat/core/pipeline.py` — `generate_player_turn`, `regenerate_from_user_index`, сборка сообщений и обработка.
- `rpchat/core/generate.py` — низкоуровневые хелперы генерации.
- `rpchat/core/dialogue.py` — логика диалога как структуры.
- `rpchat/core/scene_state.py` — операции с `SceneState`.
- `rpchat/core/scene_memory.py` — память сцены/резюме, извлечение фактов.

## Memory updater
- `rpchat/memory_updater.py` — обновление состояния сцены/памяти после хода (влияет на “🧩 Обновляю состояние сцены…”).

## Sessions / storage
- `rpchat/session_store.py` — публичная обвязка сохранения/загрузки сессий.
- `rpchat/storage/__init__.py` — init пакета storage.
- `rpchat/storage/session_store.py` — JSON-хранилище сессий (`saved_sessions/`): list/save/load/delete.

## SD pipeline (optional feature)
- `rpchat/sd_pipeline.py` — генерация SD prompt/negative_prompt на основе сцены/диалога.

## UI (Gradio)
- `rpchat/ui/assets.py` — `APP_CSS`, `APP_JS`, `APP_OVERLAY_HTML`.
- `rpchat/ui/chat_render.py` — отрисовка истории в HTML.
- `rpchat/ui/game_tab.py` — вкладка “Игра”: 5 кнопок, статус-бар, генерация/реген.
- `rpchat/ui/debug_tab.py` — вкладка Debug: prompt preview и диагностика.
- `rpchat/ui/events_tab.py` — вкладка Events: выбор/применение событий.
- `rpchat/ui/characters_tab.py` — вкладка Characters.
- `rpchat/ui/scene_tab.py` — вкладка Scene.
- `rpchat/ui/sessions_tab.py` — вкладка Sessions.
- `rpchat/ui/__init__.py` — `UIContext` (контейнер gr.State).
