from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class UserOwnedViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
