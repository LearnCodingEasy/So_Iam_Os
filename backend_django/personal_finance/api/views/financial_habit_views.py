from __future__ import annotations
from personal_finance.models import FinancialHabit
from personal_finance.api.serializers import FinancialHabitSerializer
from personal_finance.api.views.owned_views import Owned


class FinancialHabitViewSet(Owned):
    serializer_class = FinancialHabitSerializer
    queryset = FinancialHabit.objects.all()
