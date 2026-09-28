import json
import re
from django.db import transaction
from django.utils import timezone
from core.models import UserLearningSettings
from learning.models import LearningGoal, LearningTopic
from .models import Task

class DailyTaskGenerationService:
    def __init__(self, user):
        self.user = user

    def context(self):
        settings = UserLearningSettings.objects.select_related("current_learning_goal__skill").get(user=self.user)
        goal = settings.current_learning_goal
        if not goal:
            goal = LearningGoal.objects.filter(user=self.user, status=LearningGoal.Status.ACTIVE).select_related("skill").first()
        topics = LearningTopic.objects.filter(path__user=self.user, path__goal=goal).exclude(status=LearningTopic.Status.COMPLETED).select_related("path", "skill").order_by("order", "id")[:8] if goal else LearningTopic.objects.filter(path__user=self.user).exclude(status=LearningTopic.Status.COMPLETED).select_related("path", "skill").order_by("order", "id")[:8]
        existing = Task.objects.filter(user=self.user, scheduled_date=timezone.localdate()).exclude(status=Task.Status.CANCELLED).values_list("title", flat=True)
        recent = Task.objects.filter(user=self.user).order_by("-scheduled_date", "-created_at").values("title", "status")[:30]
        return settings, goal, list(topics), list(existing), list(recent)

    @transaction.atomic
    def generate(self, count=None, provider=None, model=None):
        settings, goal, topics, existing, recent = self.context()
        count = int(count or settings.daily_learning_tasks)
        count = max(1, min(10, count))
        if not settings.task_generation_enabled:
            return []
        candidates = self._ai_tasks(goal, topics, existing, recent, count, provider, model)
        if not candidates:
            candidates = self._fallback_tasks(goal, topics, count)
        created = []
        existing_normalized = {self._norm(x) for x in existing}
        for idx, item in enumerate(candidates):
            title = str(item.get("title", "")).strip()[:255]
            if not title or self._norm(title) in existing_normalized:
                continue
            topic = next((t for t in topics if t.id == item.get("learning_topic")), None)
            if topic is None and topics:
                topic = topics[min(idx, len(topics)-1)]
            task = Task.objects.create(
                user=self.user, learning_goal=goal, learning_path=topic.path if topic else None,
                learning_topic=topic, skill=(topic.skill if topic and topic.skill else getattr(goal, "skill", None)),
                title=title, description=str(item.get("description", ""))[:5000],
                scheduled_date=timezone.localdate(), estimated_minutes=max(5, min(240, int(item.get("estimated_minutes", getattr(topic, "estimated_minutes", 30) or 30)))),
                priority=item.get("priority", "medium") if item.get("priority") in {x[0] for x in Task.Priority.choices} else "medium",
                sort_order=idx, metadata={"generated_by": "daily_learning_ai", "goal_id": goal.id if goal else None, "topic_id": topic.id if topic else None}
            )
            created.append(task); existing_normalized.add(self._norm(title))
            if len(created) >= count: break
        return created

    def _ai_tasks(self, goal, topics, existing, recent, count, provider, model):
        try:
            from ai.providers import get_ai_provider
            from core.models import UserLearningSettings
            from ai.models import AISettings
            ai_settings = AISettings.objects.filter(user=self.user).first()
            provider_name = provider or (ai_settings.preferred_provider if ai_settings else "ollama")
            selected_model = model or (ai_settings.preferred_model if ai_settings else "")
            payload = {"goal": {"id": goal.id, "title": goal.title, "skill": goal.skill.name if goal.skill else None, "level": goal.current_level, "target": goal.target_level} if goal else None,
                       "topics": [{"id": t.id, "title": t.title, "description": t.description, "skill": t.skill.name if t.skill else None, "minutes": t.estimated_minutes} for t in topics],
                       "today_existing": existing, "recent_tasks": recent, "count": count}
            prompt = "Generate exactly the requested number of practical learning tasks. Return JSON only as {\\\"tasks\\\":[{\\\"title\\\":\\\"...\\\",\\\"description\\\":\\\"...\\\",\\\"estimated_minutes\\\":30,\\\"priority\\\":\\\"medium\\\",\\\"learning_topic\\\":123}]}. Never repeat existing or recent tasks. Base tasks on the goal, topics and progress context.\n" + json.dumps(payload, ensure_ascii=False, default=str)
            result = get_ai_provider(provider_name, user=self.user).generate(messages=[{"role":"system","content":"You are a precise learning task planner."},{"role":"user","content":prompt}], model=selected_model or None)
            text = result["content"].strip(); match = re.search(r"\{.*\}", text, re.S)
            data = json.loads(match.group(0) if match else text)
            return data.get("tasks", [])[:count]
        except Exception:
            return []

    def _fallback_tasks(self, goal, topics, count):
        result=[]
        templates=[("Study", "Read and summarize the core concepts."),("Practice", "Implement a focused exercise using the topic."),("Explain", "Explain the concept in your own words and record the key idea."),("Review", "Review the topic and identify one remaining knowledge gap."),("Apply", "Build a small practical example using the topic.")]
        for i in range(count):
            topic = topics[i % len(topics)] if topics else None
            verb, desc = templates[i % len(templates)]
            title = f"{verb}: {topic.title}" if topic else f"{verb}: {goal.title if goal else 'Learning'}"
            result.append({"title":title,"description":desc,"estimated_minutes":getattr(topic,"estimated_minutes",30) or 30,"priority":"medium","learning_topic":topic.id if topic else None})
        return result

    @staticmethod
    def _norm(value):
        return re.sub(r"\s+", " ", str(value).strip().lower())
