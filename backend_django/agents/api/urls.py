from rest_framework.routers import DefaultRouter

from agents.api.views import AgentViewSet, AgentConfigurationViewSet, AgentRunViewSet, AgentExecutionViewSet

router = DefaultRouter()
router.register('agents', AgentViewSet, basename='agent')
router.register('configurations', AgentConfigurationViewSet, basename='agent-configuration')
router.register('runs', AgentRunViewSet, basename='agent-run')
router.register('executions', AgentExecutionViewSet, basename='agent-execution')

urlpatterns = router.urls
