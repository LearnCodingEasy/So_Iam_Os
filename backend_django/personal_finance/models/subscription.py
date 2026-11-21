from __future__ import annotations
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Subscription(models.Model):
    CYCLE_CHOICES = (("weekly", "Weekly"), ("monthly", "Monthly"), ("quarterly", "Quarterly"), ("yearly", "Yearly"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="finance_subscriptions")
    name = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=10, default="USD")
    billing_cycle = models.CharField(max_length=20, choices=CYCLE_CHOICES, default="monthly")
    next_charge = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)
