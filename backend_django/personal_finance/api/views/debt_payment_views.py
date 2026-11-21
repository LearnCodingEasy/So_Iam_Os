from __future__ import annotations
from personal_finance.models import DebtPayment
from personal_finance.api.serializers import DebtPaymentSerializer
from personal_finance.api.views.owned_views import Owned


class DebtPaymentViewSet(Owned):
    serializer_class = DebtPaymentSerializer
    queryset = DebtPayment.objects.select_related("debt").all()
