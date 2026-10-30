"""Build a reviewable task proposal; intentionally does not write tasks."""
from typing import Any
class TaskPlanner:
    @staticmethod
    def proposal(*, title: str, description: str = "", steps: list[str] | None = None,
                 priority: str = "medium", due_date: str | None = None) -> dict[str, Any]:
        clean_title = (title or "").strip()
        if not clean_title:
            raise ValueError("Task title is required.")
        return {"title": clean_title[:255], "description": description.strip(),
                "priority": priority if priority in {"low", "medium", "high", "urgent"} else "medium",
                "due_date": due_date, "steps": [str(x).strip() for x in (steps or []) if str(x).strip()],
                "requires_confirmation": True, "status": "proposal"}
