from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import MemoryItem
from .serializers import MemoryItemSerializer
class MemoryItemViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]; serializer_class=MemoryItemSerializer
    def get_queryset(self): return MemoryItem.objects.filter(user=self.request.user)
    def perform_create(self,serializer): serializer.save(user=self.request.user)
