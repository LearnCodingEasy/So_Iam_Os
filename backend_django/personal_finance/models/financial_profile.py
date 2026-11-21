from __future__ import annotations
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class FinancialProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="finance_profile")
    base_currency = models.CharField(max_length=10, default="USD")
    emergency_target_months = models.DecimalField(max_digits=5, decimal_places=2, default=3, validators=[MinValueValidator(0)])
    weekly_summary_enabled = models.BooleanField(default=True)
    monthly_summary_enabled = models.BooleanField(default=True)
