from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .constants import API_SUCCESS, APP_NAME, APP_VERSION
from .models import UserLearningSettings
from .serializers import UserLearningSettingsSerializer
from .services import DashboardService

class CoreHealthView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        return Response({"status": API_SUCCESS, "app": APP_NAME, "version": APP_VERSION, "service": "core"})

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response(DashboardService.get_data(user=request.user))

class UserLearningSettingsView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, request):
        obj, _ = UserLearningSettings.objects.get_or_create(user=request.user)
        if obj.current_learning_goal_id and obj.current_learning_goal.user_id != request.user.id:
            obj.current_learning_goal = None
            obj.save(update_fields=["current_learning_goal", "updated_at"])
        return obj
    def get(self, request):
        return Response(UserLearningSettingsSerializer(self.get_object(request), context={"request": request}).data)
    def patch(self, request):
        obj = self.get_object(request)
        serializer = UserLearningSettingsSerializer(obj, data=request.data, partial=True, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
