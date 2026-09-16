from django.urls import path

from .views import (
    AIChatView,
    AIConversationDetailView,
    AIConversationListCreateView,
)


app_name = "ai"


urlpatterns = [
    path(
        "chat/",
        AIChatView.as_view(),
        name="chat",
    ),

    path(
        "conversations/",
        AIConversationListCreateView.as_view(),
        name="conversation-list-create",
    ),

    path(
        "conversations/<int:pk>/",
        AIConversationDetailView.as_view(),
        name="conversation-detail",
    ),
]
