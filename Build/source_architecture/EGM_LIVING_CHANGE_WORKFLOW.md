# EGM Living Change Workflow — SO_IAM_OS

**Governance:** Elephant-Goldfish Model (EGM) is the permanent lifecycle for every meaningful change. This file defines the project-side operating contract; it does not claim the external Codex plugin was executed in this environment.

## Required lifecycle

1. **Discovery (Elephant):** inspect the actual current source, tests, configs, manifests, docs, git status, and relevant runtime evidence available. Record exact files, current behavior, assumptions, and unknowns.
2. **Specification:** define user outcome, acceptance criteria, API/data contracts, permissions/ownership, UI behavior, observability, migration/rollback, and documentation impact.
3. **Impact analysis:** trace affected apps, models, serializers, endpoints, frontend routes/components/services/stores, background tasks, settings, tests, and docs. Separate confirmed edges from hypotheses.
4. **Goldfish review:** an independent reviewer challenges assumptions, missing failure paths, security, data integrity, compatibility, test coverage, and scope creep. Findings receive severity, evidence, and disposition.
5. **Owner approval:** no implementation until the owner approves the exact scope, files/operations, and any destructive or schema-changing work.
6. **Implementation:** smallest coherent change; preserve existing behavior; no unrelated refactoring; honor protected files and project manifests.
7. **Verification:** run focused tests and relevant broader tests/lint/build as approved and available. Record exact commands/results. Static inspection must never be reported as runtime verification.
8. **Documentation update:** update only impacted app guide, feature registry, API/model/dependency catalogue, Master Map, change log, and next actions.
9. **Drift review:** compare source vs docs; flag missing/obsolete references, status changes, and unverified claims. Repeat after each material change.

## Mandatory change record

- Change ID/date and owner approval reference.
- User problem and acceptance criteria.
- Before-state and exact source evidence.
- Files/components and inbound/outbound dependencies.
- API/data-contract and permission impact.
- Risks, migration/rollback, and protected-file status.
- Goldfish findings and dispositions.
- Implementation diff summary.
- Test/lint/build/runtime commands and outcomes.
- Documentation files updated and remaining drift.

## Feature registry status controls

Use `IMPLEMENTED_VERIFIED`, `PARTIAL`, `IN_PROGRESS`, `PLANNED`, `BROKEN`, or `NOT_VERIFIED`. Do not assign `IMPLEMENTED_VERIFIED` from a route, model, or URL declaration alone.

## Git and repository safety

- Capture `git status --short` before any change and again after.
- Never reset, clean, checkout over, or overwrite user changes.
- Recheck the historical modified paths listed in `CURRENT_SOURCE_BASELINE_2026-11-23.md`; do not assume the current state matches the archive.
- Do not modify `PROJECT_CONTEXT.json`, `project_manifest.json`, or protected items without explicit scope approval if they exist in the live checkout.
- Keep `Build/` as the authoritative engineering documentation root; `project_docs/` remains user-facing docs and must link to, not silently duplicate, architecture authority.

## Stop conditions

Stop and ask the owner if scope expands to production credentials, destructive data operations, irreversible migrations, broad permission changes, unreviewed external integrations, or changes outside the approved file/operation list.
