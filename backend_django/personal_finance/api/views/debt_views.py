from __future__ import annotations
from decimal import Decimal
from django.db import transaction as db_transaction
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response
from personal_finance.models import Transaction, Debt, DebtPayment
from personal_finance.api.serializers import DebtSerializer, DebtPaymentSerializer
from personal_finance.api.views.owned_views import Owned


class DebtViewSet(Owned):
    serializer_class = DebtSerializer
    queryset = Debt.objects.all()

    @action(detail=True, methods=["get"])
    def payments(self, request, pk=None):
        debt = self.get_object()
        return Response(DebtPaymentSerializer(debt.payments.all(), many=True).data)

    @action(detail=True, methods=["post"])
    def pay(self, request, pk=None):
        debt = self.get_object()
        amount = Decimal(str(request.data.get("amount", "0")))
        if amount <= 0:
            return Response({"detail": "Payment amount must be positive."}, status=400)
        if amount > debt.balance:
            return Response({"detail": "Payment cannot exceed the remaining debt balance."}, status=400)
        paid_on = request.data.get("paid_on") or timezone.localdate()
        note = request.data.get("note", "")
        with db_transaction.atomic():
            tx = Transaction.objects.create(
                user=request.user, kind="debt_payment", amount=amount, currency=debt.currency,
                occurred_on=paid_on, description=f"Debt payment: {debt.name}",
            )
            payment = DebtPayment.objects.create(user=request.user, debt=debt, amount=amount, paid_on=paid_on, note=note, transaction=tx)
            debt.balance = debt.balance - amount
            if debt.balance <= 0:
                debt.balance = 0
                debt.status = "paid"
            debt.save(update_fields=["balance", "status"])
        return Response(DebtPaymentSerializer(payment).data, status=201)
