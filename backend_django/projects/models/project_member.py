from django.conf import settings
from django.db import models
from projects.models.project import Project


class ProjectMember(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name='members'); user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='project_memberships'); role=models.CharField(max_length=80,default='member'); created_at=models.DateTimeField(auto_now_add=True)
    class Meta: constraints=[models.UniqueConstraint(fields=['project','user'],name='projects_project_user_unique')]
