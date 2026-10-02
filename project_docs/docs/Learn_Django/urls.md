## Urls

```python
from django.urls import path

from . import views

urlpatterns = [
    path("product_list/", views.product_list, name="product_list"),
]

```

```python
# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# product_list
router.register(r'product_list', views.product_list)

urlpatterns = [
    path('', include(router.urls)),
]
```
