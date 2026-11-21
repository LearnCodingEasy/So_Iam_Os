# File documentation: Tasks integration tests

## Identity and status

- **Source:** [backend_django/tasks/tests/test_tasks.py](../../../../../../backend_django/tasks/tests/test_tasks.py)
- **Area:** Django application tasks; automated tests.
- **Main declaration:** TaskIntegrationTests.
- **Evidence status:** Test setup and assertions are **VERIFIED** from source. Test execution and coverage are **NOT RUNTIME VERIFIED**.

## Purpose and test setup

This Django TestCase module contains two integration-focused tests. setUp() creates two users to distinguish the task owner from another user (lines 14–17). The file imports Django TestCase and project models, TaskSerializer, and TaskService (lines 1–11).

## Test cases

### Goal progress follows task completion

test_completing_tasks_recalculates_goal_progress_from_real_tasks() creates a goal and two tasks for the same user, completes one through TaskService, refreshes the goal, and asserts 50 percent progress with ACTIVE status. It then completes the second task and asserts 100 percent progress, COMPLETED status, and a non-null completed_at value (lines 19–34).

This verifies the assertions made by this test when run in its configured Django environment; it does not establish that all goal/task relationships or completion paths are covered.

### Serializer rejects a learning topic owned by another user

test_task_serializer_rejects_learning_topic_owned_by_another_user() creates a skill and learning goal/path/topic owned by the second user. It constructs a request-like object for the first user, validates a TaskSerializer payload that refers to the other user's topic, then asserts validation fails and includes a learning_topic error (lines 36–48).

This test exercises serializer ownership validation directly. It does not call the Tasks API viewset or prove endpoint authorization behavior.

## Inputs, outputs, and side effects

- **Inputs:** Test database records for two users, a goal, tasks, and learning entities; a request-like object with a user; serializer data containing a learning-topic primary key.
- **Operations:** Calls TaskService.complete for two tasks and TaskSerializer.is_valid for the ownership case.
- **Observed assertions:** Goal progress/status/completion timestamp and serializer validity/error key.
- **Side effects:** TestCase database writes are made by setup and each test. Django's TestCase transaction/test-database behavior was not executed or independently validated here.

## Dependencies and observations

- Imports Goal, learning models, Task, TaskSerializer, TaskService, and the configured User model.
- The model behavior is documented in [Task model file documentation](../models/task.py.md).
- View-level authorization and request handling are documented in [TaskViewSet file documentation](../api/views/tasks_views.py.md).
- GoalService is imported at line 6 but is not referenced elsewhere in this file; this is a static observation, not a lint result.

## Related documentation

- [Backend Tasks security and testing guide](../../../../../complete_project_documentation/backend/tasks/security-and-testing.md)
- [Backend Tasks service and workflow guide](../../../../../complete_project_documentation/backend/tasks/services-and-workflows.md)
- [Backend architecture](../../../../02-backend-architecture.md)
- [Data architecture](../../../../05-data-architecture.md)
- [Task model file documentation](../models/task.py.md)
- [TaskViewSet file documentation](../api/views/tasks_views.py.md)

## Coverage limits and runtime status

This file contains two test methods. That count is not a coverage percentage and does not show which tests pass. The tests cover goal progress through TaskService.complete and serializer rejection for one cross-user learning-topic association. They do not directly test the viewset actions, pagination, filters, Celery dispatch/status, cache invalidation, API responses, or frontend behavior.

The test suite was not run for this documentation pilot. Database state, migrations, fixture behavior, and runtime outcomes remain **NOT RUNTIME VERIFIED**.
