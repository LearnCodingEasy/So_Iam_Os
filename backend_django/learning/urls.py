from rest_framework.routers import DefaultRouter

from .views import (
    SkillViewSet,
    LearningGoalViewSet,
    LearningPathViewSet,
    LearningTopicViewSet,
    LessonViewSet,
    LearningResourceViewSet,
    LearningNoteViewSet,
    LearningProgressViewSet,
    LearningSessionViewSet,
    AssessmentViewSet,
    AssessmentQuestionViewSet,
    AssessmentChoiceViewSet,
    AssessmentAttemptViewSet,
    AssessmentResponseViewSet,
    KnowledgeApplicationViewSet,
    ApplicationSubmissionViewSet,
    ApplicationReviewViewSet,
    LearningRevisionViewSet,
)


router = DefaultRouter()


# ====================================================
# 🧠 Skills
# ====================================================

router.register(
    r"skills",
    SkillViewSet,
    basename="skill",
)


# ====================================================
# 🎯 Learning Goals
# ====================================================

router.register(
    r"goals",
    LearningGoalViewSet,
    basename="learning-goal",
)


# ====================================================
# 🛣️ Learning Paths
# ====================================================

router.register(
    r"paths",
    LearningPathViewSet,
    basename="learning-path",
)


# ====================================================
# 📚 Learning Topics
# ====================================================

router.register(
    r"topics",
    LearningTopicViewSet,
    basename="learning-topic",
)


# ====================================================
# 📖 Lessons
# ====================================================

router.register(
    r"lessons",
    LessonViewSet,
    basename="lesson",
)


# ====================================================
# 🔗 Learning Resources
# ====================================================

router.register(
    r"resources",
    LearningResourceViewSet,
    basename="learning-resource",
)


# ====================================================
# 📝 Learning Notes
# ====================================================

router.register(
    r"notes",
    LearningNoteViewSet,
    basename="learning-note",
)


# ====================================================
# 📊 Learning Progress
# ====================================================

router.register(
    r"progress",
    LearningProgressViewSet,
    basename="learning-progress",
)


# ====================================================
# ⏱️ Learning Sessions
# ====================================================

router.register(
    r"sessions",
    LearningSessionViewSet,
    basename="learning-session",
)


# ====================================================
# 🧪 Assessments
# ====================================================

router.register(
    r"assessments",
    AssessmentViewSet,
    basename="assessment",
)


# ====================================================
# ❓ Assessment Questions
# ====================================================

router.register(
    r"assessment-questions",
    AssessmentQuestionViewSet,
    basename="assessment-question",
)


# ====================================================
# 🔘 Assessment Choices
# ====================================================

router.register(
    r"assessment-choices",
    AssessmentChoiceViewSet,
    basename="assessment-choice",
)


# ====================================================
# 📈 Assessment Attempts
# ====================================================

router.register(
    r"assessment-attempts",
    AssessmentAttemptViewSet,
    basename="assessment-attempt",
)


# ====================================================
# ✍️ Assessment Responses
# ====================================================

router.register(
    r"assessment-responses",
    AssessmentResponseViewSet,
    basename="assessment-response",
)


# ====================================================
# 🧠 Knowledge Applications
# ====================================================

router.register(
    r"applications",
    KnowledgeApplicationViewSet,
    basename="knowledge-application",
)


# ====================================================
# 📦 Application Submissions
# ====================================================

router.register(
    r"application-submissions",
    ApplicationSubmissionViewSet,
    basename="application-submission",
)


# ====================================================
# 🤖 Application Reviews
# ====================================================

router.register(
    r"application-reviews",
    ApplicationReviewViewSet,
    basename="application-review",
)


# ====================================================
# 🔄 Learning Revisions
# ====================================================

router.register(
    r"revisions",
    LearningRevisionViewSet,
    basename="learning-revision",
)


urlpatterns = router.urls
