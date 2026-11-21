# learning API

Project prefix: /api/learning/ (source: backend_django/backend_django/urls.py). Route rows below are declarations; DRF router methods are implicit and not runtime-verified.


## Routes: learning/api/urls.py

- L13: router.register(

- L24: router.register(

- L35: router.register(

- L46: router.register(

- L57: router.register(

- L68: router.register(

- L79: router.register(

- L90: router.register(

- L101: router.register(

- L112: router.register(

- L123: router.register(

- L134: router.register(

- L145: router.register(

- L156: router.register(

- L167: router.register(

- L178: router.register(

- L189: router.register(

- L200: router.register(

## Handler declarations: learning/api/views/application_review_views.py
L11: class ApplicationReviewViewSet(
L14: permission_classes = [IsAuthenticated]
L16: def get_queryset(self):

## Handler declarations: learning/api/views/application_submission_views.py
L14: class ApplicationSubmissionViewSet(
L17: permission_classes = [IsAuthenticated]
L19: def get_queryset(self):
L33: def perform_create(self, serializer):

## Handler declarations: learning/api/views/assessment_attempt_views.py
L12: class AssessmentAttemptViewSet(
L15: serializer_class = AssessmentAttemptSerializer
L16: permission_classes = [IsAuthenticated]
L18: def get_queryset(self):

## Handler declarations: learning/api/views/assessment_choice_views.py
L12: class AssessmentChoiceViewSet(
L15: permission_classes = [IsAuthenticated]
L17: def get_queryset(self):
L31: def perform_create(self, serializer):

## Handler declarations: learning/api/views/assessment_question_views.py
L12: class AssessmentQuestionViewSet(
L15: permission_classes = [IsAuthenticated]
L17: def get_queryset(self):
L33: def perform_create(self, serializer):

## Handler declarations: learning/api/views/assessment_response_views.py
L12: class AssessmentResponseViewSet(
L15: permission_classes = [IsAuthenticated]
L17: def get_queryset(self):
L32: def perform_create(self, serializer):

## Handler declarations: learning/api/views/assessment_views.py
L17: class AssessmentViewSet(
L20: permission_classes = [IsAuthenticated]
L22: def get_queryset(self):
L48: def perform_create(self, serializer):
L58: @action(
L77: @action(
L101: @action(
L131: @action(

## Handler declarations: learning/api/views/knowledge_application_views.py
L18: class KnowledgeApplicationViewSet(
L21: serializer_class = KnowledgeApplicationSerializer
L22: permission_classes = [IsAuthenticated]
L24: def get_queryset(self):
L42: def perform_create(self, serializer):
L84: @action(
L108: @action(
L154: @action(
L169: @action(
L191: @action(

## Handler declarations: learning/api/views/learning_goal_views.py
L16: class LearningGoalViewSet(
L19: permission_classes = [IsAuthenticated]
L21: def get_queryset(self):
L50: def perform_create(self, serializer):
L55: @action(
L140: @action(
L174: @action(
L199: @action(
L220: @action(
L241: @action(
L267: @action(

## Handler declarations: learning/api/views/learning_note_views.py
L13: class LearningNoteViewSet(
L16: permission_classes = [IsAuthenticated]
L17: serializer_class = LearningNoteSerializer
L19: def get_queryset(self):
L32: def perform_create(self, serializer):

## Handler declarations: learning/api/views/learning_path_views.py
L17: class LearningPathViewSet(
L20: permission_classes = [IsAuthenticated]
L22: def get_queryset(self):
L43: def perform_create(self, serializer):
L55: @action(
L80: @action(
L103: @action(
L124: @action(
L153: @action(

## Handler declarations: learning/api/views/learning_progress_views.py
L17: class LearningProgressViewSet(
L20: serializer_class = LearningProgressSerializer
L21: permission_classes = [IsAuthenticated]
L23: def get_queryset(self):
L35: def perform_create(self, serializer):
L47: def perform_update(self, serializer):
L57: @action(
L157: @action(detail=False, methods=["get"], url_path="summary")

## Handler declarations: learning/api/views/learning_resource_views.py
L12: class LearningResourceViewSet(
L15: permission_classes = [IsAuthenticated]
L17: def get_queryset(self):
L29: def perform_create(self, serializer):

## Handler declarations: learning/api/views/learning_revision_views.py
L16: class LearningRevisionViewSet(
L19: serializer_class = LearningRevisionSerializer
L20: permission_classes = [IsAuthenticated]
L22: def get_queryset(self):
L36: def perform_create(self, serializer):
L65: @action(
L92: @action(
L133: @action(
L149: @action(

## Handler declarations: learning/api/views/learning_session_views.py
L15: class LearningSessionViewSet(
L18: permission_classes = [IsAuthenticated]
L20: def get_queryset(self):
L32: def perform_create(self, serializer):
L44: @action(

## Handler declarations: learning/api/views/learning_topic_views.py
L17: class LearningTopicViewSet(
L20: permission_classes = [IsAuthenticated]
L22: def get_queryset(self):
L44: def get_queryset_for_detail(self):
L135: def perform_create(self, serializer):
L165: @action(
L199: @action(
L218: @action(
L239: @action(
L254: @action(

## Handler declarations: learning/api/views/lesson_views.py
L14: class LessonViewSet(
L17: permission_classes = [IsAuthenticated]
L19: def get_queryset(self):
L34: def perform_create(self, serializer):
L44: @action(

## Handler declarations: learning/api/views/skill_views.py
L12: class SkillViewSet(
L26: serializer_class = SkillSerializer
L27: permission_classes = [IsAuthenticated]
L29: def get_queryset(self):

## Handler declarations: learning/api/views/user_owned_model_views.py
L6: class UserOwnedModelViewSet(
L10: permission_classes = [IsAuthenticated]

## Handler declarations: learning/api/views/user_owned_queryset_mixin_views.py
L9: class UserOwnedQuerysetMixin:
L17: def get_queryset(self):

## Handler declarations: learning/api/views/user_owned_read_only_views.py
L6: class UserOwnedReadOnlyViewSet(
L10: permission_classes = [IsAuthenticated]


Full payload/response compatibility remains UNKNOWN until handlers, serializers and active frontend consumers are traced. See [cross-project API catalog](../../05-complete-api-catalog.md).
