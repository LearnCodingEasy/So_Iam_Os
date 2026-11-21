# automation security and testing

## Permission/ownership evidence

- automation/api/views/action_views.py:L16: def get_queryset(self): return Action.objects.filter(created_by=self.request.user)
- automation/api/views/action_views.py:L22: permission_classes = [permissions.IsAuthenticated]
- automation/api/views/action_views.py:L26: serializer.save(created_by=self.request.user)
- automation/api/views/delay_views.py:L13: def get_queryset(self): return Delay.objects.filter(created_by=self.request.user)
- automation/api/views/delay_views.py:L18: permission_classes = [permissions.IsAuthenticated]
- automation/api/views/delay_views.py:L22: serializer.save(created_by=self.request.user)
- automation/api/views/program_element_views.py:L13: def get_queryset(self): return ProgramElement.objects.filter(created_by=self.request.user)
- automation/api/views/program_element_views.py:L18: permission_classes = [permissions.IsAuthenticated]
- automation/api/views/program_element_views.py:L21: serializer.save(created_by=self.request.user)
- automation/api/views/program_views.py:L18: def get_queryset(self): return Program.objects.filter(created_by=self.request.user)
- automation/api/views/program_views.py:L23: permission_classes = [permissions.IsAuthenticated]
- automation/api/views/program_views.py:L27: serializer.save(created_by=self.request.user)
- automation/api/views/program_views.py:L70: program, request.user, custom_pattern=custom_pattern
- automation/api/views/screen_state_views.py:L13: def get_queryset(self): return ScreenState.objects.filter(created_by=self.request.user)
- automation/api/views/screen_state_views.py:L28: permission_classes = [permissions.IsAuthenticated]
- automation/api/views/screen_state_views.py:L32: serializer.save(created_by=self.request.user)
- automation/api/views/task_run_views.py:L12: def get_queryset(self): return TaskRun.objects.filter(created_by=self.request.user)
- automation/api/views/task_run_views.py:L17: permission_classes = [permissions.IsAuthenticated]
- automation/api/views/task_run_views.py:L21: serializer.save(created_by=self.request.user)
- automation/api/views/task_views.py:L13: def get_queryset(self): return Task.objects.filter(created_by=self.request.user)
- automation/api/views/task_views.py:L19: permission_classes = [permissions.IsAuthenticated]
- automation/api/views/task_views.py:L23: serializer.save(created_by=self.request.user)
- automation/api/views/workflow_edge_views.py:L13: def get_queryset(self): return WorkflowEdge.objects.filter(created_by=self.request.user)
- automation/api/views/workflow_edge_views.py:L19: permission_classes = [permissions.IsAuthenticated]
- automation/api/views/workflow_edge_views.py:L23: serializer.save(created_by=self.request.user
- automation/api/views/workflow_node_views.py:L16: def get_queryset(self): return WorkflowNode.objects.filter(created_by=self.request.user)
- automation/api/views/workflow_node_views.py:L23: permission_classes = [permissions.IsAuthenticated]
- automation/api/views/workflow_node_views.py:L27: serializer.save(created_by=self.request.user)
- automation/api/views/workflow_views.py:L20: def get_queryset(self): return Workflow.objects.filter(created_by=self.request.user)
- automation/api/views/workflow_views.py:L24: permission_classes = [permissions.IsAuthenticated]
- automation/api/views/workflow_views.py:L27: serializer.save(created_by=self.request.user)
- automation/api/views/workflow_views.py:L39: task_run = TaskRun.objects.create(workflow=workflow, status="running", created_by=request.user)
- automation/api/views/workflow_views.py:L41: async_result = execute_workflow_task.delay(str(workflow.id), str(request.user.id), str(task_run.id))
- automation/api/views/workflow_views.py:L179: created_by=request.user
- automation/api/views/workflow_views.py:L214: created_by=request.user


## Tests
- automation/tests/test_automation.py
- automation/tests/__init__.py


Tests were not run. This scan is not a complete authorization/security review. Shared guidance: [authentication and permissions](../../07-authentication-and-permissions.md).
