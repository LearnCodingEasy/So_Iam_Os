# learning/serializers.py

from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import (
    Skill,
    LearningGoal,
    LearningPath,
    LearningTopic,
    Lesson,
    LearningResource,
    LearningNote,
    LearningProgress,
    LearningSession,
    Assessment,
    AssessmentQuestion,
    AssessmentChoice,
    AssessmentAttempt,
    AssessmentResponse,
    KnowledgeApplication,
    ApplicationSubmission,
    ApplicationReview,
    LearningRevision,
)


User = get_user_model()


# ===================================================
# Helpers
# ===================================================


def get_request_user(serializer):
    """
    Return the authenticated user from serializer context.
    """
    request = serializer.context.get("request")

    if request and request.user and request.user.is_authenticated:
        return request.user

    return None


def ensure_owner(user, obj, field_name="object"):
    """
    Ensure an object belongs to the current user.
    """
    if obj is None:
        return

    if hasattr(obj, "user_id"):
        if obj.user_id != user.id:
            raise serializers.ValidationError(
                {
                    field_name: (
                        "This object does not belong to the current user."
                    )
                }
            )


# ===================================================
# Skill
# ===================================================


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "category",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class SkillMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = (
            "id",
            "name",
            "slug",
            "category",
        )
        read_only_fields = fields


# ===================================================
# Learning Goal
# ===================================================


class LearningGoalSerializer(serializers.ModelSerializer):
    skill_detail = SkillMinimalSerializer(
        source="skill",
        read_only=True,
    )

    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    current_level_display = serializers.CharField(
        source="get_current_level_display",
        read_only=True,
    )

    target_level_display = serializers.CharField(
        source="get_target_level_display",
        read_only=True,
    )

    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    class Meta:
        model = LearningGoal
        fields = (
            "id",
            "user",
            "skill",
            "skill_detail",
            "title",
            "description",
            "reason",
            "current_level",
            "current_level_display",
            "target_level",
            "target_level_display",
            "status",
            "status_display",
            "target_date",
            "completed_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "user",
            "completed_at",
            "created_at",
            "updated_at",
        )

    def validate_skill(self, skill):
        if skill and not skill.is_active:
            raise serializers.ValidationError(
                "This skill is currently inactive."
            )

        return skill

    def validate(self, attrs):
        user = get_request_user(self)

        if user is None:
            raise serializers.ValidationError(
                "Authentication is required."
            )

        return attrs

    def create(self, validated_data):
        user = get_request_user(self)

        return LearningGoal.objects.create(
            user=user,
            **validated_data,
        )


# ===================================================
# Learning Path
# ===================================================


class LearningPathSerializer(serializers.ModelSerializer):
    goal_detail = LearningGoalSerializer(
        source="goal",
        read_only=True,
    )

    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    class Meta:
        model = LearningPath
        fields = (
            "id",
            "user",
            "goal",
            "goal_detail",
            "title",
            "description",
            "status",
            "status_display",
            "started_at",
            "completed_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "user",
            "started_at",
            "completed_at",
            "created_at",
            "updated_at",
        )

    def validate_goal(self, goal):
        user = get_request_user(self)

        if user is None:
            raise serializers.ValidationError(
                "Authentication is required."
            )

        ensure_owner(
            user,
            goal,
            "goal",
        )

        return goal

    def validate(self, attrs):
        user = get_request_user(self)

        if user is None:
            raise serializers.ValidationError(
                "Authentication is required."
            )

        return attrs

    def create(self, validated_data):
        user = get_request_user(self)

        return LearningPath.objects.create(
            user=user,
            **validated_data,
        )


# ===================================================
# Learning Topic
# ===================================================


class LearningTopicMinimalSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    difficulty_display = serializers.CharField(
        source="get_difficulty_display",
        read_only=True,
    )

    skill_detail = SkillMinimalSerializer(
        source="skill",
        read_only=True,
    )

    class Meta:
        model = LearningTopic
        fields = (
            "id",
            "title",
            "description",
            "order",
            "status",
            "status_display",
            "difficulty",
            "difficulty_display",
            "estimated_minutes",
            "skill",
            "skill_detail",
        )
        read_only_fields = fields


class LearningTopicSerializer(serializers.ModelSerializer):
    skill_detail = SkillMinimalSerializer(
        source="skill",
        read_only=True,
    )

    path_detail = serializers.SerializerMethodField()

    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    difficulty_display = serializers.CharField(
        source="get_difficulty_display",
        read_only=True,
    )

    prerequisites_detail = LearningTopicMinimalSerializer(
        source="prerequisites",
        many=True,
        read_only=True,
    )

    class Meta:
        model = LearningTopic
        fields = (
            "id",
            "path",
            "path_detail",
            "skill",
            "skill_detail",
            "title",
            "description",
            "order",
            "status",
            "status_display",
            "difficulty",
            "difficulty_display",
            "estimated_minutes",
            "prerequisites",
            "prerequisites_detail",
            "knowledge_item",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "path_detail",
            "skill_detail",
            "status_display",
            "difficulty_display",
            "prerequisites_detail",
            "created_at",
            "updated_at",
        )

    def get_path_detail(self, obj):
        path = obj.path

        return {
            "id": path.id,
            "title": path.title,
            "goal": path.goal_id,
            "status": path.status,
        }

    def validate_path(self, path):
        user = get_request_user(self)

        if user is None:
            raise serializers.ValidationError(
                "Authentication is required."
            )

        ensure_owner(
            user,
            path,
            "path",
        )

        return path

    def validate_skill(self, skill):
        if skill and not skill.is_active:
            raise serializers.ValidationError(
                "This skill is currently inactive."
            )

        return skill

    def validate_prerequisites(self, prerequisites):
        if self.instance:
            if self.instance in prerequisites:
                raise serializers.ValidationError(
                    "A topic cannot depend on itself."
                )

        return prerequisites


# ===================================================
# Lesson
# ===================================================


class LessonMinimalSerializer(serializers.ModelSerializer):
    content_format_display = serializers.CharField(
        source="get_content_format_display",
        read_only=True,
    )

    class Meta:
        model = Lesson
        fields = (
            "id",
            "topic",
            "title",
            "description",
            "content_format",
            "content_format_display",
            "order",
            "estimated_minutes",
            "is_active",
        )
        read_only_fields = fields


class LessonSerializer(serializers.ModelSerializer):
    content_format_display = serializers.CharField(
        source="get_content_format_display",
        read_only=True,
    )

    class Meta:
        model = Lesson
        fields = (
            "id",
            "topic",
            "title",
            "description",
            "content",
            "content_format",
            "content_format_display",
            "order",
            "estimated_minutes",
            "learning_objectives",
            "key_concepts",
            "examples",
            "practical_instructions",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "content_format_display",
            "created_at",
            "updated_at",
        )

    def validate_topic(self, topic):
        user = get_request_user(self)

        if user is None:
            raise serializers.ValidationError(
                "Authentication is required."
            )

        ensure_owner(
            user,
            topic.path,
            "topic",
        )

        return topic

    def validate(self, attrs):
        json_fields = (
            "learning_objectives",
            "key_concepts",
            "examples",
            "practical_instructions",
        )

        for field in json_fields:
            if field in attrs:
                value = attrs[field]

                if not isinstance(value, list):
                    raise serializers.ValidationError(
                        {
                            field: "This field must be a JSON list."
                        }
                    )

        return attrs


# ===================================================
# Learning Resource
# ===================================================


class LearningResourceSerializer(serializers.ModelSerializer):
    reference_type_display = serializers.CharField(
        source="get_reference_type_display",
        read_only=True,
    )

    file_url = serializers.SerializerMethodField()

    class Meta:
        model = LearningResource
        fields = (
            "id",
            "topic",
            "lesson",
            "title",
            "description",
            "reference_type",
            "reference_type_display",
            "url",
            "file",
            "file_url",
            "content",
            "caption",
            "order",
            "created_at",
        )
        read_only_fields = (
            "id",
            "reference_type_display",
            "file_url",
            "created_at",
        )

    def get_file_url(self, obj):
        if not obj.file:
            return None

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(
                obj.file.url
            )

        return obj.file.url

    def validate_topic(self, topic):
        user = get_request_user(self)

        if user is None:
            raise serializers.ValidationError(
                "Authentication is required."
            )

        ensure_owner(
            user,
            topic.path,
            "topic",
        )

        return topic

    def validate(self, attrs):
        topic = attrs.get(
            "topic",
            self.instance.topic if self.instance else None,
        )

        lesson = attrs.get(
            "lesson",
            self.instance.lesson if self.instance else None,
        )

        reference_type = attrs.get(
            "reference_type",
            (
                self.instance.reference_type
                if self.instance
                else LearningResource.ResourceType.WEBSITE
            ),
        )

        if lesson and topic:
            if lesson.topic_id != topic.id:
                raise serializers.ValidationError(
                    {
                        "lesson": (
                            "Lesson must belong to the selected topic."
                        )
                    }
                )

        if reference_type == LearningResource.ResourceType.FILE:
            file = attrs.get(
                "file",
                self.instance.file if self.instance else None,
            )

            if not file:
                raise serializers.ValidationError(
                    {
                        "file": (
                            "A file is required for file resources."
                        )
                    }
                )

        url_required_types = {
            LearningResource.ResourceType.WEBSITE,
            LearningResource.ResourceType.DOCUMENTATION,
            LearningResource.ResourceType.ARTICLE,
            LearningResource.ResourceType.VIDEO,
        }

        if reference_type in url_required_types:
            url = attrs.get(
                "url",
                self.instance.url if self.instance else "",
            )

            if not url:
                raise serializers.ValidationError(
                    {
                        "url": (
                            "A URL is required for this resource type."
                        )
                    }
                )

        return attrs


# ===================================================
# Learning Note
# ===================================================


class LearningNoteSerializer(serializers.ModelSerializer):
    note_type_display = serializers.CharField(
        source="get_note_type_display",
        read_only=True,
    )

    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    class Meta:
        model = LearningNote
        fields = (
            "id",
            "user",
            "topic",
            "lesson",
            "knowledge_item",
            "note_type",
            "note_type_display",
            "title",
            "content",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "user",
            "note_type_display",
            "created_at",
            "updated_at",
        )

    def validate_topic(self, topic):
        user = get_request_user(self)

        if user is None:
            raise serializers.ValidationError(
                "Authentication is required."
            )

        ensure_owner(
            user,
            topic.path,
            "topic",
        )

        return topic

    def validate(self, attrs):
        topic = attrs.get(
            "topic",
            self.instance.topic if self.instance else None,
        )

        lesson = attrs.get(
            "lesson",
            self.instance.lesson if self.instance else None,
        )

        if lesson and topic:
            if lesson.topic_id != topic.id:
                raise serializers.ValidationError(
                    {
                        "lesson": (
                            "Lesson must belong to the selected topic."
                        )
                    }
                )

        return attrs

    def create(self, validated_data):
        user = get_request_user(self)

        return LearningNote.objects.create(
            user=user,
            **validated_data,
        )


# ===================================================
# Learning Progress
# ===================================================


class LearningProgressSerializer(serializers.ModelSerializer):
    mastery_display = serializers.CharField(
        source="get_mastery_level_display",
        read_only=True,
    )

    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    class Meta:
        model = LearningProgress
        fields = (
            "id",
            "user",
            "topic",
            "progress_percent",
            "practice_completed",
            "notes",
            "mastery_level",
            "mastery_display",
            "last_ai_score",
            "needs_review",
            "lesson_completed",
            "quick_check_completed",
            "assessment_completed",
            "last_activity_at",
            "completed_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "user",
            "last_ai_score",
            "needs_review",
            "last_activity_at",
            "completed_at",
            "created_at",
            "updated_at",
        )

    def validate_topic(self, topic):
        user = get_request_user(self)

        if user is None:
            raise serializers.ValidationError(
                "Authentication is required."
            )

        ensure_owner(
            user,
            topic.path,
            "topic",
        )

        return topic

    def create(self, validated_data):
        user = get_request_user(self)

        return LearningProgress.objects.create(
            user=user,
            **validated_data,
        )


# ===================================================
# Learning Session
# ===================================================


class LearningSessionSerializer(serializers.ModelSerializer):
    activity_type_display = serializers.CharField(
        source="get_activity_type_display",
        read_only=True,
    )

    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    class Meta:
        model = LearningSession
        fields = (
            "id",
            "user",
            "topic",
            "lesson",
            "activity_type",
            "activity_type_display",
            "started_at",
            "ended_at",
            "duration_seconds",
            "completed",
            "metadata",
        )
        read_only_fields = (
            "id",
            "user",
            "activity_type_display",
        )

    def validate_topic(self, topic):
        user = get_request_user(self)

        if user is None:
            raise serializers.ValidationError(
                "Authentication is required."
            )

        ensure_owner(
            user,
            topic.path,
            "topic",
        )

        return topic

    def validate(self, attrs):
        topic = attrs.get(
            "topic",
            self.instance.topic if self.instance else None,
        )

        lesson = attrs.get(
            "lesson",
            self.instance.lesson if self.instance else None,
        )

        if lesson and topic:
            if lesson.topic_id != topic.id:
                raise serializers.ValidationError(
                    {
                        "lesson": (
                            "Lesson must belong to the selected topic."
                        )
                    }
                )

        started_at = attrs.get(
            "started_at",
            self.instance.started_at if self.instance else None,
        )

        ended_at = attrs.get(
            "ended_at",
            self.instance.ended_at if self.instance else None,
        )

        if started_at and ended_at and ended_at < started_at:
            raise serializers.ValidationError(
                {
                    "ended_at": (
                        "End time cannot precede start time."
                    )
                }
            )

        return attrs

    def create(self, validated_data):
        user = get_request_user(self)

        return LearningSession.objects.create(
            user=user,
            **validated_data,
        )


# ===================================================
# Assessment Choice
# ===================================================


class AssessmentChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentChoice
        fields = (
            "id",
            "question",
            "text",
            "order",
            "feedback",
        )
        read_only_fields = (
            "id",
        )


class AssessmentChoiceLearnerSerializer(
    serializers.ModelSerializer
):
    """
    Learner-facing choice serializer.

    IMPORTANT:
    is_correct is intentionally excluded.
    """

    class Meta:
        model = AssessmentChoice
        fields = (
            "id",
            "text",
            "order",
        )
        read_only_fields = fields


# ===================================================
# Assessment Question
# ===================================================


class AssessmentQuestionSerializer(serializers.ModelSerializer):
    question_type_display = serializers.CharField(
        source="get_question_type_display",
        read_only=True,
    )

    choices = AssessmentChoiceSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = AssessmentQuestion
        fields = (
            "id",
            "assessment",
            "question_type",
            "question_type_display",
            "prompt",
            "explanation",
            "points",
            "order",
            "is_required",
            "grading_data",
            "choices",
        )
        read_only_fields = (
            "id",
            "question_type_display",
            "choices",
        )

        extra_kwargs = {
            "grading_data": {
                "write_only": True,
            },
        }

    def validate_assessment(self, assessment):
        user = get_request_user(self)

        if user is None:
            raise serializers.ValidationError(
                "Authentication is required."
            )

        ensure_owner(
            user,
            assessment.topic.path,
            "assessment",
        )

        return assessment


class AssessmentQuestionLearnerSerializer(
    serializers.ModelSerializer
):
    """
    Safe serializer used while the learner is taking an assessment.

    Never exposes:
    - grading_data
    - correct answers
    """

    question_type_display = serializers.CharField(
        source="get_question_type_display",
        read_only=True,
    )

    choices = AssessmentChoiceLearnerSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = AssessmentQuestion
        fields = (
            "id",
            "assessment",
            "question_type",
            "question_type_display",
            "prompt",
            "explanation",
            "points",
            "order",
            "is_required",
            "choices",
        )
        read_only_fields = fields


# ===================================================
# Assessment
# ===================================================


class AssessmentSerializer(serializers.ModelSerializer):
    assessment_type_display = serializers.CharField(
        source="get_assessment_type_display",
        read_only=True,
    )

    questions = AssessmentQuestionSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Assessment
        fields = (
            "id",
            "topic",
            "title",
            "description",
            "instructions",
            "assessment_type",
            "assessment_type_display",
            "passing_score",
            "estimated_minutes",
            "order",
            "is_active",
            "questions",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "assessment_type_display",
            "questions",
            "created_at",
            "updated_at",
        )

    def validate_topic(self, topic):
        user = get_request_user(self)

        if user is None:
            raise serializers.ValidationError(
                "Authentication is required."
            )

        ensure_owner(
            user,
            topic.path,
            "topic",
        )

        return topic


class AssessmentLearnerSerializer(
    serializers.ModelSerializer
):
    """
    Safe assessment serializer for the learner UI.
    """

    assessment_type_display = serializers.CharField(
        source="get_assessment_type_display",
        read_only=True,
    )

    questions = AssessmentQuestionLearnerSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Assessment
        fields = (
            "id",
            "topic",
            "title",
            "description",
            "instructions",
            "assessment_type",
            "assessment_type_display",
            "passing_score",
            "estimated_minutes",
            "order",
            "is_active",
            "questions",
        )
        read_only_fields = fields


# ===================================================
# Assessment Attempt
# ===================================================


class AssessmentAttemptSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    assessment_detail = AssessmentLearnerSerializer(
        source="assessment",
        read_only=True,
    )

    class Meta:
        model = AssessmentAttempt
        fields = (
            "id",
            "assessment",
            "assessment_detail",
            "user",
            "score",
            "passed",
            "feedback",
            "started_at",
            "completed_at",
            "attempt_number",
        )
        read_only_fields = (
            "id",
            "user",
            "score",
            "passed",
            "feedback",
            "completed_at",
            "attempt_number",
        )

    def validate_assessment(self, assessment):
        user = get_request_user(self)

        if user is None:
            raise serializers.ValidationError(
                "Authentication is required."
            )

        ensure_owner(
            user,
            assessment.topic.path,
            "assessment",
        )

        return assessment

    def create(self, validated_data):
        user = get_request_user(self)

        assessment = validated_data["assessment"]

        last_attempt = (
            AssessmentAttempt.objects
            .filter(
                assessment=assessment,
                user=user,
            )
            .order_by("-attempt_number")
            .first()
        )

        next_attempt_number = (
            last_attempt.attempt_number + 1
            if last_attempt
            else 1
        )

        return AssessmentAttempt.objects.create(
            user=user,
            attempt_number=next_attempt_number,
            **validated_data,
        )


# ===================================================
# Assessment Response
# ===================================================


class AssessmentResponseSerializer(
    serializers.ModelSerializer
):
    selected_choices = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=AssessmentChoice.objects.all(),
        required=False,
    )

    class Meta:
        model = AssessmentResponse
        fields = (
            "id",
            "attempt",
            "question",
            "selected_choices",
            "text_answer",
            "is_correct",
            "points_awarded",
            "feedback",
        )
        read_only_fields = (
            "id",
            "is_correct",
            "points_awarded",
            "feedback",
        )

    def validate(self, attrs):
        user = get_request_user(self)

        if user is None:
            raise serializers.ValidationError(
                "Authentication is required."
            )

        attempt = attrs.get(
            "attempt",
            self.instance.attempt
            if self.instance
            else None,
        )

        question = attrs.get(
            "question",
            self.instance.question
            if self.instance
            else None,
        )

        if attempt and attempt.user_id != user.id:
            raise serializers.ValidationError(
                {
                    "attempt": (
                        "This attempt does not belong "
                        "to the current user."
                    )
                }
            )

        if attempt and question:
            if (
                attempt.assessment_id
                != question.assessment_id
            ):
                raise serializers.ValidationError(
                    {
                        "question": (
                            "Question must belong to "
                            "the attempt's assessment."
                        )
                    }
                )

        selected_choices = attrs.get(
            "selected_choices"
        )

        if selected_choices and question:
            invalid_choices = [
                choice.id
                for choice in selected_choices
                if choice.question_id != question.id
            ]

            if invalid_choices:
                raise serializers.ValidationError(
                    {
                        "selected_choices": (
                            "All selected choices must "
                            "belong to the selected question."
                        )
                    }
                )

        return attrs


# ===================================================
# Knowledge Application
# ===================================================


class KnowledgeApplicationSerializer(
    serializers.ModelSerializer
):
    application_type_display = serializers.CharField(
        source="get_application_type_display",
        read_only=True,
    )

    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    class Meta:
        model = KnowledgeApplication
        fields = (
            "id",
            "user",
            "topic",
            "lesson",
            "knowledge_item",
            "title",
            "content",
            "application_type",
            "application_type_display",
            "status",
            "status_display",
            "submitted_at",
            "reviewed_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "user",
            "application_type_display",
            "status_display",
            "submitted_at",
            "reviewed_at",
            "created_at",
            "updated_at",
        )

    def validate_topic(self, topic):
        user = get_request_user(self)

        if user is None:
            raise serializers.ValidationError(
                "Authentication is required."
            )

        ensure_owner(
            user,
            topic.path,
            "topic",
        )

        return topic

    def validate(self, attrs):
        topic = attrs.get(
            "topic",
            self.instance.topic if self.instance else None,
        )

        lesson = attrs.get(
            "lesson",
            self.instance.lesson if self.instance else None,
        )

        if lesson and topic:
            if lesson.topic_id != topic.id:
                raise serializers.ValidationError(
                    {
                        "lesson": (
                            "Lesson must belong to "
                            "the selected topic."
                        )
                    }
                )

        return attrs

    def create(self, validated_data):
        # user = get_request_user(self)

        return KnowledgeApplication.objects.create(
            # user=user,
            **validated_data,
        )


# ===================================================
# Application Submission
# ===================================================


class ApplicationSubmissionSerializer(
    serializers.ModelSerializer
):
    application_detail = KnowledgeApplicationSerializer(
        source="application",
        read_only=True,
    )

    class Meta:
        model = ApplicationSubmission
        fields = (
            "id",
            "application",
            "application_detail",
            "version",
            "title",
            "content",
            "submitted_at",
        )
        read_only_fields = (
            "id",
            "version",
            "submitted_at",
        )

    def validate_application(self, application):
        user = get_request_user(self)

        if user is None:
            raise serializers.ValidationError(
                "Authentication is required."
            )

        ensure_owner(
            user,
            application,
            "application",
        )

        return application

    def create(self, validated_data):
        application = validated_data["application"]

        last_submission = (
            ApplicationSubmission.objects
            .filter(application=application)
            .order_by("-version")
            .first()
        )

        next_version = (
            last_submission.version + 1
            if last_submission
            else 1
        )

        return ApplicationSubmission.objects.create(
            version=next_version,
            **validated_data,
        )


# ===================================================
# Application Review
# ===================================================


class ApplicationReviewSerializer(
    serializers.ModelSerializer
):
    mastery_display = serializers.CharField(
        source="get_mastery_level_display",
        read_only=True,
    )

    submission_detail = ApplicationSubmissionSerializer(
        source="submission",
        read_only=True,
    )

    application_detail = KnowledgeApplicationSerializer(
        source="application",
        read_only=True,
    )

    class Meta:
        model = ApplicationReview
        fields = (
            "id",
            "submission",
            "submission_detail",
            "application",
            "application_detail",
            "score",
            "mastery_level",
            "mastery_display",
            "understood",
            "applied",
            "strengths",
            "weaknesses",
            "errors",
            "needs_review",
            "knowledge_gaps",
            "recommendations",
            "feedback",
            "ai_metadata",
            "reviewed_by",
            "reviewed_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "mastery_display",
            "submission_detail",
            "application_detail",
            "reviewed_at",
            "created_at",
            "updated_at",
        )

    def validate(self, attrs):
        submission = attrs.get(
            "submission",
            self.instance.submission
            if self.instance
            else None,
        )

        application = attrs.get(
            "application",
            self.instance.application
            if self.instance
            else None,
        )

        if submission and application:
            if (
                submission.application_id
                != application.id
            ):
                raise serializers.ValidationError(
                    {
                        "application": (
                            "Application must match "
                            "the submission's application."
                        )
                    }
                )

        return attrs


# ===================================================
# Learning Revision
# ===================================================


class LearningRevisionSerializer(
    serializers.ModelSerializer
):
    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    source_review_detail = ApplicationReviewSerializer(
        source="source_review",
        read_only=True,
    )

    class Meta:
        model = LearningRevision
        fields = (
            "id",
            "user",
            "topic",
            "source_review",
            "source_review_detail",
            "concepts",
            "recommendation",
            "status",
            "status_display",
            "scheduled_for",
            "started_at",
            "completed_at",
            "outcome",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "user",
            "source_review_detail",
            "status_display",
            "created_at",
            "updated_at",
        )

    def validate_topic(self, topic):
        user = get_request_user(self)

        if user is None:
            raise serializers.ValidationError(
                "Authentication is required."
            )

        ensure_owner(
            user,
            topic.path,
            "topic",
        )

        return topic

    def validate_source_review(self, source_review):
        if source_review:
            user = get_request_user(self)

            if user is None:
                raise serializers.ValidationError(
                    "Authentication is required."
                )

            application = source_review.application

            ensure_owner(
                user,
                application,
                "source_review",
            )

        return source_review

    def validate(self, attrs):
        started_at = attrs.get(
            "started_at",
            self.instance.started_at
            if self.instance
            else None,
        )

        completed_at = attrs.get(
            "completed_at",
            self.instance.completed_at
            if self.instance
            else None,
        )

        if (
            started_at
            and completed_at
            and completed_at < started_at
        ):
            raise serializers.ValidationError(
                {
                    "completed_at": (
                        "Cannot precede start time."
                    )
                }
            )

        return attrs

    def create(self, validated_data):
        user = get_request_user(self)

        return LearningRevision.objects.create(
            user=user,
            **validated_data,
        )


# ===================================================
# Rich Topic Detail
# ===================================================

class LearningPathTopicSummarySerializer(
    serializers.ModelSerializer
):
    goal = serializers.SerializerMethodField()

    class Meta:
        model = LearningPath
        fields = (
            "id",
            "title",
            "description",
            "status",
            "goal",
        )
        read_only_fields = fields

    def get_goal(self, obj):
        if not obj.goal:
            return None

        return {
            "id": obj.goal.id,
            "title": obj.goal.title,
            "status": obj.goal.status,
            "current_level": obj.goal.current_level,
            "target_level": obj.goal.target_level,
        }


class LearningTopicDetailSerializer(
    LearningTopicSerializer
):
    """
    Rich API contract for LearningTopic.vue.

    This serializer intentionally exposes the complete learning
    context required by the Learning Loop.
    """

    # -----------------------------------------------
    # Core entities
    # -----------------------------------------------

    path = LearningPathTopicSummarySerializer(
        read_only=True,
    )

    skill = SkillSerializer(
        read_only=True,
    )

    # -----------------------------------------------
    # Learning content
    # -----------------------------------------------

    lessons = LessonSerializer(
        many=True,
        read_only=True,
    )

    lesson = serializers.SerializerMethodField()

    resources = LearningResourceSerializer(
        many=True,
        read_only=True,
    )

    references = serializers.SerializerMethodField()

    images = serializers.SerializerMethodField()

    # -----------------------------------------------
    # Knowledge
    # -----------------------------------------------

    knowledge_item = serializers.SerializerMethodField()

    notes = LearningNoteSerializer(
        many=True,
        read_only=True,
    )

    applications = KnowledgeApplicationSerializer(
        many=True,
        read_only=True,
    )

    reviews = serializers.SerializerMethodField()

    # -----------------------------------------------
    # Progress
    # -----------------------------------------------

    progress = serializers.SerializerMethodField()

    mastery = serializers.SerializerMethodField()

    # -----------------------------------------------
    # AI
    # -----------------------------------------------

    ai = serializers.SerializerMethodField()

    class Meta:
        model = LearningTopic

        fields = (
            "id",

            "title",
            "description",
            "order",

            "status",
            "status_display",

            "difficulty",
            "difficulty_display",

            "estimated_minutes",

            "path",
            "skill",

            "prerequisites",
            "prerequisites_detail",

            # Learning
            "lessons",
            "lesson",

            # Resources
            "resources",
            "references",
            "images",

            # Knowledge
            "knowledge_item",
            "notes",
            "applications",
            "reviews",

            # Progress
            "progress",
            "mastery",

            # AI
            "ai",

            "created_at",
            "updated_at",
        )

        read_only_fields = fields

    # ===============================================
    # Lesson
    # ===============================================

    def get_lesson(self, obj):
        lessons = list(obj.lessons.all())

        if not lessons:
            return None

        lesson = next(
            (
                lesson
                for lesson in lessons
                if lesson.is_active
            ),
            lessons[0],
        )

        return LessonSerializer(
            lesson,
            context=self.context,
        ).data

    # ===============================================
    # References
    # ===============================================

    def get_references(self, obj):
        return [
            LearningResourceSerializer(
                resource,
                context=self.context,
            ).data
            for resource in obj.resources.all()
            if resource.reference_type != LearningResource.ResourceType.IMAGE
        ]

    # ===============================================
    # Images
    # ===============================================

    def get_images(self, obj):
        return [
            LearningResourceSerializer(
                resource,
                context=self.context,
            ).data
            for resource in obj.resources.all()
            if resource.reference_type
            == LearningResource.ResourceType.IMAGE
        ]

    # ===============================================
    # Knowledge
    # ===============================================

    def get_knowledge_item(self, obj):
        if not obj.knowledge_item:
            return None

        from knowledge.serializers import KnowledgeItemSerializer

        return KnowledgeItemSerializer(
            obj.knowledge_item,
            context=self.context,
        ).data

    # =========================================================
    # Reviews
    # =========================================================

    def get_reviews(self, obj):
        reviews = []

        for application in obj.applications.all():
            for review in application.reviews.all():
                reviews.append(
                    ApplicationReviewSerializer(
                        review,
                        context=self.context,
                    ).data
                )

        return reviews

    # =========================================================
    # Progress
    # =========================================================

    def get_progress(self, obj):
        request = self.context.get("request")

        if not request or not request.user.is_authenticated:
            return None

        progress = next(
            iter(
                getattr(
                    obj,
                    "_current_user_progress",
                    [],
                )
            ),
            None,
        )

        if not progress:
            return {
                "id": None,
                "topic": obj.id,
                "progress_percent": 0,
                "practice_completed": False,
                "notes": "",
                "mastery_level": "not_started",
                "mastery_display": "Not Started",
                "last_ai_score": None,
                "needs_review": False,
                "lesson_completed": False,
                "quick_check_completed": False,
                "assessment_completed": False,
                "last_activity_at": None,
                "completed_at": None,
            }

        return LearningProgressSerializer(
            progress,
            context=self.context,
        ).data

    # =========================================================
    # Mastery
    # =========================================================

    def get_mastery(self, obj):
        progress = next(
            iter(
                getattr(
                    obj,
                    "_current_user_progress",
                    [],
                )
            ),
            None,
        )

        if not progress:
            return {
                "score": 0,
                "threshold": 90,
                "is_mastered": False,
                "can_advance": False,
            }

        score = (
            progress.last_ai_score
            if progress.last_ai_score is not None
            else progress.progress_percent
        )

        is_mastered = (
            score >= 90
            and progress.lesson_completed
            and progress.practice_completed
            and progress.assessment_completed
        )

        return {
            "score": score,
            "threshold": 90,
            "is_mastered": is_mastered,
            "can_advance": is_mastered,
        }

    # =========================================================
    # AI
    # =========================================================

    def get_ai(self, obj):
        lessons = list(obj.lessons.all())
        assessments = list(obj.assessments.all())

        content_available = bool(
            lessons
            and any(
                lesson.content.strip()
                for lesson in lessons
            )
        )

        timestamps = []

        for lesson in lessons:
            timestamps.append(
                lesson.updated_at
            )

        for assessment in assessments:
            timestamps.append(
                assessment.updated_at
            )

        generated_at = (
            max(timestamps)
            if timestamps
            else None
        )

        if not content_available:
            ai_status = "empty"
        else:
            ai_status = "ready"

        return {
            "content_available": content_available,
            "generated_at": generated_at,
            "status": ai_status,
        }
# ===================================================
# Rich Learning Path Detail
# ===================================================


class LearningPathDetailSerializer(
    LearningPathSerializer
):
    topics = LearningTopicMinimalSerializer(
        many=True,
        read_only=True,
    )

    class Meta(LearningPathSerializer.Meta):
        fields = (
            "id",
            "user",
            "goal",
            "goal_detail",
            "title",
            "description",
            "status",
            "status_display",
            "started_at",
            "completed_at",
            "topics",
            "created_at",
            "updated_at",
        )


# ===================================================
# Rich Learning Goal Detail
# ===================================================


class LearningGoalDetailSerializer(
    LearningGoalSerializer
):
    paths = LearningPathMinimalSerializer = serializers.SerializerMethodField()

    def get_paths(self, obj):
        paths = obj.paths.all()

        return [
            {
                "id": path.id,
                "title": path.title,
                "description": path.description,
                "status": path.status,
                "started_at": path.started_at,
                "completed_at": path.completed_at,
            }
            for path in paths
        ]

    class Meta(LearningGoalSerializer.Meta):
        fields = (
            "id",
            "user",
            "skill",
            "skill_detail",
            "title",
            "description",
            "reason",
            "current_level",
            "current_level_display",
            "target_level",
            "target_level_display",
            "status",
            "status_display",
            "target_date",
            "completed_at",
            "paths",
            "created_at",
            "updated_at",
        )


# ===================================================
# Dashboard Serializer
# ===================================================


class LearningDashboardSerializer(
    serializers.Serializer
):
    """
    Read-only serializer for the main Learning dashboard.

    Expected input:
        {
            "goals": [...],
            "active_paths": [...],
            "recent_topics": [...],
            "progress": [...],
            "reviews": [...],
            "revisions": [...]
        }
    """

    goals = LearningGoalSerializer(
        many=True,
        read_only=True,
    )

    active_paths = LearningPathSerializer(
        many=True,
        read_only=True,
    )

    recent_topics = LearningTopicMinimalSerializer(
        many=True,
        read_only=True,
    )

    progress = LearningProgressSerializer(
        many=True,
        read_only=True,
    )

    reviews = ApplicationReviewSerializer(
        many=True,
        read_only=True,
    )

    revisions = LearningRevisionSerializer(
        many=True,
        read_only=True,
    )
