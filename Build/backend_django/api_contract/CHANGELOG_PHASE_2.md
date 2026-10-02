# Phase 2 Contract Changes

## Frontend changes

- Added `frontend_vue/src/services/endpoints.js` as the canonical endpoint registry.
- Updated Learning service to use canonical endpoints.
- Added missing wrappers for path/topic/goal lifecycle actions.
- Corrected Learning Session finish from `PATCH /sessions/{id}/` to `POST /sessions/{id}/finish/`.
- Added learner assessment and assessment-start API wrappers.
- Added revision lifecycle wrappers.
- Updated Goals, Tasks, and Knowledge services to use canonical endpoint builders.
- Corrected `main.js` from `app.use(router, axios)` to `app.use(router)`.

## Backend changes

No database schema or backend endpoint behavior was changed in Phase 2. Existing Django routers and serializers remain the source of truth.

## Deferred

- Redis/Celery implementation: Phase 5.
- PrimeVue UI migration: Phase 6+.
- Learning backend fixes: Phase 9.
- Knowledge processing/viewer: Phase 13.
- Jobs domain: Phase 14.
