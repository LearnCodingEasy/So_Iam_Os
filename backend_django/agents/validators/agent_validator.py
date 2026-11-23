"""Domain validation for agent payloads."""
from rest_framework.exceptions import ValidationError


def _require_dict(attrs, field):
    if field in attrs and not isinstance(attrs[field], dict):
        raise ValidationError({field: "Must be a JSON object."})


def validate_agent_payload(attrs, instance, user):
    if "name" in attrs and not str(attrs["name"]).strip():
        raise ValidationError({"name": "Name cannot be blank."})
    _require_dict(attrs, "metadata")


def validate_configuration_payload(attrs, instance, user):
    temperature = attrs.get("temperature")
    if temperature is not None and not 0 <= temperature <= 2:
        raise ValidationError({"temperature": "Must be between 0 and 2."})
    max_steps = attrs.get("max_steps")
    if max_steps is not None and not 1 <= max_steps <= 100:
        raise ValidationError({"max_steps": "Must be between 1 and 100."})
    tools = attrs.get("tools")
    if tools is not None and (not isinstance(tools, list) or not all(isinstance(t, str) for t in tools)):
        raise ValidationError({"tools": "Must be a list of tool names."})
    _require_dict(attrs, "parameters")


def validate_run_payload(attrs, instance, user):
    if "goal" in attrs and not str(attrs["goal"]).strip():
        raise ValidationError({"goal": "Goal cannot be blank."})
    _require_dict(attrs, "input_data")
