# learning architecture

## Module structure
- Models: 20 Python files under models/.
- API: 44 Python files under api/.
- Services: 8 Python files under services/.
- Tests: 3; migrations: 2 (not run).

## Processing pattern
Where present, URL declarations bind handlers in api/views; handlers use serializers and models, with services/tasks for selected operations. Exact app-specific classes and references are listed in api.md and services-and-workflows.md. This is not assumed to be uniform.

## Source directory inventory

### api
api/urls.py
api/__init__.py
api/serializers/application_review_serializers.py
api/serializers/application_submission_serializers.py
api/serializers/assessment_attempt_serializers.py
api/serializers/assessment_choice_serializers.py
api/serializers/assessment_question_serializers.py
api/serializers/assessment_response_serializers.py
api/serializers/assessment_serializers.py
api/serializers/common.py
api/serializers/knowledge_application_serializers.py
api/serializers/learning_dashboard_serializers.py
api/serializers/learning_goal_serializers.py
api/serializers/learning_note_serializers.py
api/serializers/learning_path_serializers.py
api/serializers/learning_progress_serializers.py
api/serializers/learning_resource_serializers.py
api/serializers/learning_revision_serializers.py
api/serializers/learning_session_serializers.py
api/serializers/lesson_serializers.py
api/serializers/skill_serializers.py
api/serializers/__init__.py
api/views/application_review_views.py
api/views/application_submission_views.py
api/views/assessment_attempt_views.py
api/views/assessment_choice_views.py
api/views/assessment_question_views.py
api/views/assessment_response_views.py
api/views/assessment_views.py
api/views/knowledge_application_views.py
api/views/learning_goal_views.py
api/views/learning_note_views.py
api/views/learning_path_views.py
api/views/learning_progress_views.py
api/views/learning_resource_views.py
api/views/learning_revision_views.py
api/views/learning_session_views.py
api/views/learning_topic_views.py
api/views/lesson_views.py
api/views/skill_views.py
api/views/user_owned_model_views.py
api/views/user_owned_queryset_mixin_views.py
api/views/user_owned_read_only_views.py
api/views/__init__.py

### models
models/application_review.py
models/application_submission.py
models/assessment.py
models/assessment_attempt.py
models/assessment_choice.py
models/assessment_question.py
models/assessment_response.py
models/common.py
models/knowledge_application.py
models/learning_goal.py
models/learning_note.py
models/learning_path.py
models/learning_progress.py
models/learning_resource.py
models/learning_revision.py
models/learning_session.py
models/learning_topic.py
models/lesson.py
models/skill.py
models/__init__.py

### services
services/ai_content.py
services/ai_service.py
services/assessment.py
services/completion.py
services/learning.py
services/progress.py
services/services.py
services/__init__.py

### tests
tests/tests_completion_additions.py
tests/test_learning.py
tests/__init__.py

### migrations
migrations/0001_initial.py
migrations/__init__.py


Shared architecture links: [backend catalog](../../02-system-component-catalog.md), [data relationships](../../06-database-and-model-catalog.md), [security and permissions](../../07-authentication-and-permissions.md).
