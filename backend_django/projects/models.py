from django.conf import settings
from django.db import models

class Project(models.Model):
    class Status(models.TextChoices): PLANNING='planning','Planning'; ACTIVE='active','Active'; PAUSED='paused','Paused'; COMPLETED='completed','Completed'; ARCHIVED='archived','Archived'
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='projects')
    title=models.CharField(max_length=255); description=models.TextField(blank=True); status=models.CharField(max_length=20,choices=Status.choices,default=Status.PLANNING)
    repository_url=models.URLField(blank=True); website_url=models.URLField(blank=True); metadata=models.JSONField(default=dict,blank=True)
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=['-updated_at']
class ProjectMember(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name='members'); user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='project_memberships'); role=models.CharField(max_length=80,default='member'); created_at=models.DateTimeField(auto_now_add=True)
    class Meta: constraints=[models.UniqueConstraint(fields=['project','user'],name='projects_project_user_unique')]
class ProjectGoal(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name='goals'); goal=models.ForeignKey('goals.Goal',on_delete=models.CASCADE,related_name='project_links'); created_at=models.DateTimeField(auto_now_add=True)
    class Meta: constraints=[models.UniqueConstraint(fields=['project','goal'],name='projects_project_goal_unique')]
class ProjectTask(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name='tasks'); task=models.ForeignKey('tasks.Task',on_delete=models.CASCADE,related_name='project_links'); created_at=models.DateTimeField(auto_now_add=True)
    class Meta: constraints=[models.UniqueConstraint(fields=['project','task'],name='projects_project_task_unique')]
class ProjectContext(models.Model):
    project=models.OneToOneField(Project,on_delete=models.CASCADE,related_name='ai_context'); summary=models.TextField(blank=True); architecture=models.JSONField(default=dict,blank=True); decisions=models.JSONField(default=list,blank=True); risks=models.JSONField(default=list,blank=True); ai_metadata=models.JSONField(default=dict,blank=True); updated_at=models.DateTimeField(auto_now=True)
