from rest_framework import serializers  # noqa: F401

from core.api.owned import ensure_all_owned, ensure_owned, scope_related_fields
from analytics.models import Metric, MetricSnapshot, AnalyticsEvent, Report
from analytics.validators.analytics_validator import validate_event_payload, validate_metric_payload, validate_report_payload, validate_snapshot_payload


class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = '__all__'
        read_only_fields = ['user']
        validators = []  # uniqueness enforced by the DB constraint + service

    def validate(self, attrs):
        user = self.context['request'].user
        validate_metric_payload(attrs, self.instance, user)
        return attrs


class MetricSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetricSnapshot
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request is not None and request.user.is_authenticated:
            scope_related_fields(self.fields, request.user, {'metric': 'user'})

    def validate(self, attrs):
        user = self.context['request'].user
        ensure_owned(attrs.get('metric'), user, 'metric', 'user')
        validate_snapshot_payload(attrs, self.instance, user)
        return attrs


class AnalyticsEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyticsEvent
        fields = '__all__'
        read_only_fields = ['user']

    def validate(self, attrs):
        user = self.context['request'].user
        validate_event_payload(attrs, self.instance, user)
        return attrs


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'
        read_only_fields = ['user', 'content', 'generated_at']

    def validate(self, attrs):
        user = self.context['request'].user
        validate_report_payload(attrs, self.instance, user)
        return attrs
