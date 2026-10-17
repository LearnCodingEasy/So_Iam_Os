"""AI planning adapter for Automation.

Uses the project's central AI provider router when a user is available. The legacy
OpenAI fallback is retained only for backwards compatibility with standalone scripts.
"""
import json
from typing import List
from pydantic import BaseModel

class Action(BaseModel):
    action: str
    value: str | None = None

class AgentResponse(BaseModel):
    actions: List[Action]

SYSTEM_PROMPT = """You are the SO_IAM_OS automation planning layer. Convert user instructions into a JSON object with an 'actions' array. Only choose actions that the existing automation engine can validate. Never execute actions. Supported examples: open_program, hotkey, type_text, press, delay, notification, http, condition. If an action would require shell, filesystem, network, database or credentials, mark it as requiring permission instead of bypassing the permission system."""

def parse_prompt(prompt: str, user=None):
    messages = SYSTEM_PROMPT + "\nReturn JSON only. User request:\n" + prompt
    if user is not None:
        from ai.services import AIService
        result = AIService(user).chat(messages)
        raw = result["assistant_message"].content
    else:
        try:
            from openai import OpenAI
            raw = OpenAI().chat.completions.create(model="gpt-4o-mini", messages=[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":prompt}], response_format={"type":"json_object"}).choices[0].message.content
        except Exception as exc:
            raise RuntimeError("No central AI user context or legacy OpenAI configuration is available.") from exc
    data = json.loads(raw)
    return AgentResponse(**data).model_dump()
