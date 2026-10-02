# PHASE 1 — Database / Migration Drift + API Contract Stabilization

Date: 2026-09-30

## Scope

This phase stabilizes the existing SO_IAM_OS source tree and delivered SQLite database before Codex Foundation work.

No existing product feature was removed or replaced.

## Database reconciliation

### Reconciled migration history

- Added the missing `learning.0004_alter_applicationreview_id_and_more` migration as a compatibility/no-op node because the delivered database already records it as applied.
- Added the historical `knowledge.0002_knowledgefile` compatibility/no-op node because the delivered database records it as applied. The existing knowledge index migration now depends on this node, producing a deterministic migration graph.
- Added `social.0003_social_profile_recommendation` to the delivered database state. The source migration already existed; the database was missing its applied record and tables.
- Added `notification.0001_initial` to the delivered database state. The source migration already existed; the database was missing its applied record and table.

### Preserved data

The existing database remains the source data set. Representative row counts after reconciliation:

- Users: 2
- AI conversations: 83
- AI messages: 140
- Learning topics: 18
- Tasks: 22
- Goals: 4
- Job sources: 1
- Job opportunities: 0

No existing rows were deleted.

### New database structures reconciled

- `social_socialprofile`
- `social_socialrecommendation`
- `notification_notification`

Indexes and uniqueness constraints required by the current models are present.

## API contract reconciliation

### Root routing

Added:

```text
/api/notifications/
```

The existing domains remain available under their current `/api/<domain>/` prefixes.

### Notification contract

Canonical frontend endpoints now match Django:

```text
GET  /notifications/
GET  /notifications/unread-count/
POST /notifications/{id}/read/
POST /notifications/read-all/
POST /notifications/{id}/archive/
PATCH /notifications/{id}/
DELETE /notifications/{id}/
```

The Notification ViewSet now permits POST actions; previously its `http_method_names` prevented those declared POST actions from being dispatched correctly.

### Social contract

Canonical frontend endpoints now match the existing Django API:

```text
GET/PATCH /social/profile/
GET       /social/recommendations/
POST      /social/friends/{id}/request/
GET       /social/friends/{id}/
GET       /social/friends/suggested/
POST      /social/friends/{id}/{action}/
POST      /social/friends/{id}/unfriend/
```

### Jobs contract

Added the missing frontend builder:

```text
POST /jobs/opportunities/{id}/apply/
```

Resolved the frontend `readiness` name collision by separating:

```text
opportunityReadiness(id)
readiness
```

The former points to the per-opportunity readiness endpoint; the latter remains the collection-level readiness endpoint.

## Frontend service consistency

- Notification service now distinguishes list responses from object/count responses.
- Notification update/delete helpers were added using the canonical registry.
- Jobs service now uses `opportunityReadiness(id)` for a specific job.
- A static scan found no unresolved `endpoints.<domain>.<key>` references across the frontend services.

## Validation

Passed:

- Python syntax compilation for backend source.
- JavaScript syntax checks for modified endpoint/service files.
- Static endpoint-reference scan: no missing endpoint keys.
- SQLite integrity/schema checks for reconciled tables.
- Existing representative data counts preserved.

Runtime Django tests could not be executed in the isolated build environment because Django/dependencies are not installed and outbound package installation is unavailable. The project therefore still requires local runtime verification with the project's pinned dependencies.

## Security packaging

Production/local environment files were removed from the deliverable and replaced with `.env.example`. No Codex functionality was added in this phase.
