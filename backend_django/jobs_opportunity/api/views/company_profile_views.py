from rest_framework.decorators import action
from rest_framework.response import Response
from jobs_opportunity.models import CompanyProfile
from jobs_opportunity.api.serializers import CompanyProfileSerializer
from jobs_opportunity.api.views.user_owned_views import UserOwnedViewSet


class CompanyProfileViewSet(UserOwnedViewSet):
    serializer_class = CompanyProfileSerializer

    def get_queryset(self): return CompanyProfile.objects.filter(
        user=self.request.user)

    def perform_create(self, serializer): serializer.save(
        user=self.request.user)

    @action(detail=True, methods=["post"])
    def toggle_follow(self, request, pk=None):
        company = self.get_object()
        company.is_followed = not company.is_followed
        company.save(update_fields=["is_followed", "updated_at"])
        return Response(self.get_serializer(company).data)

    @action(detail=True, methods=["post"])
    def toggle_blacklist(self, request, pk=None):
        company = self.get_object()
        company.is_blacklisted = not company.is_blacklisted
        company.save(update_fields=["is_blacklisted", "updated_at"])
        return Response(self.get_serializer(company).data)
