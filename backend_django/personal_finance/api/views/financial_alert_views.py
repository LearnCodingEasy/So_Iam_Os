from __future__ import annotations
from rest_framework.decorators import action
from rest_framework.response import Response
from personal_finance.models import FinancialAlert
from personal_finance.api.serializers import FinancialAlertSerializer
from personal_finance.api.views.owned_views import Owned


class FinancialAlertViewSet(Owned):
    serializer_class = FinancialAlertSerializer
    queryset = FinancialAlert.objects.all()

    @action(detail=True, methods=["post"])
    def mark_read(self, request, pk=None):
        alert = self.get_object()
        alert.read = True
        alert.save(update_fields=["read"])
        return Response(FinancialAlertSerializer(alert).data)
