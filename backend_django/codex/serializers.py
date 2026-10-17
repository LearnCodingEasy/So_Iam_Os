from rest_framework import serializers

from .models import (
    ProjectRegistry, Feature, FileRegistry, APIEndpoint, ProtectedFeature,
    ProtectedItem, CodexWorkflowStep, LocalAIJob, ChangeSet, ProjectSnapshot,
    CodexFeatureDefinition, CodexToolDefinition, CodexAgentDefinition,
    CodexCapabilityRun,
)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectRegistry
        fields = "__all__"


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = "__all__"


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileRegistry
        fields = "__all__"


class APIEndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIEndpoint
        fields = "__all__"


class ProtectedFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtectedFeature
        fields = "__all__"


class ProtectedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtectedItem
        fields = "__all__"
        read_only_fields = ["approved_at", "approved_by", "created_at", "updated_at"]


class WorkflowStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodexWorkflowStep
        fields = "__all__"
        read_only_fields = ["completed_at", "updated_at"]


class LocalAIJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalAIJob
        fields = "__all__"
        read_only_fields = ["user", "status", "provider", "result", "error", "started_at", "completed_at", "created_at"]


class ChangeSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangeSet
        fields = "__all__"
        read_only_fields = ["created_by"]


class SnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectSnapshot
        fields = "__all__"
        read_only_fields = ["created_by"]


class FeatureDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodexFeatureDefinition
        fields = "__all__"


class ToolDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodexToolDefinition
        fields = "__all__"


class AgentDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodexAgentDefinition
        fields = "__all__"


class CapabilityRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodexCapabilityRun
        fields = "__all__"
