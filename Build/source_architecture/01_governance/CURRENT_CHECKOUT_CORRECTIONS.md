# Current Checkout Corrections

This additive note records corrections found during the documentation audit without rewriting pre-existing architecture documents.

## Source and application counts

The current read-only enumeration found:

| Item | Count | Scope |
|---|---:|---|
| Local Django apps | 26 | Directories with `apps.py`, registered in `backend_django/backend_django/settings.py`. |
| Backend Python files | 835 | Project-owned Python under `backend_django/`, including migrations and tests. |
| Frontend files | 288 | Files under `frontend_vue/src/` with `.js`, `.jsx`, `.ts`, `.tsx`, `.vue`, `.mjs`, `.cjs`, `.css`, `.scss`, `.html`, `.sql`, `.sh`, or `.ps1` extensions. Current files are `.css` (1), `.html` (2), `.js` (69), `.scss` (82), and `.vue` (134). |
| Root scripts | 6 | The six project-owned scripts counted by the repository inventory. |
| Total scoped source files | 1,129 | 835 + 288 + 6. This is a file-count scope, not a count of all repository files. |

The earlier `00_project_overview/REPOSITORY_INVENTORY.md` reports 287 frontend files and 1,128 total. The frontend coverage audit reports 288. The current recount returns 288 for both the audit's extension set and the inventory's narrower listed set, so use 288/1,129 for this checkout and treat 287/1,128 as stale.

## Django app registration versus URL mounting

`INSTALLED_APPS` contains 26 local applications. This does not mean every app has an API URL module or is mounted by the project URL configuration. The backend coverage audit identifies nine scaffold applications without an app URL module: `agents`, `ai_tools_laboratory`, `analytics`, `architecture`, `crm`, `marketing`, `revenue`, `sales`, and `skills`. Project-level URL includes are listed in `backend_django/backend_django/urls.py`; see also `02_backend/BACKEND_COVERAGE_AUDIT.md`.

## API count wording

The count of 222 is a count of URL declarations: 133 literal `path()`/`re_path()` calls and 89 DRF `router.register()` calls. It is not an exhaustive count of concrete HTTP method/path operations because router expansions and action routes are not fully expanded. Refer to `04_integration/API_INTEGRATION_CATALOGUE.md` for the declaration-level boundary.

## Preservation

Older summaries remain untouched to preserve the existing documentation. This correction note is the current-checkout addendum; readers should use it alongside the historical inventory and the coverage audits until a separately authorized manifest/document reconciliation is completed.
