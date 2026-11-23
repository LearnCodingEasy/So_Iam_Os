from rest_framework.decorators import action
from rest_framework.response import Response

from challenges.api.serializers import (
    ChallengeAttemptSerializer,
    ChallengeProgressSerializer,
    ChallengeSerializer,
    ChallengeStepSerializer,
)
from challenges.models import Challenge, ChallengeAttempt, ChallengeProgress, ChallengeStep
from challenges.services import challenge_service
from core.api.owned import OwnedModelViewSet

# Kept for backward compatibility with the previous public module surface.
Owned = OwnedModelViewSet


class ChallengeViewSet(OwnedModelViewSet):
    queryset_model = Challenge
    serializer_class = ChallengeSerializer
    owner_lookup = 'user'
    filter_fields = ('type', 'status', 'difficulty', 'skill', 'project', 'goal')
    search_fields = ('title', 'description')
    ordering_fields = ('title', 'created_at', 'updated_at')

    def get_queryset(self):
        return super().get_queryset().prefetch_related('steps')

    @action(detail=True, methods=['post'], url_path='complete-step')
    def complete_step(self, request, pk=None):
        """Advance the requester's progress on this challenge by one step."""
        row = challenge_service.complete_step(user=request.user, challenge=self.get_object())
        return Response(ChallengeProgressSerializer(row, context=self.get_serializer_context()).data)


class ChallengeStepViewSet(OwnedModelViewSet):
    queryset_model = ChallengeStep
    serializer_class = ChallengeStepSerializer
    owner_lookup = 'challenge__user'
    set_owner_on_create = False
    filter_fields = ('challenge',)
    search_fields = ('title', 'instructions')
    ordering_fields = ('order', 'title')


class ChallengeAttemptViewSet(OwnedModelViewSet):
    queryset_model = ChallengeAttempt
    serializer_class = ChallengeAttemptSerializer
    owner_lookup = 'user'
    filter_fields = ('challenge', 'status')
    ordering_fields = ('created_at', 'score')
    select_related = ('challenge',)

    def perform_create(self, serializer):
        data = dict(serializer.validated_data)
        challenge = data.pop('challenge')
        # A passing score also completes the requester's progress (service rule).
        serializer.instance = challenge_service.record_attempt(
            user=self.request.user, challenge=challenge, **data
        )


class ChallengeProgressViewSet(OwnedModelViewSet):
    queryset_model = ChallengeProgress
    serializer_class = ChallengeProgressSerializer
    owner_lookup = 'user'
    filter_fields = ('challenge',)
    ordering_fields = ('updated_at', 'progress_percent')
    select_related = ('challenge',)

    def perform_create(self, serializer):
        data = serializer.validated_data
        # POST is an upsert: one progress row per (challenge, user).
        serializer.instance = challenge_service.set_progress(
            user=self.request.user,
            challenge=data['challenge'],
            completed_steps=data.get('completed_steps'),
            progress_percent=data.get('progress_percent'),
        )
