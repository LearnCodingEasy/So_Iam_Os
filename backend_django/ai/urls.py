from django.urls import path

from .views import (
    AITopicChatView, AIAgentPlanView,
    AIChatView, AIConversationDetailView, AIConversationListCreateView,
    AISettingsView, AIProviderCredentialListCreateView, AIProviderCredentialDetailView,
    AIProviderModelsView, AIProviderTestView, AIProviderListView, AIUsageView,
    AIContextInspectView, AIWorkflowValidateView, AITaskProposalView, AIAgentSelectView,
    AIPromptProfileListCreateView, AIPromptProfileDetailView,
    AILearningPlanPreviewView, AILearningPlanApproveView, AILearningPlanAsyncView, AITaskStatusView,
)

app_name = "ai"

urlpatterns = [
    path("agents/plan/", AIAgentPlanView.as_view(), name="agent-plan"),
    path("topic-chat/", AITopicChatView.as_view(), name="ai-topic-chat"),
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
    path("providers/<str:provider>/test/",
         AIProviderTestView.as_view(), name="provider-test"),
    path("providers/", AIProviderListView.as_view(), name="provider-list"),
    path("usage/", AIUsageView.as_view(), name="usage"),
    path("conversations/<int:pk>/context/", AIContextInspectView.as_view(), name="conversation-context"),
    path("workflows/validate/", AIWorkflowValidateView.as_view(), name="workflow-validate"),
    path("tasks/proposal/", AITaskProposalView.as_view(), name="task-proposal"),
    path("agent/select/", AIAgentSelectView.as_view(), name="agent-select"),
    path("prompts/", AIPromptProfileListCreateView.as_view(),
         name="prompt-list-create"),
    path("prompts/<int:pk>/", AIPromptProfileDetailView.as_view(),
         name="prompt-detail"),
    path("learning/preview/", AILearningPlanPreviewView.as_view(),
         name="learning-preview"),
    path("learning/approve/", AILearningPlanApproveView.as_view(),
         name="learning-approve"),
    path("learning/async/", AILearningPlanAsyncView.as_view(), name="learning-async"),
    path("tasks/<str:task_id>/", AITaskStatusView.as_view(), name="task-status"),
]
