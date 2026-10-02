# Phase 2 — Modified / Created Files

## Modified

1. `frontend_vue/src/main.js`
   - Removed duplicate global Axios configuration.
   - `api.js` remains the single Axios client.
   - Fixed `app.use(router, axios)` to `app.use(router)`.

2. `frontend_vue/src/services/learning.js`
   - Uses canonical endpoint registry.
   - Added Topic/Path/Goal lifecycle wrappers.
   - Added learner assessment and assessment-start wrappers.
   - Corrected session finish to the backend's `POST /finish/` action.
   - Added revision lifecycle wrappers.

3. `frontend_vue/src/services/goals.js`
   - Uses canonical endpoint registry.

4. `frontend_vue/src/services/tasks.js`
   - Uses canonical endpoint registry.

5. `frontend_vue/src/services/knowledge.js`
   - Uses canonical endpoint registry.
   - Corrected archive semantics to call the archive action.
   - Added explicit restore/remove methods.
   - Corrected file upload to `/upload-file/`.

6. `frontend_vue/src/services/aiControl.js`
   - Uses canonical endpoint registry.

7. `frontend_vue/src/services/ai.js`
   - Uses canonical endpoint registry.

8. `frontend_vue/src/services/dashboard.js`
   - Uses canonical endpoint registry.

9. `frontend_vue/src/services/usersAccounts.js`
   - Uses canonical endpoint registry.

10. `backend_django/knowledge/views.py`
    - Added server-side `learning_topic` filter so Learning Topic → Knowledge queries match the frontend contract.

## Created

1. `frontend_vue/src/services/endpoints.js`
   - Canonical endpoint builders for all currently implemented API domains.

2. `backend_django/core/test_api_contract.py`
   - Routing smoke tests for critical endpoints used by the frontend.

3. `Build/architecture/PHASE_2_ARCHITECTURE.md`
   - Architecture boundaries and data-flow rules.

4. `Build/backend_django/api_contract/API_CONTRACT.md`
   - Human-readable API contract for current backend behavior.

5. `Build/backend_django/api_contract/CHANGELOG_PHASE_2.md`
   - Phase 2 contract decisions and deferred work.

6. `Build/PHASE_2_README.md`
   - Scope and validation notes.

7. `Build/PHASE_2_MODIFIED_FILES.md`
   - This file.

## Database migrations

None in Phase 2. No schema was changed.

## Intentionally deferred

- Redis/Celery: Phase 5.
- PrimeVue migration: Phase 6+.
- Learning domain fixes: Phase 9.
- Knowledge extraction pipeline: Phase 13.
- Jobs Opportunity: Phase 14.
- Final Dashboard: Phase 15.
