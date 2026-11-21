from rest_framework import serializers
from codex.models import ChangeSet


class ChangeSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangeSet
        fields = "__all__"
        read_only_fields = ["created_by"]
