from rest_framework import serializers
from learning.models import LearningGoal
from learning.api.serializers.common import get_request_user
from learning.api.serializers.skill_serializers import SkillMinimalSerializer


# ===================================================
# Learning Goal
# ===================================================


class LearningGoalSerializer(serializers.ModelSerializer):
    skill_detail = SkillMinimalSerializer(
        source="skill",
        read_only=True,
    )

    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    current_level_display = serializers.CharField(
        source="get_current_level_display",
        read_only=True,
    )

    target_level_display = serializers.CharField(
        source="get_target_level_display",
        read_only=True,
    )

    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    class Meta:
        model = LearningGoal
        fields = (
            "id",
            "user",
            "skill",
            "skill_detail",
            "title",
            "description",
            "reason",
            "current_level",
            "current_level_display",
            "target_level",
            "target_level_display",
            "status",
            "status_display",
            "target_date",
            "completed_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "user",
            "completed_at",
            "created_at",
            "updated_at",
        )

    def validate_skill(self, skill):
        if skill and not skill.is_active:
            raise serializers.ValidationError(
                "This skill is currently inactive."
            )

        return skill

    def validate(self, attrs):
        user = get_request_user(self)

        if user is None:
            raise serializers.ValidationError(
                "Authentication is required."
            )

        return attrs

    def create(self, validated_data):
        user = get_request_user(self)

        return LearningGoal.objects.create(
            user=user,
            **validated_data,
        )


# ===================================================
# Rich Learning Goal Detail
# ===================================================


class LearningGoalDetailSerializer(
    LearningGoalSerializer
):
    paths = LearningPathMinimalSerializer = serializers.SerializerMethodField()

    def get_paths(self, obj):
        paths = obj.paths.all()

        return [
            {
                "id": path.id,
                "title": path.title,
                "description": path.description,
                "status": path.status,
                "started_at": path.started_at,
                "completed_at": path.completed_at,
            }
            for path in paths
        ]

    class Meta(LearningGoalSerializer.Meta):
        fields = (
            "id",
            "user",
            "skill",
            "skill_detail",
            "title",
            "description",
            "reason",
            "current_level",
            "current_level_display",
            "target_level",
            "target_level_display",
            "status",
            "status_display",
            "target_date",
            "completed_at",
            "paths",
            "created_at",
            "updated_at",
        )
