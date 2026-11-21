from rest_framework import serializers
from codex.models import ProtectedItem


class ProtectedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtectedItem
        fields = "__all__"
        read_only_fields = ["approved_at", "approved_by", "created_at", "updated_at"]
