"""AI tools laboratory business logic."""
from django.db import transaction
from django.db.models import Avg, Count

from ai_tools_laboratory.models import Tool, ToolConfiguration, ToolExecution


@transaction.atomic
def save_configuration(serializer):
    """Save a configuration; at most one configuration per tool is the default."""
    configuration = serializer.save()
    if configuration.is_default:
        ToolConfiguration.objects.filter(tool=configuration.tool, is_default=True).exclude(
            pk=configuration.pk
        ).update(is_default=False)
    return configuration


def laboratory_summary(user):
    tools = Tool.objects.filter(user=user)
    by_status = {row["status"]: row["n"] for row in tools.values("status").annotate(n=Count("id"))}
    rated = tools.exclude(rating__isnull=True).aggregate(avg=Avg("rating"))["avg"]
    trials = ToolExecution.objects.filter(user=user)
    outcomes = {row["status"]: row["n"] for row in trials.values("status").annotate(n=Count("id"))}
    finished = outcomes.get("succeeded", 0) + outcomes.get("failed", 0)
    return {
        "tools_total": tools.count(),
        "tools_by_status": by_status,
        "average_rating": round(rated, 2) if rated is not None else None,
        "executions_total": trials.count(),
        "executions_by_status": outcomes,
        "success_rate": round(outcomes.get("succeeded", 0) / finished, 4) if finished else None,
    }
