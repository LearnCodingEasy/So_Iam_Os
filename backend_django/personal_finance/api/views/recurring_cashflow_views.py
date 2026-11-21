from __future__ import annotations
from personal_finance.models import RecurringCashflow
from personal_finance.api.serializers import RecurringCashflowSerializer
from personal_finance.api.views.owned_views import Owned


class RecurringCashflowViewSet(Owned):
    serializer_class = RecurringCashflowSerializer
    queryset = RecurringCashflow.objects.all()
