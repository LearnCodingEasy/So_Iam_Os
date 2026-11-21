# projects security and testing

## Permission/ownership evidence

- projects/api/views/projects_views.py:L3: from rest_framework.permissions import IsAuthenticated
- projects/api/views/projects_views.py:L10: permission_classes=[IsAuthenticated]; serializer_class=ProjectSerializer
- projects/api/views/projects_views.py:L11: def get_queryset(self): return Project.objects.filter(user=self.request.user).prefetch_related('members')
- projects/api/views/projects_views.py:L12: def perform_create(self,s): s.save(user=self.request.user)
- projects/api/views/projects_views.py:L21: permission_classes=[IsAuthenticated]; serializer_class=ProjectMemberSerializer
- projects/api/views/projects_views.py:L22: def get_queryset(self): return ProjectMember.objects.filter(project__user=self.request.user)
- projects/api/views/projects_views.py:L26: permission_classes=[IsAuthenticated]; serializer_class=ProjectContextSerializer
- projects/api/views/projects_views.py:L27: def get_queryset(self): return ProjectContext.objects.filter(project__user=self.request.user)


## Tests
- projects/tests/test_projects.py
- projects/tests/__init__.py


Tests were not run. This scan is not a complete authorization/security review. Shared guidance: [authentication and permissions](../../07-authentication-and-permissions.md).
