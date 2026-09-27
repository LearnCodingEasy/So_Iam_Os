# learning/services/ai_content.py

import json
import re

from django.db import transaction
from django.utils import timezone

from ai.providers import get_ai_provider
from ai.prompts import (
    build_learning_topic_content_prompt,
)

from learning.models import (
    LearningTopic,
    Lesson,
    Assessment,
    AssessmentQuestion,
    AssessmentChoice,
)


class LearningTopicAIContentService:
    """
    Generates and persists AI-powered learning content
    for a LearningTopic.
    """

    def __init__(
        self,
        *,
        user,
        provider="ollama",
        model="",
    ):
        self.user = user
        self.provider_name = provider
        self.model = model or ""

    # =========================================================
    # Public API
    # =========================================================

    @transaction.atomic
    def generate(self, topic):
        self._ensure_owner(topic)

        context = self._build_context(topic)

        prompt = build_learning_topic_content_prompt(
            context=context,
        )

        provider = get_ai_provider(
            self.provider_name,
        )

        result = provider.generate(
            messages=[
                {
                    "role": "system",
                    "content": self._system_prompt(),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            model=self.model or None,
        )

        payload = self._parse_json(
            result["content"],
        )

        self._validate_payload(
            payload,
        )

        lesson = self._save_lesson(
            topic=topic,
            payload=payload,
        )

        assessment = self._save_assessment(
            topic=topic,
            payload=payload,
        )

        return {
            "topic": topic,
            "lesson": lesson,
            "assessment": assessment,
            "provider": result["provider"],
            "model": result["model"],
            "generated_at": timezone.now(),
        }

    # =========================================================
    # Ownership
    # =========================================================

    def _ensure_owner(self, topic):
        if topic.path.user_id != self.user.id:
            raise PermissionError(
                "You do not own this learning topic."
            )

    # =========================================================
    # System Prompt
    # =========================================================

    def _system_prompt(self):
        from ai.prompts import (
            BASE_SYSTEM_PROMPT,
            LEARNING_SYSTEM_PROMPT,
        )

        return (
            BASE_SYSTEM_PROMPT.strip()
            + "\n\n"
            + LEARNING_SYSTEM_PROMPT.strip()
        )

    # =========================================================
    # Context
    # =========================================================

    def _build_context(self, topic):
        knowledge = topic.knowledge_item

        knowledge_context = None

        if knowledge:
            knowledge_context = {
                "id": knowledge.id,
                "title": knowledge.title,
                "description": knowledge.description,
                "content": self._truncate(
                    knowledge.content,
                    12000,
                ),
                "knowledge_type": knowledge.knowledge_type,
                "source_url": knowledge.source_url,
                "source_name": knowledge.source_name,
                "tags": knowledge.tags,
                "metadata": knowledge.metadata,
                "files": [
                    {
                        "name": file.name,
                        "file_type": file.file_type,
                    }
                    for file in knowledge.files.all()
                ],
            }

        progress = (
            topic.progress_records
            .filter(
                user=self.user,
            )
            .first()
        )

        previous_reviews = []

        for application in topic.applications.filter(
            user=self.user,
        ):
            for review in application.reviews.all():
                previous_reviews.append(
                    {
                        "score": review.score,
                        "mastery_level": review.mastery_level,
                        "weaknesses": review.weaknesses,
                        "knowledge_gaps": review.knowledge_gaps,
                        "recommendations": review.recommendations,
                    }
                )

        return {
            "topic": {
                "id": topic.id,
                "title": topic.title,
                "description": topic.description,
                "difficulty": topic.difficulty,
                "estimated_minutes": topic.estimated_minutes,
            },

            "path": {
                "id": topic.path.id,
                "title": topic.path.title,
                "description": topic.path.description,
            },

            "goal": {
                "id": topic.path.goal.id,
                "title": topic.path.goal.title,
                "description": topic.path.goal.description,
                "current_level": topic.path.goal.current_level,
                "target_level": topic.path.goal.target_level,
            },

            "skill": (
                {
                    "id": topic.skill.id,
                    "name": topic.skill.name,
                    "description": topic.skill.description,
                    "category": topic.skill.category,
                }
                if topic.skill
                else None
            ),

            "knowledge": knowledge_context,

            "progress": (
                {
                    "progress_percent": progress.progress_percent,
                    "mastery_level": progress.mastery_level,
                    "last_ai_score": progress.last_ai_score,
                    "needs_review": progress.needs_review,
                    "lesson_completed": progress.lesson_completed,
                    "practice_completed": progress.practice_completed,
                    "quick_check_completed": progress.quick_check_completed,
                    "assessment_completed": progress.assessment_completed,
                }
                if progress
                else None
            ),

            "previous_reviews": previous_reviews[-5:],
        }

    # =========================================================
    # Save Lesson
    # =========================================================

    def _save_lesson(self, *, topic, payload):
        lesson_data = payload["lesson"]

        lesson = (
            topic.lessons
            .filter(
                is_active=True,
            )
            .order_by("order", "id")
            .first()
        )

        if lesson is None:
            lesson = Lesson(
                topic=topic,
                order=1,
            )

        lesson.title = lesson_data["title"]
        lesson.description = lesson_data.get(
            "description",
            "",
        )
        lesson.content = lesson_data.get(
            "content",
            "",
        )
        lesson.content_format = Lesson.ContentFormat.MARKDOWN
        lesson.estimated_minutes = lesson_data.get(
            "estimated_minutes",
            topic.estimated_minutes,
        )

        lesson.learning_objectives = lesson_data.get(
            "learning_objectives",
            [],
        )

        lesson.key_concepts = lesson_data.get(
            "key_concepts",
            [],
        )

        lesson.examples = lesson_data.get(
            "examples",
            [],
        )

        lesson.practical_instructions = lesson_data.get(
            "practical_instructions",
            [],
        )

        lesson.is_active = True

        lesson.save()

        return lesson

    # =========================================================
    # Save Assessment
    # =========================================================

    def _save_assessment(self, *, topic, payload):
        quiz = payload.get("quiz")

        if not quiz:
            return None

        assessment = (
            topic.assessments
            .filter(
                assessment_type=Assessment.Type.QUIZ,
            )
            .order_by("order", "id")
            .first()
        )

        if assessment is None:
            assessment = Assessment(
                topic=topic,
                assessment_type=Assessment.Type.QUIZ,
                order=1,
            )

        assessment.title = quiz.get(
            "title",
            f"{topic.title} Quiz",
        )

        assessment.description = quiz.get(
            "description",
            "",
        )

        assessment.instructions = quiz.get(
            "instructions",
            "",
        )

        assessment.passing_score = quiz.get(
            "passing_score",
            70,
        )

        assessment.estimated_minutes = quiz.get(
            "estimated_minutes",
            10,
        )

        assessment.is_active = True

        assessment.save()

        assessment.questions.all().delete()

        for index, question_data in enumerate(
            quiz.get("questions", []),
            start=1,
        ):
            question = AssessmentQuestion.objects.create(
                assessment=assessment,
                question_type=question_data.get(
                    "question_type",
                    AssessmentQuestion.Type.SINGLE_CHOICE,
                ),
                prompt=question_data["prompt"],
                explanation=question_data.get(
                    "explanation",
                    "",
                ),
                points=question_data.get(
                    "points",
                    1,
                ),
                order=index,
                is_required=True,
                grading_data=question_data.get(
                    "grading_data",
                    {},
                ),
            )

            for choice_index, choice_data in enumerate(
                question_data.get("choices", []),
                start=1,
            ):
                AssessmentChoice.objects.create(
                    question=question,
                    text=choice_data["text"],
                    order=choice_index,
                    is_correct=choice_data.get(
                        "is_correct",
                        False,
                    ),
                    feedback=choice_data.get(
                        "feedback",
                        "",
                    ),
                )

        return assessment

    # =========================================================
    # JSON parsing
    # =========================================================

    @staticmethod
    def _parse_json(content):
        content = content.strip()

        fenced = re.search(
            r"```(?:json)?\s*(.*?)\s*```",
            content,
            flags=re.DOTALL | re.IGNORECASE,
        )

        if fenced:
            content = fenced.group(1).strip()

        try:
            return json.loads(content)

        except json.JSONDecodeError as exc:
            raise ValueError(
                "AI returned invalid JSON."
            ) from exc

    # =========================================================
    # Validation
    # =========================================================

    @staticmethod
    def _validate_payload(payload):
        if not isinstance(payload, dict):
            raise ValueError(
                "AI content must be a JSON object."
            )

        if not isinstance(
            payload.get("lesson"),
            dict,
        ):
            raise ValueError(
                "AI response is missing lesson."
            )

        if not payload["lesson"].get("title"):
            raise ValueError(
                "AI lesson title is required."
            )

        for field in (
            "learning_objectives",
            "key_concepts",
            "examples",
            "practical_instructions",
        ):
            if not isinstance(
                payload["lesson"].get(field, []),
                list,
            ):
                raise ValueError(
                    f"lesson.{field} must be a list."
                )

    @staticmethod
    def _truncate(value, limit):
        value = value or ""

        if len(value) <= limit:
            return value

        return value[:limit] + "\n...[truncated]"
