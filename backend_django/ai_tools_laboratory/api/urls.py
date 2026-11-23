from rest_framework.routers import DefaultRouter

from ai_tools_laboratory.api.views import ToolCategoryViewSet, ToolViewSet, ToolConfigurationViewSet, ToolExecutionViewSet

router = DefaultRouter()
router.register('categories', ToolCategoryViewSet, basename='tool-category')
router.register('tools', ToolViewSet, basename='tool')
router.register('configurations', ToolConfigurationViewSet, basename='tool-configuration')
router.register('executions', ToolExecutionViewSet, basename='tool-execution')

urlpatterns = router.urls
