# Goals, Tasks, Projects, and Challenges

This note covers these related planning domains. Shared architecture and API conventions are in [System Architecture](../01-system-architecture.md), [Backend Architecture](../02-backend-architecture.md), [API and Integration Map](../04-api-and-integration-map.md), and [Data Architecture](../05-data-architecture.md).

## Goals

**VERIFIED:** `backend_django/goals/models/` defines goals, milestones, activity, and plan proposals. `goals/api/views/goals_views.py` and `goals/services/` implement user-scoped listing, state/progress operations, analytics, history, coaching/plan proposal paths, and related actions. The Vue Goals view and service live in `frontend_vue/src/views/goals/Goals.vue` and `frontend_vue/src/services/Goals/goals.js`.

## Tasks

**VERIFIED:** `backend_django/tasks/models/task.py` defines user-owned tasks and references goals/milestones and learning entities. `tasks/api/views/tasks_views.py` implements CRUD and actions including today, generation, complete, postpone, start, cancel, reopen, stats, calendar, and overdue. Task services and scheduled generation are in `backend_django/tasks/services/` and `tasks/tasks.py`. Vue task views and services are under `frontend_vue/src/views/tasks/` and `frontend_vue/src/services/Tasks/`.

**UNKNOWN:** The task model stores recurrence-related data, but an active recurrence processor was not established in the inspected task implementation.

## Projects

**VERIFIED:** Project, member, context, goal-link, and task-link records are defined under `backend_django/projects/models/`. API wiring is in `projects/api/`; the routed Vue feature is `frontend_vue/src/views/projects/ProjectsView.vue` with `services/Projects/projects.js` and a Pinia store.

## Challenges

**VERIFIED:** `backend_django/challenges/models/` represents challenges, steps, attempts, and user progress. API view/serializer code is under `challenges/api/`; `frontend_vue/src/views/challenges/ChallengesView.vue` calls the challenges service.

## Cross-domain relationships

**VERIFIED:** Tasks reference goals/milestones and learning goal/path/topic/skill records (`backend_django/tasks/models/task.py`). Goals relate to learning goals and skills (`goals/models/goal.py`). Projects link to goals and tasks (`projects/models/project_goal.py`, `project_task.py`). Challenges optionally reference goals, projects, and learning skills (`challenges/models/challenge.py`).

These are schema and code relationships; they do not prove all linked operations are coordinated atomically or surfaced throughout the UI.

## Domain-specific gaps

- **PARTIAL:** Goal AI plans are represented as proposals; source explicitly records that proposing a plan does not itself create tasks or milestones (`backend_django/goals/api/views/goals_views.py`).
- **UNKNOWN:** Full recurrence semantics, cross-domain progress consistency, and all challenge lifecycle transitions.
- **INFERRED recommendation:** Keep goal/task/project ownership and derived progress rules explicit; shared data and permission risks are covered in [Data Architecture](../05-data-architecture.md) and [Security and Operations](../06-security-and-operations.md).
