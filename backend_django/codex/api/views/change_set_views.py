from codex.models import ChangeSet
from codex.api.serializers import ChangeSetSerializer
from codex.api.views.base_views import BaseViewSet


class ChangeSetViewSet(BaseViewSet):
    queryset = ChangeSet.objects.all()
    serializer_class = ChangeSetSerializer
