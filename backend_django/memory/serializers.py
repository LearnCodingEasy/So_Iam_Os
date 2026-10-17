from rest_framework import serializers
from .models import MemoryItem
class MemoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=MemoryItem
        fields='__all__'
        read_only_fields=['user','created_at','updated_at']
