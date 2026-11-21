# File documentation: TodayTasks view

## Identity and status

- **Source:** [frontend_vue/src/views/tasks/TodayTasks.vue](../../../../../../../frontend_vue/src/views/tasks/TodayTasks.vue)
- **Area:** Frontend tasks domain; routed Vue view.
- **Purpose:** Displays and manages the current user's tasks scheduled for today.
- **Evidence status:** Component behavior is **VERIFIED** by static inspection. UI/API runtime behavior is **NOT RUNTIME VERIFIED**.

## Route and responsibility

The router maps /tasks/today to this view as the today-tasks route and marks it requiresAuth (frontend_vue/src/router/index.js, lines 152–155). This component does not implement the route guard itself.

The page loads today's tasks, filters them locally, shows a completion summary, and exposes create/edit, complete, reopen, postpone, delete, and generation actions. The template contains the task list, summary panel, task form dialog, and postpone dialog (template lines 1–125).

## Component interface and state

The file uses script setup and Vue's computed, onMounted, reactive, and ref APIs (lines 126–128). No props or emitted events are declared in this file. State is local to this component; no Pinia store is imported.

| State or derived value | Role | Evidence |
|---|---|---|
| tasks | Loaded task records. | Lines 138–149 |
| loading, error, success | Request and user feedback state. | Lines 138–149 |
| dialog, editing, form | Create/edit dialog state and editable task values. | Lines 138–158, 190–216 |
| postponeDialog, postponing, postponeDate | Postpone dialog state and selected task/date. | Lines 138–149, 256–260 |
| busyTaskId, generating | Prevents overlapping task actions and repeated generation clicks in the relevant handlers. | Lines 148–149, 167–178, 230–282 |
| completed, completion, estimated | Computed summary values from the loaded task array. | Lines 159–163 |
| visibleTasks | Applies the selected status filter locally; all shows every loaded task. | Lines 144, 164–166 |

The form initializes scheduled_date from the ISO string of the current JavaScript Date and uses medium/pending defaults (lines 150–158). Because the date is taken from toISOString(), a local-date difference near a timezone boundary is a potential behavior to verify; this is an **INFERRED** risk, not a tested defect.

## User actions and data flow

- **Load:** onMounted calls load(). load() sets loading, clears the error, calls listTodayTasks(), stores the returned array, and maps an Axios-style response detail or fallback text to the error state (lines 179–189, 284).
- **Generate:** calls generateTodayTasks({ async: true }); on success it shows a queued message and schedules one load() call after 1.5 seconds. This component does not call the generation-status service or poll for completion (lines 167–178).
- **Create/edit:** openCreate resets the form; editTask copies selected task values into it. save() normalizes an empty scheduled_start to null, calls createTask or updateTask, closes the dialog and reloads on success (lines 190–228).
- **Complete:** finish() uses actual_minutes, then estimated_minutes, then zero; it calls completeTask and reloads on success. It exits when another task action is marked busy (lines 230–241).
- **Reopen:** calls reopenTask and reloads on success (lines 242–255).
- **Postpone:** openPostpone selects the task and proposes tomorrow's date. postpone() calls postponeTask with the selected ID/date and reloads on success (lines 256–271).
- **Delete:** removeTask asks for browser confirmation, calls deleteTask, reloads on success, and clears the busy task ID in finally (lines 273–283).

These handlers consume methods from services/Tasks/tasks.js; that service delegates to the shared API client and endpoint registry.

## Dependencies and error handling

The component imports eight functions from @/services/Tasks/tasks: completeTask, createTask, deleteTask, listTodayTasks, postponeTask, updateTask, generateTodayTasks, and reopenTask (lines 128–137). It has no direct Axios import.

Most handlers catch errors and display e.response?.data?.detail when present, otherwise a local fallback string. The delete handler also catches failures; save has no explicit busy guard, while the other task handlers use busyTaskId guards or state as shown above. The service/client layers may add behavior outside this file.

## Security and accessibility notes

The route metadata requires authentication, but this is frontend navigation metadata and does not replace backend authorization. Backend user scoping and permissions are covered by the API guide and viewset document.

The template uses native buttons, inputs, selects, forms, labels, and browser confirmation. This static review does not verify keyboard navigation, screen-reader announcements, focus handling in dialogs, or rendered text encoding.

## Related documentation

- [Frontend Tasks route and view guide](../../../../../../complete_project_documentation/frontend/tasks/views-and-routes.md)
- [Frontend Tasks workflow guide](../../../../../../complete_project_documentation/frontend/tasks/workflows.md)
- [Frontend Tasks service guide](../../../../../../complete_project_documentation/frontend/tasks/services-and-api.md)
- [Frontend architecture](../../../../../03-frontend-architecture.md)
- [API and integration map](../../../../../04-api-and-integration-map.md)
- [Frontend/backend mapping](../../../../../04_integration/FRONTEND_BACKEND_MAPPING.md)
- [Tasks service file documentation](../../services/Tasks/tasks.js.md)

## Tests and limitations

No test file was identified as a direct component test for this view in the inspected task-domain guides. The backend test module covers service progress and serializer ownership behavior, not this Vue component. No frontend tests were run.

This document describes source-level state and handlers only. It does not establish route-guard execution, successful API requests, actual UI rendering, time-zone outcomes, or asynchronous generation completion.
