from rest_framework.permissions import IsAuthenticated


class AIAuthenticatedPermission(IsAuthenticated):
    """
    Base permission for AI endpoints.
    """

    pass
