from __future__ import annotations
from django.conf import settings
from django.db import models


class FinancialAlert(models.Model):
    TYPE_CHOICES = (("budget", "Budget"), ("spending", "Spending"), ("debt", "Debt"), ("bill", "Bill"), ("goal", "Goal"), ("balance", "Balance"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="finance_alerts")
    alert_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=180)
    message = models.TextField()
    severity = models.CharField(max_length=20, default="info")
    read = models.BooleanField(default=False)
    due_on = models.DateField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["read", "-created_at"]
