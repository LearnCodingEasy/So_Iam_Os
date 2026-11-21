from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from learning.models import LearningTopic, LearningProgress
from learning.api.serializers import LearningProgressSerializer
from learning.services import ProgressService
from learning.services.completion import LearningCompletionService


# ===================================================
# Learning Progress
# ===================================================


class LearningProgressViewSet(
    viewsets.ModelViewSet
):
    serializer_class = LearningProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            LearningProgress.objects
            .filter(
                user=self.request.user
            )
            .select_related(
                "topic",
                "topic__path",
            )
        )

    def perform_create(self, serializer):
        topic = serializer.validated_data["topic"]

        if topic.path.user_id != self.request.user.id:
            raise PermissionDenied(
                "This topic does not belong to you."
            )

        serializer.save(
            user=self.request.user
        )

    def perform_update(self, serializer):
        topic = serializer.instance.topic

        if topic.path.user_id != self.request.user.id:
            raise PermissionDenied(
                "This topic does not belong to you."
            )

        serializer.save()

    @action(
        detail=False,
        methods=["post"],
        url_path="update-progress",
    )
    def update_progress(self, request):
        topic_id = request.data.get("topic")

        if topic_id is None:
            return Response(
                {
                    "detail": "topic is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        progress_percent = request.data.get(
            "progress_percent"
        )

        if progress_percent is None:
            return Response(
                {
                    "detail": (
                        "progress_percent is required."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            progress_percent = int(
                progress_percent
            )

            if not 0 <= progress_percent <= 100:
                raise ValueError

        except (TypeError, ValueError):
            return Response(
                {
                    "detail": (
                        "progress_percent must be "
                        "between 0 and 100."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            topic = (
                LearningTopic.objects
                .select_related("path")
                .get(
                    id=topic_id,
                    path__user=request.user,
                )
            )

        except LearningTopic.DoesNotExist:
            return Response(
                {
                    "detail": "Topic not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            progress = (
                ProgressService.update_progress(
                    user=request.user,
                    topic=topic,
                    progress_percent=progress_percent,
                    practice_completed=request.data.get("practice_completed"),
                    notes=request.data.get("notes"),
                    lesson_completed=request.data.get("lesson_completed"),
                    quick_check_completed=request.data.get(
                        "quick_check_completed"),
                    assessment_completed=request.data.get(
                        "assessment_completed"),
                )
            )

        except ValueError as exc:
            return Response(
                {
                    "detail": str(exc)
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            LearningProgressSerializer(
                progress,
                context={
                    "request": request
                },
            ).data
        )

    @action(detail=False, methods=["get"], url_path="summary")
    def summary(self, request):
        return Response(LearningCompletionService.progress_summary(request.user))
