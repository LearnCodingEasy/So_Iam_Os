from __future__ import annotations
from django.conf import settings
from django.db import models


class Category(models.Model):
    KIND_CHOICES = (
        ("income", "Income"),
        ("expense", "Expense"),
        ("saving", "Saving"),
        ("debt_payment", "Debt payment"),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="finance_categories")
    name = models.CharField(max_length=120)
    kind = models.CharField(max_length=20, choices=KIND_CHOICES, default="expense")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "name", "kind"], name="finance_category_unique"),
        ]
        ordering = ["kind", "name"]
