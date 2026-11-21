from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from learning.models import AssessmentChoice


# ===================================================
# Assessment Choices
# ===================================================


class AssessmentChoiceViewSet(
    viewsets.ModelViewSet
):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            AssessmentChoice.objects
            .filter(
                question__assessment__topic__path__user=(
                    self.request.user
                )
            )
            .select_related(
                "question",
                "question__assessment",
            )
        )

    def perform_create(self, serializer):
        question = serializer.validated_data[
            "question"
        ]

        if (
            question.assessment.topic.path.user_id
            != self.request.user.id
        ):
            raise PermissionDenied(
                "You do not own this assessment."
            )

        serializer.save()
