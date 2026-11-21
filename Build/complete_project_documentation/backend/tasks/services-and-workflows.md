# tasks services and workflows

## Service/task/signal source


### tasks/admin.py
L7: class TaskAdmin(admin.ModelAdmin):

### tasks/apps.py
L4: class TasksConfig(AppConfig):

### tasks/tasks.py
L6: def generate_daily_learning_tasks(self, user_id, count=None, provider=None, model=None):
L12: def generate_daily_learning_tasks_for_all_users():

### tasks/__init__.py
No class/function declaration matched the static inventory pattern.

### tasks/api/urls.py
No class/function declaration matched the static inventory pattern.

### tasks/api/__init__.py
No class/function declaration matched the static inventory pattern.

### tasks/api/serializers/tasks_serializers.py
L6: class TaskSerializer(serializers.ModelSerializer):
L17: class Meta:
L57: def get_overdue(self, obj):
L81: def validate_actual_minutes(self, value):
L88: def validate_estimated_minutes(self, value):
L95: def validate_sort_order(self, value):
L102: def validate(self, attrs):
L113: def final_value(field):

### tasks/api/serializers/__init__.py
No class/function declaration matched the static inventory pattern.

### tasks/api/views/tasks_views.py
L23: class TaskPagination(PageNumberPagination):
L29: class TaskViewSet(viewsets.ModelViewSet):
L44: def has_field(self, name):
L51: def invalidate_cache(self):
L54: def get_queryset(self):
L142: def completed_status_values(self):
L155: def _recalculate_goal(self, task):
L160: def perform_create(self, serializer):
L165: def perform_update(self, serializer):
L179: def perform_destroy(self, instance):
L192: def list(self, request, *args, **kwargs):
L207: def today(self, request):
L224: def generate(self, request):
L300: def complete(self, request, pk=None):
L331: def postpone(self, request, pk=None):
L362: def start(self, request, pk=None):
L366: def cancel(self, request, pk=None):
L370: def reopen(self, request, pk=None):
L373: def change_status(self, request, target):
L427: def stats(self, request):
L457: def progress(self, request):
L461: def calendar(self, request):
L504: def overdue(self, request):
L531: def generation_status(self, request, task_id=None):

### tasks/api/views/__init__.py
No class/function declaration matched the static inventory pattern.

### tasks/migrations/0001_initial.py
L9: class Migration(migrations.Migration):

### tasks/migrations/0002_task_milestone.py
L5: class Migration(migrations.Migration):

### tasks/migrations/__init__.py
No class/function declaration matched the static inventory pattern.

### tasks/models/task.py
L6: class Task(models.Model):
L7: class Status(models.TextChoices):
L14: class Priority(models.TextChoices):
L54: class Meta:
L64: def __str__(self):
L67: def mark_completed(self):

### tasks/models/__init__.py
No class/function declaration matched the static inventory pattern.

### tasks/services/daily_generation.py
L9: class DailyTaskGenerationService:
L10: def __init__(self, user):
L13: def context(self):
L24: def generate(self, count=None, provider=None, model=None):
L54: def _ai_tasks(self, goal, topics, existing, recent, count, provider, model):
L83: def _fallback_tasks(self, goal, topics, count):
L94: def _norm(value):

### tasks/services/tasks_services.py
L12: class TaskService:
L15: def complete(task, actual_minutes=None):
L51: def postpone(task, until):

### tasks/services/__init__.py
No class/function declaration matched the static inventory pattern.

### tasks/tests/test_tasks.py
L14: class TaskIntegrationTests(TestCase):
L15: def setUp(self):
L19: def test_completing_tasks_recalculates_goal_progress_from_real_tasks(self):
L36: def test_task_serializer_rejects_learning_topic_owned_by_another_user(self):

### tasks/tests/__init__.py
No class/function declaration matched the static inventory pattern.


The index does not prove callers, scheduling, successful external calls, or runtime completion. See [background jobs and integrations](../../08-background-jobs-and-integrations.md).
