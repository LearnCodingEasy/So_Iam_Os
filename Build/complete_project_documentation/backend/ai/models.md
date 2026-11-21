# ai models

Model files and declarations are extracted from source. Field excerpts retain source line numbers; inspect linked source for multiline options and complete semantics.


## audit
Source: ai/models/audit.py

- L5: class AiAuditLog(models.Model):

- L15: action = models.CharField(max_length=255)

- L16: resource = models.CharField(max_length=255, blank=True, null=True)

- L17: details = models.JSONField(default=dict, blank=True)

- L18: ip_address = models.GenericIPAddressField(blank=True, null=True)

- L19: created_at = models.DateTimeField(auto_now_add=True)

- L21: class Meta:

- L23: indexes = [

- L24: models.Index(fields=["user", "created_at"]),

- L25: models.Index(fields=["action"]),

## budgets
Source: ai/models/budgets.py

- L6: class AIBudgetPolicy(models.Model):

- L7: class Scope(models.TextChoices):

- L14: scope = models.CharField(

- L16: scope_key = models.CharField(max_length=120, default="")

- L17: daily_cost_limit = models.DecimalField(

- L19: monthly_cost_limit = models.DecimalField(

- L21: daily_token_limit = models.PositiveBigIntegerField(null=True, blank=True)

- L22: monthly_token_limit = models.PositiveBigIntegerField(null=True, blank=True)

- L23: enabled = models.BooleanField(default=True)

- L24: updated_at = models.DateTimeField(auto_now=True)

- L26: class Meta:

- L27: constraints = [

- L28: models.UniqueConstraint(

- L35: class AIBudgetReservation(models.Model):

- L38: idempotency_key = models.CharField(max_length=255)

- L39: reserved_cost = models.DecimalField(max_digits=14, decimal_places=8, default=0)

- L40: reserved_tokens = models.PositiveBigIntegerField(default=0)

- L41: status = models.CharField(max_length=20, choices=[

- L44: expires_at = models.DateTimeField()

- L45: created_at = models.DateTimeField(auto_now_add=True)

- L46: updated_at = models.DateTimeField(auto_now=True)

- L48: class Meta:

- L49: constraints = [

- L50: models.UniqueConstraint(fields=["user", "idempotency_key"], name="unique_ai_budget_reservation"),

- L52: indexes = [models.Index(fields=["user", "status", "expires_at"])]

## conversations
Source: ai/models/conversations.py

- L6: class AIConversation(models.Model):

- L23: title = models.CharField(max_length=255, blank=True, default="")

- L24: provider = models.CharField(

- L26: model = models.CharField(max_length=255, blank=True, default="")

- L27: is_active = models.BooleanField(default=True)

- L28: archived_at = models.DateTimeField(null=True, blank=True)

- L29: deleted_at = models.DateTimeField(null=True, blank=True)

- L30: last_message_at = models.DateTimeField(null=True, blank=True)

- L31: message_count = models.PositiveIntegerField(default=0)

- L32: metadata = models.JSONField(default=dict, blank=True)

- L33: created_at = models.DateTimeField(auto_now_add=True)

- L34: updated_at = models.DateTimeField(auto_now=True)

- L36: class Meta:

- L38: indexes = [models.Index(fields=["user", "-updated_at"]),

- L39: models.Index(fields=["user", "is_active"])]

- L47: class AIMessage(models.Model):

- L56: role = models.CharField(max_length=20, choices=ROLE_CHOICES)

- L57: content = models.TextField()

- L58: provider = models.CharField(max_length=50, blank=True, default="")

- L59: model = models.CharField(max_length=255, blank=True, default="")

- L60: metadata = models.JSONField(default=dict, blank=True)

- L61: created_at = models.DateTimeField(auto_now_add=True)

- L63: class Meta:

- L65: indexes = [models.Index(fields=["conversation", "created_at"])]

## executions
Source: ai/models/executions.py

- L6: class AIExecution(models.Model):

- L7: class Status(models.TextChoices):

- L18: agent = models.CharField(max_length=120, default="default")

- L19: task_type = models.CharField(max_length=80, default="chat")

- L20: requested_provider = models.CharField(

- L22: provider = models.CharField(max_length=50, blank=True, default="")

- L23: model = models.CharField(max_length=255, blank=True, default="")

- L24: status = models.CharField(

- L26: started_at = models.DateTimeField(null=True, blank=True)

- L27: finished_at = models.DateTimeField(null=True, blank=True)

- L28: duration_ms = models.PositiveIntegerField(null=True, blank=True)

- L29: input_tokens = models.PositiveIntegerField(null=True, blank=True)

- L30: output_tokens = models.PositiveIntegerField(null=True, blank=True)

- L31: estimated_cost = models.DecimalField(

- L33: retry_count = models.PositiveSmallIntegerField(default=0)

- L34: fallback_count = models.PositiveSmallIntegerField(default=0)

- L35: attempt_number = models.PositiveSmallIntegerField(default=1)

- L36: external_request_id = models.CharField(max_length=255, blank=True, default="")

- L37: idempotency_key = models.CharField(max_length=255, blank=True, default="")

- L38: genuine_result = models.BooleanField(default=False)

- L39: error_code = models.CharField(max_length=80, blank=True, default="")

- L40: error_message = models.TextField(blank=True, default="")

- L41: metadata = models.JSONField(default=dict, blank=True)

- L42: created_at = models.DateTimeField(auto_now_add=True)

- L44: class Meta:

- L46: indexes = [

- L47: models.Index(fields=["user", "-created_at"]),

- L48: models.Index(fields=["provider", "status"]),

- L49: models.Index(fields=["user", "idempotency_key"]),

- L50: models.Index(fields=["external_request_id"]),

- L52: constraints = [

- L53: models.UniqueConstraint(

## feedback
Source: ai/models/feedback.py

- L7: class AIFeedback(models.Model):

- L9: class Sentiment(models.TextChoices):

- L25: sentiment = models.CharField(

- L30: reason = models.CharField(

- L36: comment = models.TextField(

- L41: feedback_category = models.CharField(

- L47: model_version = models.CharField(

- L53: reviewed_at = models.DateTimeField(

- L58: rating = models.PositiveSmallIntegerField(

- L67: created_at = models.DateTimeField(auto_now_add=True)

- L69: class Meta:

- L70: constraints = [

- L71: models.UniqueConstraint(

- L77: indexes = [

- L78: models.Index(fields=["user", "-created_at"]),

- L79: models.Index(fields=["sentiment", "-created_at"]),

## prompts
Source: ai/models/prompts.py

- L6: class AIPromptProfile(models.Model):

- L14: name = models.CharField(max_length=120)

- L16: system_prompt = models.TextField(

- L21: context_instructions = models.TextField(

- L26: temperature = models.FloatField(

- L31: max_tokens = models.PositiveIntegerField(

- L36: is_default = models.BooleanField(default=False)

- L38: created_at = models.DateTimeField(auto_now_add=True)

- L39: updated_at = models.DateTimeField(auto_now=True)

- L41: class Meta:

- L44: constraints = [

- L45: models.UniqueConstraint(

## providers
Source: ai/models/providers.py

- L7: class AIProviderCredential(models.Model):

- L13: provider = models.CharField(

- L15: encrypted_api_key = models.TextField(blank=True, default="")

- L16: metadata = models.JSONField(default=dict, blank=True)

- L17: status = models.CharField(max_length=20, choices=[

- L20: last_used_at = models.DateTimeField(null=True, blank=True)

- L21: last_validated_at = models.DateTimeField(null=True, blank=True)

- L22: created_at = models.DateTimeField(auto_now_add=True)

- L23: updated_at = models.DateTimeField(auto_now=True)

- L25: class Meta:

- L26: constraints = [

- L27: models.UniqueConstraint(

- L30: indexes = [models.Index(fields=["user", "provider"])]

- L45: class AIProviderConfig(models.Model):

- L55: name = models.CharField(max_length=50, unique=True)

- L56: provider_type = models.CharField(max_length=20, choices=PROVIDER_TYPES)

- L57: api_key_encrypted = models.TextField(blank=True, null=True)

- L58: api_base_url = models.URLField(blank=True, null=True)

- L59: model_name = models.CharField(max_length=100, default="default")

- L60: priority = models.IntegerField(default=1)

- L61: is_active = models.BooleanField(default=True)

- L63: created_at = models.DateTimeField(auto_now_add=True)

## settings
Source: ai/models/settings.py

- L6: class AISettings(models.Model):

- L7: class Provider(models.TextChoices):

- L14: user = models.OneToOneField(

- L19: preferred_provider = models.CharField(

- L24: preferred_model = models.CharField(max_length=255, blank=True, default="")

- L32: context_enabled = models.BooleanField(default=True)

- L33: streaming_enabled = models.BooleanField(default=True)

- L34: temperature = models.FloatField(default=0.7)

- L35: timeout_seconds = models.PositiveIntegerField(default=35)

- L36: fallback_enabled = models.BooleanField(default=True)

- L37: max_context_tokens = models.PositiveIntegerField(default=6000)

- L38: created_at = models.DateTimeField(auto_now_add=True)

- L39: updated_at = models.DateTimeField(auto_now=True)

## usage
Source: ai/models/usage.py

- L6: class AIUsageRecord(models.Model):

- L13: execution = models.OneToOneField(

- L21: provider = models.CharField(max_length=50)

- L22: model = models.CharField(max_length=255, blank=True, default="")

- L23: agent = models.CharField(max_length=120, blank=True, default="")

- L25: input_tokens = models.PositiveIntegerField(default=0)

- L26: output_tokens = models.PositiveIntegerField(default=0)

- L27: cached_input_tokens = models.PositiveIntegerField(default=0)

- L29: estimated_cost = models.DecimalField(

- L35: actual_cost = models.DecimalField(

- L42: currency = models.CharField(max_length=8, default="USD")

- L43: pricing_version = models.CharField(

- L49: cost_source = models.CharField(

- L54: is_estimated = models.BooleanField(default=True)

- L56: recorded_at = models.DateTimeField(auto_now_add=True)

- L58: class Meta:

- L59: indexes = [

- L60: models.Index(fields=["user", "-recorded_at"]),

- L61: models.Index(fields=["provider", "model"]),

## workflows
Source: ai/models/workflows.py

- L6: class AIWorkflowDefinition(models.Model):

- L13: name = models.CharField(max_length=160)

- L14: description = models.TextField(blank=True, default="")

- L15: graph = models.JSONField(default=dict)

- L17: version = models.PositiveIntegerField(default=1)

- L18: is_active = models.BooleanField(default=True)

- L19: schema_version = models.CharField(max_length=32, default="1.0")

- L21: created_at = models.DateTimeField(auto_now_add=True)

- L22: updated_at = models.DateTimeField(auto_now=True)

- L24: class Meta:

- L25: constraints = [

- L26: models.UniqueConstraint(

- L31: indexes = [

- L32: models.Index(fields=["user", "-updated_at"])

- L39: class AIWorkflowRun(models.Model):

- L41: class Status(models.TextChoices):

- L68: status = models.CharField(

- L74: workflow_version = models.PositiveIntegerField(default=1)

- L75: current_node_id = models.CharField(

- L81: retry_count = models.PositiveSmallIntegerField(default=0)

- L83: input_data = models.JSONField(default=dict, blank=True)

- L84: output_data = models.JSONField(default=dict, blank=True)

- L86: error = models.TextField(blank=True, default="")

- L88: started_at = models.DateTimeField(null=True, blank=True)

- L89: finished_at = models.DateTimeField(null=True, blank=True)

- L91: created_at = models.DateTimeField(auto_now_add=True)

- L93: class Meta:

- L95: indexes = [

- L96: models.Index(fields=["user", "-created_at"]),

- L97: models.Index(fields=["workflow", "-created_at"]),

## __init__
Source: ai/models/__init__.py


Cross-app references and ownership must be confirmed from fields and write paths. See [project data catalog](../../06-database-and-model-catalog.md).
