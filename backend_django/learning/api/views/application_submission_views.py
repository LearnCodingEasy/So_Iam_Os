from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from learning.models import ApplicationSubmission
from learning.api.serializers import ApplicationSubmissionSerializer


# ===================================================
# Application Submissions
# ===================================================


class ApplicationSubmissionViewSet(
    viewsets.ModelViewSet
):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            ApplicationSubmission.objects
            .filter(
                application__user=self.request.user
            )
            .select_related(
                "application",
            )
        )

    def get_serializer_class(self):
        return ApplicationSubmissionSerializer

    def perform_create(self, serializer):
        application = serializer.validated_data[
            "application"
        ]

        if application.user_id != self.request.user.id:
            raise PermissionDenied(
                "You do not own this application."
            )

        serializer.save()

    def update(self, request, *args, **kwargs):
        return Response(
            {
                "detail": (
                    "Application submissions are immutable."
                )
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def partial_update(
        self,
        request,
        *args,
        **kwargs,
    ):
        return Response(
            {
                "detail": (
                    "Application submissions are immutable."
                )
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def destroy(
        self,
        request,
        *args,
        **kwargs,
    ):
        return Response(
            {
                "detail": (
                    "Application submissions are immutable."
                )
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
