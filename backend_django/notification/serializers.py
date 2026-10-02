from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    is_read = serializers.BooleanField(read_only=True)

    class Meta:
        model = Notification
        fields = ["id", "type", "title", "message", "action_url", "priority", "read_at", "is_read", "archived", "metadata", "created_at"]
        read_only_fields = ["id", "read_at", "is_read", "created_at"]
