from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from learning.models import LearningNote
from learning.api.serializers import LearningNoteSerializer


# ===================================================
# Learning Notes
# ===================================================


class LearningNoteViewSet(
    viewsets.ModelViewSet
):
    permission_classes = [IsAuthenticated]
    serializer_class = LearningNoteSerializer

    def get_queryset(self):
        return (
            LearningNote.objects
            .filter(
                user=self.request.user
            )
            .select_related(
                "topic",
                "lesson",
                "knowledge_item",
            )
        )

    def perform_create(self, serializer):
        topic = serializer.validated_data["topic"]

        if topic.path.user_id != self.request.user.id:
            raise PermissionDenied(
                "You do not own this learning topic."
            )

        serializer.save(
            user=self.request.user
        )
