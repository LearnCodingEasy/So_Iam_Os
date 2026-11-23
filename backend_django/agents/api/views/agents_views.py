from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from agents.services import agent_service, execution_service

from core.api.owned import OwnedModelViewSet
from agents.api.serializers import AgentSerializer, AgentConfigurationSerializer, AgentRunSerializer, AgentExecutionSerializer
from agents.models import Agent, AgentConfiguration, AgentRun, AgentExecution


class AgentViewSet(OwnedModelViewSet):
    queryset_model = Agent
    serializer_class = AgentSerializer
    owner_lookup = 'user'
    filter_fields = ('status',)
    search_fields = ('name', 'role', 'description')
    ordering_fields = ('name', 'status', 'created_at', 'updated_at')


class AgentConfigurationViewSet(OwnedModelViewSet):
    queryset_model = AgentConfiguration
    serializer_class = AgentConfigurationSerializer
    owner_lookup = 'agent__user'
    set_owner_on_create = False
    filter_fields = ('agent', 'is_active')
    ordering_fields = ('version', 'created_at')

    def perform_create(self, serializer):
        data = {k: v for k, v in serializer.validated_data.items() if k != "agent"}
        serializer.instance = agent_service.create_configuration(
            agent=serializer.validated_data["agent"], **data
        )

    @action(detail=True, methods=["post"])
    def activate(self, request, pk=None):
        configuration = agent_service.activate_configuration(self.get_object())
        return Response(self.get_serializer(configuration).data)


class AgentRunViewSet(OwnedModelViewSet):
    queryset_model = AgentRun
    serializer_class = AgentRunSerializer
    owner_lookup = 'user'
    filter_fields = ('agent', 'status')
    search_fields = ('goal',)
    ordering_fields = ('created_at', 'status')
    select_related = ('agent',)

    def perform_create(self, serializer):
        try:
            serializer.instance = execution_service.create_run(
                user=self.request.user,
                agent=serializer.validated_data["agent"],
                goal=serializer.validated_data["goal"],
                input_data=serializer.validated_data.get("input_data") or {},
            )
        except execution_service.AgentRunError as exc:
            raise ValidationError({"detail": str(exc)})

    def _transition(self, fn):
        run = self.get_object()
        try:
            run = fn(run)
        except execution_service.AgentRunError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_409_CONFLICT)
        return Response(self.get_serializer(run).data)

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        return self._transition(execution_service.approve_run)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        return self._transition(execution_service.cancel_run)

    @action(detail=True, methods=["post"])
    def execute(self, request, pk=None):
        """Run the goal once through the central AI gateway (synchronous)."""
        return self._transition(execution_service.execute_run)


class AgentExecutionViewSet(OwnedModelViewSet):
    queryset_model = AgentExecution
    serializer_class = AgentExecutionSerializer
    owner_lookup = 'run__user'
    set_owner_on_create = False
    filter_fields = ('run', 'status')
    ordering_fields = ('step_index', 'created_at')

    http_method_names = ["get", "head", "options"]
