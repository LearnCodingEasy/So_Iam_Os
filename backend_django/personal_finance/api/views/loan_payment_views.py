from __future__ import annotations
from personal_finance.models import LoanPayment
from personal_finance.api.serializers import LoanPaymentSerializer
from personal_finance.api.views.owned_views import Owned


class LoanPaymentViewSet(Owned):
    serializer_class = LoanPaymentSerializer
    queryset = LoanPayment.objects.select_related("loan").all()
