from django.conf import settings
from django.db import models
class Challenge(models.Model):
    class Type(models.TextChoices): LEARNING='learning','Learning'; CODING='coding','Coding'; GOAL='goal','Goal'; PROJECT='project','Project'
    class Status(models.TextChoices): DRAFT='draft','Draft'; ACTIVE='active','Active'; COMPLETED='completed','Completed'; ARCHIVED='archived','Archived'
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='challenges'); title=models.CharField(max_length=255); description=models.TextField(blank=True); type=models.CharField(max_length=20,choices=Type.choices,default=Type.LEARNING); status=models.CharField(max_length=20,choices=Status.choices,default=Status.ACTIVE); difficulty=models.CharField(max_length=30,default='intermediate'); skill=models.ForeignKey('learning.Skill',null=True,blank=True,on_delete=models.SET_NULL,related_name='challenges'); project=models.ForeignKey('projects.Project',null=True,blank=True,on_delete=models.SET_NULL,related_name='challenges'); goal=models.ForeignKey('goals.Goal',null=True,blank=True,on_delete=models.SET_NULL,related_name='challenges'); metadata=models.JSONField(default=dict,blank=True); created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
class ChallengeStep(models.Model):
    challenge=models.ForeignKey(Challenge,on_delete=models.CASCADE,related_name='steps'); title=models.CharField(max_length=255); instructions=models.TextField(blank=True); order=models.PositiveIntegerField(default=0); expected_output=models.TextField(blank=True); metadata=models.JSONField(default=dict,blank=True)
    class Meta: ordering=['order']
class ChallengeAttempt(models.Model):
    challenge=models.ForeignKey(Challenge,on_delete=models.CASCADE,related_name='attempts'); user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='challenge_attempts'); answer=models.TextField(blank=True); score=models.PositiveSmallIntegerField(default=0); feedback=models.TextField(blank=True); status=models.CharField(max_length=20,default='submitted'); created_at=models.DateTimeField(auto_now_add=True)
class ChallengeProgress(models.Model):
    challenge=models.ForeignKey(Challenge,on_delete=models.CASCADE,related_name='progress_rows'); user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='challenge_progress'); progress_percent=models.PositiveSmallIntegerField(default=0); completed_steps=models.PositiveIntegerField(default=0); updated_at=models.DateTimeField(auto_now=True)
    class Meta: constraints=[models.UniqueConstraint(fields=['challenge','user'],name='challenge_user_unique')]
