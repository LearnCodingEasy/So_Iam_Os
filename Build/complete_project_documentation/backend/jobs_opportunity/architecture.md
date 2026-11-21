# jobs_opportunity architecture

## Module structure
- Models: 20 Python files under models/.
- API: 38 Python files under api/.
- Services: 2 Python files under services/.
- Tests: 3; migrations: 6 (not run).

## Processing pattern
Where present, URL declarations bind handlers in api/views; handlers use serializers and models, with services/tasks for selected operations. Exact app-specific classes and references are listed in api.md and services-and-workflows.md. This is not assumed to be uniform.

## Source directory inventory

### api
api/urls.py
api/__init__.py
api/serializers/company_profile_serializers.py
api/serializers/job_alert_serializers.py
api/serializers/job_analytics_snapshot_serializers.py
api/serializers/job_application_event_serializers.py
api/serializers/job_application_serializers.py
api/serializers/job_cover_letter_serializers.py
api/serializers/job_interview_serializers.py
api/serializers/job_match_serializers.py
api/serializers/job_opportunity_serializers.py
api/serializers/job_preference_serializers.py
api/serializers/job_readiness_serializers.py
api/serializers/job_recommendation_serializers.py
api/serializers/job_resume_serializers.py
api/serializers/job_saved_search_serializers.py
api/serializers/job_skill_gap_serializers.py
api/serializers/job_skill_requirement_serializers.py
api/serializers/job_source_serializers.py
api/serializers/__init__.py
api/views/company_profile_views.py
api/views/jobs_workspace_views.py
api/views/job_alert_views.py
api/views/job_analytics_snapshot_views.py
api/views/job_application_views.py
api/views/job_cover_letter_views.py
api/views/job_interview_views.py
api/views/job_match_views.py
api/views/job_opportunity_views.py
api/views/job_preference_views.py
api/views/job_readiness_views.py
api/views/job_recommendation_views.py
api/views/job_resume_views.py
api/views/job_saved_search_views.py
api/views/job_skill_gap_views.py
api/views/job_source_views.py
api/views/user_owned_views.py
api/views/__init__.py

### models
models/common.py
models/company_profile.py
models/job_alert.py
models/job_analytics_snapshot.py
models/job_application.py
models/job_application_event.py
models/job_cover_letter.py
models/job_interview.py
models/job_match.py
models/job_opportunity.py
models/job_preference.py
models/job_readiness.py
models/job_recommendation.py
models/job_resume.py
models/job_saved_search.py
models/job_skill_gap.py
models/job_skill_requirement.py
models/job_source.py
models/job_source_sync_run.py
models/__init__.py

### services
services/jobs_opportunity_services.py
services/__init__.py

### management
management/__init__.py
management/commands/bootstrap_job_sources.py
management/commands/scrape_jobs.py
management/commands/__init__.py

### tests
tests/test_jobs_opportunity.py
tests/test_rss_parser.py
tests/__init__.py

### migrations
migrations/0001_initial.py
migrations/0002_normalize_source_types.py
migrations/0003_expand_job_url_length.py
migrations/0004_job_source_sync_run.py
migrations/0005_rename_jobs_sync_user_created_idx_jobs_opport_user_id_9739b7_idx_and_more.py
migrations/__init__.py


Shared architecture links: [backend catalog](../../02-system-component-catalog.md), [data relationships](../../06-database-and-model-catalog.md), [security and permissions](../../07-authentication-and-permissions.md).
