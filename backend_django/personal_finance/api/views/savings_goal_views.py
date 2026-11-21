from __future__ import annotations
from decimal import Decimal
from rest_framework.decorators import action
from rest_framework.response import Response
from personal_finance.models import SavingsGoal, SavingPlan
from personal_finance.api.serializers import SavingsGoalSerializer, SavingPlanSerializer
from personal_finance.api.views.owned_views import Owned


class SavingsGoalViewSet(Owned):
    serializer_class = SavingsGoalSerializer
    queryset = SavingsGoal.objects.all()

    @action(detail=True, methods=["get", "post"])
    def plan(self, request, pk=None):
        goal = self.get_object()
        if request.method == "GET":
            plan = getattr(goal, "plan", None)
            if not plan:
                return Response({"detail": "No saving plan yet."}, status=404)
            return Response(SavingPlanSerializer(plan).data)
        from django.utils import timezone as tz
        today = tz.localdate()
        remaining = max(Decimal("0"), goal.target_amount - goal.current_amount)
        days = max(1, (goal.target_date - today).days) if goal.target_date else 30
        daily = remaining / Decimal(days)
        weekly = daily * 7
        monthly = daily * 30
        plan, _ = SavingPlan.objects.update_or_create(
            goal=goal, defaults={"user": request.user, "daily_amount": daily, "weekly_amount": weekly, "monthly_amount": monthly, "expected_completion": goal.target_date}
        )
        return Response(SavingPlanSerializer(plan).data)
