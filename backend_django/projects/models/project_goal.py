from django.db import models
from projects.models.project import Project


class ProjectGoal(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name='goals'); goal=models.ForeignKey('goals.Goal',on_delete=models.CASCADE,related_name='project_links'); created_at=models.DateTimeField(auto_now_add=True)
    class Meta: constraints=[models.UniqueConstraint(fields=['project','goal'],name='projects_project_goal_unique')]
