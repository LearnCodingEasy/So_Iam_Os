"""User-scoped persistent conversation operations."""
from ..models import AIConversation, AIMessage
from ..exceptions import AIError

class ConversationService:
    @staticmethod
    def list_for_user(user):
        return AIConversation.objects.filter(user=user, is_active=True).prefetch_related("messages").order_by("-updated_at")
    @staticmethod
    def get_for_user(*, user, conversation_id):
        try:
            return AIConversation.objects.get(pk=conversation_id, user=user)
        except AIConversation.DoesNotExist as exc:
            raise AIError("Conversation does not exist.") from exc
    @staticmethod
    def rename(*, user, conversation_id, title):
        if not isinstance(title, str) or not title.strip():
            raise ValueError("A non-empty title is required.")
        conversation = ConversationService.get_for_user(user=user, conversation_id=conversation_id)
        conversation.title = title.strip()[:255]
        conversation.save(update_fields=["title", "updated_at"])
        return conversation
    @staticmethod
    def history(conversation):
        return conversation.messages.order_by("created_at")
