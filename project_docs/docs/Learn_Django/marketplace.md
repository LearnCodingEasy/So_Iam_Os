# Marketplace

<div class="" dir="rtl">انشاء فولدار </div>

```
mkdir marketplace
```

<div class="" dir="rtl">انشاء فولدار داخل ال marketplace</div>

```
cd marketplace
```

```
mkdir vendor
```

<div class="" dir="rtl">انشاء تطبيق البياعين </div>

```
python manage.py startapp vendor marketplace/vendor
```

```
python manage.py startapp vendor
```

<div class="" dir="rtl">انشاء قاعادة البيانات </div>

```python
from django.db import models
from users_accounts.models import User
import uuid

from django.utils import timezone
from django.utils.timesince import timesince


class Vendor(models.Model):
    # ___________________
    # حقل يتم تعبئة تلقائي
    # ___________________
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.OneToOneField(
        User, related_name='vendor', on_delete=models.CASCADE)

    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def created_at_formatted(self):
        return timesince(self.created_at)

```

<div class="" dir="rtl">انشاء 💼 admin لوحة الإدارة </div>

```python
from django.contrib import admin
from .models import Vendor
admin.site.register(Vendor)
```

<div class="" dir="rtl"> 
  
</div>

```python

```

<div class="" dir="rtl"> 
  
</div>

```python

```

<div class="" dir="rtl"> 
  
</div>

```python

```

<div class="" dir="rtl"> 
  
</div>

```python

```

<div class="" dir="rtl"> 
  
</div>

```python

```

<div class="" dir="rtl"> 
  
</div>

```python

```

<div class="" dir="rtl"> 
  
</div>

```python

```

<div class="" dir="rtl"> 
  
</div>

```python

```

<div class="" dir="rtl"> 
  
</div>

```python

```

<div class="" dir="rtl"> 
  
</div>

```python

```
