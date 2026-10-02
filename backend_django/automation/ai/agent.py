from openai import OpenAI
from pydantic import BaseModel
from typing import List

client = OpenAI()

class Action(BaseModel):
    action: str
    value: str | None = None

class AgentResponse(BaseModel):
    actions: List[Action]


SYSTEM_PROMPT = """
You are an automation agent.

Convert user instructions into automation actions.

Available actions:

open_program
hotkey
type_text
press

Examples:

User:
open vscode

Output:
{
 "actions":[
   {"action":"open_program","value":"vscode"}
 ]
}

User:
press ctrl shift p

Output:
{
 "actions":[
   {"action":"hotkey","value":"ctrl+shift+p"}
 ]
}
"""


def parse_prompt(prompt: str):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":SYSTEM_PROMPT},
            {"role":"user","content":prompt}
        ],
        response_format={"type": "json_object"}
    )

    return response.choices[0].message.content