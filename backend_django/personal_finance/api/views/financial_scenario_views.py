from __future__ import annotations
from personal_finance.models import FinancialScenario
from personal_finance.api.serializers import FinancialScenarioSerializer
from personal_finance.services import scenario
from personal_finance.api.views.owned_views import Owned


class FinancialScenarioViewSet(Owned):
    serializer_class = FinancialScenarioSerializer
    queryset = FinancialScenario.objects.all()

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        instance.result = scenario(
            self.request.user,
            instance.income_change_percent,
            instance.expense_change_percent,
            instance.debt_payment_extra,
            instance.case,
        )
        instance.save(update_fields=["result"])
