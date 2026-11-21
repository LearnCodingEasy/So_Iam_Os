from __future__ import annotations
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class SavingsGoal(models.Model):
    STATUS_CHOICES = (("active", "Active"), ("completed", "Completed"), ("paused", "Paused"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="finance_savings_goals")
    general_goal = models.ForeignKey("goals.Goal", null=True, blank=True, on_delete=models.SET_NULL, related_name="finance_savings_goals")
    name = models.CharField(max_length=150)
    target_amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])
    current_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=10, default="USD")
    target_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

    class Meta:
        indexes = [models.Index(fields=["user", "status", "target_date"])]
