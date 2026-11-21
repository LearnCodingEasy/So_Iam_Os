from rest_framework import serializers
from learning.models import LearningPath, LearningTopic, LearningResource
from learning.api.serializers.application_review_serializers import ApplicationReviewSerializer
from learning.api.serializers.common import ensure_owner, get_request_user
from learning.api.serializers.knowledge_application_serializers import KnowledgeApplicationSerializer
from learning.api.serializers.learning_goal_serializers import LearningGoalSerializer
from learning.api.serializers.learning_note_serializers import LearningNoteSerializer
from learning.api.serializers.learning_progress_serializers import LearningProgressSerializer
from learning.api.serializers.learning_resource_serializers import LearningResourceSerializer
from learning.api.serializers.lesson_serializers import LessonSerializer
from learning.api.serializers.skill_serializers import SkillMinimalSerializer, SkillSerializer


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
    next_topic = serializers.SerializerMethodField()

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
            "next_topic",

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

        from knowledge.api.serializers import KnowledgeItemSerializer

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

    def get_next_topic(self, obj):
        topic = obj.path.topics.filter(order__gt=obj.order).exclude(
            status=LearningTopic.Status.SKIPPED).order_by("order", "id").first()
        if not topic:
            return None
        return {"id": topic.id, "title": topic.title, "order": topic.order, "status": topic.status}

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
