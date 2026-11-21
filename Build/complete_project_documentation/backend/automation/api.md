# automation API

Project prefix: /api/automation/ (source: backend_django/backend_django/urls.py). Route rows below are declarations; DRF router methods are implicit and not runtime-verified.


## Routes: automation/api/urls.py

- L20: router.register(r'programs', ProgramViewSet, basename='program')

- L25: router.register(r'program-elements', ProgramElementViewSet,

- L31: router.register(r'workflows', WorkflowViewSet, basename='workflows')

- L36: router.register(r'workflow-nodes', WorkflowNodeViewSet,

- L42: router.register(r'workflow-edges', WorkflowEdgeViewSet,

- L48: router.register(r'actions', ActionViewSet, basename='action')

- L53: router.register(r'tasks', TaskViewSet, basename='task')

- L58: router.register(r'task-runs', TaskRunViewSet, basename='task-run')

- L63: router.register(r'screen-states', ScreenStateViewSet, basename='screen-state')

- L68: router.register(r'delays', DelayViewSet, basename='delay')

- L74: path('', include(router.urls)),

- L75: path('get_open_windows/', get_open_windows,

## Handler declarations: automation/api/views/action_views.py
L15: class ActionViewSet(viewsets.ModelViewSet):
L16: def get_queryset(self): return Action.objects.filter(created_by=self.request.user)
L18: serializer_class = ActionSerializer
L22: permission_classes = [permissions.IsAuthenticated]
L25: def perform_create(self, serializer):
L29: @action(detail=True, methods=['patch'])
L39: @action(detail=True, methods=["post"])
L51: @action(detail=False, methods=["get"])

## Handler declarations: automation/api/views/delay_views.py
L12: class DelayViewSet(viewsets.ReadOnlyModelViewSet):
L13: def get_queryset(self): return Delay.objects.filter(created_by=self.request.user)
L15: serializer_class = DelaySerializer
L18: permission_classes = [permissions.IsAuthenticated]
L21: def perform_create(self, serializer):

## Handler declarations: automation/api/views/program_element_views.py
L12: class ProgramElementViewSet(viewsets.ModelViewSet):
L13: def get_queryset(self): return ProgramElement.objects.filter(created_by=self.request.user)
L15: serializer_class = ProgramElementSerializer
L18: permission_classes = [permissions.IsAuthenticated]
L20: def perform_create(self, serializer):

## Handler declarations: automation/api/views/program_views.py
L17: class ProgramViewSet(viewsets.ModelViewSet):
L18: def get_queryset(self): return Program.objects.filter(created_by=self.request.user)
L20: serializer_class = ProgramSerializer
L23: permission_classes = [permissions.IsAuthenticated]
L26: def perform_create(self, serializer):
L29: @action(detail=True, methods=["post"])
L38: @action(detail=True, methods=["post"])
L44: @action(detail=True, methods=["get"])
L51: @action(detail=True, methods=['post'])
L57: @action(detail=True, methods=['post'])
L63: @action(detail=True, methods=["post"])

## Handler declarations: automation/api/views/screen_state_views.py
L12: class ScreenStateViewSet(viewsets.ModelViewSet):
L13: def get_queryset(self): return ScreenState.objects.filter(created_by=self.request.user)
L25: serializer_class = ScreenStateSerializer
L28: permission_classes = [permissions.IsAuthenticated]
L31: def perform_create(self, serializer):
L34: @action(detail=False, methods=["post"])
L50: @action(detail=False, methods=["get"])

## Handler declarations: automation/api/views/task_run_views.py
L11: class TaskRunViewSet(viewsets.ModelViewSet):
L12: def get_queryset(self): return TaskRun.objects.filter(created_by=self.request.user)
L14: serializer_class = TaskRunSerializer
L17: permission_classes = [permissions.IsAuthenticated]
L20: def perform_create(self, serializer):

## Handler declarations: automation/api/views/task_views.py
L12: class TaskViewSet(viewsets.ModelViewSet):
L13: def get_queryset(self): return Task.objects.filter(created_by=self.request.user)
L15: serializer_class = TaskSerializer
L19: permission_classes = [permissions.IsAuthenticated]
L22: def perform_create(self, serializer):

## Handler declarations: automation/api/views/workflow_edge_views.py
L12: class WorkflowEdgeViewSet(viewsets.ModelViewSet):
L13: def get_queryset(self): return WorkflowEdge.objects.filter(created_by=self.request.user)
L15: serializer_class = WorkflowEdgeSerializer
L19: permission_classes = [permissions.IsAuthenticated]
L22: def perform_create(self, serializer):

## Handler declarations: automation/api/views/workflow_node_views.py
L15: class WorkflowNodeViewSet(viewsets.ModelViewSet):
L16: def get_queryset(self): return WorkflowNode.objects.filter(created_by=self.request.user)
L18: serializer_class = WorkflowNodeSerializer
L23: permission_classes = [permissions.IsAuthenticated]
L26: def perform_create(self, serializer):
L29: @action(detail=True, methods=["post"])
L60: @action(detail=True, methods=["get"])

## Handler declarations: automation/api/views/workflow_views.py
L19: class WorkflowViewSet(viewsets.ModelViewSet):
L20: def get_queryset(self): return Workflow.objects.filter(created_by=self.request.user)
L22: serializer_class = WorkflowSerializer
L24: permission_classes = [permissions.IsAuthenticated]
L26: def perform_create(self, serializer):
L29: @action(detail=True, methods=["post"])
L50: @action(detail=True, methods=["get"])
L124: @action(detail=True, methods=['post'])


Full payload/response compatibility remains UNKNOWN until handlers, serializers and active frontend consumers are traced. See [cross-project API catalog](../../05-complete-api-catalog.md).
