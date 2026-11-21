from __future__ import annotations
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from personal_finance.models.debt import Debt
from personal_finance.models.transaction import Transaction


class DebtPayment(models.Model):
    debt = models.ForeignKey(Debt, on_delete=models.CASCADE, related_name="payments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="finance_debt_payments")
    amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])
    paid_on = models.DateField()
    note = models.CharField(max_length=255, blank=True)
    transaction = models.OneToOneField(Transaction, null=True, blank=True, on_delete=models.SET_NULL, related_name="debt_payment")

    class Meta:
        ordering = ["-paid_on", "-id"]
        indexes = [models.Index(fields=["user", "paid_on"])]
