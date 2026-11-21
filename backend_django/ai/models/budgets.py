from django.conf import settings
from django.db import models

from ..security import decrypt_secret, encrypt_secret

class AIBudgetPolicy(models.Model):
    class Scope(models.TextChoices):
        USER = "user", "User"
        AGENT = "agent", "Agent"
        PROVIDER = "provider", "Provider"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ai_budget_policies")
    scope = models.CharField(
        max_length=20, choices=Scope.choices, default=Scope.USER)
    scope_key = models.CharField(max_length=120, default="")
    daily_cost_limit = models.DecimalField(
        max_digits=14, decimal_places=8, null=True, blank=True)
    monthly_cost_limit = models.DecimalField(
        max_digits=14, decimal_places=8, null=True, blank=True)
    daily_token_limit = models.PositiveBigIntegerField(null=True, blank=True)
    monthly_token_limit = models.PositiveBigIntegerField(null=True, blank=True)
    enabled = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "scope", "scope_key"], name="unique_ai_budget_scope"),
        ]




class AIBudgetReservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ai_budget_reservations")
    policy = models.ForeignKey(AIBudgetPolicy, on_delete=models.CASCADE, related_name="reservations")
    idempotency_key = models.CharField(max_length=255)
    reserved_cost = models.DecimalField(max_digits=14, decimal_places=8, default=0)
    reserved_tokens = models.PositiveBigIntegerField(default=0)
    status = models.CharField(max_length=20, choices=[
        ("reserved", "Reserved"), ("settled", "Settled"), ("released", "Released")
    ], default="reserved")
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "idempotency_key"], name="unique_ai_budget_reservation"),
        ]
        indexes = [models.Index(fields=["user", "status", "expires_at"])]

