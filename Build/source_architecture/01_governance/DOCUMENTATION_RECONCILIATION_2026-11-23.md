# Documentation Reconciliation Report — 2026-11-23

## Purpose

This report records discrepancies between historical documentation and the current supplied source archive. Historical files are preserved; current source baseline and current audits supersede old counts for this archive only.

## Key corrections

| Topic | Historical claim | Current archive evidence | Resolution |
|---|---|---|---|
| Backend apps | 17 apps in older master docs | 26 directories with `apps.py`; 25 in `INSTALLED_APPS` | Current Master Map and backend audit distinguish app directories from installed apps |
| `skills` app | Described in some docs as installed | `skills/` is absent from `INSTALLED_APPS`, contains placeholder code; `learning.Skill` is the active model | Corrected `skills.md`, app index, baseline, coverage audit; did not activate scaffold |
| Backend Python count | 772 or 835 in older registers | 996 `.py` files under `backend_django/`; 836 excluding `tests/` and `migrations/` | New baseline defines counting rules; old counts are historical |
| Model declarations | 132 in previous static audit | 164 direct `models.Model` subclasses found by current AST scan | New model catalogue supersedes count; dynamic/inherited cases remain a limitation |
| Frontend source counts | 286/287/288 depending on prior inventory | 358 files under `frontend_vue/`; 142 `.vue` files; 44 router declarations extracted | New baseline and frontend audit provide explicit scopes |
| Build Markdown | 266 in older coverage register | 267 in `complete_project_documentation/`; 330 Markdown files under all `Build/` after this pass | Current manifest gives current folder-scoped totals |
| Manifest status | Older manifest marks some existing docs planned and omits later docs | Current tree includes integration, quality, task, and Goldfish docs | Added current manifest; preserved historical manifest |
| Git and user docs | Assumed project context | `.git/` and `project_docs/` absent from ZIP | Cannot certify local status or VuePress docs from this archive |

## Source-level discrepancy discovered during second review

The first documentation pass mistakenly treated all 26 app-like directories as installed. A second literal-AST check of `INSTALLED_APPS` found 25 registered local apps. The remaining `skills/` package is a generated scaffold with no model or API. Its app guide and all new current-state summaries have been corrected. No application settings were changed because adding an empty, unreferenced scaffold is not a safe or justified fix.

## Preservation policy

- Existing historical guides and reviews remain available for provenance.
- Current source baseline, current manifest, and current audits are the active navigation references.
- Do not delete or mass-rewrite legacy documentation until a separate approved archival/migration plan is reviewed.
