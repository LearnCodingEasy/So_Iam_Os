from __future__ import annotations
from personal_finance.models import FinancialProfile
from personal_finance.api.serializers import FinancialProfileSerializer
from personal_finance.api.views.owned_views import Owned


class FinancialProfileViewSet(Owned):
    serializer_class = FinancialProfileSerializer
    queryset = FinancialProfile.objects.all()
