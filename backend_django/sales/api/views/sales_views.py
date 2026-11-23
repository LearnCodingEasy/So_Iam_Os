from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from sales.services import sales_service

from core.api.owned import OwnedModelViewSet
from sales.api.serializers import OfferSerializer, DealSerializer, SaleSerializer, SalesActivitySerializer
from sales.models import Offer, Deal, Sale, SalesActivity


class OfferViewSet(OwnedModelViewSet):
    queryset_model = Offer
    serializer_class = OfferSerializer
    owner_lookup = 'user'
    filter_fields = ('status', 'project', 'currency')
    search_fields = ('name', 'description')
    ordering_fields = ('name', 'price', 'created_at')


class DealViewSet(OwnedModelViewSet):
    queryset_model = Deal
    serializer_class = DealSerializer
    owner_lookup = 'user'
    filter_fields = ('stage', 'contact', 'offer', 'currency')
    search_fields = ('title',)
    ordering_fields = ('title', 'value', 'expected_close_date', 'created_at', 'updated_at')
    select_related = ('contact', 'offer')

    @action(detail=True, methods=["post"], url_path="set-stage")
    def set_stage(self, request, pk=None):
        """Move the deal to ``stage``. Winning creates the sale; losing needs ``lost_reason``."""
        data = request.data if isinstance(request.data, dict) else {}
        try:
            deal = sales_service.set_stage(self.get_object(), data.get("stage"), data.get("lost_reason", ""))
        except sales_service.SalesError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_409_CONFLICT)
        return Response(self.get_serializer(deal).data)

    @action(detail=False, methods=["get"])
    def pipeline(self, request):
        return Response(sales_service.pipeline_summary(request.user))


class SaleViewSet(OwnedModelViewSet):
    queryset_model = Sale
    serializer_class = SaleSerializer
    owner_lookup = 'user'
    filter_fields = ('status', 'deal', 'offer', 'contact', 'currency')
    search_fields = ('reference',)
    ordering_fields = ('sold_at', 'amount', 'created_at')
    select_related = ('deal', 'offer', 'contact')

    @action(detail=True, methods=["post"])
    def refund(self, request, pk=None):
        try:
            sale = sales_service.refund_sale(self.get_object())
        except sales_service.SalesError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_409_CONFLICT)
        return Response(self.get_serializer(sale).data)


class SalesActivityViewSet(OwnedModelViewSet):
    queryset_model = SalesActivity
    serializer_class = SalesActivitySerializer
    owner_lookup = 'user'
    filter_fields = ('deal', 'activity_type')
    search_fields = ('notes',)
    ordering_fields = ('occurred_at',)
    select_related = ('deal',)
