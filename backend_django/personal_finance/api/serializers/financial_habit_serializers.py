from personal_finance.models import FinancialHabit
from personal_finance.api.serializers.owned_model_serializers import OwnedModelSerializer


class FinancialHabitSerializer(OwnedModelSerializer):
    class Meta(OwnedModelSerializer.Meta):
        model = FinancialHabit
