# So_Iam_OS — Phase 2 Architecture

## Scope

Phase 2 converts the existing project analysis into an explicit implementation contract. It does **not** replace existing apps, models, or APIs.

## Current-to-target flow

```text
Vue Page / Component
        |
        v
Vue Service Layer
        |
        v
Canonical Endpoint Contract
        |
        v
Django URL / DRF Router
        |
        v
Serializer Validation
        |
        v
Domain Service
        |
        v
Model / Task / Provider
```

## Rules

1. Existing models remain the source of truth.
2. Existing router paths are reused whenever they already express the required behavior.
3. Vue endpoint paths are centralized in `frontend_vue/src/services/endpoints.js`.
4. User-owned resources are always scoped by `request.user` on the backend.
5. Serializer validation owns request-shape validation; services own business rules.
6. Views/ViewSets orchestrate HTTP concerns and should not accumulate large business workflows.
7. Long-running work will move to Celery in Phase 5; Phase 2 only defines the contract needed by that work.
8. API credentials never cross the read API as plaintext.

## Ownership boundaries

| Layer | Responsibility |
|---|---|
| Vue component | UI state, user interaction, rendering |
| Vue service | HTTP call + response normalization |
| Endpoint registry | Canonical URL paths |
| Django ViewSet/APIView | Authentication, orchestration, HTTP status |
| Serializer | Input/output contract + validation |
| Service | Business logic and transactions |
| Model | Persistence + relational integrity |
| Celery task | Long-running/background execution |
| Redis | Broker/cache/channel backend when enabled |

## Cross-domain relationships

```text
User
 ├── Goals
 │    └── Tasks
 ├── Learning Goals
 │    └── Learning Paths
 │         └── Topics
 │              ├── Lessons
 │              ├── Progress
 │              ├── Assessments
 │              └── Knowledge
 └── AI Settings / Conversations
```

The future Jobs domain will reference the existing `learning.Skill` model rather than introduce a duplicate skill taxonomy.
