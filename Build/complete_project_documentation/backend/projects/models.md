# projects models

Model files and declarations are extracted from source. Field excerpts retain source line numbers; inspect linked source for multiline options and complete semantics.


## project
Source: projects/models/project.py

- L5: class Project(models.Model):

- L6: class Status(models.TextChoices): PLANNING='planning','Planning'; ACTIVE='active','Active'; PAUSED='paused','Paused'; COMPLETED='completed','Completed'; ARCHIVED='archived','Archived'

- L8: title=models.CharField(max_length=255); description=models.TextField(blank=True); status=models.CharField(max_length=20,choices=Status.choices,default=Status.PLANNING)

- L9: repository_url=models.URLField(blank=True); website_url=models.URLField(blank=True); metadata=models.JSONField(default=dict,blank=True)

- L10: created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)

- L11: class Meta: ordering=['-updated_at']

## project_context
Source: projects/models/project_context.py

- L5: class ProjectContext(models.Model):

- L6: project=models.OneToOneField(Project,on_delete=models.CASCADE,related_name='ai_context'); summary=models.TextField(blank=True); architecture=models.JSONField(default=dict,blank=True); decisions=models.JSONField(default=list,blank=True); risks=models.JSONField(default=list,blank=True); ai_metadata=models.JSONField(default=dict,blank=True); updated_at=models.DateTimeField(auto_now=True)

## project_goal
Source: projects/models/project_goal.py

- L5: class ProjectGoal(models.Model):

- L6: project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name='goals'); goal=models.ForeignKey('goals.Goal',on_delete=models.CASCADE,related_name='project_links'); created_at=models.DateTimeField(auto_now_add=True)

- L7: class Meta: constraints=[models.UniqueConstraint(fields=['project','goal'],name='projects_project_goal_unique')]

## project_member
Source: projects/models/project_member.py

- L6: class ProjectMember(models.Model):

- L7: project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name='members'); user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='project_memberships'); role=models.CharField(max_length=80,default='member'); created_at=models.DateTimeField(auto_now_add=True)

- L8: class Meta: constraints=[models.UniqueConstraint(fields=['project','user'],name='projects_project_user_unique')]

## project_task
Source: projects/models/project_task.py

- L5: class ProjectTask(models.Model):

- L6: project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name='tasks'); task=models.ForeignKey('tasks.Task',on_delete=models.CASCADE,related_name='project_links'); created_at=models.DateTimeField(auto_now_add=True)

- L7: class Meta: constraints=[models.UniqueConstraint(fields=['project','task'],name='projects_project_task_unique')]

## __init__
Source: projects/models/__init__.py


Cross-app references and ownership must be confirmed from fields and write paths. See [project data catalog](../../06-database-and-model-catalog.md).
