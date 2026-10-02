# backend_django\automation\admin.py


from django.contrib import admin


from .models import Program, ProgramElement, Workflow, WorkflowNode, WorkflowEdge, Action, Task, TaskRun, ScreenState, Delay


admin.site.register(Program)
admin.site.register(ProgramElement)
admin.site.register(Workflow)
admin.site.register(WorkflowNode)
admin.site.register(WorkflowEdge)
admin.site.register(Action)
admin.site.register(Task)
admin.site.register(TaskRun)
admin.site.register(ScreenState)
admin.site.register(Delay)
