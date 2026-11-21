from rest_framework.views import APIView
from rest_framework.response import Response
from codex.permissions import CodexAuthenticated
from codex.api.serializers import ChangeSetSerializer
from codex.services.change_planner import ChangePlanner


class PlanChangeView(APIView):
    permission_classes = [CodexAuthenticated]

    def post(self, request):
        obj = ChangePlanner.plan(user=request.user, title=request.data.get(
            "title", "Codex change plan"), objective=request.data.get("objective", ""), paths=request.data.get("paths", []))
        return Response(ChangeSetSerializer(obj).data, status=201)
