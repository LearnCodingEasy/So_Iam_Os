# projects API

Project prefix: /api/projects/ (source: backend_django/backend_django/urls.py). Route rows below are declarations; DRF router methods are implicit and not runtime-verified.


## Routes: projects/api/urls.py

- L3: router=DefaultRouter(); router.register('projects',ProjectViewSet,basename='project'); router.register('members',ProjectMemberViewSet,basename='project-member'); router.register('contexts',ProjectContextViewSet,basename='project-context')

## Handler declarations: projects/api/views/projects_views.py
L9: class ProjectViewSet(viewsets.ModelViewSet):
L10: permission_classes=[IsAuthenticated]; serializer_class=ProjectSerializer
L11: def get_queryset(self): return Project.objects.filter(user=self.request.user).prefetch_related('members')
L12: def perform_create(self,s): s.save(user=self.request.user)
L13: @action(detail=True,methods=['get','put','patch'])
L20: class ProjectMemberViewSet(viewsets.ModelViewSet):
L21: permission_classes=[IsAuthenticated]; serializer_class=ProjectMemberSerializer
L22: def get_queryset(self): return ProjectMember.objects.filter(project__user=self.request.user)
L25: class ProjectContextViewSet(viewsets.ReadOnlyModelViewSet):
L26: permission_classes=[IsAuthenticated]; serializer_class=ProjectContextSerializer
L27: def get_queryset(self): return ProjectContext.objects.filter(project__user=self.request.user)


Full payload/response compatibility remains UNKNOWN until handlers, serializers and active frontend consumers are traced. See [cross-project API catalog](../../05-complete-api-catalog.md).
