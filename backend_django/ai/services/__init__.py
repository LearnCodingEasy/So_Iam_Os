"""Modular AI service package with lazy, backward-compatible public exports."""

from importlib import import_module

_EXPORTS = {
    "AIService": ".core",
    "AIContextBuilder": ".core",
    "AIFallbackChainService": ".core",
    "AgentSelector": ".agent_selector",
    "AgentSelection": ".agent_selector",
    "AgentExecutor": ".agent_executor",
    "ProviderManager": ".provider_manager",
    "FallbackService": ".fallback_service",
    "ConversationService": ".conversation_service",
    "ContextInspector": ".context_inspector",
    "PromptTemplateService": ".prompt_template_service",
    "TaskPlanner": ".task_planner",
    "UsageService": ".usage_service",
    "WorkflowService": ".workflow_service",
}

__all__ = list(_EXPORTS)


def __getattr__(name):
    module_name = _EXPORTS.get(name)
    if not module_name:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module = import_module(module_name, __name__)
    value = getattr(module, name)
    globals()[name] = value
    return value
