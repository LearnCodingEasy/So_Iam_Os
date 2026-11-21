# File documentation: TaskViewSet

## Identity and status

- **Source:** [backend_django/tasks/api/views/tasks_views.py](../../../../../../../backend_django/tasks/api/views/tasks_views.py)
- **Area:** Django application tasks; REST API view module.
- **Main declarations:** TaskPagination and TaskViewSet.
- **Evidence status:** Handler behavior is **VERIFIED** from source. Effective runtime routing, database behavior, and worker behavior are **NOT RUNTIME VERIFIED**.

## Purpose

This module implements the Tasks REST API on top of Django REST Framework's ModelViewSet. It provides standard model operations plus custom list, scheduling, generation, status, statistics, calendar, overdue, and asynchronous-generation-status behavior. It centralizes per-user queryset filtering and performs goal/cache side effects around mutations.

## Classes and configuration

### TaskPagination

Uses page-number pagination with a default page size of 20, a client page-size query parameter, and a maximum page size of 100 (lines 23–26).

### TaskViewSet

- Uses TaskSerializer, IsAuthenticated, and TaskPagination (lines 29–32).
- Searches title and description, and conditionally selects related goal/learning fields (lines 34–42).
- The registered router and project mount are in backend_django/tasks/api/urls.py and backend_django/backend_django/urls.py.

## Query and ownership behavior

get_queryset() starts from Task.objects.filter(user=self.request.user), so standard detail lookups and custom actions that use this queryset are scoped to the authenticated user (lines 54–62). It conditionally applies related-object selection, exact status/priority/relationship filters, date and date-range filters, overdue filtering, case-insensitive title/description search, and a fixed ordering allowlist (lines 64–140). Invalid date query values produce an empty queryset for the date filters rather than a custom error response (lines 80–99).

has_field() checks model metadata and returns false on FieldDoesNotExist (lines 44–49). completed_status_values() derives completion values from model choices, recognizing common labels/values, and falls back to the string completed (lines 142–153).

list() adds a 400 response for a supplied status value that is not in the model's choice values, then delegates valid requests to the parent implementation (lines 192–204).

## Mutation side effects

- Create saves the authenticated user as owner, recalculates the goal when linked, and invalidates that user's dashboard cache (lines 155–163).
- Update captures previous goal/milestone references, saves, recalculates the current task's goal, recalculates an old milestone/goal when relationships changed, then invalidates cache (lines 165–177).
- Delete captures related goal/milestone references, deletes through the parent viewset, recalculates affected progress, and invalidates cache (lines 179–190).
- Cache invalidation delegates to core.cache_utils.invalidate_dashboard for the request user's ID (lines 51–52).

These are source-level call paths; transaction guarantees beyond the explicit actions below are not inferred.

## Custom actions

| Action | Method and route suffix | Behavior and validation | Evidence |
|---|---|---|---|
| today | GET today | Filters the user's queryset to the local current date and returns a paginated or unpaginated serialized list. | Lines 206–221 |
| generate | POST generate | Reads count, async, provider, and model. async must be boolean; count, if present, must convert to an integer from 1 to 100. Defaults async to true. | Lines 223–248 |
| generate, queued path | Celery task dispatch | When async is true, attempts generate_daily_learning_tasks.delay for the request user. Returns queued status and task ID with 202. A dispatch exception is logged and falls through to synchronous generation. | Lines 250–269 |
| generate, synchronous path | Service call | Calls DailyTaskGenerationService.generate. ValidationError/ValueError returns 400; other exceptions are logged and return 500. Success invalidates cache and returns serialized created tasks with 201. | Lines 270–297 |
| complete | POST detail/complete | Validates optional actual_minutes as a non-negative integer; loads the user-scoped object; calls TaskService.complete inside transaction.atomic and schedules cache invalidation on commit. Validation/value errors return 400. | Lines 299–328 |
| postpone | POST detail/postpone | Requires until and accepts a parseable ISO date or datetime. Calls TaskService.postpone atomically and invalidates cache on commit; validation/value errors return 400. | Lines 330–359 |
| start, cancel, reopen | POST detail actions | Delegate to change_status with in_progress, cancelled, or pending respectively. | Lines 361–371 |
| change_status | Internal helper | Resolves a target against choice values/labels. It blocks starting a completed task and reopening a task that is not completed. Successful changes save status, recalculate goal progress, invalidate cache, and serialize the object. | Lines 373–424 |
| stats / progress | GET stats; GET progress | stats aggregates task counts by status and returns total, completed, remaining, completion percentage, and by-status counts. progress delegates to stats. | Lines 426–458 |
| calendar | GET calendar | Parses date_from/date_to, defaults to local today and a 30-day range, rejects invalid or reversed ranges and ranges above 366 days, then returns counts grouped by scheduled date. | Lines 460–501 |
| overdue | GET overdue | Filters tasks scheduled before local today, excludes completed values when the status field exists, and paginates when configured. | Lines 503–524 |
| generation_status | GET generation-status/{task_id} | Reads Celery result metadata and requires its user_id to match the request user. Mismatches return 404; success returns task ID/status and result or failure detail as applicable. Exceptions are logged and return 503. | Lines 526–572 |

Exact router-expanded URLs and standard ModelViewSet method routes depend on DRF router behavior. The source declares the action methods and router registration; no runtime route enumeration was performed.

## Dependencies and data flow

- Imports Task, TaskSerializer, TaskService, DailyTaskGenerationService, and dashboard cache invalidation (lines 13–17).
- Imports GoalService lazily for goal and milestone progress recalculation (lines 155–158, 171–176, 184–189, 420–423).
- Imports the Celery task lazily for generation dispatch/status lookup (lines 252–259 and 535–541).
- The Task model fields and relationships are documented in [task.py.md](../../models/task.py.md).
- The frontend service and verified representative path are described in the [integration map](../../../../../../source_architecture/04_integration/FRONTEND_BACKEND_MAPPING.md).

## Security and error handling

IsAuthenticated is the viewset permission class (line 31). The base queryset filters by the current user (line 55), and generation-status lookup additionally checks the user ID published in result metadata (lines 532–553). Custom actions return explicit 400, 404, 500, or 503 responses on the branches cited above. This is not a complete security audit: global DRF authentication settings, middleware, deployment settings, and Celery result-backend behavior are outside this file.

## Related documentation

- [Backend Tasks API guide](../../../../../../complete_project_documentation/backend/tasks/api.md)
- [Backend Tasks security and testing guide](../../../../../../complete_project_documentation/backend/tasks/security-and-testing.md)
- [Backend Tasks services and workflows](../../../../../../complete_project_documentation/backend/tasks/services-and-workflows.md)
- [Backend architecture](../../../../../02-backend-architecture.md)
- [API and integration map](../../../../../04-api-and-integration-map.md)
- [Frontend/backend mapping](../../../../../04_integration/FRONTEND_BACKEND_MAPPING.md)

## Tests and limitations

The related test module is backend_django/tasks/tests/test_tasks.py. It tests service-driven goal progress and serializer ownership validation, not every viewset action or route. Tests were not run.

No request/response schema is asserted here beyond the explicit request reads and response branches in this source. Serializer behavior and client compatibility should be checked in the serializer and frontend service documentation. API calls, task dispatch, permission enforcement, cache behavior, and database transactions were not runtime verified.
