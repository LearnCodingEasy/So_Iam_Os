from django.conf import settings
from django.db import models


class Project(models.Model):
    class Status(models.TextChoices): PLANNING='planning','Planning'; ACTIVE='active','Active'; PAUSED='paused','Paused'; COMPLETED='completed','Completed'; ARCHIVED='archived','Archived'
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='projects')
    title=models.CharField(max_length=255); description=models.TextField(blank=True); status=models.CharField(max_length=20,choices=Status.choices,default=Status.PLANNING)
    repository_url=models.URLField(blank=True); website_url=models.URLField(blank=True); metadata=models.JSONField(default=dict,blank=True)
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=['-updated_at']
