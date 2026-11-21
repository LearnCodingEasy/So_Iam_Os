from __future__ import annotations
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Debt(models.Model):
    STATUS_CHOICES = (("active", "Active"), ("paid", "Paid"), ("paused", "Paused"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="finance_debts")
    name = models.CharField(max_length=150)
    balance = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])
    minimum_payment = models.DecimalField(max_digits=14, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    interest_rate = models.DecimalField(max_digits=8, decimal_places=4, default=0, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=10, default="USD")
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

    class Meta:
        indexes = [models.Index(fields=["user", "status", "due_date"])]
