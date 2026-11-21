# scraper API

Project prefix: /api/scraper/ (source: backend_django/backend_django/urls.py). Route rows below are declarations; DRF router methods are implicit and not runtime-verified.


## Routes: scraper/api/urls.py

- L5: router.register("sources", WebsiteViewSet, basename="scraper-source")

- L6: router.register("selectors", ParentSelectorViewSet, basename="scraper-selector")

- L7: router.register("configs", ScrapingConfigViewSet, basename="scraper-config")

- L8: router.register("runs", ScrapingJobViewSet, basename="scraper-run")

## Handler declarations: scraper/api/views/scraper_views.py
L12: class OwnedQuerysetMixin:
L13: permission_classes = [IsAuthenticated]
L15: def get_queryset(self):
L25: class WebsiteViewSet(viewsets.ModelViewSet):
L26: serializer_class = WebsiteSerializer
L27: permission_classes = [IsAuthenticated]
L29: def get_queryset(self):
L35: def perform_create(self, serializer):
L38: def perform_update(self, serializer):
L44: def perform_destroy(self, instance):
L54: @action(detail=True, methods=["post"])
L63: @action(detail=True, methods=["post"])
L85: @action(detail=False, methods=["get"])
L100: class ParentSelectorViewSet(viewsets.ModelViewSet):
L101: serializer_class = ParentSelectorSerializer
L102: permission_classes = [IsAuthenticated]
L103: def perform_create(self, serializer):
L110: def perform_update(self, serializer):
L117: def get_queryset(self):
L123: class ScrapingConfigViewSet(viewsets.ModelViewSet):
L124: serializer_class = ScrapingConfigSerializer
L125: permission_classes = [IsAuthenticated]
L126: def perform_create(self, serializer):
L133: def perform_update(self, serializer):
L140: def get_queryset(self):
L146: class ScrapingJobViewSet(viewsets.ReadOnlyModelViewSet):
L147: serializer_class = ScrapingJobSerializer
L148: permission_classes = [IsAuthenticated]
L150: def get_queryset(self):
L154: @action(detail=True, methods=["get"])


Full payload/response compatibility remains UNKNOWN until handlers, serializers and active frontend consumers are traced. See [cross-project API catalog](../../05-complete-api-catalog.md).
