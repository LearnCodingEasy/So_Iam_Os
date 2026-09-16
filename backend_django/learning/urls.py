from rest_framework.routers import DefaultRouter

from .views import (
    SkillViewSet,
    LearningGoalViewSet,
    LearningPathViewSet,
    LearningTopicViewSet,
    LearningProgressViewSet,
    AssessmentViewSet,
    AssessmentAttemptViewSet,
    KnowledgeApplicationViewSet,
)

router = DefaultRouter()

router.register(
    r"skills",
    SkillViewSet,
    basename="learning-skill",
)

router.register(
    r"goals",
    LearningGoalViewSet,
    basename="learning-goal",
)

router.register(
    r"paths",
    LearningPathViewSet,
    basename="learning-path",
)

router.register(
    r"topics",
    LearningTopicViewSet,
    basename="learning-topic",
)

router.register(
    r"progress",
    LearningProgressViewSet,
    basename="learning-progress",
)

router.register(
    r"assessments",
    AssessmentViewSet,
    basename="learning-assessment",
)

router.register(
    r"assessment-attempts",
    AssessmentAttemptViewSet,
    basename="learning-assessment-attempt",
)

router.register(
    r"applications",
    KnowledgeApplicationViewSet,
    basename="learning-application",
)

urlpatterns = router.urls
