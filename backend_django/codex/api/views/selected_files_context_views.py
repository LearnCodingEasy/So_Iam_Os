from pathlib import Path
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.response import Response
from codex.permissions import CodexAuthenticated
from codex.models import ProjectRegistry


class SelectedFilesContextView(APIView):
    permission_classes = [CodexAuthenticated]

    def post(self, request):
        project = ProjectRegistry.objects.get_or_create(
            key="so_iam_os", defaults={"name": "SO_IAM_OS"})[0]
        root = Path(project.root_path or Path(
            settings.BASE_DIR).parent).resolve()
        paths = request.data.get("paths") or []
        if not isinstance(paths, list):
            return Response({"detail": "paths must be a list."}, status=400)
        rows, total = [], 0
        for rel in paths[:20]:
            try:
                target = (root / str(rel).replace("\\", "/")).resolve()
                if root not in target.parents or not target.is_file():
                    continue
                content = target.read_text(encoding="utf-8", errors="ignore")
                remaining = max(0, 120_000 - total)
                content = content[:remaining]
                rows.append({"path": target.relative_to(
                    root).as_posix(), "content": content})
                total += len(content)
                if total >= 120_000:
                    break
            except (OSError, UnicodeError):
                continue
        return Response({"files": rows, "total_chars": total, "limit_chars": 120000})
