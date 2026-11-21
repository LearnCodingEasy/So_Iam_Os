from pathlib import Path
from codex.models import FileRegistry
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.response import Response
from codex.models import FileRegistry
from codex.api.views.capability_registry_mixin_views import CapabilityRegistryMixin


class FileContentView(CapabilityRegistryMixin, APIView):
    def get(self, request, file_id):
        project = self.project()
        try:
            record = FileRegistry.objects.get(project=project, id=file_id)
        except FileRegistry.DoesNotExist:
            return Response({'detail': 'File not found.'}, status=404)
        root = Path(project.root_path or Path(
            settings.BASE_DIR).parent).resolve()
        target = (root/record.path).resolve()
        if root not in target.parents or not target.is_file():
            return Response({'detail': 'File is outside the allowed project root or does not exist.'}, status=403)
        if target.stat().st_size > 2_000_000:
            return Response({'detail': 'File is larger than the Codex viewer limit.', 'size': target.stat().st_size}, status=413)
        try:
            content = target.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            return Response({'detail': 'Binary file preview is not supported by the text viewer.'}, status=415)
        suffix = target.suffix.lower().lstrip('.') or 'text'
        return Response({'id': record.id, 'path': record.path, 'kind': record.kind, 'size': target.stat().st_size, 'language': suffix, 'content': content})
