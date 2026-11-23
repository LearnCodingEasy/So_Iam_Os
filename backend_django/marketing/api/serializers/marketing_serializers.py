from rest_framework import serializers  # noqa: F401

from core.api.owned import ensure_all_owned, ensure_owned, scope_related_fields
from marketing.models import MarketingChannel, Campaign, MarketingContent, LeadSource
from marketing.validators.marketing_validator import validate_campaign_payload, validate_channel_payload, validate_content_payload, validate_lead_source_payload


class MarketingChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketingChannel
        fields = '__all__'
        read_only_fields = ['user']

    def validate(self, attrs):
        user = self.context['request'].user
        validate_channel_payload(attrs, self.instance, user)
        return attrs


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = '__all__'
        read_only_fields = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request is not None and request.user.is_authenticated:
            scope_related_fields(self.fields, request.user, {'channel': 'user'})

    def validate(self, attrs):
        user = self.context['request'].user
        ensure_owned(attrs.get('channel'), user, 'channel', 'user')
        validate_campaign_payload(attrs, self.instance, user)
        return attrs


class MarketingContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketingContent
        fields = '__all__'
        read_only_fields = ['user', 'published_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request is not None and request.user.is_authenticated:
            scope_related_fields(self.fields, request.user, {'campaign': 'user'})

    def validate(self, attrs):
        user = self.context['request'].user
        ensure_owned(attrs.get('campaign'), user, 'campaign', 'user')
        validate_content_payload(attrs, self.instance, user)
        return attrs


class LeadSourceSerializer(serializers.ModelSerializer):
    leads_count = serializers.SerializerMethodField()

    def get_leads_count(self, obj):
        return obj.contacts.count()

    class Meta:
        model = LeadSource
        fields = '__all__'
        read_only_fields = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request is not None and request.user.is_authenticated:
            scope_related_fields(self.fields, request.user, {'channel': 'user', 'campaign': 'user', 'contacts': 'user'})

    def validate(self, attrs):
        user = self.context['request'].user
        ensure_owned(attrs.get('channel'), user, 'channel', 'user')
        ensure_owned(attrs.get('campaign'), user, 'campaign', 'user')
        ensure_all_owned(attrs.get('contacts'), user, 'contacts', 'user')
        validate_lead_source_payload(attrs, self.instance, user)
        return attrs
