from rest_framework import serializers

from challenges.models import Challenge, ChallengeStep, ChallengeAttempt, ChallengeProgress
from challenges.validators.challenge_validator import (
    validate_attempt_payload,
    validate_challenge_payload,
    validate_progress_payload,
    validate_step_payload,
)
from core.api.owned import ensure_owned, scope_related_fields


class _OwnedRelationsMixin:
    """Limit selectable related objects to the requester's own records."""

    related_scope = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request is not None and request.user.is_authenticated:
            scope_related_fields(self.fields, request.user, self.related_scope)


class ChallengeStepSerializer(_OwnedRelationsMixin, serializers.ModelSerializer):
    related_scope = {'challenge': 'user'}

    class Meta:
        model = ChallengeStep
        fields = '__all__'

    def validate(self, attrs):
        user = self.context['request'].user
        ensure_owned(attrs.get('challenge'), user, 'challenge', 'user')
        validate_step_payload(attrs, self.instance, user)
        return attrs


class ChallengeSerializer(_OwnedRelationsMixin, serializers.ModelSerializer):
    related_scope = {'project': 'user', 'goal': 'user'}
    steps = ChallengeStepSerializer(many=True, read_only=True)

    class Meta:
        model = Challenge
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']

    def validate(self, attrs):
        user = self.context['request'].user
        ensure_owned(attrs.get('project'), user, 'project', 'user')
        ensure_owned(attrs.get('goal'), user, 'goal', 'user')
        validate_challenge_payload(attrs, self.instance, user)
        return attrs


class ChallengeAttemptSerializer(_OwnedRelationsMixin, serializers.ModelSerializer):
    related_scope = {'challenge': 'user'}

    class Meta:
        model = ChallengeAttempt
        fields = '__all__'
        read_only_fields = ['user', 'created_at']

    def validate(self, attrs):
        user = self.context['request'].user
        ensure_owned(attrs.get('challenge'), user, 'challenge', 'user')
        validate_attempt_payload(attrs, self.instance, user)
        return attrs


class ChallengeProgressSerializer(_OwnedRelationsMixin, serializers.ModelSerializer):
    related_scope = {'challenge': 'user'}

    class Meta:
        model = ChallengeProgress
        fields = '__all__'
        read_only_fields = ['user', 'updated_at']
        # (challenge, user) uniqueness is handled as an upsert by the service layer.
        validators = []

    def validate(self, attrs):
        user = self.context['request'].user
        ensure_owned(attrs.get('challenge'), user, 'challenge', 'user')
        validate_progress_payload(attrs, self.instance, user)
        return attrs
