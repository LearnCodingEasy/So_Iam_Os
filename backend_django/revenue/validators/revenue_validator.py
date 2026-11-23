"""Domain validation for revenue payloads."""
from decimal import Decimal

from django.utils.dateparse import parse_date
from rest_framework.exceptions import ValidationError

from revenue.models import RevenueRecord


def _nonblank(attrs, field):
    if field in attrs and not str(attrs[field]).strip():
        raise ValidationError({field: "This field cannot be blank."})


def _currency(attrs):
    code = attrs.get("currency")
    if code is not None and not (len(code) == 3 and code.isalpha() and code.isupper()):
        raise ValidationError({"currency": "Use a 3-letter uppercase currency code, e.g. USD."})


def parse_period(start, end):
    """Parse optional ?start=&end= date query parameters."""
    out = []
    for field, value in (("start", start), ("end", end)):
        if not value:
            out.append(None)
            continue
        parsed = parse_date(value)
        if parsed is None:
            raise ValidationError({field: "Use an ISO date (YYYY-MM-DD)."})
        out.append(parsed)
    if out[0] and out[1] and out[1] < out[0]:
        raise ValidationError({"end": "End must not be before start."})
    return out[0], out[1]


def validate_source_payload(attrs, instance, user):
    _nonblank(attrs, "name")


def validate_stream_payload(attrs, instance, user):
    _nonblank(attrs, "name")


def _require_amount(attrs, instance):
    if instance is None and attrs.get("amount") is None:
        raise ValidationError({"amount": "This field is required."})


def validate_record_payload(attrs, instance, user):
    _currency(attrs)
    _require_amount(attrs, instance)
    if attrs.get("amount") is not None and attrs["amount"] <= Decimal("0"):
        raise ValidationError({"amount": "Amount must be greater than zero."})
    sale = attrs.get("sale")
    if sale is None:
        return
    if sale.status != "completed":
        raise ValidationError({"sale": "Only completed sales can be recognised as revenue."})
    clash = RevenueRecord.objects.filter(sale=sale)
    if instance is not None:
        clash = clash.exclude(pk=instance.pk)
    if clash.exists():
        raise ValidationError({"sale": "This sale is already attributed to a revenue record."})
    currency = attrs.get("currency", instance.currency if instance else "USD")
    if currency != sale.currency:
        raise ValidationError({"currency": "Currency must match the sale (%s)." % sale.currency})


def validate_recurring_payload(attrs, instance, user):
    _currency(attrs)
    _require_amount(attrs, instance)
    if attrs.get("amount") is not None and attrs["amount"] <= Decimal("0"):
        raise ValidationError({"amount": "Amount must be greater than zero."})
    start = attrs.get("start_date", instance.start_date if instance else None)
    end = attrs.get("end_date", instance.end_date if instance else None)
    if start and end and end < start:
        raise ValidationError({"end_date": "End date must not be before the start date."})
