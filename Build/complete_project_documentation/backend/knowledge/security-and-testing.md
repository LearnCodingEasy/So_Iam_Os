# knowledge security and testing

## Permission/ownership evidence

- knowledge/api/views/knowledge_file_views.py:L11: from rest_framework.permissions import IsAuthenticated
- knowledge/api/views/knowledge_file_views.py:L29: Files are always scoped through their KnowledgeItem owner.
- knowledge/api/views/knowledge_file_views.py:L32: permission_classes = [
- knowledge/api/views/knowledge_file_views.py:L33: IsAuthenticated,
- knowledge/api/views/knowledge_file_views.py:L48: def get_queryset(self):
- knowledge/api/views/knowledge_file_views.py:L52: knowledge__user=self.request.user,
- knowledge/api/views/knowledge_file_views.py:L80: if knowledge.user_id != self.request.user.id:
- knowledge/api/views/knowledge_file_views.py:L125: != self.request.user.id
- knowledge/api/views/knowledge_file_views.py:L140: != self.request.user.id
- knowledge/api/views/knowledge_item_views.py:L12: from rest_framework.permissions import IsAuthenticated
- knowledge/api/views/knowledge_item_views.py:L38: permission_classes = [
- knowledge/api/views/knowledge_item_views.py:L39: IsAuthenticated,
- knowledge/api/views/knowledge_item_views.py:L54: def get_queryset(self):
- knowledge/api/views/knowledge_item_views.py:L72: user=self.request.user,
- knowledge/api/views/knowledge_item_views.py:L100: user=self.request.user,
- knowledge/api/views/knowledge_item_views.py:L162: user=self.request.user
- knowledge/api/views/knowledge_item_views.py:L172: if instance.user_id != self.request.user.id:
- knowledge/api/views/knowledge_item_views.py:L184: if instance.user_id != self.request.user.id:
- knowledge/api/views/knowledge_item_views.py:L235: user=request.user,
- knowledge/api/views/knowledge_item_views.py:L263: user=request.user,
- knowledge/api/views/knowledge_item_views.py:L326: user=request.user,
- knowledge/api/views/knowledge_item_views.py:L400: user=request.user,
- knowledge/api/views/knowledge_item_views.py:L485: user=request.user,
- knowledge/api/views/knowledge_item_views.py:L547: queryset = self.get_queryset()


## Tests
- knowledge/tests/test_api.py
- knowledge/tests/test_file_validation.py
- knowledge/tests/test_metadata_extractor.py
- knowledge/tests/__init__.py


Tests were not run. This scan is not a complete authorization/security review. Shared guidance: [authentication and permissions](../../07-authentication-and-permissions.md).
