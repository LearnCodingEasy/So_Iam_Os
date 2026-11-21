from rest_framework import serializers
from codex.models import Feature, CodexFeatureDefinition


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = "__all__"


class FeatureDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodexFeatureDefinition
        fields = "__all__"
