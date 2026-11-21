# codex models

Model files and declarations are extracted from source. Field excerpts retain source line numbers; inspect linked source for multiline options and complete semantics.


## api_endpoint
Source: codex/models/api_endpoint.py

- L5: class APIEndpoint(models.Model):

- L8: method = models.CharField(max_length=16, default="ANY")

- L9: path = models.CharField(max_length=700)

- L10: name = models.CharField(max_length=240, blank=True)

- L11: source = models.CharField(max_length=300, blank=True)

- L12: app_label = models.CharField(max_length=100, blank=True)

- L13: frontend_route = models.CharField(max_length=220, default="/codex")

- L14: frontend_section = models.CharField(max_length=160, default="API Registry")

- L15: frontend_service = models.CharField(max_length=220, blank=True)

- L16: coverage_status = models.CharField(

- L18: protected = models.BooleanField(default=False)

- L19: metadata = models.JSONField(default=dict, blank=True)

- L21: class Meta:

- L22: constraints = [models.UniqueConstraint(

## architecture_edge
Source: codex/models/architecture_edge.py

- L6: class ArchitectureEdge(models.Model):

- L13: relation = models.CharField(max_length=120)

- L14: metadata = models.JSONField(default=dict, blank=True)

- L16: class Meta:

- L17: constraints = [models.UniqueConstraint(

## architecture_node
Source: codex/models/architecture_node.py

- L5: class ArchitectureNode(models.Model):

- L8: key = models.CharField(max_length=500)

- L9: kind = models.CharField(max_length=80)

- L10: label = models.CharField(max_length=300)

- L11: path = models.CharField(max_length=700, blank=True)

- L12: metadata = models.JSONField(default=dict, blank=True)

- L14: class Meta:

- L15: constraints = [models.UniqueConstraint(

## change_set
Source: codex/models/change_set.py

- L6: class ChangeSet(models.Model):

- L13: title = models.CharField(max_length=240)

- L14: objective = models.TextField(blank=True)

- L15: status = models.CharField(max_length=30, choices=STATUS, default="planned")

- L16: impact = models.JSONField(default=dict, blank=True)

- L17: plan = models.JSONField(default=list, blank=True)

- L18: diff_summary = models.JSONField(default=dict, blank=True)

- L19: snapshot_id = models.CharField(max_length=120, blank=True)

- L20: created_at = models.DateTimeField(auto_now_add=True)

- L21: updated_at = models.DateTimeField(auto_now=True)

## codex_agent_definition
Source: codex/models/codex_agent_definition.py

- L5: class CodexAgentDefinition(models.Model):

- L8: key = models.CharField(max_length=180)

- L9: name = models.CharField(max_length=220)

- L10: category = models.CharField(max_length=120)

- L11: purpose = models.TextField(blank=True)

- L12: input_schema = models.JSONField(default=dict, blank=True)

- L13: output_schema = models.JSONField(default=dict, blank=True)

- L14: tools = models.JSONField(default=list, blank=True)

- L15: permissions = models.JSONField(default=list, blank=True)

- L16: risk = models.CharField(max_length=30, default='medium')

- L17: validation = models.JSONField(default=list, blank=True)

- L18: implementation = models.CharField(

- L20: enabled = models.BooleanField(default=True)

- L21: version = models.CharField(max_length=30, default='1.0.0')

- L22: metadata = models.JSONField(default=dict, blank=True)

- L23: created_at = models.DateTimeField(auto_now_add=True)

- L24: updated_at = models.DateTimeField(auto_now=True)

- L26: class Meta:

- L27: constraints = [models.UniqueConstraint(

## codex_agent_run
Source: codex/models/codex_agent_run.py

- L6: class CodexAgentRun(models.Model):

- L13: request = models.TextField()

- L14: mode = models.CharField(max_length=60, default='safe-agent')

- L15: status = models.CharField(max_length=30, choices=STATUS, default='planned')

- L16: plan = models.JSONField(default=dict, blank=True)

- L17: result = models.JSONField(default=dict, blank=True)

- L18: created_at = models.DateTimeField(auto_now_add=True)

- L19: updated_at = models.DateTimeField(auto_now=True)

## codex_analysis
Source: codex/models/codex_analysis.py

- L5: class CodexAnalysis(models.Model):

- L12: request = models.TextField()

- L14: provider = models.CharField(

- L19: result = models.JSONField(

- L24: context = models.JSONField(

- L29: created_at = models.DateTimeField(

## codex_audit_event
Source: codex/models/codex_audit_event.py

- L6: class CodexAuditEvent(models.Model):

- L11: event_type = models.CharField(max_length=100)

- L12: action = models.CharField(max_length=180)

- L13: status = models.CharField(max_length=40, default='success')

- L14: payload = models.JSONField(default=dict, blank=True)

- L15: created_at = models.DateTimeField(auto_now_add=True)

## codex_capability_run
Source: codex/models/codex_capability_run.py

- L6: class CodexCapabilityRun(models.Model):

- L15: kind = models.CharField(max_length=20, choices=KIND_CHOICES)

- L16: key = models.CharField(max_length=180)

- L17: status = models.CharField(

- L19: input_data = models.JSONField(default=dict, blank=True)

- L20: output_data = models.JSONField(default=dict, blank=True)

- L21: validation = models.JSONField(default=dict, blank=True)

- L22: created_at = models.DateTimeField(auto_now_add=True)

- L23: completed_at = models.DateTimeField(null=True, blank=True)

## codex_change_file
Source: codex/models/codex_change_file.py

- L5: class CodexChangeFile(models.Model):

- L8: path = models.CharField(max_length=700)

- L9: before_content = models.TextField(blank=True)

- L10: after_content = models.TextField(blank=True)

- L11: before_sha256 = models.CharField(max_length=64, blank=True)

- L12: after_sha256 = models.CharField(max_length=64, blank=True)

- L13: created_at = models.DateTimeField(auto_now_add=True)

## codex_conversation
Source: codex/models/codex_conversation.py

- L6: class CodexConversation(models.Model):

- L18: title = models.CharField(max_length=240, blank=True)

- L19: provider = models.CharField(

- L27: created_at = models.DateTimeField(auto_now_add=True)

- L28: updated_at = models.DateTimeField(auto_now=True)

## codex_execution_request
Source: codex/models/codex_execution_request.py

- L6: class CodexExecutionRequest(models.Model):

- L13: tool_key = models.CharField(max_length=160)

- L14: status = models.CharField(max_length=30, choices=STATUS, default='pending')

- L15: approval_note = models.TextField(blank=True)

- L16: result = models.JSONField(default=dict, blank=True)

- L17: created_at = models.DateTimeField(auto_now_add=True)

- L18: completed_at = models.DateTimeField(null=True, blank=True)

## codex_feature_definition
Source: codex/models/codex_feature_definition.py

- L5: class CodexFeatureDefinition(models.Model):

- L8: key = models.CharField(max_length=180)

- L9: name = models.CharField(max_length=220)

- L10: category = models.CharField(max_length=120)

- L11: purpose = models.TextField(blank=True)

- L12: status = models.CharField(max_length=30, default='implemented')

- L13: protection_level = models.CharField(max_length=30, default='NORMAL')

- L14: permissions = models.JSONField(default=list, blank=True)

- L15: integration = models.JSONField(default=dict, blank=True)

- L16: tests = models.JSONField(default=list, blank=True)

- L17: metadata = models.JSONField(default=dict, blank=True)

- L18: enabled = models.BooleanField(default=True)

- L19: version = models.CharField(max_length=30, default='1.0.0')

- L20: created_at = models.DateTimeField(auto_now_add=True)

- L21: updated_at = models.DateTimeField(auto_now=True)

- L23: class Meta:

- L24: constraints = [models.UniqueConstraint(

## codex_finding
Source: codex/models/codex_finding.py

- L5: class CodexFinding(models.Model):

- L8: category = models.CharField(max_length=80)

- L9: severity = models.CharField(max_length=30, default='medium')

- L10: title = models.CharField(max_length=220)

- L11: path = models.CharField(max_length=700, blank=True)

- L12: line = models.PositiveIntegerField(null=True, blank=True)

- L13: message = models.TextField()

- L14: metadata = models.JSONField(default=dict, blank=True)

- L15: resolved = models.BooleanField(default=False)

- L16: created_at = models.DateTimeField(auto_now_add=True)

## codex_message
Source: codex/models/codex_message.py

- L5: class CodexMessage(models.Model):

- L17: role = models.CharField(

- L21: content = models.TextField()

- L22: metadata = models.JSONField(

- L26: created_at = models.DateTimeField(

## codex_policy
Source: codex/models/codex_policy.py

- L6: class CodexPolicy(models.Model):

- L11: permissions = models.JSONField(default=dict, blank=True)

- L12: updated_at = models.DateTimeField(auto_now=True)

- L14: class Meta:

- L15: constraints = [models.UniqueConstraint(

## codex_tool
Source: codex/models/codex_tool.py

- L5: class CodexTool(models.Model):

- L8: key = models.CharField(max_length=160)

- L9: name = models.CharField(max_length=220)

- L10: capability = models.CharField(max_length=60, default='read')

- L11: enabled = models.BooleanField(default=True)

- L12: metadata = models.JSONField(default=dict, blank=True)

- L14: class Meta:

- L15: constraints = [models.UniqueConstraint(

## codex_tool_definition
Source: codex/models/codex_tool_definition.py

- L5: class CodexToolDefinition(models.Model):

- L8: key = models.CharField(max_length=180)

- L9: name = models.CharField(max_length=220)

- L10: category = models.CharField(max_length=120)

- L11: capability = models.CharField(max_length=40, default='read')

- L12: risk = models.CharField(max_length=30, default='low')

- L13: permission = models.CharField(max_length=80, default='READ_FILES')

- L14: input_schema = models.JSONField(default=dict, blank=True)

- L15: output_schema = models.JSONField(default=dict, blank=True)

- L16: purpose = models.TextField(blank=True)

- L17: implementation = models.CharField(

- L19: enabled = models.BooleanField(default=True)

- L20: version = models.CharField(max_length=30, default='1.0.0')

- L21: metadata = models.JSONField(default=dict, blank=True)

- L22: created_at = models.DateTimeField(auto_now_add=True)

- L23: updated_at = models.DateTimeField(auto_now=True)

- L25: class Meta:

- L26: constraints = [models.UniqueConstraint(

## codex_workflow_step
Source: codex/models/codex_workflow_step.py

- L5: class CodexWorkflowStep(models.Model):

- L15: key = models.CharField(max_length=120)

- L16: name = models.CharField(max_length=220)

- L17: order = models.PositiveIntegerField(default=0)

- L18: status = models.CharField(

- L20: description = models.TextField(blank=True)

- L21: dependencies = models.JSONField(default=list, blank=True)

- L22: checks = models.JSONField(default=list, blank=True)

- L23: evidence = models.JSONField(default=dict, blank=True)

- L24: completed_at = models.DateTimeField(null=True, blank=True)

- L25: updated_at = models.DateTimeField(auto_now=True)

- L27: class Meta:

- L28: constraints = [

- L29: models.UniqueConstraint(

## feature
Source: codex/models/feature.py

- L5: class Feature(models.Model):

- L10: key = models.CharField(max_length=180)

- L11: name = models.CharField(max_length=220)

- L12: app_label = models.CharField(max_length=100, blank=True)

- L13: description = models.TextField(blank=True)

- L14: status = models.CharField(

- L16: protected = models.BooleanField(default=False)

- L17: metadata = models.JSONField(default=dict, blank=True)

- L19: class Meta:

- L20: constraints = [models.UniqueConstraint(

## file_registry
Source: codex/models/file_registry.py

- L5: class FileRegistry(models.Model):

- L8: path = models.CharField(max_length=700)

- L9: kind = models.CharField(max_length=80, blank=True)

- L10: app_label = models.CharField(max_length=100, blank=True)

- L11: sha256 = models.CharField(max_length=64, blank=True)

- L12: size = models.PositiveBigIntegerField(default=0)

- L13: protected = models.BooleanField(default=False)

- L14: metadata = models.JSONField(default=dict, blank=True)

- L15: scanned_at = models.DateTimeField(auto_now=True)

- L17: class Meta:

- L18: constraints = [models.UniqueConstraint(

## local_ai_job
Source: codex/models/local_ai_job.py

- L6: class LocalAIJob(models.Model):

- L25: task_type = models.CharField(

- L27: status = models.CharField(

- L29: input_data = models.JSONField(default=dict, blank=True)

- L30: result = models.JSONField(default=dict, blank=True)

- L31: provider = models.CharField(max_length=80, default="local")

- L32: error = models.TextField(blank=True)

- L33: created_at = models.DateTimeField(auto_now_add=True)

- L34: started_at = models.DateTimeField(null=True, blank=True)

- L35: completed_at = models.DateTimeField(null=True, blank=True)

- L37: class Meta:

## project_registry
Source: codex/models/project_registry.py

- L4: class ProjectRegistry(models.Model):

- L5: key = models.CharField(max_length=120, unique=True, default="so_iam_os")

- L6: name = models.CharField(max_length=200, default="SO_IAM_OS")

- L7: root_path = models.CharField(max_length=500, blank=True)

- L8: metadata = models.JSONField(default=dict, blank=True)

- L9: scanned_at = models.DateTimeField(null=True, blank=True)

- L10: created_at = models.DateTimeField(auto_now_add=True)

- L11: updated_at = models.DateTimeField(auto_now=True)

## project_snapshot
Source: codex/models/project_snapshot.py

- L6: class ProjectSnapshot(models.Model):

- L11: label = models.CharField(max_length=220)

- L12: manifest = models.JSONField(default=dict, blank=True)

- L13: created_at = models.DateTimeField(auto_now_add=True)

## protected_feature
Source: codex/models/protected_feature.py

- L6: class ProtectedFeature(models.Model):

- L11: key = models.CharField(max_length=180)

- L12: reason = models.TextField(blank=True)

- L13: paths = models.JSONField(default=list, blank=True)

- L14: rules = models.JSONField(default=dict, blank=True)

- L15: enabled = models.BooleanField(default=True)

- L16: created_at = models.DateTimeField(auto_now_add=True)

- L18: class Meta:

- L19: constraints = [models.UniqueConstraint(

## protected_item
Source: codex/models/protected_item.py

- L6: class ProtectedItem(models.Model):

- L18: key = models.CharField(max_length=220)

- L19: item_type = models.CharField(

- L21: path = models.CharField(max_length=700, blank=True)

- L22: target = models.CharField(max_length=700, blank=True)

- L23: reason = models.TextField(blank=True)

- L24: approved = models.BooleanField(default=False)

- L25: frozen = models.BooleanField(default=False)

- L26: rules = models.JSONField(default=dict, blank=True)

- L27: metadata = models.JSONField(default=dict, blank=True)

- L28: approved_at = models.DateTimeField(null=True, blank=True)

- L31: created_at = models.DateTimeField(auto_now_add=True)

- L32: updated_at = models.DateTimeField(auto_now=True)

- L34: class Meta:

- L35: constraints = [

- L36: models.UniqueConstraint(

## __init__
Source: codex/models/__init__.py


Cross-app references and ownership must be confirmed from fields and write paths. See [project data catalog](../../06-database-and-model-catalog.md).
