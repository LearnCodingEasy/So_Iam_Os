# Backend–Frontend Integration Matrix

| Backend Feature | API Endpoint | Frontend Integration | Test Result |
|---|---|---|---|
| ai | `/api/ai/agents/plan/` | `frontend_vue/src/services/ai.js + AIService.js + composables/useAI.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| ai | `/api/ai/topic-chat/` | `frontend_vue/src/services/ai.js + AIService.js + composables/useAI.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| ai | `/api/ai/chat/` | `frontend_vue/src/services/ai.js + AIService.js + composables/useAI.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| ai | `/api/ai/conversations/` | `frontend_vue/src/services/ai.js + AIService.js + composables/useAI.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| ai | `/api/ai/conversations/<int:pk>/` | `frontend_vue/src/services/ai.js + AIService.js + composables/useAI.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| ai | `/api/ai/settings/` | `frontend_vue/src/services/ai.js + AIService.js + composables/useAI.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| ai | `/api/ai/credentials/` | `frontend_vue/src/services/ai.js + AIService.js + composables/useAI.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| ai | `/api/ai/credentials/<str:provider>/` | `frontend_vue/src/services/ai.js + AIService.js + composables/useAI.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| ai | `/api/ai/providers/<str:provider>/models/` | `frontend_vue/src/services/ai.js + AIService.js + composables/useAI.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| ai | `/api/ai/prompts/` | `frontend_vue/src/services/ai.js + AIService.js + composables/useAI.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| ai | `/api/ai/prompts/<int:pk>/` | `frontend_vue/src/services/ai.js + AIService.js + composables/useAI.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| ai | `/api/ai/learning/preview/` | `frontend_vue/src/services/ai.js + AIService.js + composables/useAI.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| ai | `/api/ai/learning/approve/` | `frontend_vue/src/services/ai.js + AIService.js + composables/useAI.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| ai | `/api/ai/learning/async/` | `frontend_vue/src/services/ai.js + AIService.js + composables/useAI.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| ai | `/api/ai/tasks/<str:task_id>/` | `frontend_vue/src/services/ai.js + AIService.js + composables/useAI.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/skills/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/skills/<pk>/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/goals/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/goals/<pk>/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/goals/generate/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/goals/dashboard/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/goals/<pk>/complete/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/goals/<pk>/pause/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/goals/<pk>/resume/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/goals/<pk>/certificate/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/goals/<pk>/export-plan/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/paths/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/paths/<pk>/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/paths/<pk>/start/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/paths/<pk>/complete/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/paths/<pk>/pause/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/paths/<pk>/analytics/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/paths/<pk>/reorder-topics/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/topics/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/topics/<pk>/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/topics/<pk>/start/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/topics/<pk>/complete/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/topics/<pk>/skip/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/topics/<pk>/bookmark/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/topics/<pk>/generate-content/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/lessons/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/lessons/<pk>/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/lessons/<pk>/mark-complete/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/resources/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/resources/<pk>/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/notes/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/notes/<pk>/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/progress/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/progress/<pk>/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/progress/update-progress/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/progress/summary/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/sessions/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/sessions/<pk>/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/sessions/<pk>/finish/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/assessments/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/assessments/<pk>/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/assessments/<pk>/learner/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/assessments/<pk>/analytics/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/assessments/<pk>/start/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/assessments/<pk>/submit/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/assessment-questions/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/assessment-questions/<pk>/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/assessment-choices/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/assessment-choices/<pk>/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/assessment-attempts/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/assessment-attempts/<pk>/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/assessment-responses/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/assessment-responses/<pk>/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/applications/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/applications/<pk>/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/applications/<pk>/submit/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/applications/<pk>/review/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/applications/<pk>/request-peer-review/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/applications/<pk>/submit-peer-review/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/applications/<pk>/history/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/application-submissions/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/application-submissions/<pk>/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/application-reviews/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/application-reviews/<pk>/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/revisions/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/revisions/<pk>/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/revisions/<pk>/start/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/revisions/<pk>/complete/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/revisions/<pk>/snooze/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| learning | `/api/learning/revisions/<pk>/skip/` | `frontend_vue/src/services/learning.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| knowledge | `/api/knowledge/items/` | `frontend_vue/src/services/knowledge.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| knowledge | `/api/knowledge/items/<pk>/` | `frontend_vue/src/services/knowledge.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| knowledge | `/api/knowledge/items/<pk>/extract-metadata/` | `frontend_vue/src/services/knowledge.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| knowledge | `/api/knowledge/items/<pk>/archive/` | `frontend_vue/src/services/knowledge.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| knowledge | `/api/knowledge/items/<pk>/restore/` | `frontend_vue/src/services/knowledge.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| knowledge | `/api/knowledge/items/<pk>/connect-topic/` | `frontend_vue/src/services/knowledge.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| knowledge | `/api/knowledge/items/<pk>/disconnect-topic/` | `frontend_vue/src/services/knowledge.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| knowledge | `/api/knowledge/items/<pk>/files/` | `frontend_vue/src/services/knowledge.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| knowledge | `/api/knowledge/items/<pk>/upload-file/` | `frontend_vue/src/services/knowledge.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| knowledge | `/api/knowledge/items/archive-all/` | `frontend_vue/src/services/knowledge.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| knowledge | `/api/knowledge/files/` | `frontend_vue/src/services/knowledge.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| knowledge | `/api/knowledge/files/<pk>/` | `frontend_vue/src/services/knowledge.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| tasks | `/api/tasks/` | `frontend_vue/src/services/tasks.js + taskService.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| tasks | `/api/tasks/<pk>/` | `frontend_vue/src/services/tasks.js + taskService.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| tasks | `/api/tasks/today/` | `frontend_vue/src/services/tasks.js + taskService.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| tasks | `/api/tasks/generate/` | `frontend_vue/src/services/tasks.js + taskService.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| tasks | `/api/tasks/<pk>/complete/` | `frontend_vue/src/services/tasks.js + taskService.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| tasks | `/api/tasks/<pk>/postpone/` | `frontend_vue/src/services/tasks.js + taskService.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| tasks | `/api/tasks/<pk>/start/` | `frontend_vue/src/services/tasks.js + taskService.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| tasks | `/api/tasks/<pk>/cancel/` | `frontend_vue/src/services/tasks.js + taskService.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| tasks | `/api/tasks/<pk>/reopen/` | `frontend_vue/src/services/tasks.js + taskService.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| tasks | `/api/tasks/stats/` | `frontend_vue/src/services/tasks.js + taskService.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| tasks | `/api/tasks/progress/` | `frontend_vue/src/services/tasks.js + taskService.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| tasks | `/api/tasks/calendar/` | `frontend_vue/src/services/tasks.js + taskService.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| tasks | `/api/tasks/overdue/` | `frontend_vue/src/services/tasks.js + taskService.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
| tasks | `/api/tasks/generation-status/(?P<task_id>[^/.]+)/` | `frontend_vue/src/services/tasks.js + taskService.js` | `STATIC-AUDIT PASS / RUNTIME PENDING` |
