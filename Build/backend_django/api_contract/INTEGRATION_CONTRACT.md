# API Integration Contract

## Authentication

Frontend sends `Authorization: Bearer <access-token>` through the shared Axios client.

## Canonical domains

- `/api/core/` — dashboard and shared settings.
- `/api/tasks/` — task CRUD/actions.
- `/api/goals/` — goal CRUD/actions.
- `/api/learning/` — learning domain, progress and assessments.
- `/api/knowledge/` — knowledge items/files and topic connections.
- `/api/ai/` — AI settings, chat and learning generation.
- `/api/jobs/` — sources, opportunities, matches and applications.

## Progress

`GET /api/learning/progress/summary/` returns the server-calculated learning summary used by the Progress UI.

## Error shape

The frontend accepts DRF's `detail`, `message`, `error`, and field-level validation errors. New endpoints should prefer `{ "detail": "..." }` for single-operation errors.
