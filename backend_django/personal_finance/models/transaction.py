from __future__ import annotations
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from personal_finance.models.category import Category


class Transaction(models.Model):
    KIND_CHOICES = (
        ("income", "Income"),
        ("expense", "Expense"),
        ("debt_payment", "Debt payment"),
        ("saving", "Saving"),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="finance_transactions")
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name="transactions")
    kind = models.CharField(max_length=20, choices=KIND_CHOICES)
    amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=10, default="USD")
    occurred_on = models.DateField()
    description = models.CharField(max_length=255, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    priority = models.CharField(max_length=20, default="normal")
    necessity = models.CharField(max_length=20, default="necessary")
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-occurred_on", "-id"]
        indexes = [
            models.Index(fields=["user", "occurred_on", "kind"]),
            models.Index(fields=["user", "currency", "occurred_on"]),
        ]
