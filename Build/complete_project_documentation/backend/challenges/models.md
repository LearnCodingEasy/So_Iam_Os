# challenges models

Model files and declarations are extracted from source. Field excerpts retain source line numbers; inspect linked source for multiline options and complete semantics.


## challenge
Source: challenges/models/challenge.py

- L5: class Challenge(models.Model):

- L6: class Type(models.TextChoices): LEARNING='learning','Learning'; CODING='coding','Coding'; GOAL='goal','Goal'; PROJECT='project','Project'

- L7: class Status(models.TextChoices): DRAFT='draft','Draft'; ACTIVE='active','Active'; COMPLETED='completed','Completed'; ARCHIVED='archived','Archived'

- L8: user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='challenges'); title=models.CharField(max_length=255); description=models.TextField(blank=True); type=models.CharField(max_length=20,choices=Type.choices,default=Type.LEARNING); status=models.CharField(max_length=20,choices=Status.choices,default=Status.ACTIVE); difficulty=models.CharField(max_length=30,default='intermediate'); skill=models.ForeignKey('learning.Skill',null=True,blank=True,on_delete=models.SET_NULL,related_name='challenges'); project=models.ForeignKey('projects.Project',null=True,blank=True,on_delete=models.SET_NULL,related_name='challenges'); goal=models.ForeignKey('goals.Goal',null=True,blank=True,on_delete=models.SET_NULL,related_name='challenges'); metadata=models.JSONField(default=dict,blank=True); created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)

## challenge_attempt
Source: challenges/models/challenge_attempt.py

- L6: class ChallengeAttempt(models.Model):

- L7: challenge=models.ForeignKey(Challenge,on_delete=models.CASCADE,related_name='attempts'); user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='challenge_attempts'); answer=models.TextField(blank=True); score=models.PositiveSmallIntegerField(default=0); feedback=models.TextField(blank=True); status=models.CharField(max_length=20,default='submitted'); created_at=models.DateTimeField(auto_now_add=True)

## challenge_progress
Source: challenges/models/challenge_progress.py

- L6: class ChallengeProgress(models.Model):

- L7: challenge=models.ForeignKey(Challenge,on_delete=models.CASCADE,related_name='progress_rows'); user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='challenge_progress'); progress_percent=models.PositiveSmallIntegerField(default=0); completed_steps=models.PositiveIntegerField(default=0); updated_at=models.DateTimeField(auto_now=True)

- L8: class Meta: constraints=[models.UniqueConstraint(fields=['challenge','user'],name='challenge_user_unique')]

## challenge_step
Source: challenges/models/challenge_step.py

- L5: class ChallengeStep(models.Model):

- L6: challenge=models.ForeignKey(Challenge,on_delete=models.CASCADE,related_name='steps'); title=models.CharField(max_length=255); instructions=models.TextField(blank=True); order=models.PositiveIntegerField(default=0); expected_output=models.TextField(blank=True); metadata=models.JSONField(default=dict,blank=True)

- L7: class Meta: ordering=['order']

## __init__
Source: challenges/models/__init__.py


Cross-app references and ownership must be confirmed from fields and write paths. See [project data catalog](../../06-database-and-model-catalog.md).
