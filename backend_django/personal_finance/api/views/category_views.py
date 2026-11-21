from __future__ import annotations
from personal_finance.models import Category
from personal_finance.api.serializers import CategorySerializer
from personal_finance.api.views.owned_views import Owned


class CategoryViewSet(Owned):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
