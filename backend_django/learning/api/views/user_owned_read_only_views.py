from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from learning.api.views.user_owned_queryset_mixin_views import UserOwnedQuerysetMixin


class UserOwnedReadOnlyViewSet(
    UserOwnedQuerysetMixin,
    viewsets.ReadOnlyModelViewSet,
):
    permission_classes = [IsAuthenticated]
