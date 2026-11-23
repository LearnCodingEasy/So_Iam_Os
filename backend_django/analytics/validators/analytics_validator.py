"""Domain validation for analytics payloads and query parameters."""
from django.utils.dateparse import parse_date, parse_datetime
from rest_framework.exceptions import ValidationError

from analytics.models import Metric


def _parse(value, field):
    if not value:
        return None
    parsed = parse_datetime(value) or parse_date(value)
    if parsed is None:
        raise ValidationError({field: "Use an ISO date (YYYY-MM-DD) or datetime."})
    return parsed


def parse_period(start, end):
    """Parse optional ?start=&end= query parameters."""
    start_value, end_value = _parse(start, "start"), _parse(end, "end")
    if start_value and end_value and type(start_value) is type(end_value) and start_value > end_value:
        raise ValidationError({"end": "End must not be before start."})
    return start_value, end_value


def validate_metric_payload(attrs, instance, user):
    key = attrs.get("key")
    if key is not None:
        clash = Metric.objects.filter(user=user, key=key)
        if instance is not None:
            clash = clash.exclude(pk=instance.pk)
        if clash.exists():
            raise ValidationError({"key": "You already track a metric with this key."})
    if "name" in attrs and not str(attrs["name"]).strip():
        raise ValidationError({"name": "Name cannot be blank."})


def validate_snapshot_payload(attrs, instance, user):
    if instance is not None and "metric" in attrs and attrs["metric"] != instance.metric:
        raise ValidationError({"metric": "A snapshot cannot be moved to another metric."})
    if "dimensions" in attrs and not isinstance(attrs["dimensions"], dict):
        raise ValidationError({"dimensions": "Must be a JSON object."})


def validate_event_payload(attrs, instance, user):
    if "name" in attrs and not str(attrs["name"]).strip():
        raise ValidationError({"name": "Name cannot be blank."})
    if "properties" in attrs and not isinstance(attrs["properties"], dict):
        raise ValidationError({"properties": "Must be a JSON object."})


def validate_report_payload(attrs, instance, user):
    start = attrs.get("period_start", instance.period_start if instance else None)
    end = attrs.get("period_end", instance.period_end if instance else None)
    if start and end and end < start:
        raise ValidationError({"period_end": "End must not be before start."})
    if "parameters" in attrs and not isinstance(attrs["parameters"], dict):
        raise ValidationError({"parameters": "Must be a JSON object."})
