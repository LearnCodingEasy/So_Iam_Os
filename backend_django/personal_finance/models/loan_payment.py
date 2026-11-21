from __future__ import annotations
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from personal_finance.models.lending_borrowing import LendingBorrowing


class LoanPayment(models.Model):
    loan = models.ForeignKey(LendingBorrowing, on_delete=models.CASCADE, related_name="payments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="finance_loan_payments")
    amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])
    paid_on = models.DateField()
    note = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-paid_on", "-id"]
