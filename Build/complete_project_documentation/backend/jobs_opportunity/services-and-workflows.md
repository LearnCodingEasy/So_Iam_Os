# jobs_opportunity services and workflows

## Service/task/signal source


### jobs_opportunity/signals.py
L8: def provision_default_job_sources(sender, instance, created, **kwargs):

### jobs_opportunity/tasks.py
L19: def _safe_url(url):
L40: def _json_path(data, path):
L57: def _skill_names(item):
L65: def _canonical_key(item):
L76: def _safe_published_at(value):
L92: def _safe_decimal(value):
L102: def _safe_job_url(value):
L121: def _upsert_job(source, item):
L190: def _rss_items(content):
L212: def child_text(node, *names):
L251: def sync_job_source(self, source_id, sync_run_id=None):
L345: def refresh_all_job_sources():
L354: def refresh_all_job_matches():
L365: def expire_old_jobs():

### jobs_opportunity/services/jobs_opportunity_services.py
L19: class JobMatchingService:
L23: def _user_skill_levels(cls, user):
L39: def calculate(cls, user, job):
L112: def refresh_for_user(cls, user):
L117: class JobGapService:
L119: def sync_from_match(user, match):
L132: def create_learning_goal(user, gap):
L142: class JobParserService:
L147: def analyze(cls, job, user=None, use_ai=False):
L222: def _clean_strings(value, limit=12, width=600):
L260: class ReadinessService:
L262: def calculate(user, job, match=None):
L275: class JobRecommendationService:
L277: def refresh(user, limit=50):
L288: class JobAnalyticsService:
L290: def dashboard(user, *, persist_snapshot=False):
L310: def _persist_snapshot(user, snapshot, *, attempts=3):
L337: class JobService:
L340: def save_source(user, **data):
L345: def create_job(user, **data):
L355: def apply(user, job, **data):

### jobs_opportunity/services/__init__.py
No class/function declaration matched the static inventory pattern.


The index does not prove callers, scheduling, successful external calls, or runtime completion. See [background jobs and integrations](../../08-background-jobs-and-integrations.md).
