# Phase 2 — Architecture + API Contract

This build is the result of Phase 2 only.

## What was implemented

- Canonical frontend API endpoint registry.
- Alignment of existing Vue service calls with the actual Django router/action contract.
- Lifecycle wrappers for existing Learning actions.
- Correct HTTP method for Learning Session finish.
- Corrected Vue router plugin registration in `main.js`.
- Architecture and API contract documentation.

## What was intentionally not implemented yet

The following belong to later phases and were not introduced prematurely:

- Redis/Celery infrastructure.
- New Jobs models/APIs.
- Learning model redesign.
- PrimeVue redesign.
- Knowledge file extraction pipeline.
- Dashboard rewrite.

## Validation

The environment used for packaging does not contain the project's Python dependencies or frontend `node_modules`, so runtime Django/Vite tests cannot be executed here. Static Python syntax validation and source-level contract checks are performed before packaging.
