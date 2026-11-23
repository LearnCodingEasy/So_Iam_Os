from rest_framework.decorators import action
from rest_framework.response import Response
from architecture.services import architecture_service

from core.api.owned import OwnedModelViewSet
from architecture.api.serializers import ArchitectureSerializer, ComponentSerializer, DependencySerializer, ArchitectureDecisionSerializer
from architecture.models import Architecture, Component, Dependency, ArchitectureDecision


class ArchitectureViewSet(OwnedModelViewSet):
    queryset_model = Architecture
    serializer_class = ArchitectureSerializer
    owner_lookup = 'user'
    filter_fields = ('status',)
    search_fields = ('name', 'description')
    ordering_fields = ('name', 'status', 'created_at', 'updated_at')

    @action(detail=True, methods=["get"])
    def graph(self, request, pk=None):
        """Components as nodes, dependencies as edges, plus simple health metrics."""
        return Response(architecture_service.build_graph(self.get_object()))


class ComponentViewSet(OwnedModelViewSet):
    queryset_model = Component
    serializer_class = ComponentSerializer
    owner_lookup = 'architecture__user'
    set_owner_on_create = False
    filter_fields = ('architecture', 'component_type')
    search_fields = ('name', 'description', 'technology')
    ordering_fields = ('name', 'component_type', 'created_at')
    select_related = ('architecture',)


class DependencyViewSet(OwnedModelViewSet):
    queryset_model = Dependency
    serializer_class = DependencySerializer
    owner_lookup = 'source__architecture__user'
    set_owner_on_create = False
    filter_fields = ('source', 'target', 'dependency_type')
    ordering_fields = ('created_at',)
    select_related = ('source', 'target')


class ArchitectureDecisionViewSet(OwnedModelViewSet):
    queryset_model = ArchitectureDecision
    serializer_class = ArchitectureDecisionSerializer
    owner_lookup = 'architecture__user'
    set_owner_on_create = False
    filter_fields = ('architecture', 'status')
    search_fields = ('title', 'context', 'decision')
    ordering_fields = ('title', 'status', 'decided_on', 'created_at')
    select_related = ('architecture',)
