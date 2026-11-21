import logging
from django.utils import timezone
from django.db import transaction

from ..models import AIExecution, AIUsageRecord, AiAuditLog

logger = logging.getLogger(__name__)


class ExecutionService:
    @staticmethod
    def start(*, user, agent="default", task_type="chat", conversation=None,
              provider="", model="", metadata=None, idempotency_key="", external_request_id=""):
        if idempotency_key:
            existing = AIExecution.objects.filter(
                user=user, idempotency_key=idempotency_key).first()
            if existing:
                return existing
        obj = AIExecution.objects.create(
            user=user,
            conversation=conversation,
            agent=agent,
            task_type=task_type,
            requested_provider=provider or "",
            provider=provider or "",
            model=model or "",
            status=AIExecution.Status.RUNNING,
            idempotency_key=idempotency_key or "",
            external_request_id=external_request_id or "",
            started_at=timezone.now(),
            metadata=metadata or {},
        )
        AiAuditLog.objects.create(
            user=user,
            action="execution.started",
            resource=task_type,
            details={
                "execution_id": obj.pk,
                "result": "started",
                "provider": provider or "",
                "model": model or "",
            },
        )
        return obj

    @staticmethod
    def finish(obj, *, status="succeeded", provider=None, model=None,
               retry_count=None, fallback_count=None, genuine_result=None,
               input_tokens=None, output_tokens=None, cost=None,
               error_code="", error_message="", metadata=None):
        now = timezone.now()
        terminal = {AIExecution.Status.SUCCEEDED,
                    AIExecution.Status.FAILED, AIExecution.Status.CANCELLED}
        if obj.status in terminal and status != obj.status:
            return obj
        if status not in dict(AIExecution.Status.choices):
            raise ValueError(f"Invalid AI execution status: {status}")
        obj.status = status
        obj.finished_at = now
        obj.provider = provider or obj.provider
        obj.model = model or obj.model
        if retry_count is not None:
            obj.retry_count = max(0, int(retry_count))
        if fallback_count is not None:
            obj.fallback_count = max(0, int(fallback_count))
        if genuine_result is not None:
            obj.genuine_result = bool(genuine_result)
        obj.input_tokens = input_tokens
        obj.output_tokens = output_tokens
        obj.estimated_cost = cost
        obj.error_code = error_code or ""
        obj.error_message = (error_message or "")[:4000]
        if metadata:
            obj.metadata = {**(obj.metadata or {}), **metadata}
        if obj.started_at:
            obj.duration_ms = max(
                0, int((now - obj.started_at).total_seconds() * 1000)
            )
        obj.save()

        AIUsageRecord.objects.update_or_create(
            execution=obj,
            defaults={
                "user": obj.user,
                "provider": obj.provider,
                "model": obj.model,
                "agent": obj.agent,
                "input_tokens": input_tokens or 0,
                "output_tokens": output_tokens or 0,
                "estimated_cost": cost or 0,
                "is_estimated": cost is None,
            },
        )
        AiAuditLog.objects.create(
            user=obj.user,
            action=f"execution.{status}",
            resource=obj.task_type,
            details={
                "execution_id": obj.pk,
                "result": "success" if status == "succeeded" else "failed",
                "provider": obj.provider,
                "model": obj.model,
                "duration_ms": obj.duration_ms,
                "retry_count": obj.retry_count,
                "fallback_count": obj.fallback_count,
            },
        )
        return obj
