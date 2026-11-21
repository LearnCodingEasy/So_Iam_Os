from codex.services.intelligence import code_review
from rest_framework.views import APIView
from rest_framework.response import Response
from codex.permissions import CodexAuthenticated
from codex.models import ProjectRegistry


class CodeReviewView(APIView):
    permission_classes = [CodexAuthenticated]

    def post(self, request):
        project = ProjectRegistry.objects.get(key='so_iam_os')
        return Response({'path': request.data.get('path', ''), 'findings': code_review(project, request.data.get('path', ''), request.user)})
