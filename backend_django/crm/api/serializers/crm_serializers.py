from rest_framework import serializers  # noqa: F401

from core.api.owned import ensure_all_owned, ensure_owned, scope_related_fields
from crm.models import Company, Contact, Interaction, CustomerRelationship
from crm.validators.crm_validator import validate_company_payload, validate_contact_payload, validate_interaction_payload, validate_relationship_payload


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
        read_only_fields = ['user']

    def validate(self, attrs):
        user = self.context['request'].user
        validate_company_payload(attrs, self.instance, user)
        return attrs


class ContactSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Contact
        fields = '__all__'
        read_only_fields = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request is not None and request.user.is_authenticated:
            scope_related_fields(self.fields, request.user, {'company': 'user'})

    def validate(self, attrs):
        user = self.context['request'].user
        ensure_owned(attrs.get('company'), user, 'company', 'user')
        validate_contact_payload(attrs, self.instance, user)
        return attrs


class InteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaction
        fields = '__all__'
        read_only_fields = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request is not None and request.user.is_authenticated:
            scope_related_fields(self.fields, request.user, {'contact': 'user'})

    def validate(self, attrs):
        user = self.context['request'].user
        ensure_owned(attrs.get('contact'), user, 'contact', 'user')
        validate_interaction_payload(attrs, self.instance, user)
        return attrs


class CustomerRelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerRelationship
        fields = '__all__'
        read_only_fields = ['user', 'stage_changed_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request is not None and request.user.is_authenticated:
            scope_related_fields(self.fields, request.user, {'contact': 'user'})

    def validate(self, attrs):
        user = self.context['request'].user
        ensure_owned(attrs.get('contact'), user, 'contact', 'user')
        validate_relationship_payload(attrs, self.instance, user)
        return attrs
