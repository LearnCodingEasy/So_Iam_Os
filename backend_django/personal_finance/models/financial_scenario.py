from __future__ import annotations
from django.conf import settings
from django.db import models


class FinancialScenario(models.Model):
    CASE_CHOICES = (("best", "Best case"), ("expected", "Expected case"), ("worst", "Worst case"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="finance_scenarios")
    name = models.CharField(max_length=150)
    income_change_percent = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    expense_change_percent = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    debt_payment_extra = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    case = models.CharField(max_length=20, choices=CASE_CHOICES, default="expected")
    result = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
