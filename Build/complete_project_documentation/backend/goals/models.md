# goals models

Model files and declarations are extracted from source. Field excerpts retain source line numbers; inspect linked source for multiline options and complete semantics.


## goal
Source: goals/models/goal.py

- L7: class Goal(models.Model):

- L8: class Status(models.TextChoices):

- L18: class Priority(models.TextChoices):

- L24: class Category(models.TextChoices):

- L35: title = models.CharField(max_length=255)

- L36: description = models.TextField(blank=True)

- L37: category = models.CharField(max_length=24, choices=Category.choices, default=Category.PERSONAL)

- L38: priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.MEDIUM)

- L39: status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)

- L40: start_date = models.DateField(default=timezone.localdate)

- L41: target_date = models.DateField(null=True, blank=True)

- L42: estimated_minutes = models.PositiveIntegerField(default=0)

- L43: actual_minutes = models.PositiveIntegerField(default=0)

- L44: progress_percent = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

- L45: measurement_unit = models.CharField(max_length=40, blank=True)

- L46: initial_value = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)

- L47: target_value = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)

- L48: current_value = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)

- L49: completion_notes = models.TextField(blank=True)

- L50: completed_at = models.DateTimeField(null=True, blank=True)

- L51: metadata = models.JSONField(default=dict, blank=True)

- L52: created_at = models.DateTimeField(auto_now_add=True)

- L53: updated_at = models.DateTimeField(auto_now=True)

- L55: learning_goals = models.ManyToManyField("learning.LearningGoal", blank=True, related_name="general_goals")

- L56: skills = models.ManyToManyField("learning.Skill", blank=True, related_name="goals")

- L57: related_goals = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="related_to")

- L59: class Meta:

- L61: indexes = [

- L62: models.Index(fields=["user", "status"]),

- L63: models.Index(fields=["user", "target_date"]),

- L64: models.Index(fields=["user", "priority"]),

- L65: models.Index(fields=["user", "category", "status"]),

## goal_activity
Source: goals/models/goal_activity.py

- L6: class GoalActivity(models.Model):

- L9: event_type = models.CharField(max_length=50)

- L10: description = models.TextField(blank=True)

- L11: data = models.JSONField(default=dict, blank=True)

- L12: created_at = models.DateTimeField(auto_now_add=True)

- L14: class Meta:

- L16: indexes = [models.Index(fields=["goal", "created_at"])]

## goal_milestone
Source: goals/models/goal_milestone.py

- L6: class GoalMilestone(models.Model):

- L7: class Status(models.TextChoices):

- L14: depends_on = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="dependent_milestones")

- L15: title = models.CharField(max_length=255)

- L16: description = models.TextField(blank=True)

- L17: sequence = models.PositiveIntegerField(default=0)

- L18: start_date = models.DateField(null=True, blank=True)

- L19: target_date = models.DateField(null=True, blank=True)

- L20: status = models.CharField(max_length=16, choices=Status.choices, default=Status.PLANNED)

- L21: progress_percent = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

- L22: weight = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

- L23: completion_criteria = models.TextField(blank=True)

- L24: completion_evidence = models.TextField(blank=True)

- L25: completed_at = models.DateTimeField(null=True, blank=True)

- L26: created_at = models.DateTimeField(auto_now_add=True)

- L27: updated_at = models.DateTimeField(auto_now=True)

- L29: class Meta:

- L31: constraints = [models.UniqueConstraint(fields=["goal", "sequence"], name="goal_milestone_seq_uniq")]

- L32: indexes = [models.Index(fields=["goal", "status"]), models.Index(fields=["goal", "target_date"])]

## goal_plan_proposal
Source: goals/models/goal_plan_proposal.py

- L6: class GoalPlanProposal(models.Model):

- L7: class Status(models.TextChoices):

- L14: payload = models.JSONField(default=dict)

- L15: provider = models.CharField(max_length=40, blank=True)

- L16: status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)

- L17: approved_at = models.DateTimeField(null=True, blank=True)

- L18: created_at = models.DateTimeField(auto_now_add=True)

- L20: class Meta:

- L22: indexes = [models.Index(fields=["user", "status"])]

## __init__
Source: goals/models/__init__.py


Cross-app references and ownership must be confirmed from fields and write paths. See [project data catalog](../../06-database-and-model-catalog.md).
