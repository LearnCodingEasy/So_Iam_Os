"""Domain validation for CRM payloads."""
from rest_framework.exceptions import ValidationError

from crm.models import CustomerRelationship


def _nonblank(attrs, field):
    if field in attrs and not str(attrs[field]).strip():
        raise ValidationError({field: "This field cannot be blank."})


def validate_company_payload(attrs, instance, user):
    _nonblank(attrs, "name")


def validate_contact_payload(attrs, instance, user):
    _nonblank(attrs, "first_name")


def validate_interaction_payload(attrs, instance, user):
    _nonblank(attrs, "subject")
    occurred = attrs.get("occurred_at", instance.occurred_at if instance else None)
    follow_up = attrs.get("follow_up_at", instance.follow_up_at if instance else None)
    if occurred and follow_up and follow_up < occurred:
        raise ValidationError({"follow_up_at": "Follow-up cannot be before the interaction."})


def validate_relationship_payload(attrs, instance, user):
    score = attrs.get("health_score")
    if score is not None and not 0 <= score <= 100:
        raise ValidationError({"health_score": "Must be between 0 and 100."})
    if instance is not None and "contact" in attrs and attrs["contact"] != instance.contact:
        raise ValidationError({"contact": "The contact of a relationship cannot be changed."})
