from __future__ import annotations
from personal_finance.models import Budget
from personal_finance.api.serializers import BudgetSerializer
from personal_finance.api.views.owned_views import Owned


class BudgetViewSet(Owned):
    serializer_class = BudgetSerializer
    queryset = Budget.objects.select_related("category").all()
