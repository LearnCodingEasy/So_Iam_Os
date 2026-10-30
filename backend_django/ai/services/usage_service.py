"""Usage aggregation from persisted AI messages where available."""
from django.db.models import Count
from ..models import AIConversation, AIMessage
class UsageService:
    @staticmethod
    def summarize(*, user=None):
        qs = AIMessage.objects.filter(conversation__user=user) if user is not None else AIMessage.objects.all()
        return {"message_count": qs.count(),
                "assistant_message_count": qs.filter(role=AIMessage.ROLE_ASSISTANT).count(),
                "by_provider": list(qs.filter(provider__gt="").values("provider").annotate(count=Count("id")).order_by("-count"))}
