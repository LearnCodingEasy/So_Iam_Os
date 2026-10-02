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
class ArchitectureNode(models.Model):
    project = models.ForeignKey(ProjectRegistry, on_delete=models.CASCADE, related_name='architecture_nodes')
    key = models.CharField(max_length=500)
    kind = models.CharField(max_length=80)
    label = models.CharField(max_length=300)
    path = models.CharField(max_length=700, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['project', 'key'], name='codex_arch_node_unique')]


class ArchitectureEdge(models.Model):
    project = models.ForeignKey(ProjectRegistry, on_delete=models.CASCADE, related_name='architecture_edges')
    source = models.ForeignKey(ArchitectureNode, on_delete=models.CASCADE, related_name='out_edges')
    target = models.ForeignKey(ArchitectureNode, on_delete=models.CASCADE, related_name='in_edges')
    relation = models.CharField(max_length=120)
    metadata = models.JSONField(default=dict, blank=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['project', 'source', 'target', 'relation'], name='codex_arch_edge_unique')]


class CodexPolicy(models.Model):
    project = models.ForeignKey(ProjectRegistry, on_delete=models.CASCADE, related_name='policies')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    permissions = models.JSONField(default=dict, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['project', 'user'], name='codex_policy_project_user_unique')]


class CodexTool(models.Model):
    project = models.ForeignKey(ProjectRegistry, on_delete=models.CASCADE, related_name='tools')
    key = models.CharField(max_length=160)
    name = models.CharField(max_length=220)
    capability = models.CharField(max_length=60, default='read')
    enabled = models.BooleanField(default=True)
    metadata = models.JSONField(default=dict, blank=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['project', 'key'], name='codex_tool_project_key_unique')]


class CodexAuditEvent(models.Model):
    project = models.ForeignKey(ProjectRegistry, on_delete=models.CASCADE, related_name='audit_events')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    event_type = models.CharField(max_length=100)
    action = models.CharField(max_length=180)
    status = models.CharField(max_length=40, default='success')
    payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class CodexFinding(models.Model):
    project = models.ForeignKey(ProjectRegistry, on_delete=models.CASCADE, related_name='findings')
    category = models.CharField(max_length=80)
    severity = models.CharField(max_length=30, default='medium')
    title = models.CharField(max_length=220)
    path = models.CharField(max_length=700, blank=True)
    line = models.PositiveIntegerField(null=True, blank=True)
    message = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)
    resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class CodexAgentRun(models.Model):
    STATUS = [('planned', 'Planned'), ('approved', 'Approved'), ('running', 'Running'), ('completed', 'Completed'), ('failed', 'Failed'), ('cancelled', 'Cancelled')]
    project = models.ForeignKey(ProjectRegistry, on_delete=models.CASCADE, related_name='agent_runs')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    request = models.TextField()
    mode = models.CharField(max_length=60, default='safe-agent')
    status = models.CharField(max_length=30, choices=STATUS, default='planned')
    plan = models.JSONField(default=dict, blank=True)
    result = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CodexExecutionRequest(models.Model):
    STATUS = [('pending', 'Pending'), ('approved', 'Approved'), ('running', 'Running'), ('completed', 'Completed'), ('failed', 'Failed'), ('denied', 'Denied')]
    project = models.ForeignKey(ProjectRegistry, on_delete=models.CASCADE, related_name='execution_requests')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    tool_key = models.CharField(max_length=160)
    status = models.CharField(max_length=30, choices=STATUS, default='pending')
    approval_note = models.TextField(blank=True)
    result = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

class CodexChangeFile(models.Model):
    changeset = models.ForeignKey(ChangeSet, on_delete=models.CASCADE, related_name='file_changes')
    path = models.CharField(max_length=700)
    before_content = models.TextField(blank=True)
    after_content = models.TextField(blank=True)
    before_sha256 = models.CharField(max_length=64, blank=True)
    after_sha256 = models.CharField(max_length=64, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
