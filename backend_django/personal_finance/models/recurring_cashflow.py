from __future__ import annotations
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class RecurringCashflow(models.Model):
    KIND_CHOICES = (("income", "Income"), ("expense", "Expense"))
    FREQUENCY_CHOICES = (("daily", "Daily"), ("weekly", "Weekly"), ("biweekly", "Bi-weekly"), ("semimonthly", "Semi-monthly"), ("monthly", "Monthly"), ("yearly", "Yearly"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="finance_recurring_cashflows")
    name = models.CharField(max_length=150)
    kind = models.CharField(max_length=20, choices=KIND_CHOICES)
    amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=10, default="USD")
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default="monthly")
    source = models.CharField(max_length=150, blank=True)
    next_date = models.DateField()
    active = models.BooleanField(default=True)
    description = models.CharField(max_length=255, blank=True)
