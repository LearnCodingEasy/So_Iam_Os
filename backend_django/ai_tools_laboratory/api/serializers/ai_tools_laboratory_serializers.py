from rest_framework import serializers  # noqa: F401

from core.api.owned import ensure_all_owned, ensure_owned, scope_related_fields
from ai_tools_laboratory.models import ToolCategory, Tool, ToolConfiguration, ToolExecution
from ai_tools_laboratory.validators.tool_validator import validate_category_payload, validate_configuration_payload, validate_execution_payload, validate_tool_payload


class ToolCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ToolCategory
        fields = '__all__'
        read_only_fields = ['user']
        validators = []  # uniqueness enforced by the DB constraint + service

    def validate(self, attrs):
        user = self.context['request'].user
        validate_category_payload(attrs, self.instance, user)
        return attrs


class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = '__all__'
        read_only_fields = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request is not None and request.user.is_authenticated:
            scope_related_fields(self.fields, request.user, {'category': 'user'})

    def validate(self, attrs):
        user = self.context['request'].user
        ensure_owned(attrs.get('category'), user, 'category', 'user')
        validate_tool_payload(attrs, self.instance, user)
        return attrs


class ToolConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToolConfiguration
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request is not None and request.user.is_authenticated:
            scope_related_fields(self.fields, request.user, {'tool': 'user'})

    def validate(self, attrs):
        user = self.context['request'].user
        ensure_owned(attrs.get('tool'), user, 'tool', 'user')
        validate_configuration_payload(attrs, self.instance, user)
        return attrs


class ToolExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToolExecution
        fields = '__all__'
        read_only_fields = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request is not None and request.user.is_authenticated:
            scope_related_fields(self.fields, request.user, {'tool': 'user', 'configuration': 'tool__user'})

    def validate(self, attrs):
        user = self.context['request'].user
        ensure_owned(attrs.get('tool'), user, 'tool', 'user')
        ensure_owned(attrs.get('configuration'), user, 'configuration', 'tool.user')
        validate_execution_payload(attrs, self.instance, user)
        return attrs
