"""Deal pipeline and sale lifecycle."""
from collections import defaultdict
from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from sales.models import Deal, Sale


class SalesError(Exception):
    """Raised when a pipeline operation is not allowed."""


def set_stage(deal, stage, lost_reason=""):
    valid = {value for value, _ in Deal.STAGE_CHOICES}
    if stage not in valid:
        raise SalesError("Unknown stage. Choose one of: %s." % ", ".join(sorted(valid)))
    with transaction.atomic():
        deal = Deal.objects.select_for_update().get(pk=deal.pk)
        if deal.stage not in Deal.OPEN_STAGES:
            raise SalesError("A closed deal cannot change stage.")
        if stage == Deal.STAGE_WON and deal.value <= 0:
            raise SalesError("Set a deal value above zero before marking it won.")
        if stage == Deal.STAGE_LOST and not str(lost_reason or "").strip():
            raise SalesError("A reason is required to mark a deal lost.")
        now = timezone.now()
        deal.stage = stage
        if stage in (Deal.STAGE_WON, Deal.STAGE_LOST):
            deal.closed_at = now
        if stage == Deal.STAGE_LOST:
            deal.lost_reason = str(lost_reason).strip()
        deal.save()
        if stage == Deal.STAGE_WON:
            Sale.objects.create(
                user=deal.user, deal=deal, offer=deal.offer, contact=deal.contact,
                amount=deal.value, currency=deal.currency, sold_at=now,
            )
    return deal


def refund_sale(sale):
    with transaction.atomic():
        sale = Sale.objects.select_for_update().get(pk=sale.pk)
        if sale.status != Sale.STATUS_COMPLETED:
            raise SalesError("Only completed sales can be refunded.")
        sale.status = Sale.STATUS_REFUNDED
        sale.save(update_fields=["status"])
    return sale


def pipeline_summary(user):
    stages = {stage: {"count": 0, "value": defaultdict(float)} for stage, _ in Deal.STAGE_CHOICES}
    for deal in Deal.objects.filter(user=user).only("stage", "value", "currency"):
        bucket = stages[deal.stage]
        bucket["count"] += 1
        bucket["value"][deal.currency] += float(deal.value)
    won, lost = stages[Deal.STAGE_WON]["count"], stages[Deal.STAGE_LOST]["count"]
    return {
        "stages": {k: {"count": v["count"], "value": dict(v["value"])} for k, v in stages.items()},
        "open_count": sum(stages[s]["count"] for s in Deal.OPEN_STAGES),
        "win_rate": round(won / (won + lost), 4) if (won + lost) else None,
    }
