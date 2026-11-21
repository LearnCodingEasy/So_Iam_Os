from django.conf import settings
from django.db import models
from goals.models.goal import Goal


class GoalPlanProposal(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending approval"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name="plan_proposals")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="goal_plan_proposals")
    payload = models.JSONField(default=dict)
    provider = models.CharField(max_length=40, blank=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["user", "status"])]
