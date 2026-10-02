import os

from openai import OpenAI


class OpenAIService:
    """
    OpenAI provider for Codex.

    The API key never reaches the Vue frontend.
    """

    DEFAULT_MODEL = os.getenv(
        "CODEX_OPENAI_MODEL",
        "gpt-5-mini",
    )

    SYSTEM_PROMPT = """
You are Codex, the engineering intelligence layer
of SO_IAM_OS.

You work on a real Django + Django REST Framework +
Vue 3 project.

IMPORTANT RULES:

1. Never invent project facts.

2. Never guess:
   - Django model names
   - serializers
   - API endpoints
   - URL routes
   - Vue components
   - frontend services
   - stores
   - file paths
   - database fields
   - upload mechanisms
   - storage configuration

3. Use only the supplied project context.

4. If information is not available, explicitly return:
   NOT_FOUND_IN_PROJECT_CONTEXT

5. First analyze.

6. Then identify affected files.

7. Then identify affected APIs.

8. Then identify database impact.

9. Then produce a safe change plan.

10. Do NOT execute code changes.

11. Execution requires explicit user approval
    through the Codex change workflow.

For every request, analyze:

- Feature
- Backend
- Frontend
- APIs
- Database
- Files
- Routes
- Dependencies
- Impact
- Risks
- Validation
- Change plan

Return structured JSON whenever possible.
"""

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not configured."
            )

        self.client = OpenAI(api_key=api_key)

    def analyze(
        self,
        *,
        request,
        project_context,
        user=None,
    ):
        user_context = (
            f"Authenticated user id: {user.pk}"
            if user and user.is_authenticated
            else "Anonymous user"
        )

        prompt = f"""
PROJECT CONTEXT
===============

{project_context}


USER
====

{user_context}


REQUEST
=======

{request}


Return a structured engineering analysis.

Required structure:

{{
  "request": {{
    "summary": "",
    "goal": ""
  }},
  "feature": {{
    "name": "",
    "found": false
  }},
  "backend": {{
    "model": "",
    "serializer": "",
    "view": "",
    "endpoint": "",
    "upload_field": "",
    "storage": ""
  }},
  "frontend": {{
    "page": "",
    "service": "",
    "store": "",
    "route": ""
  }},
  "database": {{
    "migration_required": false,
    "reason": ""
  }},
  "affected_files": [],
  "affected_apis": [],
  "risks": [],
  "validation": [],
  "plan": [],
  "unknowns": []
}}
"""

        response = self.client.responses.create(
            model=self.DEFAULT_MODEL,
            instructions=self.SYSTEM_PROMPT,
            input=prompt,
            safety_identifier=(
                str(user.pk)
                if user and user.is_authenticated
                else None
            ),
        )

        return response.output_text
