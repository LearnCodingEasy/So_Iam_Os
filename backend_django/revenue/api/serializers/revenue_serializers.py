from rest_framework import serializers  # noqa: F401

from core.api.owned import ensure_all_owned, ensure_owned, scope_related_fields
from revenue.models import RevenueSource, RevenueStream, RevenueRecord, RecurringRevenue
from revenue.validators.revenue_validator import validate_record_payload, validate_recurring_payload, validate_source_payload, validate_stream_payload


class RevenueSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RevenueSource
        fields = '__all__'
        read_only_fields = ['user']

    def validate(self, attrs):
        user = self.context['request'].user
        validate_source_payload(attrs, self.instance, user)
        return attrs


class RevenueStreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = RevenueStream
        fields = '__all__'
        read_only_fields = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request is not None and request.user.is_authenticated:
            scope_related_fields(self.fields, request.user, {'source': 'user'})

    def validate(self, attrs):
        user = self.context['request'].user
        ensure_owned(attrs.get('source'), user, 'source', 'user')
        validate_stream_payload(attrs, self.instance, user)
        return attrs


class RevenueRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = RevenueRecord
        fields = '__all__'
        read_only_fields = ['user']
        validators = []  # uniqueness enforced by the DB constraint + service

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request is not None and request.user.is_authenticated:
            scope_related_fields(self.fields, request.user, {'stream': 'user', 'sale': 'user'})

    def validate(self, attrs):
        user = self.context['request'].user
        ensure_owned(attrs.get('stream'), user, 'stream', 'user')
        ensure_owned(attrs.get('sale'), user, 'sale', 'user')
        validate_record_payload(attrs, self.instance, user)
        return attrs


class RecurringRevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringRevenue
        fields = '__all__'
        read_only_fields = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request is not None and request.user.is_authenticated:
            scope_related_fields(self.fields, request.user, {'stream': 'user'})

    def validate(self, attrs):
        user = self.context['request'].user
        ensure_owned(attrs.get('stream'), user, 'stream', 'user')
        validate_recurring_payload(attrs, self.instance, user)
        return attrs
