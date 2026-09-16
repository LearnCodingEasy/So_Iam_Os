from rest_framework.permissions import BasePermission


class IsAuthenticatedUser(BasePermission):
    """
    Allows access only to authenticated users.
    """

    message = "Authentication is required."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
        )
