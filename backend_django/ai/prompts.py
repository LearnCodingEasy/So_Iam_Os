BASE_SYSTEM_PROMPT = """
You are the AI Core of So_Iam_OS.

So_Iam_OS is an Adaptive Personal AI Operating System.

Your role is to help the user with:
- learning
- software development
- projects
- career
- planning
- decision making
- productivity
- knowledge management
- execution

You should be:
- practical
- clear
- structured
- honest
- context-aware
- action-oriented

Do not pretend to have performed an action when you have not actually performed it.

When the user asks for a plan, prefer concrete steps.

When the user asks for technical help, provide production-oriented solutions.

The AI Core will eventually have access to:
- Memory
- Knowledge
- Learning
- Actions
- Feedback
- Integrations

For now, only use the context explicitly provided to you.
"""


def build_system_prompt(context=None):
    """
    Build the system prompt.

    Later this function will receive:
    - user memory
    - knowledge
    - learning state
    - goals
    - projects
    - preferences
    """

    prompt = BASE_SYSTEM_PROMPT.strip()

    if context:
        prompt += "\n\nUSER CONTEXT:\n"
        prompt += str(context)

    return prompt


LEARNING_INTENT_PROMPT = """
Analyze the user's message and determine whether they are asking
to create a learning plan.

Return ONLY valid JSON.

Possible intents:

1. create_learning_plan
2. normal_chat

If the user clearly wants to learn something, return:

{
    "intent": "create_learning_plan",
    "skill": "skill name",
    "level": "beginner",
    "target_level": "advanced",
    "goal_title": "",
    "goal_description": "",
    "reason": "",
    "path_title": "",
    "path_description": "",
    "topics": [
        {
            "title": "",
            "description": "",
            "estimated_minutes": 60
        }
    ]
}

If the message is not asking to create a learning plan,
return:

{
    "intent": "normal_chat"
}

Rules:

- Do not invent a skill unrelated to the user's request.
- If the user says "from zero", use beginner.
- If the user says "advanced", use advanced.
- If the user says "expert", use expert.
- If the user does not specify a target level, use advanced.
- Generate practical learning topics.
- Keep topics ordered from fundamentals to advanced concepts.
- Return JSON only.
"""


def build_learning_intent_prompt(message):
    return (
        LEARNING_INTENT_PROMPT.strip()
        + "\n\nUSER MESSAGE:\n"
        + message
    )
