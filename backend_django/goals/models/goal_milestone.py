from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from goals.models.goal import Goal


class GoalMilestone(models.Model):
    class Status(models.TextChoices):
        PLANNED = "planned", "Planned"
        ACTIVE = "active", "Active"
        BLOCKED = "blocked", "Blocked"
        COMPLETED = "completed", "Completed"

    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name="milestones")
    depends_on = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="dependent_milestones")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    sequence = models.PositiveIntegerField(default=0)
    start_date = models.DateField(null=True, blank=True)
    target_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PLANNED)
    progress_percent = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    completion_criteria = models.TextField(blank=True)
    completion_evidence = models.TextField(blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sequence", "target_date", "id"]
        constraints = [models.UniqueConstraint(fields=["goal", "sequence"], name="goal_milestone_seq_uniq")]
        indexes = [models.Index(fields=["goal", "status"]), models.Index(fields=["goal", "target_date"])]

    def __str__(self):
        return f"{self.goal.title}: {self.title}"
