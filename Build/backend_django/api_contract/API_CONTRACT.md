# So_Iam_OS API Contract — Phase 2

Base URL in development:

```text
http://127.0.0.1:8000/api
```

Authentication:

```http
Authorization: Bearer <access-token>
```

Default API permission is authenticated access. Resource ownership is enforced server-side.

## Response conventions

### Success

- `200 OK` — read/update/action completed.
- `201 Created` — resource created.
- `204 No Content` — resource deleted.

### Client errors

- `400 Bad Request` — validation/business input error.
- `401 Unauthorized` — missing/invalid authentication.
- `403 Forbidden` — authenticated user cannot access the resource.
- `404 Not Found` — resource does not exist or is not owned by the user.

### Generic error extraction

Frontend should check, in order:

```text
response.data.detail
response.data.message
response.data.error
field-level validation object
```

## Users

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/users/signup/` | Create account |
| POST | `/users/login/` | Obtain tokens |
| POST | `/users/refresh/` | Refresh access token |
| GET | `/users/me/` | Current user |
| GET | `/users/profile/{id}/` | User profile |
| POST | `/users/editprofile/` | Update profile |
| POST | `/users/editpassword/` | Change password |

## Goals

| Method | Endpoint | Purpose |
|---|---|---|
| GET/POST | `/goals/` | List/create |
| GET/PATCH/DELETE | `/goals/{id}/` | Read/update/delete |
| POST | `/goals/{id}/complete/` | Complete |
| POST | `/goals/{id}/pause/` | Pause |
| POST | `/goals/{id}/resume/` | Resume |
| POST | `/goals/{id}/progress/` | Update progress |

Progress request:

```json
{"progress_percent": 75}
```

## Tasks

| Method | Endpoint | Purpose |
|---|---|---|
| GET/POST | `/tasks/` | List/create |
| GET/PATCH/DELETE | `/tasks/{id}/` | Read/update/delete |
| GET | `/tasks/today/` | Today's tasks |
| POST | `/tasks/{id}/complete/` | Complete |
| POST | `/tasks/{id}/postpone/` | Postpone |

## Learning

### Skills

```text
GET /learning/skills/
GET /learning/skills/{id}/
```

Skills are global read-only entities for learners.

### Learning goals

```text
GET/POST /learning/goals/
GET/PATCH/DELETE /learning/goals/{id}/
POST /learning/goals/generate/
GET /learning/goals/dashboard/
POST /learning/goals/{id}/complete/
POST /learning/goals/{id}/pause/
POST /learning/goals/{id}/resume/
```

### Learning paths

```text
GET/POST /learning/paths/
GET/PATCH/DELETE /learning/paths/{id}/
POST /learning/paths/{id}/start/
POST /learning/paths/{id}/complete/
POST /learning/paths/{id}/pause/
POST /learning/paths/{id}/reorder-topics/
```

Reorder request:

```json
{"topic_ids": [12, 15, 13]}
```

### Topics

```text
GET/POST /learning/topics/
GET/PATCH/DELETE /learning/topics/{id}/
POST /learning/topics/{id}/start/
POST /learning/topics/{id}/complete/
POST /learning/topics/{id}/skip/
POST /learning/topics/{id}/generate-content/
```

### Progress

```text
GET/POST /learning/progress/
POST /learning/progress/update-progress/
```

The progress serializer supports:

```json
{
  "topic": 123,
  "progress_percent": 80,
  "practice_completed": true,
  "lesson_completed": true,
  "quick_check_completed": false,
  "assessment_completed": false,
  "notes": "..."
}
```

The server remains authoritative for derived fields such as completion timestamps, review flags, and AI score.

### Sessions

```text
GET/POST /learning/sessions/
GET/PATCH/DELETE /learning/sessions/{id}/
POST /learning/sessions/{id}/finish/
```

The finish action is `POST`, not `PATCH`.

### Assessments

```text
GET/POST /learning/assessments/
GET/PATCH/DELETE /learning/assessments/{id}/
GET /learning/assessments/{id}/learner/
POST /learning/assessments/{id}/start/
POST /learning/assessments/{id}/submit/
```

Learner-facing assessment data intentionally does **not** expose `is_correct`.

### Knowledge applications

```text
GET/POST /learning/applications/
GET/PATCH/DELETE /learning/applications/{id}/
POST /learning/applications/{id}/submit/
POST /learning/applications/{id}/review/
GET /learning/applications/{id}/history/
```

### Revisions

```text
GET/PATCH/DELETE /learning/revisions/{id}/
POST /learning/revisions/{id}/start/
POST /learning/revisions/{id}/complete/
POST /learning/revisions/{id}/skip/
```

## Knowledge

```text
GET/POST /knowledge/items/
GET/PATCH/DELETE /knowledge/items/{id}/
POST /knowledge/items/{id}/archive/
POST /knowledge/items/{id}/restore/
POST /knowledge/items/{id}/connect-topic/
POST /knowledge/items/{id}/disconnect-topic/
GET /knowledge/items/{id}/files/
POST /knowledge/items/{id}/upload-file/
GET /knowledge/files/
GET/PATCH/DELETE /knowledge/files/{id}/
POST /knowledge/items/archive-all/
```

File uploads use `multipart/form-data`.

## AI

```text
POST /ai/chat/
GET/POST /ai/conversations/
GET/DELETE /ai/conversations/{id}/
GET/PATCH /ai/settings/
GET/POST /ai/credentials/
DELETE /ai/credentials/{provider}/
GET /ai/providers/{provider}/models/
GET/POST /ai/prompts/
GET/PATCH/DELETE /ai/prompts/{id}/
POST /ai/learning/preview/
POST /ai/learning/approve/
```

Credential responses expose status/metadata, not plaintext secrets.

## Explicit contract decisions from Phase 2

1. Topic completion uses `/learning/topics/{id}/complete/`.
2. Session completion uses `POST /learning/sessions/{id}/finish/`.
3. Assessment grading is backend-owned; frontend must not depend on `is_correct`.
4. Endpoint paths are centralized in Vue.
5. Jobs endpoints are intentionally absent until Phase 14; no fake API is introduced.
