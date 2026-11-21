from ..models import AIFeedback, AIMessage

class FeedbackService:
    @staticmethod
    def upsert(*, user, message_id, sentiment, reason="", comment="", feedback_category="", rating=None):
        if sentiment not in {"like","dislike"}:
            raise ValueError("sentiment must be like or dislike")
        message=AIMessage.objects.filter(
            pk=message_id, conversation__user=user, role=AIMessage.ROLE_ASSISTANT
        ).first()
        if not message: raise ValueError("Message not found.")
        return AIFeedback.objects.update_or_create(user=user,message=message,defaults={
            "sentiment":sentiment,"reason":reason[:255],"comment":comment, "feedback_category":feedback_category[:80], "rating":rating
        })[0]
