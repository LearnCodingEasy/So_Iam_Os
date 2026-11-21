from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from learning.models import AssessmentResponse


# ===================================================
# Assessment Responses
# ===================================================


class AssessmentResponseViewSet(
    viewsets.ModelViewSet
):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            AssessmentResponse.objects
            .filter(
                attempt__user=self.request.user
            )
            .select_related(
                "attempt",
                "question",
            )
            .prefetch_related(
                "selected_choices",
            )
        )

    def perform_create(self, serializer):
        attempt = serializer.validated_data[
            "attempt"
        ]

        if attempt.user_id != self.request.user.id:
            raise PermissionDenied(
                "This attempt does not belong to you."
            )

        serializer.save()
