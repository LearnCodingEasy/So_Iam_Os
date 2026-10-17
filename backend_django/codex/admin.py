from django.contrib import admin

from .models import (
    ProjectRegistry, Feature, FileRegistry, APIEndpoint, ProtectedFeature,
    ProtectedItem, CodexWorkflowStep, LocalAIJob, ChangeSet, ProjectSnapshot,
    CodexConversation, CodexMessage, CodexAnalysis,
    CodexFeatureDefinition, CodexToolDefinition, CodexAgentDefinition,
    CodexCapabilityRun,
)

admin.site.register([
    ProjectRegistry, Feature, FileRegistry, APIEndpoint, ProtectedFeature,
    ProtectedItem, CodexWorkflowStep, LocalAIJob, ChangeSet, ProjectSnapshot,
    CodexConversation, CodexMessage, CodexAnalysis,
    CodexFeatureDefinition, CodexToolDefinition, CodexAgentDefinition,
    CodexCapabilityRun,
])
