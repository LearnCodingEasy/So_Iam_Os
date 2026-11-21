from rest_framework.decorators import action
from rest_framework.response import Response
from jobs_opportunity.models import JobSkillGap
from jobs_opportunity.api.serializers import JobSkillGapSerializer
from jobs_opportunity.services import JobGapService
from jobs_opportunity.api.views.user_owned_views import UserOwnedViewSet


class JobSkillGapViewSet(UserOwnedViewSet):
    serializer_class = JobSkillGapSerializer

    def get_queryset(self): return JobSkillGap.objects.filter(
        user=self.request.user).select_related("job", "skill", "learning_goal")

    @action(detail=True, methods=["post"])
    def start_learning(self, request, pk=None):
        goal = JobGapService.create_learning_goal(
            request.user, self.get_object())
        return Response({"learning_goal_id": goal.id, "title": goal.title})
