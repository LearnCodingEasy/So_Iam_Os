# Shared Infrastructure Catalogue

> Static inventory of cross-cutting infrastructure locations. Presence does not prove every app uses each facility.

## `backend_django/backend_django/` (6 source files)

- `backend_django/backend_django/celery.py`
- `backend_django/backend_django/settings.py`
- `backend_django/backend_django/urls.py`
- `backend_django/backend_django/asgi.py`
- `backend_django/backend_django/wsgi.py`
- `backend_django/backend_django/__init__.py`

## `backend_django/core/` (33 source files)

- `backend_django/core/signals.py`
- `backend_django/core/constants.py`
- `backend_django/core/cache_utils.py`
- `backend_django/core/admin.py`
- `backend_django/core/apps.py`
- `backend_django/core/permissions.py`
- `backend_django/core/utils.py`
- `backend_django/core/pagination.py`
- `backend_django/core/managers.py`
- `backend_django/core/exceptions.py`
- `backend_django/core/__init__.py`
- `backend_django/core/tests/test_api_contract.py`
- `backend_django/core/tests/tests_learning_settings.py`
- `backend_django/core/tests/test_core.py`
- `backend_django/core/tests/__init__.py`
- `backend_django/core/models/base_model.py`
- `backend_django/core/models/user_learning_settings.py`
- `backend_django/core/models/__init__.py`
- `backend_django/core/api/owned.py`
- `backend_django/core/api/urls.py`
- `backend_django/core/api/__init__.py`
- `backend_django/core/migrations/__init__.py`
- `backend_django/core/migrations/0001_initial.py`
- `backend_django/core/debug_console/routing.py`
- `backend_django/core/debug_console/consumers.py`
- `backend_django/core/debug_console/handlers.py`
- `backend_django/core/debug_console/__init__.py`
- `backend_django/core/services/core_services.py`
- `backend_django/core/services/__init__.py`
- `backend_django/core/api/views/core_views.py`
- `backend_django/core/api/views/__init__.py`
- `backend_django/core/api/serializers/__init__.py`
- `backend_django/core/api/serializers/core_serializers.py`

## `frontend_vue/src/services/` (41 source files)

- `frontend_vue/src/services/Jobs/jobs.js`
- `frontend_vue/src/services/AI/sse.js`
- `frontend_vue/src/services/AI/aiControl.js`
- `frontend_vue/src/services/AI/aiPlatformService.js`
- `frontend_vue/src/services/AI/Ai.js`
- `frontend_vue/src/services/AI/AIService.js`
- `frontend_vue/src/services/Knowledge/Knowledge.js`
- `frontend_vue/src/services/Accounts/usersAccounts.js`
- `frontend_vue/src/services/Notifications/notifications.js`
- `frontend_vue/src/services/Analytics/Analytics.js`
- `frontend_vue/src/services/AI_Tools_Laboratory/AI_Tools_Laboratory.js`
- `frontend_vue/src/services/Marketing/Marketing.js`
- `frontend_vue/src/services/Revenue/Revenue.js`
- `frontend_vue/src/services/Shared/explainsService.js`
- `frontend_vue/src/services/Shared/api.js`
- `frontend_vue/src/services/Shared/product_services.js`
- `frontend_vue/src/services/Shared/endpoints.js`
- `frontend_vue/src/services/Shared/axiosInstance.js`
- `frontend_vue/src/services/Shared/ecosystemApi.js`
- `frontend_vue/src/services/Shared/mcpService.js`
- `frontend_vue/src/services/Codex/codex.js`
- `frontend_vue/src/services/Core/dashboard.js`
- `frontend_vue/src/services/Core/settings.js`
- `frontend_vue/src/services/Learning/learning.js`
- `frontend_vue/src/services/Architecture/Architecture.js`
- `frontend_vue/src/services/Sales/Sales.js`
- `frontend_vue/src/services/Challenges/challenges.js`
- `frontend_vue/src/services/Projects/projects.js`
- `frontend_vue/src/services/Social/social.js`
- `frontend_vue/src/services/Finance/finance.js`
- `frontend_vue/src/services/Goals/goals.js`
- `frontend_vue/src/services/Tasks/tasks.js`
- `frontend_vue/src/services/Memory/memory.js`
- `frontend_vue/src/services/Agents/Agents.js`
- `frontend_vue/src/services/CRM/CRM.js`
- `frontend_vue/src/services/Scraper/scraperApi.js`
- `frontend_vue/src/services/Automation/AutomationService.js`
- `frontend_vue/src/services/Automation/nodeStorageService.js`
- `frontend_vue/src/services/Automation/workflowService.js`
- `frontend_vue/src/services/Automation/taskService.js`
- `frontend_vue/src/services/AI/__tests__/AIService.spec.js`

## `frontend_vue/src/stores/` (32 source files)

- `frontend_vue/src/stores/challenges/challengesStore.js`
- `frontend_vue/src/stores/projects/projects.js`
- `frontend_vue/src/stores/analytics/analyticsStore.js`
- `frontend_vue/src/stores/crm/crmStore.js`
- `frontend_vue/src/stores/codex/codex.js`
- `frontend_vue/src/stores/shared/primeTheme.js`
- `frontend_vue/src/stores/shared/counter.js`
- `frontend_vue/src/stores/ai/useAIStore.js`
- `frontend_vue/src/stores/marketing/marketingStore.js`
- `frontend_vue/src/stores/ai_tools_laboratory/aiToolsLaboratoryStore.js`
- `frontend_vue/src/stores/automation/useWorkflowStore.js`
- `frontend_vue/src/stores/automation/useProgramElementStore.js`
- `frontend_vue/src/stores/automation/useProgramStore.js`
- `frontend_vue/src/stores/automation/useTaskStore.js`
- `frontend_vue/src/stores/sales/salesStore.js`
- `frontend_vue/src/stores/goals/goalsStore.js`
- `frontend_vue/src/stores/knowledge/knowledgeStore.js`
- `frontend_vue/src/stores/revenue/revenueStore.js`
- `frontend_vue/src/stores/agents/agentsStore.js`
- `frontend_vue/src/stores/accounts/user.js`
- `frontend_vue/src/stores/architecture/architectureStore.js`
- `frontend_vue/src/stores/architecture/__tests__/architectureStore.spec.js`
- `frontend_vue/src/stores/agents/__tests__/agentsStore.spec.js`
- `frontend_vue/src/stores/revenue/__tests__/revenueStore.spec.js`
- `frontend_vue/src/stores/knowledge/__tests__/knowledgeStore.spec.js`
- `frontend_vue/src/stores/goals/__tests__/goalsStore.spec.js`
- `frontend_vue/src/stores/sales/__tests__/salesStore.spec.js`
- `frontend_vue/src/stores/ai_tools_laboratory/__tests__/aiToolsLaboratoryStore.spec.js`
- `frontend_vue/src/stores/marketing/__tests__/marketingStore.spec.js`
- `frontend_vue/src/stores/crm/__tests__/crmStore.spec.js`
- `frontend_vue/src/stores/analytics/__tests__/analyticsStore.spec.js`
- `frontend_vue/src/stores/challenges/__tests__/challengesStore.spec.js`

## `frontend_vue/src/router/` (1 source files)

- `frontend_vue/src/router/index.js`

## `frontend_vue/src/composables/` (8 source files)

- `frontend_vue/src/composables/useAppToast.js`
- `frontend_vue/src/composables/useToastHelper.js`
- `frontend_vue/src/composables/useTheme.js`
- `frontend_vue/src/composables/usePrograms.js`
- `frontend_vue/src/composables/useApiTracker.js`
- `frontend_vue/src/composables/useNodeDragDrop.js`
- `frontend_vue/src/composables/useAsyncAction.js`
- `frontend_vue/src/composables/useAI.js`

## `frontend_vue/src/utils/` (1 source files)

- `frontend_vue/src/utils/apiError.js`
