from rest_framework.permissions import IsAuthenticated

class CodexAuthenticated(IsAuthenticated):
    """Foundation access is authenticated; destructive execution is intentionally not exposed here."""
    pass
