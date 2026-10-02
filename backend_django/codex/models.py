from django.conf import settings
from django.db import models

class ProjectRegistry(models.Model):
    key=models.CharField(max_length=120, unique=True, default="so_iam_os")
    name=models.CharField(max_length=200, default="SO_IAM_OS")
    root_path=models.CharField(max_length=500, blank=True)
    metadata=models.JSONField(default=dict, blank=True)
    scanned_at=models.DateTimeField(null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Feature(models.Model):
    STATUS_CHOICES=[("active","Active"),("planned","Planned"),("deprecated","Deprecated")]
    project=models.ForeignKey(ProjectRegistry,on_delete=models.CASCADE,related_name="features")
    key=models.CharField(max_length=180)
    name=models.CharField(max_length=220)
    app_label=models.CharField(max_length=100,blank=True)
    description=models.TextField(blank=True)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default="active")
    protected=models.BooleanField(default=False)
    metadata=models.JSONField(default=dict,blank=True)
    class Meta:
        constraints=[models.UniqueConstraint(fields=["project","key"],name="codex_feature_project_key")]

class FileRegistry(models.Model):
    project=models.ForeignKey(ProjectRegistry,on_delete=models.CASCADE,related_name="files")
    path=models.CharField(max_length=700)
    kind=models.CharField(max_length=80,blank=True)
    app_label=models.CharField(max_length=100,blank=True)
    sha256=models.CharField(max_length=64,blank=True)
    size=models.PositiveBigIntegerField(default=0)
    protected=models.BooleanField(default=False)
    metadata=models.JSONField(default=dict,blank=True)
    scanned_at=models.DateTimeField(auto_now=True)
    class Meta:
        constraints=[models.UniqueConstraint(fields=["project","path"],name="codex_file_project_path")]

class APIEndpoint(models.Model):
    project=models.ForeignKey(ProjectRegistry,on_delete=models.CASCADE,related_name="apis")
    method=models.CharField(max_length=16,default="ANY")
    path=models.CharField(max_length=700)
    name=models.CharField(max_length=240,blank=True)
    source=models.CharField(max_length=300,blank=True)
    app_label=models.CharField(max_length=100,blank=True)
    frontend_route=models.CharField(max_length=220,default="/codex")
    frontend_section=models.CharField(max_length=160,default="API Registry")
    frontend_service=models.CharField(max_length=220,blank=True)
    coverage_status=models.CharField(max_length=40,default="registry-covered")
    protected=models.BooleanField(default=False)
    metadata=models.JSONField(default=dict,blank=True)
    class Meta:
        constraints=[models.UniqueConstraint(fields=["project","method","path","name"],name="codex_api_unique")]

class ProtectedFeature(models.Model):
    project=models.ForeignKey(ProjectRegistry,on_delete=models.CASCADE,related_name="protected_features")
    feature=models.ForeignKey(Feature,on_delete=models.CASCADE,related_name="protection_rules",null=True,blank=True)
    key=models.CharField(max_length=180)
    reason=models.TextField(blank=True)
    paths=models.JSONField(default=list,blank=True)
    rules=models.JSONField(default=dict,blank=True)
    enabled=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints=[models.UniqueConstraint(fields=["project","key"],name="codex_protected_project_key")]

class ChangeSet(models.Model):
    STATUS=[("planned","Planned"),("approved","Approved"),("applied","Applied"),("rolled_back","Rolled back"),("rejected","Rejected")]
    project=models.ForeignKey(ProjectRegistry,on_delete=models.CASCADE,related_name="changesets")
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)
    title=models.CharField(max_length=240)
    objective=models.TextField(blank=True)
    status=models.CharField(max_length=30,choices=STATUS,default="planned")
    impact=models.JSONField(default=dict,blank=True)
    plan=models.JSONField(default=list,blank=True)
    diff_summary=models.JSONField(default=dict,blank=True)
    snapshot_id=models.CharField(max_length=120,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class ProjectSnapshot(models.Model):
    project=models.ForeignKey(ProjectRegistry,on_delete=models.CASCADE,related_name="snapshots")
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)
    label=models.CharField(max_length=220)
    manifest=models.JSONField(default=dict,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

class CodexConversation(models.Model):
    project = models.ForeignKey(
        ProjectRegistry,
        on_delete=models.CASCADE,
        related_name="codex_conversations",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=240, blank=True)
    provider = models.CharField(
        max_length=40,
        default="local",
        choices=[
            ("local", "Local"),
            ("openai", "OpenAI"),
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CodexMessage(models.Model):
    ROLE_CHOICES = [
        ("user", "User"),
        ("assistant", "Assistant"),
        ("system", "System"),
    ]

    conversation = models.ForeignKey(
        CodexConversation,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
    )
    content = models.TextField()
    metadata = models.JSONField(
        default=dict,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )


class CodexAnalysis(models.Model):
    conversation = models.ForeignKey(
        CodexConversation,
        on_delete=models.CASCADE,
        related_name="analyses",
    )

    request = models.TextField()

    provider = models.CharField(
        max_length=40,
        default="local",
    )

    result = models.JSONField(
        default=dict,
        blank=True,
    )

    context = models.JSONField(
        default=dict,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )