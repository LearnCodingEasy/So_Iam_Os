# learning services and workflows

## Service/task/signal source


### learning/services/ai_content.py
L22: class LearningTopicAIContentService:
L28: def __init__(
L44: def generate(self, topic):
L107: def _ensure_owner(self, topic):
L117: def _system_prompt(self):
L133: def _build_context(self, topic):
L239: def _save_source_lesson(self, *, topic, knowledge):
L258: def _save_lesson(self, *, topic, payload):
L321: def _save_assessment(self, *, topic, payload):
L426: def _parse_json(content):
L451: def _validate_payload(payload):
L485: def _truncate(value, limit):

### learning/services/ai_service.py
L7: class LearningAIService:
L25: def analyze_application(
L185: def calculate_mastery(score):

### learning/services/assessment.py
L4: class AssessmentService:
L7: def submit_attempt(

### learning/services/completion.py
L5: class LearningCompletionService:
L8: def complete_topic(cls, *, user, topic):
L42: def progress_summary(user):
L51: def _goal_progress(goal):

### learning/services/learning.py
L10: class LearningService:
L14: def create_path(
L35: def create_topic(
L62: def get_user_learning_overview(user):

### learning/services/progress.py
L7: class ProgressService:
L13: def update_progress(*, user, topic, progress_percent, practice_completed=None,

### learning/services/services.py
L23: class ApplicationService:
L42: def submit_application(
L111: class ApplicationReviewService:
L121: def save_review(
L236: def update_learning_progress(
L318: def create_revision_if_needed(
L385: def calculate_mastery(score):
L411: class AssessmentService:
L418: def submit_attempt(
L513: class LearningService:
L524: def create_goal(
L544: def create_path(
L569: def create_topic(
L619: def get_user_learning_overview(user):
L695: class ProgressService:
L702: def update_progress(

### learning/services/__init__.py
No class/function declaration matched the static inventory pattern.


The index does not prove callers, scheduling, successful external calls, or runtime completion. See [background jobs and integrations](../../08-background-jobs-and-integrations.md).
