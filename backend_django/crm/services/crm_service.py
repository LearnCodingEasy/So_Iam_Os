"""CRM business logic: pipeline summary, follow-ups and stage tracking."""
from datetime import timedelta

from django.utils import timezone

from crm.models import CustomerRelationship, Interaction


def save_relationship(serializer):
    """Save a relationship update and stamp ``stage_changed_at`` when the stage changed."""
    previous = serializer.instance.stage if serializer.instance else None
    relationship = serializer.save()
    if previous is not None and relationship.stage != previous:
        relationship.stage_changed_at = timezone.now()
        relationship.save(update_fields=["stage_changed_at"])
    return relationship


def pipeline_summary(user):
    counts = {stage: 0 for stage, _ in CustomerRelationship.STAGE_CHOICES}
    for relationship in CustomerRelationship.objects.filter(user=user).values_list("stage", flat=True):
        counts[relationship] = counts.get(relationship, 0) + 1
    total = sum(counts.values())
    return {"total": total, "stages": counts}


def due_follow_ups(user, days=7):
    horizon = timezone.now() + timedelta(days=days)
    return (
        Interaction.objects.filter(user=user, follow_up_at__isnull=False, follow_up_at__lte=horizon)
        .select_related("contact")
        .order_by("follow_up_at")
    )
