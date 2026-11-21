from codex.models import CodexWorkflowStep
from codex.models import CodexWorkflowStep
from codex.api.serializers import WorkflowStepSerializer
from codex.api.views.base_views import BaseViewSet


class WorkflowStepViewSet(BaseViewSet):
    queryset = CodexWorkflowStep.objects.all()
    serializer_class = WorkflowStepSerializer
    filterset_fields = ["project", "status"]
