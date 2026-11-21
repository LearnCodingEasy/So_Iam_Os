from __future__ import annotations
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from personal_finance.models.category import Category


class Budget(models.Model):
    PERIOD_CHOICES = (("daily", "Daily"), ("weekly", "Weekly"), ("monthly", "Monthly"), ("yearly", "Yearly"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="finance_budgets")
    name = models.CharField(max_length=150)
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES, default="monthly")
    limit_amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=10, default="USD")
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    active = models.BooleanField(default=True)
