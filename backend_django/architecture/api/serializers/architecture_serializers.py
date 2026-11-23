from rest_framework import serializers  # noqa: F401

from core.api.owned import ensure_all_owned, ensure_owned, scope_related_fields
from architecture.models import Architecture, Component, Dependency, ArchitectureDecision
from architecture.validators.architecture_validator import validate_architecture_payload, validate_component_payload, validate_decision_payload, validate_dependency_payload


class ArchitectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Architecture
        fields = '__all__'
        read_only_fields = ['user']

    def validate(self, attrs):
        user = self.context['request'].user
        validate_architecture_payload(attrs, self.instance, user)
        return attrs


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request is not None and request.user.is_authenticated:
            scope_related_fields(self.fields, request.user, {'architecture': 'user'})

    def validate(self, attrs):
        user = self.context['request'].user
        ensure_owned(attrs.get('architecture'), user, 'architecture', 'user')
        validate_component_payload(attrs, self.instance, user)
        return attrs


class DependencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dependency
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request is not None and request.user.is_authenticated:
            scope_related_fields(self.fields, request.user, {'source': 'architecture__user', 'target': 'architecture__user'})

    def validate(self, attrs):
        user = self.context['request'].user
        ensure_owned(attrs.get('source'), user, 'source', 'architecture.user')
        ensure_owned(attrs.get('target'), user, 'target', 'architecture.user')
        validate_dependency_payload(attrs, self.instance, user)
        return attrs


class ArchitectureDecisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchitectureDecision
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request is not None and request.user.is_authenticated:
            scope_related_fields(self.fields, request.user, {'architecture': 'user', 'superseded_by': 'architecture__user'})

    def validate(self, attrs):
        user = self.context['request'].user
        ensure_owned(attrs.get('architecture'), user, 'architecture', 'user')
        ensure_owned(attrs.get('superseded_by'), user, 'superseded_by', 'architecture.user')
        validate_decision_payload(attrs, self.instance, user)
        return attrs
