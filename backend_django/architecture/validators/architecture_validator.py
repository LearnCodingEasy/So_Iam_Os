"""Domain validation for architecture payloads."""
from rest_framework.exceptions import ValidationError

from architecture.services.architecture_service import would_create_cycle


def _nonblank(attrs, field):
    if field in attrs and not str(attrs[field]).strip():
        raise ValidationError({field: "This field cannot be blank."})


def validate_architecture_payload(attrs, instance, user):
    _nonblank(attrs, "name")
    _nonblank(attrs, "version")


def validate_component_payload(attrs, instance, user):
    _nonblank(attrs, "name")
    if instance is not None and "architecture" in attrs and attrs["architecture"] != instance.architecture:
        raise ValidationError({"architecture": "A component cannot be moved to another architecture."})


def validate_dependency_payload(attrs, instance, user):
    source = attrs.get("source") or (instance.source if instance else None)
    target = attrs.get("target") or (instance.target if instance else None)
    if source is None or target is None:
        return
    if source.pk == target.pk:
        raise ValidationError({"target": "A component cannot depend on itself."})
    if source.architecture_id != target.architecture_id:
        raise ValidationError({"target": "Both components must belong to the same architecture."})
    if would_create_cycle(source, target, ignore_pk=instance.pk if instance else None):
        raise ValidationError({"target": "This dependency would create a circular dependency."})


def validate_decision_payload(attrs, instance, user):
    _nonblank(attrs, "title")
    architecture = attrs.get("architecture") or (instance.architecture if instance else None)
    successor = attrs.get("superseded_by")
    if successor is not None:
        if instance is not None and successor.pk == instance.pk:
            raise ValidationError({"superseded_by": "A decision cannot supersede itself."})
        if architecture is not None and successor.architecture_id != architecture.pk:
            raise ValidationError({"superseded_by": "Must be a decision of the same architecture."})
    status = attrs.get("status", instance.status if instance else None)
    replacement = attrs["superseded_by"] if "superseded_by" in attrs else (instance.superseded_by if instance else None)
    if status == "superseded" and replacement is None:
        raise ValidationError({"superseded_by": "Choose the decision that supersedes this one."})
