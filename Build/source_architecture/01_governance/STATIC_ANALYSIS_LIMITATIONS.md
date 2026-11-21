# Static Analysis Limitations

## Scope inspected

This architecture set records static inspection of the checked-out repository. Its inventory defines project source as Python beneath `backend_django/`, frontend source and styles beneath `frontend_vue/src/`, and six root scripts. It excludes dependency trees, virtual environments, Git metadata, caches, build output, media, databases, binary assets, and Markdown from the source-file total. See [repository inventory](../00_project_overview/REPOSITORY_INVENTORY.md).

Inspection references include Django settings and URL declarations, application model and task modules, Vue route declarations, source-file catalogues, and existing per-application and per-domain documentation. Existing documentation is supporting context; current source is authoritative.

## Findings that are static only

- Counts of 26 local Django applications, 18 routed Vue domains, 835 backend Python files, 288 frontend source/style files, 132 model declarations, 222 URL declarations, 134 Vue SFCs, 32 frontend service-layer files, and 11 Celery task declarations are repository-syntax inventories. The counting scopes and qualifications are in the [inventory](../00_project_overview/REPOSITORY_INVENTORY.md), [backend audit](../02_backend/BACKEND_COVERAGE_AUDIT.md), and [frontend audit](../03_frontend/FRONTEND_COVERAGE_AUDIT.md).
- A `path()`, `re_path()`, or router registration declaration does not prove the effective runtime route, method set, or request behavior. The API catalogue explicitly does not expand router registrations or fully resolve route composition: [API integration catalogue](../04_integration/API_INTEGRATION_CATALOGUE.md).
- A model class and its declared fields do not prove the live database schema, applied migrations, constraints, indexes, or data state. The backend coverage audit reports exhaustive field and relationship inventory as unresolved.
- A declared Celery task or schedule does not prove a worker, broker, or scheduler is configured and running. No background task was executed.
- A Vue route or service call does not prove a user can reach the view or that an HTTP request succeeds. No frontend build, browser session, or HTTP request was performed.
- Matching frontend and backend URL strings establishes a source-level candidate connection only. It does not prove effective Axios URL composition, method compatibility, payload compatibility, authorization behavior, or successful responses.

## Inferences

Any architectural grouping inferred from directory names, class names, route prefixes, imports, or existing documentation is an inference unless a direct source reference establishes the relationship. The integration map labels broad/partial traces and records unresolved mappings; these should not be read as exhaustive proof of endpoint consumption.

## Not verified at runtime

The following were not run or verified:

- Django tests, frontend tests, static checks, builds, or application startup.
- Database migrations, schema inspection, database queries, or transaction behavior.
- API requests, route resolution through a running Django resolver, or response payloads.
- Authentication flows, permission enforcement, object ownership, or role behavior.
- Celery workers, brokers, schedules, retries, task results, or failure handling.
- External providers, scraping targets, email/notification delivery, file extraction, or other network integrations.
- Deployment configuration, production environment values, or infrastructure behavior.

## Runtime verification still needed

Use a separately authorized runtime validation plan to verify route resolution and representative API contracts, database state and migration alignment, authentication and permission behavior, task scheduling and failure paths, and deployment-specific settings. No runtime guarantee is made by this document.
