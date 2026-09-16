from rest_framework import serializers

from .models import (
    Skill,
    LearningGoal,
    LearningPath,
    LearningTopic,
    LearningProgress,
    Assessment,
    AssessmentAttempt,
    KnowledgeApplication,
    ApplicationReview,
)


class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "category",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class LearningGoalSerializer(serializers.ModelSerializer):

    class Meta:
        model = LearningGoal

        fields = [
            "id",
            "title",
            "description",
            "skill",
            "reason",
            "target_level",
            "status",
            "target_date",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class LearningPathSerializer(serializers.ModelSerializer):

    class Meta:
        model = LearningPath

        fields = [
            "id",
            "goal",
            "title",
            "description",
            "status",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class LearningTopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = LearningTopic

        fields = [
            "id",
            "path",
            "skill",
            "title",
            "description",
            "order",
            "status",
            "estimated_minutes",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_order(self, value):

        if value < 1:
            raise serializers.ValidationError(
                "Order must start from 1."
            )

        return value


class AssessmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assessment

        fields = [
            "id",
            "topic",
            "title",
            "description",
            "assessment_type",
            "passing_score",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class AssessmentAttemptSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = AssessmentAttempt

        fields = [
            "id",
            "assessment",
            "score",
            "passed",
            "feedback",
            "attempted_at",
        ]

        read_only_fields = [
            "id",
            "passed",
            "attempted_at",
        ]


class ApplicationReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplicationReview
        fields = [
            "id",
            "score",
            "mastery_level",
            "understood",
            "applied",
            "strengths",
            "weaknesses",
            "errors",
            "needs_review",
            "feedback",
            "ai_metadata",
            "reviewed_by",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class KnowledgeApplicationSerializer(serializers.ModelSerializer):

    review = ApplicationReviewSerializer(
        read_only=True
    )

    class Meta:
        model = KnowledgeApplication

        fields = [
            "id",
            "topic",
            "knowledge_item",
            "title",
            "content",
            "status",
            "submitted_at",
            "reviewed_at",
            "review",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "user",
            "status",
            "submitted_at",
            "reviewed_at",
            "review",
            "created_at",
            "updated_at",
        ]


class LearningProgressSerializer(serializers.ModelSerializer):

    class Meta:
        model = LearningProgress

        fields = [
            "id",
            "topic",
            "user",
            "progress_percent",
            "practice_completed",
            "notes",
            "mastery_level",
            "last_ai_score",
            "needs_review",
            "last_activity_at",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "user",
            "last_ai_score",
            "mastery_level",
            "needs_review",
            "last_activity_at",
            "created_at",
            "updated_at",
        ]


class LearningTopicDetailSerializer(serializers.ModelSerializer):

    progress = serializers.SerializerMethodField()

    knowledge_items = serializers.SerializerMethodField()

    applications = serializers.SerializerMethodField()

    assessments = serializers.SerializerMethodField()

    path = serializers.SerializerMethodField()

    class Meta:
        model = LearningTopic

        fields = [
            "id",
            "path",
            "skill",
            "title",
            "description",
            "order",
            "status",
            "estimated_minutes",
            "progress",
            "knowledge_items",
            "applications",
            "assessments",
            "created_at",
            "updated_at",
        ]

    def get_path(self, obj):
        return {
            "id": obj.path.id,
            "title": obj.path.title,
            "goal_id": obj.path.goal_id,
        }

    def get_progress(self, obj):
        request = self.context.get("request")

        if not request or not request.user.is_authenticated:
            return None

        progress = obj.progress_records.filter(
            user=request.user
        ).first()

        if not progress:
            return None

        return LearningProgressSerializer(
            progress,
            context=self.context,
        ).data

    def get_knowledge_items(self, obj):
        from knowledge.serializers import KnowledgeItemSerializer

        return KnowledgeItemSerializer(
            obj.knowledge_items.filter(
                user=self.context["request"].user,
                is_archived=False,
            ),
            many=True,
            context=self.context,
        ).data

    def get_applications(self, obj):

        applications = obj.applications.filter(
            user=self.context["request"].user
        )

        return KnowledgeApplicationSerializer(
            applications,
            many=True,
            context=self.context,
        ).data

    def get_assessments(self, obj):

        return AssessmentSerializer(
            Assessment.objects.filter(
                topic=obj,
                is_active=True,
            ),
            many=True,
            context=self.context,
        ).data
