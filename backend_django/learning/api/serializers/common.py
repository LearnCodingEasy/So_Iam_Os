from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


# ===================================================
# Helpers
# ===================================================


def get_request_user(serializer):
    """
    Return the authenticated user from serializer context.
    """
    request = serializer.context.get("request")

    if request and request.user and request.user.is_authenticated:
        return request.user

    return None


def ensure_owner(user, obj, field_name="object"):
    """
    Ensure an object belongs to the current user.
    """
    if obj is None:
        return

    if hasattr(obj, "user_id"):
        if obj.user_id != user.id:
            raise serializers.ValidationError(
                {
                    field_name: (
                        "This object does not belong to the current user."
                    )
                }
            )
