from personal_finance.models import RecurringCashflow
from personal_finance.api.serializers.owned_model_serializers import OwnedModelSerializer


class RecurringCashflowSerializer(OwnedModelSerializer):
    class Meta(OwnedModelSerializer.Meta):
        model = RecurringCashflow
