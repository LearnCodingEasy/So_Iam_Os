"""Metric aggregation, event counting and report generation (real DB aggregates)."""
from datetime import datetime, time, timedelta

from django.db.models import Avg, Count, Max, Min
from django.utils import timezone

from analytics.models import AnalyticsEvent, Metric, MetricSnapshot


def _bounds(start, end):
    """Accept date/datetime/None and return aware datetimes (end is inclusive for dates)."""
    def aware(value, end_of_day=False):
        if value is None:
            return None
        if not isinstance(value, datetime):
            value = datetime.combine(value, time.max if end_of_day else time.min)
        return timezone.make_aware(value) if timezone.is_naive(value) else value

    return aware(start), aware(end, end_of_day=True)


def _number(value):
    return float(value) if value is not None else None


def record_snapshot(metric, value, recorded_at=None, dimensions=None):
    return MetricSnapshot.objects.create(
        metric=metric, value=value, recorded_at=recorded_at or timezone.now(), dimensions=dimensions or {}
    )


def metric_summary(metric, start=None, end=None):
    start_dt, end_dt = _bounds(start, end)
    rows = MetricSnapshot.objects.filter(metric=metric)
    if start_dt:
        rows = rows.filter(recorded_at__gte=start_dt)
    if end_dt:
        rows = rows.filter(recorded_at__lte=end_dt)
    stats = rows.aggregate(count=Count("id"), minimum=Min("value"), maximum=Max("value"), average=Avg("value"))
    first = rows.order_by("recorded_at", "id").first()
    latest = rows.order_by("-recorded_at", "-id").first()
    change = change_percent = None
    if first and latest and first.pk != latest.pk:
        change = float(latest.value - first.value)
        if first.value:
            change_percent = round(change / float(first.value) * 100, 2)
    return {
        "metric": metric.pk, "key": metric.key, "unit": metric.unit, "count": stats["count"],
        "latest": _number(latest.value) if latest else None,
        "latest_at": latest.recorded_at if latest else None,
        "min": _number(stats["minimum"]), "max": _number(stats["maximum"]),
        "average": round(_number(stats["average"]), 4) if stats["average"] is not None else None,
        "change": change, "change_percent": change_percent,
    }


def event_counts(user, start=None, end=None):
    start_dt, end_dt = _bounds(start, end)
    rows = AnalyticsEvent.objects.filter(user=user)
    if start_dt:
        rows = rows.filter(occurred_at__gte=start_dt)
    if end_dt:
        rows = rows.filter(occurred_at__lte=end_dt)
    grouped = rows.values("name").annotate(count=Count("id")).order_by("-count", "name")
    return {"total": rows.count(), "events": list(grouped)}


def generate_report(report):
    """Compute and persist the report content from the user's own data."""
    start, end = report.period_start, report.period_end
    if report.report_type == report.TYPE_SUMMARY:
        metrics = Metric.objects.filter(user=report.user, is_active=True)
        content = {"metrics": [metric_summary(m, start, end) for m in metrics]}
    elif report.report_type == report.TYPE_EVENTS:
        content = event_counts(report.user, start, end)
    else:  # metric_trend
        try:
            metric_id = int(report.parameters.get("metric"))
        except (TypeError, ValueError):
            metric_id = None
        metric = Metric.objects.filter(user=report.user, pk=metric_id).first() if metric_id else None
        if metric is None:
            content = {"error": "Set parameters.metric to the id of one of your metrics."}
        else:
            start_dt, end_dt = _bounds(start, end)
            rows = metric.snapshots.order_by("recorded_at", "id")
            if start_dt:
                rows = rows.filter(recorded_at__gte=start_dt)
            if end_dt:
                rows = rows.filter(recorded_at__lte=end_dt)
            content = {"metric": metric.pk, "key": metric.key,
                       "points": [{"at": r.recorded_at, "value": float(r.value)} for r in rows]}
    report.content = _jsonable(content)
    report.generated_at = timezone.now()
    report.save(update_fields=["content", "generated_at", "updated_at"])
    return report


def _jsonable(value):
    if isinstance(value, dict):
        return {k: _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(v) for v in value]
    if isinstance(value, datetime):
        return value.isoformat()
    return value
