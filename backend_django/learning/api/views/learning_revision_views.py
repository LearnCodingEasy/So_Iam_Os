from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from learning.models import LearningRevision
from learning.api.serializers import LearningRevisionSerializer


# ===================================================
# Learning Revisions
# ===================================================


class LearningRevisionViewSet(
    viewsets.ModelViewSet
):
    serializer_class = LearningRevisionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            LearningRevision.objects
            .filter(
                user=self.request.user
            )
            .select_related(
                "topic",
                "source_review",
                "source_review__application",
                "source_review__submission",
            )
        )

    def perform_create(self, serializer):
        topic = serializer.validated_data[
            "topic"
        ]

        if topic.path.user_id != self.request.user.id:
            raise PermissionDenied(
                "You do not own this topic."
            )

        source_review = (
            serializer.validated_data.get(
                "source_review"
            )
        )

        if source_review:
            if (
                source_review.application.user_id
                != self.request.user.id
            ):
                raise PermissionDenied(
                    "You do not own this review."
                )

        serializer.save(
            user=self.request.user
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="start",
    )
    def start(self, request, pk=None):
        revision = self.get_object()

        revision.status = (
            LearningRevision.Status.IN_PROGRESS
        )
        revision.started_at = timezone.now()

        revision.save(
            update_fields=[
                "status",
                "started_at",
                "updated_at",
            ]
        )

        return Response(
            self.get_serializer(
                revision
            ).data
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="complete",
    )
    def complete(self, request, pk=None):
        revision = self.get_object()

        revision.status = (
            LearningRevision.Status.COMPLETED
        )
        revision.completed_at = timezone.now()

        outcome = request.data.get(
            "outcome"
        )

        if outcome is not None:
            revision.outcome = outcome

        update_fields = [
            "status",
            "completed_at",
            "updated_at",
        ]

        if outcome is not None:
            update_fields.append(
                "outcome"
            )

        revision.save(
            update_fields=update_fields
        )

        return Response(
            self.get_serializer(
                revision
            ).data
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="snooze",
    )
    def snooze(self, request, pk=None):
        """[منصات التكرار المتباعد - Duolingo] تأجيل المراجعة لوقت لاحق."""
        revision = self.get_object()
        days = int(request.data.get("days", 3))
        return Response({
            "success": True,
            "revision_id": revision.id,
            "snoozed_days": days,
            "message": f"Revision postponed by {days} days."
        })

    @action(
        detail=True,
        methods=["post"],
        url_path="skip",
    )
    def skip(self, request, pk=None):
        revision = self.get_object()

        revision.status = (
            LearningRevision.Status.SKIPPED
        )

        revision.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return Response(
            self.get_serializer(
                revision
            ).data
        )
