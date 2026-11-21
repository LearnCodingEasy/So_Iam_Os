# automation models

Model files and declarations are extracted from source. Field excerpts retain source line numbers; inspect linked source for multiline options and complete semantics.


## action
Source: automation/models/action.py

- L11: class Action(models.Model):

- L20: id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

- L21: slug = models.SlugField(

- L24: created_at = models.DateTimeField(auto_now_add=True)

- L25: updated_at = models.DateTimeField(auto_now=True)

- L33: action_type = models.CharField(max_length=50)

- L35: payload = models.JSONField(default=dict)

## delay
Source: automation/models/delay.py

- L12: class Delay(models.Model):

- L17: id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

- L18: slug = models.SlugField(

- L21: created_at = models.DateTimeField(auto_now_add=True)

- L22: updated_at = models.DateTimeField(auto_now=True)

- L25: name = models.CharField(max_length=200)

- L26: seconds = models.IntegerField()

## program
Source: automation/models/program.py

- L13: class Program(models.Model):

- L18: id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

- L19: slug = models.SlugField(

- L22: created_at = models.DateTimeField(auto_now_add=True)

- L23: updated_at = models.DateTimeField(auto_now=True)

- L27: name = models.CharField(max_length=100)

- L28: description = models.TextField(blank=True)

- L31: executable_path = models.CharField(max_length=500)

- L32: project_path = models.CharField(max_length=500, blank=True, null=True)

- L34: working_directory = models.CharField(max_length=500, blank=True, null=True)

- L36: window_title_pattern = models.CharField(max_length=255, blank=True)

- L38: # global_shortcuts = models.JSONField(default=dict, blank=True)

- L42: # is_running = models.BooleanField(default=False)

- L43: # last_run_at = models.DateTimeField(null=True, blank=True)

- L44: # last_status = models.CharField(

- L56: # icon = models.CharField(max_length=100, blank=True)

- L57: image = models.ImageField(upload_to="programs", blank=True, null=True)

- L58: # is_installed = models.BooleanField(default=True)

- L62: # settings = models.JSONField(default=dict, blank=True)

- L64: # env_variables = models.JSONField(default=dict, blank=True)

## program_element
Source: automation/models/program_element.py

- L12: class ProgramElement(models.Model):

- L36: id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

- L37: slug = models.SlugField(max_length=255, unique=True, blank=True)

- L38: created_at = models.DateTimeField(auto_now_add=True)

- L39: updated_at = models.DateTimeField(auto_now=True)

- L49: name = models.CharField(max_length=255, db_index=True)

- L50: display_text = models.CharField(max_length=500, blank=True)

- L51: element_type = models.CharField(

- L53: description = models.TextField(blank=True)

- L56: automation_id = models.CharField(max_length=500, blank=True, db_index=True)

- L57: class_name = models.CharField(

- L59: selector_type = models.CharField(

- L61: selector_value = models.TextField(blank=True)   # Ù„Ù„Ù€ xpath / image path

- L62: keyboard_shortcut = models.CharField(

- L64: help_text = models.TextField(blank=True)

- L67: x_coordinate = models.IntegerField(null=True, blank=True)

- L68: y_coordinate = models.IntegerField(null=True, blank=True)

- L69: width = models.IntegerField(null=True, blank=True)

- L70: height = models.IntegerField(null=True, blank=True)

- L73: tree_path = models.CharField(max_length=1000, blank=True)

- L74: depth_level = models.IntegerField(default=0)

- L77: is_visible = models.BooleanField(default=True)

- L78: is_enabled = models.BooleanField(default=True)

- L79: is_clickable = models.BooleanField(default=True)

- L80: is_active = models.BooleanField(default=True)

- L83: raw_properties = models.JSONField(default=dict)

- L84: stability_score = models.FloatField(default=1.0)

- L85: image = models.ImageField(

- L87: confidence = models.FloatField(default=0.8)

- L89: class Meta:

- L90: indexes = [

- L91: models.Index(fields=['program', 'automation_id']),

- L92: models.Index(fields=['program', 'name']),

## screen_state
Source: automation/models/screen_state.py

- L13: class ScreenState(models.Model):

- L22: id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

- L23: slug = models.SlugField(

- L26: created_at = models.DateTimeField(auto_now_add=True)

- L27: updated_at = models.DateTimeField(auto_now=True)

- L33: screenshot = models.ImageField(upload_to="screens")

- L35: detected_elements = models.JSONField(default=dict)

- L37: active_program = models.CharField(max_length=100)

- L38: action_id = models.UUIDField()

- L39: screenshot_path = models.TextField(blank=True, null=True)

- L40: status = models.CharField(max_length=20)

- L41: created_at = models.DateTimeField(auto_now_add=True)

## task
Source: automation/models/task.py

- L11: class Task(models.Model):

- L16: id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

- L17: slug = models.SlugField(

- L20: created_at = models.DateTimeField(auto_now_add=True)

- L21: updated_at = models.DateTimeField(auto_now=True)

- L24: name = models.CharField(max_length=200)

- L25: description = models.TextField(blank=True, null=True)

## task_run
Source: automation/models/task_run.py

- L13: class TaskRun(models.Model):

- L27: id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

- L28: slug = models.SlugField(

- L31: created_at = models.DateTimeField(auto_now_add=True)

- L32: updated_at = models.DateTimeField(auto_now=True)

- L37: status = models.CharField(max_length=20, choices=STATUS)

- L39: started_at = models.DateTimeField(auto_now_add=True)

- L40: finished_at = models.DateTimeField(null=True, blank=True)

- L42: logs = models.TextField(blank=True)

## workflow
Source: automation/models/workflow.py

- L12: class Workflow(models.Model):

- L27: id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

- L28: slug = models.SlugField(

- L31: created_at = models.DateTimeField(auto_now_add=True)

- L32: updated_at = models.DateTimeField(auto_now=True)

- L35: name = models.CharField(max_length=150)

- L36: description = models.TextField(blank=True)

- L38: status = models.CharField(max_length=20, choices=STATUS, default="draft")

- L39: permissions = models.JSONField(default=dict, blank=True)

## workflow_edge
Source: automation/models/workflow_edge.py

- L12: class WorkflowEdge(models.Model):

- L20: id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

- L21: slug = models.SlugField(

- L24: created_at = models.DateTimeField(auto_now_add=True)

- L25: updated_at = models.DateTimeField(auto_now=True)

- L47: condition = models.CharField(

- L49: edge_type = models.CharField(max_length=50, default="default")

## workflow_node
Source: automation/models/workflow_node.py

- L13: class WorkflowNode(models.Model):

- L21: id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

- L22: slug = models.SlugField(

- L25: created_at = models.DateTimeField(auto_now_add=True)

- L26: updated_at = models.DateTimeField(auto_now=True)

- L36: node_type = models.CharField(max_length=50)

- L38: label = models.CharField(max_length=100)

- L47: position_x = models.FloatField()

- L48: position_y = models.FloatField()

- L51: config = models.JSONField(default=dict, blank=True)

## __init__
Source: automation/models/__init__.py


Cross-app references and ownership must be confirmed from fields and write paths. See [project data catalog](../../06-database-and-model-catalog.md).
