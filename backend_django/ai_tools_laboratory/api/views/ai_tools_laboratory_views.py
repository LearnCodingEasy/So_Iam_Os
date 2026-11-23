from rest_framework.decorators import action
from rest_framework.response import Response
from ai_tools_laboratory.services import tool_service

from core.api.owned import OwnedModelViewSet
from ai_tools_laboratory.api.serializers import ToolCategorySerializer, ToolSerializer, ToolConfigurationSerializer, ToolExecutionSerializer
from ai_tools_laboratory.models import ToolCategory, Tool, ToolConfiguration, ToolExecution


class ToolCategoryViewSet(OwnedModelViewSet):
    queryset_model = ToolCategory
    serializer_class = ToolCategorySerializer
    owner_lookup = 'user'
    search_fields = ('name', 'description')
    ordering_fields = ('name', 'created_at')


class ToolViewSet(OwnedModelViewSet):
    queryset_model = Tool
    serializer_class = ToolSerializer
    owner_lookup = 'user'
    filter_fields = ('status', 'category')
    search_fields = ('name', 'vendor', 'description', 'notes')
    ordering_fields = ('name', 'rating', 'status', 'created_at', 'updated_at')
    select_related = ('category',)

    @action(detail=False, methods=["get"])
    def summary(self, request):
        """Counts, average rating and trial outcomes across the user's laboratory."""
        return Response(tool_service.laboratory_summary(request.user))


class ToolConfigurationViewSet(OwnedModelViewSet):
    queryset_model = ToolConfiguration
    serializer_class = ToolConfigurationSerializer
    owner_lookup = 'tool__user'
    set_owner_on_create = False
    filter_fields = ('tool', 'is_default')
    search_fields = ('name',)
    ordering_fields = ('name', 'created_at')

    def perform_create(self, serializer):
        serializer.instance = tool_service.save_configuration(serializer)

    def perform_update(self, serializer):
        serializer.instance = tool_service.save_configuration(serializer)


class ToolExecutionViewSet(OwnedModelViewSet):
    queryset_model = ToolExecution
    serializer_class = ToolExecutionSerializer
    owner_lookup = 'user'
    filter_fields = ('tool', 'status')
    search_fields = ('input_text', 'output_text', 'notes')
    ordering_fields = ('executed_at', 'status', 'duration_ms')
    select_related = ('tool',)
