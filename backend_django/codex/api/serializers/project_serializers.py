from rest_framework import serializers
from codex.models import ProjectRegistry


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectRegistry
        fields = "__all__"
