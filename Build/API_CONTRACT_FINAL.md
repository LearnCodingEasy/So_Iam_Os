# SO_IAM_OS — Stabilized API Contract

Base: `/api/`
Authentication: `Authorization: Bearer <access-token>`

## Core domains

```text
/users/
/core/
/tasks/
/goals/
/learning/
/knowledge/
/ai/
/jobs/
/social/
/notifications/
```

## Notifications

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/notifications/` | List current user's active notifications |
| GET | `/notifications/unread-count/` | Return unread count |
| POST | `/notifications/{id}/read/` | Mark one notification read |
| POST | `/notifications/read-all/` | Mark all current-user notifications read |
| POST | `/notifications/{id}/archive/` | Archive one notification |
| PATCH | `/notifications/{id}/` | Update a notification |
| DELETE | `/notifications/{id}/` | Delete a notification |

## Social

| Method | Endpoint | Purpose |
|---|---|---|
| GET/PATCH | `/social/profile/` | Read/update current user's social profile |
| GET | `/social/recommendations/` | Social recommendations |
| GET | `/social/friends/{id}/` | Friend list and incoming requests for the user |
| POST | `/social/friends/{id}/request/` | Send connection request |
| GET | `/social/friends/suggested/` | Friend suggestions |
| POST | `/social/friends/{id}/{action}/` | Accept/reject/cancel request |
| POST | `/social/friends/{id}/unfriend/` | Remove friendship |

## Jobs

The existing Jobs API is preserved. The frontend contract now explicitly includes:

```text
POST /jobs/opportunities/{id}/apply/
GET  /jobs/opportunities/{id}/readiness/
```

The Vue registry uses `opportunityReadiness(id)` for the per-job endpoint and `readiness` for the collection-level endpoint.

## Contract rule

`frontend_vue/src/services/endpoints.js` is the canonical frontend endpoint registry. New frontend API calls must be added there rather than hard-coded in feature services.
