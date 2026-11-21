from personal_finance.models import LendingBorrowing
from personal_finance.api.serializers.owned_model_serializers import OwnedModelSerializer


class LendingBorrowingSerializer(OwnedModelSerializer):
    class Meta(OwnedModelSerializer.Meta):
        model = LendingBorrowing
        read_only_fields = ["user"]
