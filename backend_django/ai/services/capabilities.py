"""Single source of truth for AI platform capabilities exposed to the UI."""
FEATURES = [
    ("provider_health", "Provider health checks"), ("credential_validation", "Encrypted credential validation"),
    ("model_discovery", "Live model discovery"), ("provider_switching", "Per-request provider switching"),
    ("fallback_chain", "Bounded provider fallback"), ("retry_policy", "Bounded retry policy"),
    ("timeouts", "Configurable provider timeout"), ("idempotency", "Idempotent AI executions"),
    ("request_tracing", "Execution/request tracing"), ("audit_log", "AI audit logging"),
    ("usage_tracking", "Token and usage tracking"), ("cost_tracking", "Estimated/actual cost tracking"),
    ("budget_policies", "Budget limits"), ("budget_reservations", "Atomic budget reservations"),
    ("conversation_history", "Persistent conversation history"), ("conversation_archive", "Conversation archive/restore"),
    ("conversation_soft_delete", "Conversation soft delete"), ("message_metrics", "Conversation message metrics"),
    ("prompt_profiles", "Reusable prompt profiles"), ("context_builder", "Cross-domain user context"),
    ("context_token_cap", "Context size protection"), ("learning_preview", "AI learning plan preview"),
    ("learning_approval", "Explicit learning-plan approval"), ("async_tasks", "Async AI tasks"),
    ("task_status", "Owner-scoped task status"), ("topic_tutor", "Learning topic AI tutor"),
    ("agent_planning", "Safe agent planning"), ("workflow_validation", "Workflow graph validation"),
    ("workflow_versioning", "Workflow versioning"), ("workflow_history", "Workflow execution history"),
    ("feedback", "Message feedback"), ("monitoring", "Execution monitoring"),
    ("structured_errors", "Typed provider errors"), ("jwt_refresh", "Automatic JWT refresh"),
    ("safe_frontend_telemetry", "Redacted frontend telemetry"), ("request_ids", "Request correlation IDs"),
    ("rate_limiting", "AI endpoint throttling"), ("pagination", "Paginated AI resources"),
    ("filtering", "AI resource filtering"), ("streaming", "SSE response streaming"),
    ("cancel_requests", "Client-side request cancellation"), ("health_cache", "Cached provider health"),
    ("model_cache", "Cached model discovery"), ("response_cache", "Privacy-scoped response cache"),
    ("circuit_breaker", "Failure isolation"), ("prompt_guard", "Prompt safety guardrails"),
    ("secret_redaction", "Secret redaction in logs"), ("api_contract", "Canonical API contract"),
    ("connection_diagnostics", "End-to-end diagnostics"), ("production_checks", "Production readiness checks"),
]

def get_capabilities():
    return [{"key":k,"name":n,"enabled":True} for k,n in FEATURES]
