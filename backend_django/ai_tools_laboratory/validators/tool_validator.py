"""Domain validation for the AI tools laboratory."""
from rest_framework.exceptions import ValidationError

from ai_tools_laboratory.models import ToolCategory

SECRET_MARKERS = ("key", "secret", "token", "password", "credential")


def validate_category_payload(attrs, instance, user):
    name = attrs.get("name")
    if name is None:
        return
    name = str(name).strip()
    if not name:
        raise ValidationError({"name": "Name cannot be blank."})
    clash = ToolCategory.objects.filter(user=user, name__iexact=name)
    if instance is not None:
        clash = clash.exclude(pk=instance.pk)
    if clash.exists():
        raise ValidationError({"name": "You already have a category with this name."})


def validate_tool_payload(attrs, instance, user):
    if "name" in attrs and not str(attrs["name"]).strip():
        raise ValidationError({"name": "Name cannot be blank."})
    rating = attrs.get("rating")
    if rating is not None and not 1 <= rating <= 5:
        raise ValidationError({"rating": "Rating must be between 1 and 5."})
    tags = attrs.get("tags")
    if tags is not None and (not isinstance(tags, list) or not all(isinstance(t, str) for t in tags)):
        raise ValidationError({"tags": "Tags must be a list of strings."})


def _looks_secret(key):
    name = str(key).lower()
    # Token *counts* such as max_tokens / num_tokens are ordinary settings, not credentials.
    if name.endswith("tokens"):
        return False
    return any(marker in name for marker in SECRET_MARKERS)


def _secret_keys(value, found=None):
    found = [] if found is None else found
    if isinstance(value, dict):
        for key, item in value.items():
            if _looks_secret(key):
                found.append(str(key))
            _secret_keys(item, found)
    elif isinstance(value, list):
        for item in value:
            _secret_keys(item, found)
    return found


def validate_configuration_payload(attrs, instance, user):
    if "name" in attrs and not str(attrs["name"]).strip():
        raise ValidationError({"name": "Name cannot be blank."})
    settings_value = attrs.get("settings")
    if settings_value is None:
        return
    if not isinstance(settings_value, dict):
        raise ValidationError({"settings": "Settings must be a JSON object."})
    secrets = _secret_keys(settings_value)
    if secrets:
        raise ValidationError({"settings": "Do not store credentials here (found: %s)." % ", ".join(sorted(set(secrets)))})


def validate_execution_payload(attrs, instance, user):
    tool = attrs.get("tool") or (instance.tool if instance else None)
    configuration = attrs.get("configuration", instance.configuration if instance else None)
    if configuration is not None and tool is not None and configuration.tool_id != tool.pk:
        raise ValidationError({"configuration": "Configuration belongs to a different tool."})
