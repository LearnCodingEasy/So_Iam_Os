from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .constants import API_SUCCESS, APP_NAME, APP_VERSION
from .services import DashboardService


class CoreHealthView(APIView):
    """
    Health/status endpoint for the Core application.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        return Response(
            {
                "status": API_SUCCESS,
                "app": APP_NAME,
                "version": APP_VERSION,
                "service": "core",
            }
        )


class DashboardView(APIView):
    """
    Main dashboard endpoint.

    Aggregates information from the different
    So_Iam_OS applications for the authenticated user.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = DashboardService.get_data(
            user=request.user,
        )

        return Response(data)
