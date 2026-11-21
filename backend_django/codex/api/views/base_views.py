from rest_framework.viewsets import ModelViewSet
from codex.permissions import CodexAuthenticated


class BaseViewSet(ModelViewSet):
    permission_classes = [CodexAuthenticated]
