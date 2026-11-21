from personal_finance.models import Debt
from personal_finance.api.serializers.owned_model_serializers import OwnedModelSerializer


class DebtSerializer(OwnedModelSerializer):
    class Meta(OwnedModelSerializer.Meta):
        model = Debt
