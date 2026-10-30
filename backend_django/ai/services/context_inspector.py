"""Safe context summary that avoids exposing prompt or secret contents."""
from ..models import AIConversation
class ContextInspector:
    @staticmethod
    def inspect_conversation(*, user, conversation_id):
        conversation = AIConversation.objects.filter(user=user, pk=conversation_id).first()
        if conversation is None:
            return None
        messages = conversation.messages.order_by("created_at")
        return {"conversation_id": conversation.pk, "message_count": messages.count(),
                "roles": list(messages.values_list("role", flat=True).distinct()),
                "provider": conversation.provider, "model": conversation.model,
                "note": "System prompt and message contents are intentionally omitted."}
