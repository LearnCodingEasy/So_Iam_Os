# File documentation: Task model

## Identity and status

- **Source:** [backend_django/tasks/models/task.py](../../../../../../backend_django/tasks/models/task.py)
- **Area:** Django application tasks; model module.
- **Purpose:** Defines the persisted task entity used by the Tasks API and task services.
- **Evidence status:** Source behavior below is **VERIFIED** by static inspection. Database/runtime behavior is **NOT RUNTIME VERIFIED**.

## Purpose and responsibilities

Task represents a user-owned item with a scheduled date, optional start time and due timestamp, duration estimates, priority, status, completion/postponement information, recurrence data, and arbitrary metadata. It can optionally link to a goal, goal milestone, learning goal, learning path, learning topic, and skill. The model also defines default ordering, indexes, a display string, and a completion helper.

## Declared structure

### Choices

- Status values: pending, in_progress, completed, cancelled, and postponed.
- Priority values: low, medium, high, and critical.

Evidence: source lines 7–18.

### Fields and relationships

| Field or group | Declaration and behavior | Evidence |
|---|---|---|
| user | Required foreign key to settings.AUTH_USER_MODEL; deleting the user cascades to tasks; reverse name is tasks. | Lines 20–21 |
| goal, milestone | Optional foreign keys to goals.Goal and goals.GoalMilestone; both use SET_NULL; reverse name is tasks. | Lines 22–25 |
| learning_goal, learning_path, learning_topic, skill | Optional foreign keys to the corresponding learning models; all use SET_NULL; reverse name is tasks. | Lines 26–33 |
| title, description | Required CharField title with maximum length 255; blank-allowed text description. | Lines 35–36 |
| Scheduling | scheduled_date defaults to timezone.localdate; scheduled_start and due_at are nullable/blank. | Lines 37–39 |
| Duration | estimated_minutes and actual_minutes are PositiveIntegerField values defaulting to zero. | Lines 40–41 |
| Priority and status | Character fields use the choices above; defaults are medium priority and pending status. | Lines 42–45 |
| Completion and ordering | sort_order defaults to zero; completed_at and postponed_until are nullable/blank. | Lines 46–48 |
| Flexible data | recurrence_rule and metadata are JSON fields with dict defaults and blank=True. | Lines 49–50 |
| Timestamps | created_at is set on insert; updated_at is updated automatically by Django on save. | Lines 51–52 |

No explicit primary-key field is declared in this module. No unique_together or constraints declaration appears in this model's Meta class; this statement is limited to this file.

### Model options

Default ordering is by scheduled_date, sort_order, descending priority, scheduled_start, and created_at. Four indexes are declared:

- user, scheduled_date, status
- user, priority
- goal, status
- learning_topic, status

Evidence: lines 54–62.

## Methods and side effects

- __str__() returns the task title (lines 64–65).
- mark_completed() sets status to COMPLETED, preserves an existing completed_at or assigns the current time, then saves only status, completed_at, and updated_at (lines 67–70). It does not update actual_minutes or recalculate goal progress in this method.

Other completion paths exist in tasks.services.tasks_services.TaskService; that service is responsible for its own validation and goal recalculation. See the existing service guide and API file documentation for those paths.

## Dependencies and relationships

- Imports Django settings for the configured user model, Django ORM fields, and Django timezone utilities (lines 1–3).
- The Tasks API imports this model and scopes its queryset to the authenticated user: [tasks_views.py](../api/views/tasks_views.py.md), source lines 13 and 54–62.
- The serializer exposes and validates model data: backend_django/tasks/api/serializers/tasks_serializers.py.
- TaskService updates completion and postponement state: backend_django/tasks/services/tasks_services.py.
- Goal and learning model definitions are in the goals and learning applications. The foreign-key declarations establish these references; runtime loading and database state were not inspected.

## Validation, security, and error handling

This model declares field types, choices, nullability, blank handling, and defaults. It does not define a custom clean() method or custom validation method in this file. API-level validation is implemented in the serializer and view/service layers and is documented in their existing guides.

The required user foreign key and CASCADE deletion rule express ownership-related persistence behavior. Request authorization and user isolation are enforced in the API layer, not by this model declaration alone.

## Related documentation

- [Tasks model guide](../../../../../complete_project_documentation/backend/tasks/models.md)
- [Tasks service and workflow guide](../../../../../complete_project_documentation/backend/tasks/services-and-workflows.md)
- [Project data architecture](../../../../05-data-architecture.md)
- [Backend architecture](../../../../02-backend-architecture.md)

## Tests and coverage limits

The selected related test file is [test_tasks.py](../../../../../../backend_django/tasks/tests/test_tasks.py); it exercises service-driven goal progress and serializer ownership validation. It does not establish database migration behavior or complete model coverage. Tests were not run for this documentation pilot.

## Static-analysis limitations

This document reflects declarations in this source file and references to inspected callers. It does not establish the active database schema, applied migrations, generated primary-key type, query plans, or runtime behavior. No database, migration, API, or test execution was performed.
