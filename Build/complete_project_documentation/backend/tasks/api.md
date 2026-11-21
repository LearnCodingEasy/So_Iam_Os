# tasks API

Project prefix: /api/tasks/ (source: backend_django/backend_django/urls.py). Route rows below are declarations; DRF router methods are implicit and not runtime-verified.


## Routes: tasks/api/urls.py

- L7: router.register(r"", TaskViewSet, basename="task")

## Handler declarations: tasks/api/views/tasks_views.py
L23: class TaskPagination(PageNumberPagination):
L29: class TaskViewSet(viewsets.ModelViewSet):
L30: serializer_class = TaskSerializer
L31: permission_classes = [IsAuthenticated]
L54: def get_queryset(self):
L160: def perform_create(self, serializer):
L165: def perform_update(self, serializer):
L179: def perform_destroy(self, instance):
L206: @action(detail=False, methods=["get"], url_path="today")
L223: @action(detail=False, methods=["post"], url_path="generate")
L299: @action(detail=True, methods=["post"])
L330: @action(detail=True, methods=["post"])
L361: @action(detail=True, methods=["post"])
L365: @action(detail=True, methods=["post"])
L369: @action(detail=True, methods=["post"])
L426: @action(detail=False, methods=["get"], url_path="stats")
L456: @action(detail=False, methods=["get"], url_path="progress")
L460: @action(detail=False, methods=["get"], url_path="calendar")
L503: @action(detail=False, methods=["get"], url_path="overdue")
L526: @action(


Full payload/response compatibility remains UNKNOWN until handlers, serializers and active frontend consumers are traced. See [cross-project API catalog](../../05-complete-api-catalog.md).
