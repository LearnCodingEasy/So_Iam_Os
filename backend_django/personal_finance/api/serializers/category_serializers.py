from personal_finance.models import Category
from personal_finance.api.serializers.owned_model_serializers import OwnedModelSerializer


class CategorySerializer(OwnedModelSerializer):
    class Meta(OwnedModelSerializer.Meta):
        model = Category
