## Serializers

```python
# Serializers.py

from rest_framework import serializers
from .models import Product

# ----------------------------
# 🔘 Product Serializer
# ----------------------------

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'created_at',
            'created_at_formatted',
            'updated_at',
            'updated_at_formatted',
            # 'created_by',

            'name',
            'description',
            'price',
            'is_available',
        ]
```
