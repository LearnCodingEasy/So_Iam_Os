import hashlib
import json
import tempfile
from pathlib import Path
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import patch

from codex.services import build_workspace


class BuildWorkspaceSafetyTests(TestCase):
    def test_safe_path_rejects_traversal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            with self.assertRaises(ValueError):
                build_workspace.safe_path(root, '../outside.txt')

    def test_build_graph_never_calls_file_presence_execution_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for rel in ('README.md', 'requirements.txt', 'backend_django/manage.py',
                        'backend_django/backend_django/settings.py',
                        'frontend_vue/package.json', 'frontend_vue/src'):
                p = root / rel
                p.mkdir(parents=True, exist_ok=True) if rel.endswith('/src') else p.parent.mkdir(parents=True, exist_ok=True)
                if not rel.endswith('/src'):
                    p.write_text('{}', encoding='utf-8')
            project = SimpleNamespace(name='test-project', root_path=str(root))
            with patch.object(build_workspace.ProtectedItem.objects, 'filter') as filter_mock:
                filter_mock.return_value = []
                graph = build_workspace.build_graph(project)
            for node in graph['nodes'][:len(build_workspace.STAGES)]:
                self.assertEqual(node['data']['progress'], 0)
                self.assertFalse(node['data']['execution_verified'])
                self.assertNotEqual(node['data']['status'], 'completed')

    def test_root_discovery_finds_repository_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/'backend_django'/'backend_django').mkdir(parents=True)
            (root/'backend_django'/'manage.py').write_text('', encoding='utf-8')
            (root/'frontend_vue').mkdir()
            (root/'frontend_vue'/'package.json').write_text('{}', encoding='utf-8')
            project = SimpleNamespace(root_path='')
            with patch.object(build_workspace.settings, 'BASE_DIR', root/'backend_django'/'backend_django'):
                self.assertEqual(build_workspace.root_for(project), root.resolve())

class BuildWorkspaceURLContractTests(TestCase):
    """The public Build endpoint must remain registered at project URL level."""

    def test_public_workspace_route_is_resolvable(self):
        from django.urls import resolve
        match = resolve('/api/codex/build/workspace/')
        self.assertEqual(match.url_name, 'codex-build-workspace')
        self.assertEqual(match.func.view_class.__name__, 'BuildWorkspaceView')

    def test_public_manifest_route_is_resolvable(self):
        from django.urls import resolve
        match = resolve('/api/codex/build/manifest/')
        self.assertEqual(match.url_name, 'codex-build-manifest')
        self.assertEqual(match.func.view_class.__name__, 'BuildManifestView')
