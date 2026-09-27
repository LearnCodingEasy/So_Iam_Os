from django.db import transaction
from django.utils.text import slugify

from learning.models import (
    Skill,
    LearningGoal,
    LearningPath,
    LearningTopic,
)
from learning.services import LearningService


import json
import re

from ai.exceptions import AIResponseError
from ai.providers import get_ai_provider
from ai.prompts import build_learning_intent_prompt
from ai.serializers import AILearningPlanSerializer


LEARNING_PATTERNS = [
    r"\bعايز\s+أتعلم\b",
    r"\bعايز\s+اتعلم\b",
    r"\bاريد\s+تعلم\b",
    r"\bأريد\s+تعلم\b",
    r"\bنفسي\s+اتعلم\b",
    r"\bنفسي\s+أتعلم\b",
    r"\bحابب\s+اتعلم\b",
    r"\bحابب\s+أتعلم\b",
    r"\bمحتاج\s+اتعلم\b",
    r"\bمحتاج\s+أتعلم\b",

    r"\bi\s+want\s+to\s+learn\b",
    r"\bi'd\s+like\s+to\s+learn\b",
    r"\bi\s+would\s+like\s+to\s+learn\b",
    r"\bteach\s+me\b",
]


def looks_like_learning_request(message):
    if not message:
        return False

    normalized = " ".join(
        message.strip().split()
    ).lower()

    return any(
        re.search(
            pattern,
            normalized,
            flags=re.IGNORECASE,
        )
        for pattern in LEARNING_PATTERNS
    )


def extract_learning_skill(message):
    """
    Extract the skill after common learning phrases.

    Examples:
        عايز أتعلم Django
        عايز اتعلم Python
        I want to learn Django
    """

    if not message:
        return ""

    text = " ".join(
        message.strip().split()
    )

    patterns = [
        r"عايز\s+أتعلم\s+(.+)",
        r"عايز\s+اتعلم\s+(.+)",
        r"اريد\s+تعلم\s+(.+)",
        r"أريد\s+تعلم\s+(.+)",
        r"نفسي\s+اتعلم\s+(.+)",
        r"نفسي\s+أتعلم\s+(.+)",
        r"حابب\s+اتعلم\s+(.+)",
        r"حابب\s+أتعلم\s+(.+)",
        r"محتاج\s+اتعلم\s+(.+)",
        r"محتاج\s+أتعلم\s+(.+)",
        r"i\s+want\s+to\s+learn\s+(.+)",
        r"i'd\s+like\s+to\s+learn\s+(.+)",
        r"i\s+would\s+like\s+to\s+learn\s+(.+)",
        r"teach\s+me\s+(.+)",
    ]

    skill = ""

    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if match:
            skill = match.group(1)
            break

    if not skill:
        return ""

    # Remove common trailing context.
    skill = re.split(
        r"\s+(?:من\s+الصفر|من\s+البداية|للعمل|عشان|لكي|for|from|starting)\b",
        skill,
        maxsplit=1,
        flags=re.IGNORECASE,
    )[0]

    skill = skill.strip(
        " \t\n\r.,!?؟:؛،"
    )

    # Remove common Arabic prefixes.
    skill = re.sub(
        r"^(لغة|مهارة|تكنولوجيا|تقنية|الـ)\s+",
        "",
        skill,
        flags=re.IGNORECASE,
    )

    return skill.strip()


class AILearningActionService:
    """
    Executes structured learning actions requested through AI.

    Flow:
        AI Intent
            ↓
        Skill
            ↓
        Learning Goal
            ↓
        Learning Path
            ↓
        Learning Topics
    """

    def __init__(self, user):
        self.user = user

    @staticmethod
    def generate_ai_plan(*, message, provider="ollama", model="", user=None):
        """Generate and validate a complete learning plan with the configured LLM."""
        prompt = build_learning_intent_prompt(message)
        ai_provider = get_ai_provider(provider or "ollama", user=user)

        result = ai_provider.generate(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You generate structured learning plans for So_Iam_OS. "
                        "Return ONLY one valid JSON object. No markdown, no explanation. "
                        "Generate 6 to 15 ordered practical topics. "
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            model=model or None,
        )

        content = (result.get("content") or "").strip()
        if not content:
            raise AIResponseError("AI returned an empty learning plan.")

        # Accept fenced JSON and recover a JSON object if the model added prose.
        if content.startswith("```"):
            content = re.sub(r"^```(?:json)?\s*", "", content, flags=re.I)
            content = re.sub(r"\s*```$", "", content)

        start = content.find("{")
        end = content.rfind("}")
        if start < 0 or end <= start:
            raise AIResponseError("AI did not return a JSON learning plan.")

        try:
            raw = json.loads(content[start:end + 1])
        except json.JSONDecodeError as exc:
            raise AIResponseError(
                f"AI returned invalid learning-plan JSON: {exc}"
            ) from exc

        if raw.get("intent") != "create_learning_plan":
            raise AIResponseError("AI did not return a learning-plan intent.")

        serializer = AILearningPlanSerializer(data=raw)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)

        topics = list(data.get("topics") or [])
        if not topics:
            raise AIResponseError(
                "AI returned a learning plan without topics.")

        # Never trust duplicate/invalid ordering from the model.
        for index, topic in enumerate(topics, start=1):
            topic["order"] = index

        data["topics"] = topics
        data["provider"] = result.get("provider")
        data["model"] = result.get("model")
        return data

    @staticmethod
    def generate_topics(skill_name):
        """
        Deterministic starter curriculum.

        We intentionally keep this local for now instead of trusting
        arbitrary LLM-generated JSON.
        """

        normalized = skill_name.strip().lower()

        if normalized == "django":
            return [
                {
                    "title": "Django Fundamentals",
                    "description": "Understand Django architecture, MTV, projects, and apps.",
                    "estimated_minutes": 90,
                },
                {
                    "title": "Django Project Setup",
                    "description": "Create a Django project, configure settings, and manage environments.",
                    "estimated_minutes": 90,
                },
                {
                    "title": "URLs and Views",
                    "description": "Learn URL routing, function-based views, and class-based views.",
                    "estimated_minutes": 120,
                },
                {
                    "title": "Templates",
                    "description": "Build dynamic pages using Django templates and template inheritance.",
                    "estimated_minutes": 90,
                },
                {
                    "title": "Models and ORM",
                    "description": "Work with models, migrations, QuerySets, relationships, and the Django ORM.",
                    "estimated_minutes": 180,
                },
                {
                    "title": "Forms and Authentication",
                    "description": "Handle forms, validation, authentication, permissions, and user accounts.",
                    "estimated_minutes": 150,
                },
                {
                    "title": "Django REST Framework",
                    "description": "Build APIs using serializers, views, routers, authentication, and permissions.",
                    "estimated_minutes": 180,
                },
                {
                    "title": "Testing Django Applications",
                    "description": "Write tests for models, views, APIs, authentication, and business logic.",
                    "estimated_minutes": 120,
                },
                {
                    "title": "Production and Deployment",
                    "description": "Prepare a Django application for production and deployment.",
                    "estimated_minutes": 150,
                },
            ]

        if normalized == "python":
            return [
                {
                    "title": "Python Fundamentals",
                    "description": "Variables, types, operators, conditions, and loops.",
                    "estimated_minutes": 120,
                },
                {
                    "title": "Functions",
                    "description": "Functions, parameters, return values, scope, and reusable code.",
                    "estimated_minutes": 120,
                },
                {
                    "title": "Data Structures",
                    "description": "Lists, tuples, sets, dictionaries, and practical usage.",
                    "estimated_minutes": 150,
                },
                {
                    "title": "Object-Oriented Programming",
                    "description": "Classes, objects, inheritance, composition, and abstraction.",
                    "estimated_minutes": 180,
                },
                {
                    "title": "Modules and Packages",
                    "description": "Imports, packages, virtual environments, and dependency management.",
                    "estimated_minutes": 120,
                },
                {
                    "title": "Files and Exceptions",
                    "description": "File handling, exceptions, context managers, and robust programs.",
                    "estimated_minutes": 120,
                },
                {
                    "title": "Testing",
                    "description": "Unit testing and writing maintainable Python applications.",
                    "estimated_minutes": 120,
                },
                {
                    "title": "Practical Python Project",
                    "description": "Apply the learned concepts in a complete practical project.",
                    "estimated_minutes": 240,
                },
            ]

        return [
            {
                "title": f"{skill_name} Fundamentals",
                "description": f"Understand the fundamental concepts of {skill_name}.",
                "estimated_minutes": 120,
            },
            {
                "title": f"{skill_name} Setup and Environment",
                "description": f"Set up the tools and environment required for {skill_name}.",
                "estimated_minutes": 90,
            },
            {
                "title": f"{skill_name} Core Concepts",
                "description": f"Learn the main concepts and building blocks of {skill_name}.",
                "estimated_minutes": 150,
            },
            {
                "title": f"{skill_name} Practical Application",
                "description": f"Apply {skill_name} through practical exercises.",
                "estimated_minutes": 180,
            },
            {
                "title": f"{skill_name} Intermediate Concepts",
                "description": f"Move from fundamentals into intermediate {skill_name} concepts.",
                "estimated_minutes": 180,
            },
            {
                "title": f"{skill_name} Advanced Concepts",
                "description": f"Study advanced concepts and production-oriented practices.",
                "estimated_minutes": 180,
            },
            {
                "title": f"{skill_name} Testing and Debugging",
                "description": f"Learn how to test and debug {skill_name} applications.",
                "estimated_minutes": 120,
            },
            {
                "title": f"{skill_name} Practical Project",
                "description": f"Build a complete project using {skill_name}.",
                "estimated_minutes": 240,
            },
        ]

    @transaction.atomic
    def create_learning_plan(
        self,
        *,
        skill_name,
        level="beginner",
        target_level="advanced",
        goal_title=None,
        goal_description="",
        reason="",
        path_title=None,
        path_description="",
        topics=None,
    ):
        skill_name = (skill_name or "").strip()

        if not skill_name:
            raise ValueError("skill_name is required.")

        valid_levels = {
            Skill.Level.BEGINNER,
            Skill.Level.INTERMEDIATE,
            Skill.Level.ADVANCED,
            Skill.Level.EXPERT,
        }

        if level not in valid_levels:
            level = Skill.Level.BEGINNER

        if target_level not in valid_levels:
            target_level = Skill.Level.ADVANCED

        slug = slugify(skill_name)

        if not slug:
            raise ValueError("Could not generate a valid skill slug.")

        skill, _ = Skill.objects.get_or_create(
            slug=slug,
            defaults={
                "name": skill_name,
                "description": f"Learning skill: {skill_name}",
                "category": "AI Generated",
                "is_active": True,
            },
        )

        if not skill.is_active:
            skill.is_active = True
            skill.save(
                update_fields=[
                    "is_active",
                    "updated_at",
                ]
            )

        # Prevent duplicate active goals.
        goal = (
            LearningGoal.objects
            .filter(
                user=self.user,
                skill=skill,
                status=LearningGoal.Status.ACTIVE,
            )
            .order_by("-created_at")
            .first()
        )

        if goal:
            path = (
                LearningPath.objects
                .filter(
                    user=self.user,
                    goal=goal,
                )
                .order_by("-created_at")
                .first()
            )

            if not path:
                path = LearningService.create_path(
                    user=self.user,
                    goal=goal,
                    title=path_title or f"{skill.name} Learning Path",
                    description=(
                        path_description
                        or f"A structured learning path for {skill.name}."
                    ),
                )

            existing_topics = list(
                LearningTopic.objects
                .filter(path=path)
                .order_by("order", "id")
            )

            if not existing_topics:
                existing_topics = self._create_topics(
                    path=path,
                    skill=skill,
                    topics=topics,
                )

            return {
                "created": False,
                "skill": skill,
                "goal": goal,
                "path": path,
                "topics": existing_topics,
            }

        goal = LearningGoal.objects.create(
            user=self.user,
            title=goal_title or f"Learn {skill.name}",
            description=(
                goal_description
                or f"Learn {skill.name} from {level} to {target_level}."
            ),
            skill=skill,
            reason=reason,
            current_level=level,
            target_level=target_level,
        )

        path = LearningService.create_path(
            user=self.user,
            goal=goal,
            title=path_title or f"{skill.name} Learning Path",
            description=(
                path_description
                or f"A structured learning path for {skill.name}."
            ),
        )

        topics = list(topics or [])
        if not topics:
            raise ValueError("Learning plan must contain at least one topic.")

        created_topics = self._create_topics(
            path=path,
            skill=skill,
            topics=topics,
        )

        return {
            "created": True,
            "skill": skill,
            "goal": goal,
            "path": path,
            "topics": created_topics,
        }

    def _create_topics(self, *, path, skill, topics):
        created_topics = []

        for index, topic in enumerate(topics, start=1):
            if isinstance(topic, str):
                topic = {
                    "title": topic,
                }

            title = str(
                topic.get("title", "")
            ).strip()

            if not title:
                continue

            created_topic = LearningService.create_topic(
                user=self.user,
                path=path,
                title=title[:255],
                description=str(
                    topic.get("description", "")
                ),
                skill=skill,
                order=index,
                difficulty=str(topic.get("difficulty", "")).strip()[:20],
                estimated_minutes=max(
                    0,
                    int(
                        topic.get(
                            "estimated_minutes",
                            0,
                        )
                    ),
                ),
            )

            created_topics.append(created_topic)

        return created_topics
