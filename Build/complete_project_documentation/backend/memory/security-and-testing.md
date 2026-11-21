# memory security and testing

## Permission/ownership evidence

- memory/api/views/memory_views.py:L2: from rest_framework.permissions import IsAuthenticated
- memory/api/views/memory_views.py:L8: permission_classes=[IsAuthenticated]; serializer_class=MemoryItemSerializer
- memory/api/views/memory_views.py:L9: def get_queryset(self): return MemoryItem.objects.filter(user=self.request.user)
- memory/api/views/memory_views.py:L10: def perform_create(self,serializer): serializer.save(user=self.request.user)


## Tests
- memory/tests/test_memory.py
- memory/tests/__init__.py


Tests were not run. This scan is not a complete authorization/security review. Shared guidance: [authentication and permissions](../../07-authentication-and-permissions.md).
