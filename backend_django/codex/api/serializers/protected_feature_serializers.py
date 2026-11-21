from rest_framework import serializers
from codex.models import ProtectedFeature


class ProtectedFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtectedFeature
        fields = "__all__"
