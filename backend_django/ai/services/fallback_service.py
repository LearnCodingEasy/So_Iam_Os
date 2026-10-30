"""Bounded fallback execution; only retries on provider failures."""
import logging
from ..exceptions import AIProviderError, AIResponseError
from .agent_executor import AgentExecutor
logger = logging.getLogger(__name__)

class FallbackService:
    def __init__(self, user=None, providers=None):
        self.user = user
        self.providers = list(providers or [])
    def execute(self, *, messages, model=None, temperature=None, max_tokens=None):
        if not self.providers:
            raise AIProviderError("No fallback providers are configured.")
        failures = []
        for name in self.providers[:3]:
            try:
                return AgentExecutor(self.user).execute(provider=name, messages=messages, model=model,
                    temperature=temperature, max_tokens=max_tokens)
            except (AIProviderError, AIResponseError) as exc:
                failures.append(name)
                logger.warning("AI provider %s failed; trying configured fallback (%s/%s)", name, len(failures), min(3, len(self.providers)))
        raise AIProviderError("All configured AI providers failed: " + ", ".join(failures))
