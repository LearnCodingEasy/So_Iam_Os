from rest_framework.decorators import action
from rest_framework.response import Response
from crm.services import crm_service

from core.api.owned import OwnedModelViewSet
from crm.api.serializers import CompanySerializer, ContactSerializer, InteractionSerializer, CustomerRelationshipSerializer
from crm.models import Company, Contact, Interaction, CustomerRelationship


class CompanyViewSet(OwnedModelViewSet):
    queryset_model = Company
    serializer_class = CompanySerializer
    owner_lookup = 'user'
    search_fields = ('name', 'industry', 'notes')
    ordering_fields = ('name', 'created_at', 'updated_at')


class ContactViewSet(OwnedModelViewSet):
    queryset_model = Contact
    serializer_class = ContactSerializer
    owner_lookup = 'user'
    filter_fields = ('status', 'company', 'source')
    search_fields = ('first_name', 'last_name', 'email', 'job_title', 'notes')
    ordering_fields = ('first_name', 'last_name', 'created_at', 'updated_at')
    select_related = ('company',)


class InteractionViewSet(OwnedModelViewSet):
    queryset_model = Interaction
    serializer_class = InteractionSerializer
    owner_lookup = 'user'
    filter_fields = ('contact', 'interaction_type')
    search_fields = ('subject', 'notes')
    ordering_fields = ('occurred_at', 'follow_up_at', 'created_at')
    select_related = ('contact',)

    @action(detail=False, methods=["get"], url_path="follow-ups")
    def follow_ups(self, request):
        """Interactions with a follow-up due within ?days= (default 7), overdue first."""
        try:
            days = max(0, min(int(request.query_params.get("days", 7)), 365))
        except ValueError:
            days = 7
        rows = crm_service.due_follow_ups(request.user, days)
        return Response(self.get_serializer(rows, many=True).data)


class CustomerRelationshipViewSet(OwnedModelViewSet):
    queryset_model = CustomerRelationship
    serializer_class = CustomerRelationshipSerializer
    owner_lookup = 'user'
    filter_fields = ('stage', 'contact')
    search_fields = ('next_step', 'contact__first_name', 'contact__last_name')
    ordering_fields = ('stage', 'health_score', 'updated_at')
    select_related = ('contact',)

    def perform_update(self, serializer):
        serializer.instance = crm_service.save_relationship(serializer)

    @action(detail=False, methods=["get"])
    def pipeline(self, request):
        """Number of relationships per stage."""
        return Response(crm_service.pipeline_summary(request.user))
