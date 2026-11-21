from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from learning.models import ApplicationReview


# ===================================================
# Application Reviews
# ===================================================


class ApplicationReviewViewSet(
    viewsets.ReadOnlyModelViewSet
):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            ApplicationReview.objects
            .filter(
                application__user=self.request.user
            )
            .select_related(
                "application",
                "submission",
                "submission__application",
            )
        )
