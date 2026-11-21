import json
import re

from django.utils.dateparse import parse_date, parse_datetime


class GoalCoachService:
    """Uses the project's configured AI fallback service; never mutates goal data."""

    @staticmethod
    def propose_plan(goal, user, instructions=""):
        from ai.services import AIFallbackChainService
        from ai.models import AISettings

        preferences = AISettings.objects.filter(user=user).first()
        preferred = getattr(preferences, "preferred_provider", None)
        goal_context = {
            "linked_tasks": list(goal.tasks.values("id", "title", "status", "scheduled_date", "due_at", "estimated_minutes")[:30]),
            "milestones": list(goal.milestones.values("id", "title", "status", "progress_percent", "target_date", "weight")[:20]),
            "learning_goals": list(goal.learning_goals.values("id", "title", "status", "target_date")[:20]),
            "projects": list(goal.project_links.select_related("project").values("project__id", "project__title", "project__status")[:10]),
        }
        if preferences and preferences.context_enabled:
            from ai.services import AIContextBuilder
            user_context = AIContextBuilder(user).build()
            goal_context["authorized_user_context"] = {
                "knowledge": user_context.get("knowledge", [])[:5],
                "learning_paths": user_context.get("learning_paths", [])[:10],
                "memory": user_context.get("memory", [])[:10],
            }
        prompt = f"""You are the SO_IAM_OS Goal Coach. Return ONLY valid JSON (no markdown).
Create an actionable SMART execution plan for the user's goal. Do not claim certainty.
Schema: {{"summary":"string","success_criteria":["string"],"risks":["string"],"resources":["string"],"milestones":[{{"title":"string","description":"string","start_date":"YYYY-MM-DD or null","target_date":"YYYY-MM-DD or null","weight":0,"completion_criteria":"string","tasks":[{{"title":"string","description":"string","scheduled_date":"YYYY-MM-DD or null","due_at":"ISO datetime or null","priority":"low|medium|high|critical","estimated_minutes":0}}]}}]}}
Rules: use 2-8 milestones; weights must total at most 100; do not create or execute tasks; this is a proposal only. Use dates consistent with the goal dates. Return valid JSON.
Goal: {json.dumps({'title': goal.title, 'description': goal.description, 'category': goal.category, 'priority': goal.priority, 'start_date': str(goal.start_date), 'target_date': str(goal.target_date) if goal.target_date else None, 'measurement_unit': goal.measurement_unit, 'initial_value': str(goal.initial_value) if goal.initial_value is not None else None, 'target_value': str(goal.target_value) if goal.target_value is not None else None}, ensure_ascii=False)}
Existing goal execution context (use only to improve the proposal; do not change it): {json.dumps(goal_context, ensure_ascii=False, default=str)[:14000]}
Additional user guidance: {instructions[:4000]}
"""
        result = AIFallbackChainService.generate_completion(
            messages=[
                {"role": "system", "content": "You are the SO_IAM_OS Goal Coach. Return strict JSON only."},
                {"role": "user", "content": prompt},
            ],
            user=user,
            preferred_provider=preferred,
            temperature=0.3,
            max_tokens=5000,
        )
        content = result.get("content", "")
        match = re.search(r"\{.*\}", content, re.S)
        if not match:
            raise ValueError("AI provider did not return a valid JSON plan.")
        payload = json.loads(match.group(0))
        milestones = payload.get("milestones")
        if not isinstance(milestones, list) or not 1 <= len(milestones) <= 12:
            raise ValueError("AI plan must contain between 1 and 12 milestones.")
        total_weight = sum(float(item.get("weight", 0) or 0) for item in milestones if isinstance(item, dict))
        if total_weight > 100:
            raise ValueError("AI plan milestone weights exceed 100.")
        from tasks.models import Task
        for item in milestones:
            if not isinstance(item, dict) or not str(item.get("title", "")).strip():
                raise ValueError("AI plan contains an invalid milestone.")
            try:
                weight = float(item.get("weight", 0) or 0)
            except (TypeError, ValueError) as exc:
                raise ValueError("AI plan contains an invalid milestone weight.") from exc
            if not 0 <= weight <= 100:
                raise ValueError("Milestone weights must be between 0 and 100.")
            start_date = item.get("start_date")
            target_date = item.get("target_date")
            if start_date and not parse_date(start_date):
                raise ValueError("AI plan contains an invalid milestone start date.")
            if target_date and not parse_date(target_date):
                raise ValueError("AI plan contains an invalid milestone target date.")
            if start_date and target_date and parse_date(target_date) < parse_date(start_date):
                raise ValueError("A milestone deadline cannot precede its start date.")
            tasks = item.get("tasks", [])
            if not isinstance(tasks, list):
                raise ValueError("AI plan contains an invalid task list.")
            for task in tasks:
                if not isinstance(task, dict) or not str(task.get("title", "")).strip():
                    raise ValueError("AI plan contains a task without a title.")
                if task.get("priority", Task.Priority.MEDIUM) not in Task.Priority.values:
                    raise ValueError("AI plan contains an invalid task priority.")
                if task.get("scheduled_date") and not parse_date(task["scheduled_date"]):
                    raise ValueError("AI plan contains an invalid task date.")
                if task.get("due_at") and not parse_datetime(task["due_at"]):
                    raise ValueError("AI plan contains an invalid task deadline.")
                try:
                    minutes = int(task.get("estimated_minutes", 0) or 0)
                except (TypeError, ValueError) as exc:
                    raise ValueError("AI plan contains invalid task duration.") from exc
                if minutes < 0:
                    raise ValueError("Task duration cannot be negative.")
        return payload, result.get("provider", "")
    @staticmethod
    def answer(goal, user, message):
        from ai.services import AIFallbackChainService
        from ai.models import AISettings

        preferences = AISettings.objects.filter(user=user).first()
        context = {
            "goal": {"id": goal.id, "title": goal.title, "description": goal.description,
                     "status": goal.status, "progress_percent": goal.progress_percent,
                     "target_date": str(goal.target_date) if goal.target_date else None},
            "tasks": list(goal.tasks.values("title", "status", "scheduled_date", "due_at")[:25]),
            "milestones": list(goal.milestones.values("title", "status", "progress_percent", "target_date", "weight")[:15]),
        }
        if preferences and preferences.context_enabled:
            from ai.services import AIContextBuilder
            user_context = AIContextBuilder(user).build()
            context["learning"] = user_context.get("learning_goals", [])[:10]
            context["memory"] = user_context.get("memory", [])[:10]
            context["knowledge"] = user_context.get("knowledge", [])[:5]
        result = AIFallbackChainService.generate_completion(
            messages=[
                {"role": "system", "content": "You are the SO_IAM_OS Goal Coach. Analyze only the supplied authorized context. Give practical, evidence-based advice. Never claim to have changed data or executed actions. Clearly distinguish facts from estimates."},
                {"role": "user", "content": f"Goal context: {json.dumps(context, ensure_ascii=False, default=str)[:12000]}\nQuestion: {message[:4000]}"},
            ],
            user=user,
            preferred_provider=getattr(preferences, "preferred_provider", None),
            temperature=0.4,
            max_tokens=2500,
        )
        return {"content": result.get("content", ""), "provider": result.get("provider", ""), "model": result.get("model", "")}



