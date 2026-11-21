from __future__ import annotations
from django.conf import settings
from django.db import models


class FinancialHabit(models.Model):
    STATUS_CHOICES = (("active", "Active"), ("paused", "Paused"), ("completed", "Completed"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="finance_habits")
    name = models.CharField(max_length=150)
    target = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    duration_days = models.PositiveIntegerField(default=30)
    progress = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    streak = models.PositiveIntegerField(default=0)
    started_on = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    reminder_time = models.TimeField(null=True, blank=True)
