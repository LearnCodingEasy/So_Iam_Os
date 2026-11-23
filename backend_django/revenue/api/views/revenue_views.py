from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from revenue.services import revenue_service
from revenue.validators.revenue_validator import parse_period
from sales.models import Sale

from core.api.owned import OwnedModelViewSet
from revenue.api.serializers import RevenueSourceSerializer, RevenueStreamSerializer, RevenueRecordSerializer, RecurringRevenueSerializer
from revenue.models import RevenueSource, RevenueStream, RevenueRecord, RecurringRevenue


class RevenueSourceViewSet(OwnedModelViewSet):
    queryset_model = RevenueSource
    serializer_class = RevenueSourceSerializer
    owner_lookup = 'user'
    filter_fields = ('source_type', 'is_active')
    search_fields = ('name', 'description')
    ordering_fields = ('name', 'created_at')


class RevenueStreamViewSet(OwnedModelViewSet):
    queryset_model = RevenueStream
    serializer_class = RevenueStreamSerializer
    owner_lookup = 'user'
    filter_fields = ('source', 'status')
    search_fields = ('name', 'description')
    ordering_fields = ('name', 'created_at')
    select_related = ('source',)


class RevenueRecordViewSet(OwnedModelViewSet):
    queryset_model = RevenueRecord
    serializer_class = RevenueRecordSerializer
    owner_lookup = 'user'
    filter_fields = ('stream', 'sale', 'currency')
    search_fields = ('description', 'reference')
    ordering_fields = ('received_on', 'amount', 'created_at')
    select_related = ('stream', 'sale')

    @action(detail=False, methods=["get"])
    def summary(self, request):
        """Totals per currency by month and by source (?start=&end= as dates)."""
        start, end = parse_period(request.query_params.get("start"), request.query_params.get("end"))
        return Response(revenue_service.summary(request.user, start, end))

    @action(detail=False, methods=["post"], url_path="from-sale")
    def from_sale(self, request):
        """Attribute a completed sale as received revenue (idempotent per sale)."""
        data = request.data if isinstance(request.data, dict) else {}
        sale = Sale.objects.filter(user=request.user, pk=data.get("sale")).first() if str(data.get("sale", "")).isdigit() else None
        if sale is None:
            return Response({"sale": "Select one of your sales."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            record, created = revenue_service.record_from_sale(request.user, sale, stream=None)
        except revenue_service.RevenueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_409_CONFLICT)
        return Response(self.get_serializer(record).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class RecurringRevenueViewSet(OwnedModelViewSet):
    queryset_model = RecurringRevenue
    serializer_class = RecurringRevenueSerializer
    owner_lookup = 'user'
    filter_fields = ('stream', 'status', 'interval', 'currency')
    search_fields = ('name',)
    ordering_fields = ('start_date', 'amount', 'created_at')
    select_related = ('stream',)

    @action(detail=False, methods=["get"])
    def mrr(self, request):
        """Monthly and annualised recurring revenue per currency."""
        return Response(revenue_service.monthly_recurring_revenue(request.user))
