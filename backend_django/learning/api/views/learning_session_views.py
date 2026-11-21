from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from learning.models import LearningSession


# ===================================================
# Learning Sessions
# ===================================================


class LearningSessionViewSet(
    viewsets.ModelViewSet
):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            LearningSession.objects
            .filter(
                user=self.request.user
            )
            .select_related(
                "topic",
                "lesson",
            )
        )

    def perform_create(self, serializer):
        topic = serializer.validated_data["topic"]

        if topic.path.user_id != self.request.user.id:
            raise PermissionDenied(
                "You do not own this topic."
            )

        serializer.save(
            user=self.request.user
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="finish",
    )
    def finish(self, request, pk=None):
        session = self.get_object()

        ended_at = timezone.now()

        session.ended_at = ended_at
        session.completed = True

        if session.started_at:
            session.duration_seconds = max(
                0,
                int(
                    (
                        ended_at
                        - session.started_at
                    ).total_seconds()
                ),
            )

        session.save(
            update_fields=[
                "ended_at",
                "completed",
                "duration_seconds",
            ]
        )

        return Response(
            self.get_serializer(session).data
        )
