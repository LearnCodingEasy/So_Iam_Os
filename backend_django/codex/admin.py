from django.contrib import admin
from .models import ProjectRegistry, Feature, FileRegistry, APIEndpoint, ProtectedFeature, ChangeSet, ProjectSnapshot,    CodexConversation, CodexMessage, CodexAnalysis


admin.site.register([
    ProjectRegistry,
    Feature,
    FileRegistry,
    APIEndpoint,
    ProtectedFeature,
    ChangeSet,
    ProjectSnapshot,
    CodexConversation,
    CodexMessage,
    CodexAnalysis,
])
