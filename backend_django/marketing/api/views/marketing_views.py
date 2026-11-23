from rest_framework.decorators import action
from rest_framework.response import Response
from marketing.services import marketing_service

from core.api.owned import OwnedModelViewSet
from marketing.api.serializers import MarketingChannelSerializer, CampaignSerializer, MarketingContentSerializer, LeadSourceSerializer
from marketing.models import MarketingChannel, Campaign, MarketingContent, LeadSource


class MarketingChannelViewSet(OwnedModelViewSet):
    queryset_model = MarketingChannel
    serializer_class = MarketingChannelSerializer
    owner_lookup = 'user'
    filter_fields = ('channel_type', 'is_active')
    search_fields = ('name',)
    ordering_fields = ('name', 'created_at')


class CampaignViewSet(OwnedModelViewSet):
    queryset_model = Campaign
    serializer_class = CampaignSerializer
    owner_lookup = 'user'
    filter_fields = ('status', 'channel')
    search_fields = ('name', 'objective')
    ordering_fields = ('name', 'status', 'budget', 'start_date', 'created_at')
    select_related = ('channel',)

    @action(detail=True, methods=["get"])
    def performance(self, request, pk=None):
        """Budget use, lead count, cost per lead and content output of one campaign."""
        return Response(marketing_service.campaign_performance(self.get_object()))

    @action(detail=False, methods=["get"])
    def overview(self, request):
        return Response(marketing_service.overview(request.user))


class MarketingContentViewSet(OwnedModelViewSet):
    queryset_model = MarketingContent
    serializer_class = MarketingContentSerializer
    owner_lookup = 'user'
    filter_fields = ('status', 'content_type', 'campaign')
    search_fields = ('title', 'body')
    ordering_fields = ('title', 'status', 'publish_at', 'created_at', 'updated_at')
    select_related = ('campaign',)

    @action(detail=True, methods=["post"])
    def publish(self, request, pk=None):
        """Mark the content as published now (records the time; does not post anywhere)."""
        return Response(self.get_serializer(marketing_service.mark_published(self.get_object())).data)


class LeadSourceViewSet(OwnedModelViewSet):
    queryset_model = LeadSource
    serializer_class = LeadSourceSerializer
    owner_lookup = 'user'
    filter_fields = ('channel', 'campaign', 'is_active')
    search_fields = ('name', 'description')
    ordering_fields = ('name', 'created_at')
    select_related = ('channel', 'campaign')
