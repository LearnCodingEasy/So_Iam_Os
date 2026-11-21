# Background Task Catalogue

## Scope

Static catalogue of functions decorated with Celery task decorators under `backend_django/`, the declared Celery beat schedule, Celery app setup, and discovered Django management commands. A declaration does not prove that a worker, broker, or scheduler runs. No task or command was executed.

## Celery task definitions

| Task | Source | Trigger/input | Observable source-level behavior | Retry/result notes |
|---|---|---|---|---|
| `execute_workflow_task` | `backend_django/automation/tasks.py` | Celery call with workflow, user, and task-run IDs | Loads workflow and run constrained to the user; calls `execute_workflow`; stores finish time and truncated result log; on exception attempts to mark the run failed, then re-raises. | `bind=True`; no decorator retry policy. |
| `run_local_ai_job` (`codex.run_local_ai_job`) | `backend_django/codex/tasks.py` | Job ID | Marks `LocalAIJob` running, then handles summarize/metadata, classify, markdown index, architecture, or fallback task types; records result/completion or failure/error. File paths in summarize/metadata are resolved and checked beneath the project root. | `bind=True`; no decorator retry policy. |
| `generate_learning_plan` | `backend_django/ai/tasks/ai_tasks.py` | User ID, message, optional provider/model | Publishes `STARTED` state with user metadata; loads user; invokes `AILearningActionService.generate_ai_plan`; returns user ID and result. | Retries any exception, backoff, maximum two retries. |
| `generate_daily_learning_tasks` | `backend_django/tasks/tasks.py` | User ID and optional count/provider/model | Loads user; delegates to `DailyTaskGenerationService`; returns created count and task IDs. | Retries any exception, backoff, maximum two retries. |
| `generate_daily_learning_tasks_for_all_users` | `backend_django/tasks/tasks.py` | No explicit arguments | Iterates active users, generates daily tasks for each, returns total created count. | No explicit retry options. |
| `process_knowledge_file` (`knowledge.tasks.process_knowledge_file`) | `backend_django/knowledge/tasks/knowledge_file_tasks.py` | Knowledge file ID | Marks processing; validates upload and extracts text; records per-file extraction metadata; populates related knowledge content only when currently blank, inside a transaction; records failure state/error and re-raises. | Retries any exception, backoff, maximum two retries; explicit task name preserves a legacy queue name. |
| `run_scraping_job` | `backend_django/scraper/tasks.py` | Job ID | Calls `ScrapingService.start_scraping_job`. | Up to two retries with 60-second default delay; explicitly retries connection/timeout/temporary/502–504-like errors with exponential delay. |
| `sync_job_source` | `backend_django/jobs_opportunity/tasks.py` | Source ID and optional sync-run ID | Handles disabled sources; fetches configured scraper/RSS/XML/JSON data, adapts supported provider payloads, upserts bounded job items in a transaction, and records source/sync-run success or failure state. | Retries request/network/timeout errors with backoff up to three retries; ignores result. |
| `refresh_all_job_sources` | `backend_django/jobs_opportunity/tasks.py` | No explicit arguments | Queues `sync_job_source.delay(source_id)` for each enabled source; returns number queued. | Ignores result. |
| `refresh_all_job_matches` | `backend_django/jobs_opportunity/tasks.py` | No explicit arguments | For each active user refreshes matches, refreshes recommendations, and computes dashboard analytics; returns total refreshed matches. | No explicit retry options. |
| `expire_old_jobs` | `backend_django/jobs_opportunity/tasks.py` | No explicit arguments | Bulk-updates active opportunities whose expiry precedes current time to inactive and expired; returns update count. | No explicit retry options. |

## Declared schedule

`backend_django/backend_django/settings.py` declares one `CELERY_BEAT_SCHEDULE` entry: `tasks.tasks.generate_daily_learning_tasks_for_all_users` at `86400.0` seconds. This establishes a configured schedule declaration only; deployment of Celery Beat and actual invocation are not verified.

## Celery applications

- `backend_django/backend_django/celery.py` creates Celery app `so_iam_os`, loads Django settings under the `CELERY` namespace, and autodiscovers tasks.
- `backend_django/automation/celery.py` separately creates Celery app `automation`, sets `DJANGO_SETTINGS_MODULE` to `project.settings`, loads namespaced settings, and autodiscovers tasks. Whether this alternate app is used in deployment is unknown.

## Management commands discovered

The following command classes were found by static search. Their argument contracts and effects require individual review before use; none was run.

| Command file | Command class |
|---|---|
| `backend_django/codex/management/commands/codex_seed_capabilities.py` | `Command` |
| `backend_django/codex/management/commands/codex_scan.py` | `Command` |
| `backend_django/codex/management/commands/codex_export_context.py` | `Command` |
| `backend_django/codex/management/commands/codex_bootstrap_governance.py` | `Command` |
| `backend_django/jobs_opportunity/management/commands/scrape_jobs.py` | `Command` |
| `backend_django/jobs_opportunity/management/commands/bootstrap_job_sources.py` | `Command` |

## Limitations

No command or task was run. Broker availability, worker registration, beat deployment, task delivery, database side effects, retries under live failures, and task result storage remain unverified. The 11-task total counts decorated function definitions found by static search, not runtime-registered tasks.
