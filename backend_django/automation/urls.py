
# backend_django/automation/urls.py

from django.urls import path, include

from rest_framework.routers import DefaultRouter


from .views import (
    ProgramViewSet,
    ProgramElementViewSet,
    WorkflowViewSet,
    WorkflowNodeViewSet,
    WorkflowEdgeViewSet,
    ActionViewSet,
    TaskViewSet,
    TaskRunViewSet,
    ScreenStateViewSet,
    DelayViewSet,
    get_open_windows
)

# ==================================================
# 🚦 DRF Router
# ==================================================
router = DefaultRouter()


# ==================================================
# 1️⃣ Program (فتح / غلق البرامج)
# ==================================================
router.register(r'programs', ProgramViewSet, basename='program')

# ==================================================
# 2️⃣ Program Elements (أزرار – منيو – عناصر)
# ==================================================
router.register(r'program-elements', ProgramElementViewSet,
                basename='program-element')

# ==================================================
# 3️⃣ Workflow (العقل الأساسي)
# ==================================================
router.register(r'workflows', WorkflowViewSet, basename='workflows')

# ==================================================
# 4️⃣ Workflow Nodes (Vue Flow Nodes)
# ==================================================
router.register(r'workflow-nodes', WorkflowNodeViewSet,
                basename='workflow-node')

# ==================================================
# 5️⃣ Workflow Edges (الربط بين النودز)
# ==================================================
router.register(r'workflow-edges', WorkflowEdgeViewSet,
                basename='workflow-edge')

# ==================================================
# 6️⃣ Actions (الأوامر الفعلية)
# ==================================================
router.register(r'actions', ActionViewSet, basename='action')

# ==================================================
# 7️⃣ Tasks
# ==================================================
router.register(r'tasks', TaskViewSet, basename='task')

# ==================================================
# 8️⃣ Task Runs (التنفيذ + اللوجز)
# ==================================================
router.register(r'task-runs', TaskRunViewSet, basename='task-run')

# ==================================================
# 9️⃣ ScreenState 🎥 (مهم جداً للمونتاج)
# ==================================================
router.register(r'screen-states', ScreenStateViewSet, basename='screen-state')

# ==================================================
# 🔟 Delay ⏱️
# ==================================================
router.register(r'delays', DelayViewSet, basename='delay')

# ==================================================
# 🌍 URL Patterns
# ==================================================
urlpatterns = [
    path('', include(router.urls)),
    path('get_open_windows/', get_open_windows,
         name='get_open_windows'),

]
