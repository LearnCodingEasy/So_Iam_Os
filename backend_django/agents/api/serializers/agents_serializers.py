from rest_framework import serializers  # noqa: F401

from core.api.owned import ensure_all_owned, ensure_owned, scope_related_fields
from agents.models import Agent, AgentConfiguration, AgentRun, AgentExecution
from agents.validators.agent_validator import validate_agent_payload, validate_configuration_payload, validate_run_payload


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'
        read_only_fields = ['user']

    def validate(self, attrs):
        user = self.context['request'].user
        validate_agent_payload(attrs, self.instance, user)
        return attrs


class AgentConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentConfiguration
        fields = '__all__'
        read_only_fields = ['version', 'is_active']
        validators = []  # uniqueness enforced by the DB constraint + service

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request is not None and request.user.is_authenticated:
            scope_related_fields(self.fields, request.user, {'agent': 'user'})

    def validate(self, attrs):
        user = self.context['request'].user
        ensure_owned(attrs.get('agent'), user, 'agent', 'user')
        validate_configuration_payload(attrs, self.instance, user)
        return attrs


class AgentRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentRun
        fields = '__all__'
        read_only_fields = ['user', 'configuration', 'status', 'result', 'error', 'approved_at', 'started_at', 'finished_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request is not None and request.user.is_authenticated:
            scope_related_fields(self.fields, request.user, {'agent': 'user'})

    def validate(self, attrs):
        user = self.context['request'].user
        ensure_owned(attrs.get('agent'), user, 'agent', 'user')
        validate_run_payload(attrs, self.instance, user)
        return attrs


class AgentExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentExecution
        fields = '__all__'
        read_only_fields = ['run', 'step_index', 'action', 'status', 'input_data', 'output_data', 'error', 'duration_ms']

    def validate(self, attrs):
        user = self.context['request'].user
        return attrs
