"""User-scoped prompt profile CRUD helpers."""
from ..models import AIPromptProfile
class PromptTemplateService:
    @staticmethod
    def list_for_user(user):
        return AIPromptProfile.objects.filter(user=user).order_by("name")
    @staticmethod
    def create(*, user, name, system_prompt, context_instructions="", temperature=0.7, max_tokens=2048):
        if not name or not name.strip() or not system_prompt or not system_prompt.strip():
            raise ValueError("Name and system prompt are required.")
        return AIPromptProfile.objects.create(user=user, name=name.strip()[:120],
            system_prompt=system_prompt, context_instructions=context_instructions,
            temperature=temperature, max_tokens=max_tokens)
