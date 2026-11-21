from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from learning.models import AssessmentAttempt
from learning.api.serializers import AssessmentAttemptSerializer


# ===================================================
# Assessment Attempts
# ===================================================


class AssessmentAttemptViewSet(
    viewsets.ReadOnlyModelViewSet
):
    serializer_class = AssessmentAttemptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            AssessmentAttempt.objects
            .filter(
                user=self.request.user
            )
            .select_related(
                "assessment",
                "assessment__topic",
            )
            .prefetch_related(
                "responses",
                "responses__question",
                "responses__selected_choices",
            )
        )
