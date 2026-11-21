from django.conf import settings
from django.db import models


class Challenge(models.Model):
    class Type(models.TextChoices): LEARNING='learning','Learning'; CODING='coding','Coding'; GOAL='goal','Goal'; PROJECT='project','Project'
    class Status(models.TextChoices): DRAFT='draft','Draft'; ACTIVE='active','Active'; COMPLETED='completed','Completed'; ARCHIVED='archived','Archived'
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='challenges'); title=models.CharField(max_length=255); description=models.TextField(blank=True); type=models.CharField(max_length=20,choices=Type.choices,default=Type.LEARNING); status=models.CharField(max_length=20,choices=Status.choices,default=Status.ACTIVE); difficulty=models.CharField(max_length=30,default='intermediate'); skill=models.ForeignKey('learning.Skill',null=True,blank=True,on_delete=models.SET_NULL,related_name='challenges'); project=models.ForeignKey('projects.Project',null=True,blank=True,on_delete=models.SET_NULL,related_name='challenges'); goal=models.ForeignKey('goals.Goal',null=True,blank=True,on_delete=models.SET_NULL,related_name='challenges'); metadata=models.JSONField(default=dict,blank=True); created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
