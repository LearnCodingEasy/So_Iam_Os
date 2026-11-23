# Project Next Actions — Source-Verified Backlog

**Checkpoint:** 2026-11-23. Priorities are engineering recommendations from static inspection, not approved implementation tasks.

## P0 — establish reliable orientation

1. Use `Build/PROJECT_MASTER_MAP.md` as the single entry point.
2. Keep `CURRENT_SOURCE_BASELINE_2026-11-23.md` as the count authority for this archive; reconcile only when a fresh source snapshot is supplied.
3. Reconcile `DOCUMENTATION_MANIFEST.md`, older 17-app overview/counts, and 266/267 documentation totals in a future approved documentation-only change. Existing historical documents were not silently rewritten.
4. Add the live `PROJECT_CONTEXT.json`, `project_manifest.json`, `.git` state, and `project_docs/` to the next local-checkout audit; they were absent from this ZIP.

## P1 — close architecture coverage gaps

5. Expand each app guide into a source-traced flow: model → serializer → view/service → URL → permission/ownership → test → frontend consumer.
6. Expand API catalogue from URL declarations to resolved operations with request/response/error schemas, authentication, permissions, pagination/filtering, and ownership rules.
7. Complete model fields, constraints, indexes, inheritance, migrations, and cross-app relation targets; validate against migrations and a safe database snapshot.
8. Complete frontend route → page → component → store/service → backend operation mapping; resolve route count and Vue SFC count differences with documented counting rules.
9. Trace Celery tasks, scheduling, retries, idempotency, failure handling, and enqueue callers.
10. Verify the nine apps without root API mounts (if still absent in the live checkout) and decide whether they are intentionally model/scaffold-only or require integration.

## P2 — runtime verification (separate approved phase)

11. Install from declared lockfiles/manifests in a controlled environment.
12. Run Django system checks and focused backend tests; then full backend tests as feasible.
13. Run frontend lint without auto-fix first, unit tests, and production build.
14. Exercise authentication, representative CRUD, cross-domain flows, background jobs, and authorization boundaries in a disposable test environment.
15. Record results and update feature statuses only from actual evidence.

## Gate for each task

No item above is permission to modify the live checkout. Apply EGM discovery → impact analysis → Goldfish review → explicit owner approval → implementation → verification → documentation update → drift review.
