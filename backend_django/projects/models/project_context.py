from django.db import models
from projects.models.project import Project


class ProjectContext(models.Model):
    project=models.OneToOneField(Project,on_delete=models.CASCADE,related_name='ai_context'); summary=models.TextField(blank=True); architecture=models.JSONField(default=dict,blank=True); decisions=models.JSONField(default=list,blank=True); risks=models.JSONField(default=list,blank=True); ai_metadata=models.JSONField(default=dict,blank=True); updated_at=models.DateTimeField(auto_now=True)
