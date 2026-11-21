from django.db import models
from projects.models.project import Project


class ProjectTask(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name='tasks'); task=models.ForeignKey('tasks.Task',on_delete=models.CASCADE,related_name='project_links'); created_at=models.DateTimeField(auto_now_add=True)
    class Meta: constraints=[models.UniqueConstraint(fields=['project','task'],name='projects_project_task_unique')]
