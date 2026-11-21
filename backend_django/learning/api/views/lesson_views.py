from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from learning.models import Lesson


# ===================================================
# Lesson
# ===================================================


class LessonViewSet(
    viewsets.ModelViewSet
):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Lesson.objects
            .filter(
                topic__path__user=self.request.user
            )
            .select_related(
                "topic",
                "topic__path",
            )
            .prefetch_related(
                "resources",
            )
        )

    def perform_create(self, serializer):
        topic = serializer.validated_data["topic"]

        if topic.path.user_id != self.request.user.id:
            raise PermissionDenied(
                "You do not own this learning topic."
            )

        serializer.save()

    @action(
        detail=True,
        methods=["post"],
        url_path="mark-complete",
    )
    def mark_complete(self, request, pk=None):
        """[تحكم إضافي] تحديد الدرس كمكتمل منفردًا."""
        lesson = self.get_object()
        return Response({
            "success": True,
            "lesson_id": lesson.id,
            "completed": True,
            "message": "Lesson marked as completed."
        })
