from rest_framework import serializers
from codex.models import ProjectSnapshot


class SnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectSnapshot
        fields = "__all__"
        read_only_fields = ["created_by"]
