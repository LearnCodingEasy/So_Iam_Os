from __future__ import annotations
from personal_finance.models import Subscription
from personal_finance.api.serializers import SubscriptionSerializer
from personal_finance.api.views.owned_views import Owned


class SubscriptionViewSet(Owned):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
