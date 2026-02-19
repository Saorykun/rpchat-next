# Target architecture (rpchat-next)

Цель: сохранить внешний результат/функциональность legacy RPChat, но сделать архитектуру масштабируемой и дебажимой.

## Invariants (must keep)
- Промпты остаются теми же (копируем verbatim из legacy).
- Debug показывает реальные промпты, отправленные в модель (для всех действий).
- Одна точка входа LLM + одна модель в памяти (gateway/cache).
- Работают: диалог, автоход игрока, регенерация автохода, регенерация ответа NPC, редактирование прошлого.

## Layers
- `domain/` — модели данных + промпты (чистый слой, без I/O).
- `engine/` — ActionEngine: оркестрация 5 действий, единый поток событий (stage/progress/history/prompt).
- `services/` — операции над историей, прогресс, нормализация, парсинг.
- `infra/` — LLM gateway (llama.cpp), storage (sessions/events), логирование.
- `ui/` — Gradio UI: тонкий слой, реагирует на events.

## Migration mode
Начинаем в bridge-mode:
- Engine делегирует в legacy реализацию (поведение 1-в-1).
Постепенно переносим логику внутрь engine:
- NPC streaming core
- regen/edit core
- auto-player generation
- post-steps (memory updater)
