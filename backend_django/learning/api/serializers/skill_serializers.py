from rest_framework import serializers
from learning.models import Skill


# ===================================================
# Skill
# ===================================================


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "category",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class SkillMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = (
            "id",
            "name",
            "slug",
            "category",
        )
        read_only_fields = fields
