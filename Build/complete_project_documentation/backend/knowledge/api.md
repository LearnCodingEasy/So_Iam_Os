# knowledge API

Project prefix: /api/knowledge/ (source: backend_django/backend_django/urls.py). Route rows below are declarations; DRF router methods are implicit and not runtime-verified.


## Routes: knowledge/api/urls.py

- L16: router.register(

- L27: router.register(

## Handler declarations: knowledge/api/views/knowledge_file_views.py
L25: class KnowledgeFileViewSet(viewsets.ModelViewSet):
L32: permission_classes = [
L42: serializer_class = KnowledgeFileSerializer
L48: def get_queryset(self):
L66: def perform_create(self, serializer):
L120: def perform_update(self, serializer):
L137: def perform_destroy(self, instance):

## Handler declarations: knowledge/api/views/knowledge_item_views.py
L31: class KnowledgeItemViewSet(viewsets.ModelViewSet):
L38: permission_classes = [
L48: serializer_class = KnowledgeItemSerializer
L54: def get_queryset(self):
L160: def perform_create(self, serializer):
L169: def perform_update(self, serializer):
L183: def perform_destroy(self, instance):
L195: @action(detail=True, methods=["post"], url_path="extract-metadata")
L225: @action(
L253: @action(
L281: @action(
L352: @action(
L423: @action(
L453: @action(
L538: @action(


Full payload/response compatibility remains UNKNOWN until handlers, serializers and active frontend consumers are traced. See [cross-project API catalog](../../05-complete-api-catalog.md).
