"""Domain validation for marketing payloads."""
from decimal import Decimal

from rest_framework.exceptions import ValidationError


def _nonblank(attrs, field):
    if field in attrs and not str(attrs[field]).strip():
        raise ValidationError({field: "This field cannot be blank."})


def validate_channel_payload(attrs, instance, user):
    _nonblank(attrs, "name")


def validate_campaign_payload(attrs, instance, user):
    _nonblank(attrs, "name")
    for field in ("budget", "spent"):
        if attrs.get(field) is not None and attrs[field] < Decimal("0"):
            raise ValidationError({field: "Cannot be negative."})
    start = attrs.get("start_date", instance.start_date if instance else None)
    end = attrs.get("end_date", instance.end_date if instance else None)
    if start and end and end < start:
        raise ValidationError({"end_date": "End date must not be before the start date."})


def validate_content_payload(attrs, instance, user):
    _nonblank(attrs, "title")
    status = attrs.get("status", instance.status if instance else None)
    publish_at = attrs.get("publish_at", instance.publish_at if instance else None)
    if status == "scheduled" and publish_at is None:
        raise ValidationError({"publish_at": "Choose when scheduled content should go out."})


def validate_lead_source_payload(attrs, instance, user):
    _nonblank(attrs, "name")
