"""Domain validation for challenge payloads."""
from rest_framework.exceptions import ValidationError


def validate_challenge_payload(attrs, instance, user):
    if "title" in attrs and not str(attrs["title"]).strip():
        raise ValidationError({"title": "Title cannot be blank."})
    if "metadata" in attrs and not isinstance(attrs["metadata"], dict):
        raise ValidationError({"metadata": "Must be a JSON object."})


def validate_step_payload(attrs, instance, user):
    if "title" in attrs and not str(attrs["title"]).strip():
        raise ValidationError({"title": "Title cannot be blank."})
    if "metadata" in attrs and not isinstance(attrs["metadata"], dict):
        raise ValidationError({"metadata": "Must be a JSON object."})


def validate_attempt_payload(attrs, instance, user):
    score = attrs.get("score")
    if score is not None and not 0 <= score <= 100:
        raise ValidationError({"score": "Must be between 0 and 100."})


def validate_progress_payload(attrs, instance, user):
    percent = attrs.get("progress_percent")
    if percent is not None and not 0 <= percent <= 100:
        raise ValidationError({"progress_percent": "Must be between 0 and 100."})
    challenge = attrs.get("challenge") or getattr(instance, "challenge", None)
    steps = attrs.get("completed_steps")
    if challenge is not None and steps is not None and steps > challenge.steps.count():
        raise ValidationError({"completed_steps": "Cannot exceed the number of steps in the challenge."})
