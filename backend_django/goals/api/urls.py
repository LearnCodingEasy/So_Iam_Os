from rest_framework.routers import DefaultRouter
from goals.api.views import GoalMilestoneViewSet, GoalViewSet

router = DefaultRouter()
router.register(r"milestones", GoalMilestoneViewSet, basename="goal-milestone")
router.register(r"", GoalViewSet, basename="goal")
urlpatterns = router.urls
