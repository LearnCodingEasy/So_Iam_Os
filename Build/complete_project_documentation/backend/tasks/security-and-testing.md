# tasks security and testing

## Permission/ownership evidence

- tasks/api/views/tasks_views.py:L11: from rest_framework.permissions import IsAuthenticated
- tasks/api/views/tasks_views.py:L31: permission_classes = [IsAuthenticated]
- tasks/api/views/tasks_views.py:L52: invalidate_dashboard(self.request.user.id)
- tasks/api/views/tasks_views.py:L54: def get_queryset(self):
- tasks/api/views/tasks_views.py:L55: qs = Task.objects.filter(user=self.request.user)
- tasks/api/views/tasks_views.py:L161: task = serializer.save(user=self.request.user)
- tasks/api/views/tasks_views.py:L208: qs = self.get_queryset()
- tasks/api/views/tasks_views.py:L255: request.user.id,
- tasks/api/views/tasks_views.py:L267: request.user.id,
- tasks/api/views/tasks_views.py:L272: request.user
- tasks/api/views/tasks_views.py:L286: request.user.id,
- tasks/api/views/tasks_views.py:L428: qs = self.get_queryset()
- tasks/api/views/tasks_views.py:L488: qs = self.get_queryset().filter(
- tasks/api/views/tasks_views.py:L511: qs = self.get_queryset().filter(
- tasks/api/views/tasks_views.py:L532: # Security requirement: the Celery task must publish its owner ID
- tasks/api/views/tasks_views.py:L543: owner_id = (
- tasks/api/views/tasks_views.py:L549: if str(owner_id) != str(request.user.id):


## Tests
- tasks/tests/test_tasks.py
- tasks/tests/__init__.py


Tests were not run. This scan is not a complete authorization/security review. Shared guidance: [authentication and permissions](../../07-authentication-and-permissions.md).
