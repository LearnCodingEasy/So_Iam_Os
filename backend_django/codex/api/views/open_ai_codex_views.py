import json
from pathlib import Path
from codex.services.openai_service import OpenAIService
from codex.services.project_context import ProjectContextService
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.response import Response
from codex.permissions import CodexAuthenticated
from codex.models import ProjectRegistry


class OpenAICodexView(APIView):
    permission_classes = [CodexAuthenticated]

    def post(self, request):

        message = str(
            request.data.get("message", "")
        ).strip()
        selected_paths = request.data.get("paths") or []
        if not isinstance(selected_paths, list):
            selected_paths = []

        if not message:
            return Response(
                {
                    "detail": "message is required."
                },
                status=400,
            )

        project = ProjectRegistry.objects.get(
            key="so_iam_os"
        )

        context = ProjectContextService(
            project=project
        ).build_context(message)
        # Multi-file Codex context: bounded, path-safe, read-only source payload.
        if selected_paths:
            root = Path(project.root_path or Path(
                settings.BASE_DIR).parent).resolve()
            selected_context = []
            total_chars = 0
            for rel in selected_paths[:20]:
                try:
                    target = (root / str(rel).replace("\\", "/")).resolve()
                    if root not in target.parents or not target.is_file():
                        continue
                    content = target.read_text(
                        encoding="utf-8", errors="ignore")
                    remaining = max(0, 120_000 - total_chars)
                    content = content[:remaining]
                    selected_context.append(
                        {"path": target.relative_to(root).as_posix(), "content": content})
                    total_chars += len(content)
                    if total_chars >= 120_000:
                        break
                except (OSError, UnicodeError):
                    continue
            context["selected_files"] = selected_context

        conversation = CodexConversation.objects.create(
            project=project,
            user=request.user,
            title=message[:240],
            provider="openai",
        )

        CodexMessage.objects.create(
            conversation=conversation,
            role="user",
            content=message,
        )

        try:

            raw_result = OpenAIService().analyze(
                request=message,
                project_context=json.dumps(
                    context,
                    ensure_ascii=False,
                    indent=2,
                ),
                user=request.user,
            )

        except Exception as exc:

            return Response(
                {
                    "provider": "openai",
                    "success": False,
                    "detail": str(exc),
                },
                status=502,
            )

        result = self._parse_json(raw_result)

        CodexMessage.objects.create(
            conversation=conversation,
            role="assistant",
            content=raw_result,
        )

        analysis = CodexAnalysis.objects.create(
            conversation=conversation,
            request=message,
            provider="openai",
            result=result,
            context=context,
        )

        return Response(
            {
                "success": True,
                "provider": "openai",
                "conversation_id": conversation.id,
                "analysis_id": analysis.id,
                "context": context,
                "result": result,
                "raw": raw_result,
            }
        )

    @staticmethod
    def _parse_json(value):

        try:
            return json.loads(value)

        except (TypeError, json.JSONDecodeError):

            return {
                "type": "text",
                "content": value,
            }
