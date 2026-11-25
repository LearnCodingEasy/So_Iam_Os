"""AI insight over the user's real CRM -> Sales -> Revenue data.

All figures are aggregated from the database for ``user`` only; nothing is
invented. If the user has no business records the service refuses instead of
asking the model to analyse an empty set. The model call goes through
``AIFallbackChainService.generate_completion`` so the execution, usage and
audit rows (AIExecution / AIUsageRecord / AiAuditLog) are created by the
existing audited path, tagged ``task_type="business_insight"``.
"""
import json
from datetime import timedelta

from django.db.models import Avg, Count, Sum
from django.utils import timezone

from ai.exceptions import AIError

TASK_TYPE = "business_insight"


class NoBusinessDataError(AIError):
    default_message = "There is no CRM, sales or revenue data to analyse yet."

    def __init__(self, message=None):
        super().__init__(message, category="no_business_data", retryable=False)


def collect_business_snapshot(user, *, days=90):
    from crm.models import Contact, CustomerRelationship
    from sales.models import Deal, Sale
    from revenue.models import RevenueRecord

    since = timezone.now() - timedelta(days=days)
    contacts = Contact.objects.filter(user=user)
    relationships = CustomerRelationship.objects.filter(user=user)
    deals = Deal.objects.filter(user=user)
    sales = Sale.objects.filter(user=user, status=Sale.STATUS_COMPLETED)
    revenue = RevenueRecord.objects.filter(user=user, received_on__gte=since.date())

    def money(qs, field):
        return float(qs.aggregate(t=Sum(field))["t"] or 0)

    pipeline = {
        row["stage"]: {"count": row["n"], "value": float(row["v"] or 0)}
        for row in deals.values("stage").annotate(n=Count("id"), v=Sum("value"))
    }
    snapshot = {
        "window_days": days,
        "crm": {
            "contacts": contacts.count(),
            "relationship_stages": {
                r["stage"]: r["n"] for r in relationships.values("stage").annotate(n=Count("id"))
            },
            "avg_health_score": round(float(relationships.aggregate(a=Avg("health_score"))["a"] or 0), 1),
        },
        "sales": {
            "pipeline_by_stage": pipeline,
            "open_pipeline_value": sum(v["value"] for k, v in pipeline.items() if k in Deal.OPEN_STAGES),
            "completed_sales": sales.count(),
            "completed_sales_amount": money(sales, "amount"),
        },
        "revenue": {
            "records_in_window": revenue.count(),
            "received_in_window": money(revenue, "amount"),
            "attributed_to_sales": revenue.filter(sale__isnull=False).count(),
        },
    }
    has_data = (
        snapshot["crm"]["contacts"] or pipeline or snapshot["sales"]["completed_sales"]
        or snapshot["revenue"]["records_in_window"]
    )
    return snapshot, bool(has_data)


def generate_business_insight(user, *, provider=None, model=None, timeout_seconds=None, days=90):
    from .core import AIFallbackChainService, AIService

    snapshot, has_data = collect_business_snapshot(user, days=days)
    if not has_data:
        raise NoBusinessDataError()

    if not provider:
        provider = AIService(user).get_settings().preferred_provider
    messages = [
        {"role": "system", "content": (
            "You are a business analyst inside So_Iam_OS. Use ONLY the JSON figures provided. "
            "Do not invent numbers, customers or trends. If a figure is missing or zero, say so. "
            "Answer with: 1) a two-sentence summary, 2) the top 3 risks, 3) the top 3 next actions."
        )},
        {"role": "user", "content": "Business snapshot:\n" + json.dumps(snapshot, ensure_ascii=False)},
    ]
    result = AIFallbackChainService.generate_completion(
        messages=messages, user=user, preferred_provider=provider, model=model or None,
        temperature=0.3, max_tokens=900, task_type=TASK_TYPE,
        timeout_seconds=timeout_seconds,
    )
    return {
        "insight": result["content"],
        "provider": result.get("provider"),
        "model": result.get("model"),
        "execution_id": result.get("execution_id"),
        "snapshot": snapshot,
    }
