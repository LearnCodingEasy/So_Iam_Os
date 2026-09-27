from django.urls import path

from .views import (
    AIChatView, AIConversationDetailView, AIConversationListCreateView,
    AISettingsView, AIProviderCredentialListCreateView, AIProviderCredentialDetailView,
    AIProviderModelsView, AIPromptProfileListCreateView, AIPromptProfileDetailView,
    AILearningPlanPreviewView, AILearningPlanApproveView,
)

app_name = "ai"

urlpatterns = [
    path("chat/", AIChatView.as_view(), name="chat"),
    path("conversations/", AIConversationListCreateView.as_view(),
         name="conversation-list-create"),
    path("conversations/<int:pk>/", AIConversationDetailView.as_view(),
         name="conversation-detail"),
    path("settings/", AISettingsView.as_view(), name="settings"),
    path("credentials/", AIProviderCredentialListCreateView.as_view(),
         name="credentials"),
    path("credentials/<str:provider>/",
         AIProviderCredentialDetailView.as_view(), name="credential-detail"),
    path("providers/<str:provider>/models/",
         AIProviderModelsView.as_view(), name="provider-models"),
    path("prompts/", AIPromptProfileListCreateView.as_view(),
         name="prompt-list-create"),
    path("prompts/<int:pk>/", AIPromptProfileDetailView.as_view(),
         name="prompt-detail"),
    path("learning/preview/", AILearningPlanPreviewView.as_view(),
         name="learning-preview"),
    path("learning/approve/", AILearningPlanApproveView.as_view(),
         name="learning-approve"),
    # path("learning/async/", AILearningPlanAsyncView.as_view(), name="learning-async"),
    # path("tasks/<str:task_id>/", AITaskStatusView.as_view(), name="task-status"),
]
