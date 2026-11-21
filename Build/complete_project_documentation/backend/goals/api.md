# goals API

Project prefix: /api/goals/ (source: backend_django/backend_django/urls.py). Route rows below are declarations; DRF router methods are implicit and not runtime-verified.


## Routes: goals/api/urls.py

- L5: router.register(r"milestones", GoalMilestoneViewSet, basename="goal-milestone")

- L6: router.register(r"", GoalViewSet, basename="goal")

## Handler declarations: goals/api/views/goals_views.py
L22: class GoalPagination(PageNumberPagination):
L28: class GoalViewSet(viewsets.ModelViewSet):
L29: serializer_class = GoalSerializer
L30: permission_classes = [IsAuthenticated]
L33: def get_queryset(self):
L59: def perform_create(self, serializer):
L70: def perform_update(self, serializer):
L88: def perform_destroy(self, instance):
L93: @action(detail=False, methods=["get"])
L97: @action(detail=True, methods=["get"])
L103: @action(detail=True, methods=["post"])
L112: @action(detail=True, methods=["post"])
L116: @action(detail=True, methods=["post"])
L120: @action(detail=True, methods=["post"])
L132: @action(detail=True, methods=["post"], url_path="progress")
L143: @action(detail=True, methods=["post"])
L157: @action(detail=True, methods=["post"])
L195: @action(detail=True, methods=["post"], url_path="plan")
L233: @action(detail=True, methods=["post"], url_path="reject-plan")
L247: @action(detail=True, methods=["get"])
L252: @action(detail=True, methods=["post"], url_path="approve-plan")
L270: @action(detail=True, methods=["post"])
L281: @action(detail=True, methods=["post"], url_path="milestones/reorder")
L302: @action(detail=True, methods=["get", "post"], url_path="projects")
L320: @action(detail=True, methods=["get"])
L325: class GoalMilestoneViewSet(viewsets.ModelViewSet):
L326: serializer_class = GoalMilestoneSerializer
L327: permission_classes = [IsAuthenticated]
L329: def get_queryset(self):
L337: def perform_create(self, serializer):
L350: def perform_update(self, serializer):
L367: def perform_destroy(self, instance):


Full payload/response compatibility remains UNKNOWN until handlers, serializers and active frontend consumers are traced. See [cross-project API catalog](../../05-complete-api-catalog.md).
