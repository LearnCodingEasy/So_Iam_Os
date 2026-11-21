from ..models import AiAuditLog


class AuditService:
    @staticmethod
    def record(*, user, action, resource="", result="success", execution=None, metadata=None):
        safe = dict(metadata or {})
        for key in ("api_key", "token", "password", "secret", "authorization"):
            safe.pop(key, None)
        safe.update({"result": result})
        if execution is not None:
            safe["execution_id"] = execution.pk
        return AiAuditLog.objects.create(
            user=user,
            action=action,
            resource=resource or "",
            details=safe,
        )

    @staticmethod
    def list_for_user(user, limit=100):
        return AiAuditLog.objects.filter(user=user).order_by("-created_at")[:max(1, min(limit, 500))]

    @staticmethod
    def log_event(user, action, resource=None, details=None, ip_address=None):
        return AiAuditLog.objects.create(
            user=user,
            action=action,
            resource=resource,
            details=details or {},
            ip_address=ip_address,
        )
