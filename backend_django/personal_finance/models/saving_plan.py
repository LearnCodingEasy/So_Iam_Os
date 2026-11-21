from __future__ import annotations
from django.conf import settings
from django.db import models
from personal_finance.models.savings_goal import SavingsGoal


class SavingPlan(models.Model):
    goal = models.OneToOneField(SavingsGoal, on_delete=models.CASCADE, related_name="plan")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="finance_saving_plans")
    daily_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    weekly_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    monthly_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    expected_completion = models.DateField(null=True, blank=True)
