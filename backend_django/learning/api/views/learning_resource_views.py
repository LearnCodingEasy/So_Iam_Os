from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from learning.models import LearningResource


# ===================================================
# Learning Resource
# ===================================================


class LearningResourceViewSet(
    viewsets.ModelViewSet
):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            LearningResource.objects
            .filter(
                topic__path__user=self.request.user
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
                "You do not own this learning topic."
            )

        lesson = serializer.validated_data.get(
            "lesson"
        )

        if lesson and lesson.topic_id != topic.id:
            raise PermissionDenied(
                "Lesson does not belong to this topic."
            )

        serializer.save()
