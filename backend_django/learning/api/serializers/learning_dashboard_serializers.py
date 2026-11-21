from rest_framework import serializers
from learning.api.serializers.application_review_serializers import ApplicationReviewSerializer
from learning.api.serializers.learning_goal_serializers import LearningGoalSerializer
from learning.api.serializers.learning_path_serializers import LearningPathSerializer, LearningTopicMinimalSerializer
from learning.api.serializers.learning_progress_serializers import LearningProgressSerializer
from learning.api.serializers.learning_revision_serializers import LearningRevisionSerializer


# ===================================================
# Dashboard Serializer
# ===================================================


class LearningDashboardSerializer(
    serializers.Serializer
):
    """
    Read-only serializer for the main Learning dashboard.

    Expected input:
        {
            "goals": [...],
            "active_paths": [...],
            "recent_topics": [...],
            "progress": [...],
            "reviews": [...],
            "revisions": [...]
        }
    """

    goals = LearningGoalSerializer(
        many=True,
        read_only=True,
    )

    active_paths = LearningPathSerializer(
        many=True,
        read_only=True,
    )

    recent_topics = LearningTopicMinimalSerializer(
        many=True,
        read_only=True,
    )

    progress = LearningProgressSerializer(
        many=True,
        read_only=True,
    )

    reviews = ApplicationReviewSerializer(
        many=True,
        read_only=True,
    )

    revisions = LearningRevisionSerializer(
        many=True,
        read_only=True,
    )
