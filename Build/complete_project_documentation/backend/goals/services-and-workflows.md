# goals services and workflows

## Service/task/signal source


### goals/services/coach.py
L7: class GoalCoachService:
L11: def propose_plan(goal, user, instructions=""):
L98: def answer(goal, user, message):

### goals/services/goals_services.py
L11: class GoalService:
L24: def record(goal, user, event_type, description="", data=None):
L29: def notify(user, title, message, obj, action_url="/goals"):
L41: def set_status(cls, goal, status, user, notes=""):
L65: def complete(cls, goal, user, notes=""):
L70: def update_progress(cls, goal, progress, user, source="user"):
L96: def recalculate_goal(cls, goal):
L105: def recalculate_from_tasks(cls, goal):
L118: def recalculate_milestone(cls, milestone):
L135: def recalculate_for_task(cls, task):
L144: def recalculate_from_milestones(cls, goal):
L160: def _save_derived_progress(goal, progress, source):
L182: def approve_plan(cls, proposal, user):
L230: class GoalAnalyticsService:
L232: def dashboard(user):
L270: class GoalRiskService:
L272: def analyze(goal):

### goals/services/__init__.py
No class/function declaration matched the static inventory pattern.


The index does not prove callers, scheduling, successful external calls, or runtime completion. See [background jobs and integrations](../../08-background-jobs-and-integrations.md).
