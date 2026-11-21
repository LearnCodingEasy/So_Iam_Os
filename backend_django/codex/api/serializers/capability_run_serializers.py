from rest_framework import serializers
from codex.models import CodexCapabilityRun


class CapabilityRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodexCapabilityRun
        fields = "__all__"
