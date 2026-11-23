from rest_framework import serializers  # noqa: F401

from core.api.owned import ensure_all_owned, ensure_owned, scope_related_fields
from sales.models import Offer, Deal, Sale, SalesActivity
from sales.validators.sales_validator import validate_deal_payload, validate_offer_payload, validate_sale_payload


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'
        read_only_fields = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request is not None and request.user.is_authenticated:
            scope_related_fields(self.fields, request.user, {'project': 'user'})

    def validate(self, attrs):
        user = self.context['request'].user
        ensure_owned(attrs.get('project'), user, 'project', 'user')
        validate_offer_payload(attrs, self.instance, user)
        return attrs


class DealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deal
        fields = '__all__'
        read_only_fields = ['user', 'stage', 'closed_at', 'lost_reason']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request is not None and request.user.is_authenticated:
            scope_related_fields(self.fields, request.user, {'contact': 'user', 'offer': 'user'})

    def validate(self, attrs):
        user = self.context['request'].user
        ensure_owned(attrs.get('contact'), user, 'contact', 'user')
        ensure_owned(attrs.get('offer'), user, 'offer', 'user')
        validate_deal_payload(attrs, self.instance, user)
        return attrs


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'
        read_only_fields = ['user', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request is not None and request.user.is_authenticated:
            scope_related_fields(self.fields, request.user, {'deal': 'user', 'offer': 'user', 'contact': 'user'})

    def validate(self, attrs):
        user = self.context['request'].user
        ensure_owned(attrs.get('deal'), user, 'deal', 'user')
        ensure_owned(attrs.get('offer'), user, 'offer', 'user')
        ensure_owned(attrs.get('contact'), user, 'contact', 'user')
        validate_sale_payload(attrs, self.instance, user)
        return attrs


class SalesActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesActivity
        fields = '__all__'
        read_only_fields = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request is not None and request.user.is_authenticated:
            scope_related_fields(self.fields, request.user, {'deal': 'user'})

    def validate(self, attrs):
        user = self.context['request'].user
        ensure_owned(attrs.get('deal'), user, 'deal', 'user')
        return attrs
