"""Domain validation for sales payloads."""
from decimal import Decimal

from rest_framework.exceptions import ValidationError


def _nonblank(attrs, field):
    if field in attrs and not str(attrs[field]).strip():
        raise ValidationError({field: "This field cannot be blank."})


def _currency(attrs):
    code = attrs.get("currency")
    if code is not None and not (len(code) == 3 and code.isalpha() and code.isupper()):
        raise ValidationError({"currency": "Use a 3-letter uppercase currency code, e.g. USD."})


def validate_offer_payload(attrs, instance, user):
    _nonblank(attrs, "name")
    _currency(attrs)
    if attrs.get("price") is not None and attrs["price"] < Decimal("0"):
        raise ValidationError({"price": "Price cannot be negative."})


def validate_deal_payload(attrs, instance, user):
    _nonblank(attrs, "title")
    _currency(attrs)
    if attrs.get("value") is not None and attrs["value"] < Decimal("0"):
        raise ValidationError({"value": "Value cannot be negative."})
    if instance is not None and instance.stage in ("won", "lost") and {"value", "currency", "offer", "contact"} & set(attrs):
        raise ValidationError({"detail": "A closed deal can no longer be edited."})


def validate_sale_payload(attrs, instance, user):
    _currency(attrs)
    if attrs.get("amount") is not None and attrs["amount"] <= Decimal("0"):
        raise ValidationError({"amount": "Amount must be greater than zero."})
    if instance is not None and {"amount", "currency"} & set(attrs):
        records = getattr(instance, "revenue_records", None)  # reverse relation owned by the revenue app
        if records is not None and records.exists():
            raise ValidationError({"detail": "A sale with attributed revenue cannot change amount or currency."})
