from personal_finance.models import Subscription
from personal_finance.api.serializers.owned_model_serializers import OwnedModelSerializer


class SubscriptionSerializer(OwnedModelSerializer):
    class Meta(OwnedModelSerializer.Meta):
        model = Subscription
