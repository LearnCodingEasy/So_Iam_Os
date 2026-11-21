from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from learning.models import AssessmentQuestion


# ===================================================
# Assessment Questions
# ===================================================


class AssessmentQuestionViewSet(
    viewsets.ModelViewSet
):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            AssessmentQuestion.objects
            .filter(
                assessment__topic__path__user=(
                    self.request.user
                )
            )
            .select_related(
                "assessment",
            )
            .prefetch_related(
                "choices",
            )
        )

    def perform_create(self, serializer):
        assessment = serializer.validated_data[
            "assessment"
        ]

        if (
            assessment.topic.path.user_id
            != self.request.user.id
        ):
            raise PermissionDenied(
                "You do not own this assessment."
            )

        serializer.save()
