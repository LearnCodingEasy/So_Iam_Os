# ai API

Project prefix: /api/ai/ (source: backend_django/backend_django/urls.py). Route rows below are declarations; DRF router methods are implicit and not runtime-verified.


## Routes: ai/api/urls.py

- L8: path("agents/plan/", AIAgentPlanView.as_view(), name="agent-plan"),

- L9: path("topic-chat/", AITopicChatView.as_view(), name="ai-topic-chat"),

- L10: path("chat/", AIChatView.as_view(), name="chat"),

- L11: path("chat/stream/", AIChatStreamView.as_view(), name="chat-stream"),

- L12: path("health/", AIHealthView.as_view(), name="health"),

- L13: path("capabilities/", AICapabilitiesView.as_view(), name="capabilities"),

- L14: path("conversations/", AIConversationListCreateView.as_view(),

- L16: path("conversations/<int:pk>/", AIConversationDetailView.as_view(),

- L18: path("settings/", AISettingsView.as_view(), name="settings"),

- L19: path("credentials/", AIProviderCredentialListCreateView.as_view(),

- L21: path("credentials/<str:provider>/",

- L23: path("providers/<str:provider>/models/",

- L25: path("providers/<str:provider>/test/",

- L27: path("providers/", AIProviderListView.as_view(), name="provider-list"),

- L28: path("usage/", AIUsageView.as_view(), name="usage"),

- L29: path("executions/", AIExecutionListView.as_view(), name="executions"),

- L30: path("budgets/", AIBudgetListCreateView.as_view(), name="budgets"),

- L31: path("budgets/<int:pk>/", AIBudgetDetailView.as_view(), name="budget-detail"),

- L32: path("workflows/", AIWorkflowListCreateView.as_view(),

- L34: path("workflows/<int:pk>/", AIWorkflowDetailView.as_view(),

- L36: path("workflows/<int:pk>/runs/",

- L38: path("audit/", AIAuditListView.as_view(), name="audit"),

- L39: path("feedback/", AIFeedbackView.as_view(), name="feedback"),

- L40: path("conversations/<int:pk>/context/",

- L42: path("workflows/validate/", AIWorkflowValidateView.as_view(),

- L44: path("tasks/proposal/", AITaskProposalView.as_view(), name="task-proposal"),

- L45: path("agent/select/", AIAgentSelectView.as_view(), name="agent-select"),

- L46: path("prompts/", AIPromptProfileListCreateView.as_view(),

- L48: path("prompts/<int:pk>/", AIPromptProfileDetailView.as_view(),

- L50: path("learning/preview/", AILearningPlanPreviewView.as_view(),

- L52: path("learning/approve/", AILearningPlanApproveView.as_view(),

- L54: path("learning/async/", AILearningPlanAsyncView.as_view(), name="learning-async"),

- L55: path("tasks/<str:task_id>/", AITaskStatusView.as_view(), name="task-status"),

## Handler declarations: ai/api/views/ai_views.py
L3: from rest_framework.decorators import permission_classes
L21: class AIChatView(APIView):
L22: permission_classes = [AIAuthenticatedPermission]
L66: class AIConversationListCreateView(APIView):
L67: permission_classes = [AIAuthenticatedPermission]
L81: class AIConversationDetailView(APIView):
L82: permission_classes = [AIAuthenticatedPermission]
L124: class AISettingsView(APIView):
L125: permission_classes = [IsAuthenticated]
L140: class AIProviderCredentialListCreateView(APIView):
L141: permission_classes = [IsAuthenticated]
L155: class AIProviderCredentialDetailView(APIView):
L156: permission_classes = [IsAuthenticated]
L167: class AIProviderModelsView(APIView):
L168: permission_classes = [IsAuthenticated]
L186: class AIProviderTestView(APIView):
L188: permission_classes = [IsAuthenticated]
L256: class AIProviderListView(APIView):
L257: permission_classes = [IsAuthenticated]
L264: class AIExecutionListView(APIView):
L265: permission_classes = [IsAuthenticated]
L273: class AIBudgetListCreateView(APIView):
L274: permission_classes = [IsAuthenticated]
L293: class AIAuditListView(APIView):
L294: permission_classes = [IsAuthenticated]
L302: class AIFeedbackView(APIView):
L304: permission_classes = [IsAuthenticated]
L333: class AIBudgetDetailView(APIView):
L334: permission_classes = [IsAuthenticated]
L356: class AIWorkflowListCreateView(APIView):
L357: permission_classes = [IsAuthenticated]
L376: class AIWorkflowDetailView(APIView):
L377: permission_classes = [IsAuthenticated]
L405: class AIWorkflowRunsView(APIView):
L406: permission_classes = [IsAuthenticated]
L423: class AIUsageView(APIView):
L424: permission_classes = [IsAuthenticated]
L431: class AIContextInspectView(APIView):
L432: permission_classes = [IsAuthenticated]
L443: class AIWorkflowValidateView(APIView):
L444: permission_classes = [IsAuthenticated]
L452: class AITaskProposalView(APIView):
L453: permission_classes = [IsAuthenticated]
L470: class AIAgentSelectView(APIView):
L471: permission_classes = [IsAuthenticated]
L492: class AIPromptProfileViewSetMixin:
L496: class AIPromptProfileListCreateView(APIView):
L497: permission_classes = [IsAuthenticated]
L515: class AIPromptProfileDetailView(APIView):
L516: permission_classes = [IsAuthenticated]
L550: class AILearningPlanPreviewView(APIView):
L551: permission_classes = [IsAuthenticated]
L569: class AILearningPlanApproveView(APIView):
L570: permission_classes = [IsAuthenticated]
L585: class AILearningPlanAsyncView(APIView):
L586: permission_classes = [IsAuthenticated]
L626: class AITaskStatusView(APIView):
L627: permission_classes = [IsAuthenticated]
L662: class AITopicChatView(APIView):
L663: permission_classes = [AIAuthenticatedPermission]
L753: class AIAgentPlanView(APIView):
L754: permission_classes = [IsAuthenticated]
L778: class AIHealthView(APIView):
L779: permission_classes = [AIAuthenticatedPermission]
L786: class AICapabilitiesView(APIView):
L787: permission_classes = [AIAuthenticatedPermission]
L795: class AIChatStreamView(APIView):
L796: permission_classes = [AIAuthenticatedPermission]


Full payload/response compatibility remains UNKNOWN until handlers, serializers and active frontend consumers are traced. See [cross-project API catalog](../../05-complete-api-catalog.md).
