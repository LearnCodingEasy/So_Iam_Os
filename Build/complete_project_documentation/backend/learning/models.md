# learning models

Model files and declarations are extracted from source. Field excerpts retain source line numbers; inspect linked source for multiline options and complete semantics.


## application_review
Source: learning/models/application_review.py

- L9: class ApplicationReview(models.Model):

- L10: class Mastery(models.TextChoices):

- L30: score = models.FloatField(validators=SCORE_VALIDATORS)

- L31: mastery_level = models.CharField(

- L37: understood = models.JSONField(default=list, blank=True)

- L38: applied = models.JSONField(default=list, blank=True)

- L39: strengths = models.JSONField(default=list, blank=True)

- L40: weaknesses = models.JSONField(default=list, blank=True)

- L41: errors = models.JSONField(default=list, blank=True)

- L42: needs_review = models.JSONField(default=list, blank=True)

- L43: knowledge_gaps = models.JSONField(default=list, blank=True)

- L44: recommendations = models.JSONField(default=list, blank=True)

- L46: feedback = models.TextField(blank=True)

- L47: ai_metadata = models.JSONField(default=dict, blank=True)

- L48: reviewed_by = models.CharField(max_length=100, default="ai")

- L49: reviewed_at = models.DateTimeField(default=timezone.now)

- L51: created_at = models.DateTimeField(auto_now_add=True)

- L52: updated_at = models.DateTimeField(auto_now=True)

- L54: class Meta:

- L56: indexes = [

- L57: models.Index(fields=["application", "reviewed_at"]),

## application_submission
Source: learning/models/application_submission.py

- L6: class ApplicationSubmission(models.Model):

- L14: version = models.PositiveIntegerField()

- L15: title = models.CharField(max_length=255)

- L16: content = models.TextField()

- L17: submitted_at = models.DateTimeField(default=timezone.now)

- L19: class Meta:

- L21: constraints = [

- L22: models.UniqueConstraint(

## assessment
Source: learning/models/assessment.py

- L7: class Assessment(models.Model):

- L8: class Type(models.TextChoices):

- L19: title = models.CharField(max_length=255)

- L20: description = models.TextField(blank=True)

- L21: instructions = models.TextField(blank=True)

- L23: assessment_type = models.CharField(

- L28: passing_score = models.PositiveSmallIntegerField(

- L32: estimated_minutes = models.PositiveIntegerField(

- L36: order = models.PositiveIntegerField(default=0)

- L37: is_active = models.BooleanField(default=True)

- L39: created_at = models.DateTimeField(auto_now_add=True)

- L40: updated_at = models.DateTimeField(auto_now=True)

- L42: class Meta:

- L44: indexes = [

- L45: models.Index(fields=["topic", "assessment_type", "is_active"]),

- L47: constraints = [

## assessment_attempt
Source: learning/models/assessment_attempt.py

- L9: class AssessmentAttempt(models.Model):

- L21: score = models.PositiveSmallIntegerField(

- L26: passed = models.BooleanField(default=False)

- L27: feedback = models.TextField(blank=True)

- L29: started_at = models.DateTimeField(default=timezone.now)

- L30: completed_at = models.DateTimeField(null=True, blank=True)

- L31: attempt_number = models.PositiveIntegerField(default=1)

- L33: class Meta:

- L35: constraints = [

- L36: models.UniqueConstraint(

- L41: indexes = [

- L42: models.Index(fields=["user", "assessment", "started_at"]),

## assessment_choice
Source: learning/models/assessment_choice.py

- L5: class AssessmentChoice(models.Model):

- L11: text = models.TextField()

- L12: order = models.PositiveIntegerField(default=0)

- L15: is_correct = models.BooleanField(default=False)

- L17: feedback = models.TextField(blank=True)

- L19: class Meta:

## assessment_question
Source: learning/models/assessment_question.py

- L5: class AssessmentQuestion(models.Model):

- L6: class Type(models.TextChoices):

- L18: question_type = models.CharField(

- L22: prompt = models.TextField()

- L23: explanation = models.TextField(blank=True)

- L24: points = models.PositiveIntegerField(default=1)

- L25: order = models.PositiveIntegerField(default=0)

- L26: is_required = models.BooleanField(default=True)

- L29: grading_data = models.JSONField(default=dict, blank=True)

- L31: class Meta:

- L33: indexes = [

- L34: models.Index(fields=["assessment", "order"]),

## assessment_response
Source: learning/models/assessment_response.py

- L8: class AssessmentResponse(models.Model):

- L19: selected_choices = models.ManyToManyField(

- L24: text_answer = models.TextField(blank=True)

- L25: is_correct = models.BooleanField(null=True, blank=True)

- L26: points_awarded = models.FloatField(default=0)

- L27: feedback = models.TextField(blank=True)

- L29: class Meta:

- L30: constraints = [

- L31: models.UniqueConstraint(

## common
Source: learning/models/common.py

## knowledge_application
Source: learning/models/knowledge_application.py

- L8: class KnowledgeApplication(models.Model):

- L9: class Status(models.TextChoices):

- L14: class ApplicationType(models.TextChoices):

- L47: title = models.CharField(max_length=255)

- L48: content = models.TextField()

- L49: application_type = models.CharField(

- L54: status = models.CharField(

- L60: submitted_at = models.DateTimeField(null=True, blank=True)

- L61: reviewed_at = models.DateTimeField(null=True, blank=True)

- L63: created_at = models.DateTimeField(auto_now_add=True)

- L64: updated_at = models.DateTimeField(auto_now=True)

- L66: class Meta:

- L68: indexes = [

- L69: models.Index(fields=["user", "topic", "status"]),

## learning_goal
Source: learning/models/learning_goal.py

- L6: class LearningGoal(models.Model):

- L7: class Status(models.TextChoices):

- L26: title = models.CharField(max_length=255)

- L27: description = models.TextField(blank=True)

- L28: reason = models.TextField(blank=True)

- L30: current_level = models.CharField(

- L35: target_level = models.CharField(

- L41: status = models.CharField(

- L46: target_date = models.DateField(null=True, blank=True)

- L47: completed_at = models.DateTimeField(null=True, blank=True)

- L49: created_at = models.DateTimeField(auto_now_add=True)

- L50: updated_at = models.DateTimeField(auto_now=True)

- L52: class Meta:

- L54: indexes = [

- L55: models.Index(fields=["user", "status"]),

- L56: models.Index(fields=["user", "target_date"]),

## learning_note
Source: learning/models/learning_note.py

- L8: class LearningNote(models.Model):

- L9: class NoteType(models.TextChoices):

- L44: note_type = models.CharField(

- L49: title = models.CharField(max_length=255, blank=True)

- L50: content = models.TextField()

- L52: created_at = models.DateTimeField(auto_now_add=True)

- L53: updated_at = models.DateTimeField(auto_now=True)

- L55: class Meta:

- L57: indexes = [

- L58: models.Index(fields=["user", "topic"]),

- L59: models.Index(fields=["user", "note_type"]),

## learning_path
Source: learning/models/learning_path.py

- L7: class LearningPath(models.Model):

- L8: class Status(models.TextChoices):

- L25: title = models.CharField(max_length=255)

- L26: description = models.TextField(blank=True)

- L27: status = models.CharField(

- L33: started_at = models.DateTimeField(null=True, blank=True)

- L34: completed_at = models.DateTimeField(null=True, blank=True)

- L36: created_at = models.DateTimeField(auto_now_add=True)

- L37: updated_at = models.DateTimeField(auto_now=True)

- L39: class Meta:

- L41: indexes = [

- L42: models.Index(fields=["user", "status"]),

- L43: models.Index(fields=["goal", "status"]),

## learning_progress
Source: learning/models/learning_progress.py

- L15: class LearningProgress(models.Model):

- L16: class Mastery(models.TextChoices):

- L35: progress_percent = models.PositiveSmallIntegerField(

- L39: practice_completed = models.BooleanField(default=False)

- L42: notes = models.TextField(blank=True)

- L44: mastery_level = models.CharField(

- L49: last_ai_score = models.FloatField(

- L54: needs_review = models.BooleanField(default=False)

- L56: lesson_completed = models.BooleanField(default=False)

- L57: quick_check_completed = models.BooleanField(default=False)

- L58: assessment_completed = models.BooleanField(default=False)

- L60: last_activity_at = models.DateTimeField(null=True, blank=True)

- L61: completed_at = models.DateTimeField(null=True, blank=True)

- L63: created_at = models.DateTimeField(auto_now_add=True)

- L64: updated_at = models.DateTimeField(auto_now=True)

- L66: class Meta:

- L68: constraints = [

- L69: models.UniqueConstraint(

- L79: indexes = [

- L80: models.Index(fields=["user", "needs_review"]),

- L81: models.Index(fields=["user", "last_activity_at"]),

## learning_resource
Source: learning/models/learning_resource.py

- L7: class LearningResource(models.Model):

- L8: class ResourceType(models.TextChoices):

- L33: title = models.CharField(max_length=255)

- L34: description = models.TextField(blank=True)

- L35: reference_type = models.CharField(

- L41: url = models.URLField(blank=True)

- L42: file = models.FileField(

- L47: content = models.TextField(blank=True)

- L48: caption = models.CharField(max_length=255, blank=True)

- L50: order = models.PositiveIntegerField(default=0)

- L51: created_at = models.DateTimeField(auto_now_add=True)

- L53: class Meta:

- L55: indexes = [

- L56: models.Index(fields=["topic", "order"]),

## learning_revision
Source: learning/models/learning_revision.py

- L8: class LearningRevision(models.Model):

- L9: class Status(models.TextChoices):

- L33: concepts = models.JSONField(default=list, blank=True)

- L34: recommendation = models.TextField(blank=True)

- L35: status = models.CharField(

- L40: scheduled_for = models.DateTimeField(null=True, blank=True)

- L41: started_at = models.DateTimeField(null=True, blank=True)

- L42: completed_at = models.DateTimeField(null=True, blank=True)

- L43: outcome = models.TextField(blank=True)

- L45: created_at = models.DateTimeField(auto_now_add=True)

- L46: updated_at = models.DateTimeField(auto_now=True)

- L48: class Meta:

- L50: indexes = [

- L51: models.Index(fields=["user", "status", "scheduled_for"]),

## learning_session
Source: learning/models/learning_session.py

- L10: class LearningSession(models.Model):

- L11: class ActivityType(models.TextChoices):

- L37: activity_type = models.CharField(

- L42: started_at = models.DateTimeField(default=timezone.now)

- L43: ended_at = models.DateTimeField(null=True, blank=True)

- L44: duration_seconds = models.PositiveIntegerField(

- L48: completed = models.BooleanField(default=False)

- L49: metadata = models.JSONField(default=dict, blank=True)

- L51: class Meta:

- L53: indexes = [

- L54: models.Index(fields=["user", "started_at"]),

- L55: models.Index(fields=["topic", "started_at"]),

## learning_topic
Source: learning/models/learning_topic.py

- L8: class LearningTopic(models.Model):

- L9: class Status(models.TextChoices):

- L15: class Difficulty(models.TextChoices):

- L33: title = models.CharField(max_length=255)

- L34: description = models.TextField(blank=True)

- L35: order = models.PositiveIntegerField(default=0)

- L36: status = models.CharField(

- L41: difficulty = models.CharField(

- L46: estimated_minutes = models.PositiveIntegerField(

- L51: prerequisites = models.ManyToManyField(

- L66: created_at = models.DateTimeField(auto_now_add=True)

- L67: updated_at = models.DateTimeField(auto_now=True)

- L69: class Meta:

- L71: indexes = [

- L72: models.Index(fields=["path", "order"]),

- L73: models.Index(fields=["path", "status"]),

- L75: constraints = [

- L76: models.UniqueConstraint(

## lesson
Source: learning/models/lesson.py

- L7: class Lesson(models.Model):

- L8: class ContentFormat(models.TextChoices):

- L18: title = models.CharField(max_length=255)

- L19: description = models.TextField(blank=True)

- L20: content = models.TextField(blank=True)

- L21: content_format = models.CharField(

- L27: order = models.PositiveIntegerField(default=0)

- L28: estimated_minutes = models.PositiveIntegerField(

- L33: learning_objectives = models.JSONField(default=list, blank=True)

- L34: key_concepts = models.JSONField(default=list, blank=True)

- L35: examples = models.JSONField(default=list, blank=True)

- L36: practical_instructions = models.JSONField(default=list, blank=True)

- L38: is_active = models.BooleanField(default=True)

- L40: created_at = models.DateTimeField(auto_now_add=True)

- L41: updated_at = models.DateTimeField(auto_now=True)

- L43: class Meta:

- L45: indexes = [

- L46: models.Index(fields=["topic", "order"]),

## skill
Source: learning/models/skill.py

- L4: class Skill(models.Model):

- L5: class Level(models.TextChoices):

- L11: name = models.CharField(max_length=150)

- L12: slug = models.SlugField(max_length=180, unique=True)

- L13: description = models.TextField(blank=True)

- L14: category = models.CharField(max_length=100, blank=True)

- L15: is_active = models.BooleanField(default=True)

- L17: created_at = models.DateTimeField(auto_now_add=True)

- L18: updated_at = models.DateTimeField(auto_now=True)

- L20: class Meta:

- L22: indexes = [

- L23: models.Index(fields=["category", "is_active"]),

## __init__
Source: learning/models/__init__.py


Cross-app references and ownership must be confirmed from fields and write paths. See [project data catalog](../../06-database-and-model-catalog.md).
