# memory API

Project prefix: /api/memory/ (source: backend_django/backend_django/urls.py). Route rows below are declarations; DRF router methods are implicit and not runtime-verified.


## Routes: memory/api/urls.py

- L3: router=DefaultRouter(); router.register('items',MemoryItemViewSet,basename='memory-item')

## Handler declarations: memory/api/views/memory_views.py
L7: class MemoryItemViewSet(viewsets.ModelViewSet):
L8: permission_classes=[IsAuthenticated]; serializer_class=MemoryItemSerializer
L9: def get_queryset(self): return MemoryItem.objects.filter(user=self.request.user)
L10: def perform_create(self,serializer): serializer.save(user=self.request.user)


Full payload/response compatibility remains UNKNOWN until handlers, serializers and active frontend consumers are traced. See [cross-project API catalog](../../05-complete-api-catalog.md).
