# Codex Release Validation

## Implemented scope

This release changes **only the `codex` application and its direct frontend integration**.
Existing SO_IAM_OS applications are treated as dependencies/context and are not rebuilt.

### Capability registry

- 150 Codex Features
- 100 Codex Tools
- 100 Codex Agents
- Versioned catalog: `1.0.0`
- Unique keys enforced by database constraints
- Permission/risk/validation contracts
- Tool and agent execution audit records
- Project Context export
- Codex capability health endpoint
- Codex capability validation endpoint

### Frontend

- New `CodexCapabilities.vue`
- PrimeVue DataTables for all 350 capabilities
- Search/filtering
- Registry health display
- Bootstrap and Validate actions
- Tool execution action
- Agent execution action
- Integrated into existing `CodexView.vue`

### Backend endpoints

- `/api/codex/registry/features/`
- `/api/codex/registry/tools/`
- `/api/codex/registry/agents/`
- `/api/codex/registry/summary/`
- `/api/codex/registry/health/`
- `/api/codex/registry/bootstrap/`
- `/api/codex/registry/validate/`
- `/api/codex/registry/runs/`
- `/api/codex/registry/tools/<key>/execute/`
- `/api/codex/registry/agents/<key>/execute/`
- `/api/codex/context/export/`
- `/api/codex/files/<id>/content/`

## Validation performed in the build environment

- Python syntax compilation: **PASS**
- Canonical catalog counts: **150 / 100 / 100 — PASS**
- Canonical key uniqueness: **PASS**
- Project context JSON counts: **PASS**
- Backend route contract scan: **PASS**
- Frontend service contract scan: **PASS**
- Codex UI integration scan: **PASS**
- Node syntax checks for modified JS files: **PASS**

## Environment limitation

The build environment did not contain the project's Django/Node dependency trees. Network access was unavailable, so dependency installation could not complete. Therefore a live Django test server and a full Vite production build could not be executed in this environment.

The repository includes runtime tests for the complete registry:

```text
backend_django/codex/tests/test_capability_registry.py
```

Run in the project environment:

```bash
cd backend_django
python manage.py migrate
python manage.py codex_seed_capabilities
python manage.py test codex.tests.test_capability_registry
```

Frontend:

```bash
cd frontend_vue
npm ci
npm run build
npm run test:unit
```

The release is intentionally **non-destructive**: no existing Codex model was deleted or replaced.
