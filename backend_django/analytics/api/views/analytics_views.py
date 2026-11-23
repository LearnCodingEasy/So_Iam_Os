from rest_framework.decorators import action
from rest_framework.response import Response
from analytics.services import analytics_service
from analytics.validators.analytics_validator import parse_period

from core.api.owned import OwnedModelViewSet
from analytics.api.serializers import MetricSerializer, MetricSnapshotSerializer, AnalyticsEventSerializer, ReportSerializer
from analytics.models import Metric, MetricSnapshot, AnalyticsEvent, Report


class MetricViewSet(OwnedModelViewSet):
    queryset_model = Metric
    serializer_class = MetricSerializer
    owner_lookup = 'user'
    filter_fields = ('source_app', 'kind', 'is_active')
    search_fields = ('key', 'name', 'description')
    ordering_fields = ('name', 'key', 'created_at')

    @action(detail=True, methods=["get"])
    def summary(self, request, pk=None):
        start, end = parse_period(request.query_params.get("start"), request.query_params.get("end"))
        return Response(analytics_service.metric_summary(self.get_object(), start, end))


class MetricSnapshotViewSet(OwnedModelViewSet):
    queryset_model = MetricSnapshot
    serializer_class = MetricSnapshotSerializer
    owner_lookup = 'metric__user'
    set_owner_on_create = False
    filter_fields = ('metric',)
    ordering_fields = ('recorded_at', 'value')
    select_related = ('metric',)


class AnalyticsEventViewSet(OwnedModelViewSet):
    queryset_model = AnalyticsEvent
    serializer_class = AnalyticsEventSerializer
    owner_lookup = 'user'
    filter_fields = ('name', 'source_app')
    search_fields = ('name',)
    ordering_fields = ('occurred_at', 'name')

    @action(detail=False, methods=["get"])
    def counts(self, request):
        """Number of events per name (optionally within ?start=&end=)."""
        start, end = parse_period(request.query_params.get("start"), request.query_params.get("end"))
        return Response(analytics_service.event_counts(request.user, start, end))


class ReportViewSet(OwnedModelViewSet):
    queryset_model = Report
    serializer_class = ReportSerializer
    owner_lookup = 'user'
    filter_fields = ('report_type',)
    search_fields = ('title',)
    ordering_fields = ('title', 'created_at', 'generated_at')

    @action(detail=True, methods=["post"])
    def generate(self, request, pk=None):
        report = analytics_service.generate_report(self.get_object())
        return Response(self.get_serializer(report).data)
