from __future__ import annotations
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class LendingBorrowing(models.Model):
    DIRECTION_CHOICES = (("lent", "Lent"), ("borrowed", "Borrowed"))
    STATUS_CHOICES = (("upcoming", "Upcoming"), ("partial", "Partial"), ("paid", "Paid"), ("overdue", "Overdue"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="finance_loans")
    direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES)
    person = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])
    remaining = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=10, default="USD")
    date = models.DateField()
    due_date = models.DateField(null=True, blank=True)
    notes = models.CharField(max_length=500, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="upcoming")

    class Meta:
        ordering = ["due_date", "-id"]
        indexes = [models.Index(fields=["user", "direction", "status", "due_date"])]
