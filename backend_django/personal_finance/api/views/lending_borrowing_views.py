from __future__ import annotations
from decimal import Decimal
from django.db import transaction as db_transaction
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response
from personal_finance.models import LendingBorrowing, LoanPayment
from personal_finance.api.serializers import LendingBorrowingSerializer
from personal_finance.api.views.owned_views import Owned


class LendingBorrowingViewSet(Owned):
    serializer_class = LendingBorrowingSerializer
    queryset = LendingBorrowing.objects.all()

    @action(detail=True, methods=["post"])
    def pay(self, request, pk=None):
        loan = self.get_object()
        amount = Decimal(str(request.data.get("amount", "0")))
        if amount <= 0 or amount > loan.remaining:
            return Response({"detail": "Payment amount must be positive and cannot exceed remaining amount."}, status=400)
        with db_transaction.atomic():
            LoanPayment.objects.create(
                user=request.user, loan=loan, amount=amount,
                paid_on=request.data.get("paid_on") or timezone.localdate(),
                note=request.data.get("note", ""),
            )
            loan.remaining -= amount
            loan.status = "paid" if loan.remaining <= 0 else "partial"
            loan.save(update_fields=["remaining", "status"])
        return Response(LendingBorrowingSerializer(loan).data)
