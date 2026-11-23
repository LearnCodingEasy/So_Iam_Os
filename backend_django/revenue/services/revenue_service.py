"""Revenue reporting, MRR and sale attribution. All money is kept as Decimal."""
from collections import defaultdict
from decimal import ROUND_HALF_UP, Decimal

from django.db import IntegrityError, transaction
from django.utils import timezone

from revenue.models import RecurringRevenue, RevenueRecord
from sales.models import Sale

CENT = Decimal("0.01")
MONTHS_PER_INTERVAL = {"monthly": 1, "quarterly": 3, "yearly": 12}


class RevenueError(Exception):
    """Raised when an attribution cannot be made."""


def _money(value):
    return str(Decimal(value).quantize(CENT, rounding=ROUND_HALF_UP))


def record_from_sale(user, sale, stream=None):
    """Create (once) the revenue record for ``sale``. Returns ``(record, created)``."""
    if sale.user_id != user.pk:
        raise RevenueError("Sale not found.")
    if sale.status != Sale.STATUS_COMPLETED:
        raise RevenueError("Only completed sales can be recognised as revenue.")
    existing = RevenueRecord.objects.filter(sale=sale).first()
    if existing:
        return existing, False
    try:
        with transaction.atomic():
            record = RevenueRecord.objects.create(
                user=user, sale=sale, stream=stream, amount=sale.amount, currency=sale.currency,
                received_on=timezone.localdate(sale.sold_at), reference=sale.reference,
                description="Sale #%s" % sale.pk,
            )
    except IntegrityError:  # concurrent request attributed the same sale first
        return RevenueRecord.objects.get(sale=sale), False
    return record, True


def summary(user, start=None, end=None):
    rows = RevenueRecord.objects.filter(user=user).select_related("stream__source")
    if start:
        rows = rows.filter(received_on__gte=start)
    if end:
        rows = rows.filter(received_on__lte=end)
    totals = defaultdict(Decimal)
    by_month = defaultdict(lambda: defaultdict(Decimal))
    by_source = defaultdict(lambda: defaultdict(Decimal))
    for row in rows:
        totals[row.currency] += row.amount
        by_month[row.currency][row.received_on.strftime("%Y-%m")] += row.amount
        label = row.stream.source.name if row.stream_id else "Unattributed"
        by_source[row.currency][label] += row.amount
    return {
        "count": rows.count(),
        "totals": {c: _money(v) for c, v in sorted(totals.items())},
        "by_month": {c: {m: _money(v) for m, v in sorted(months.items())} for c, months in sorted(by_month.items())},
        "by_source": {c: {s: _money(v) for s, v in sorted(src.items())} for c, src in sorted(by_source.items())},
    }


def monthly_recurring_revenue(user, on=None):
    on = on or timezone.localdate()
    items = RecurringRevenue.objects.filter(user=user, status=RecurringRevenue.STATUS_ACTIVE, start_date__lte=on)
    mrr = defaultdict(Decimal)
    count = 0
    for item in items:
        if item.end_date and item.end_date < on:
            continue
        mrr[item.currency] += item.amount / MONTHS_PER_INTERVAL[item.interval]
        count += 1
    return {
        "as_of": on.isoformat(),
        "active_items": count,
        "mrr": {c: _money(v) for c, v in sorted(mrr.items())},
        "arr": {c: _money(v * 12) for c, v in sorted(mrr.items())},
    }
