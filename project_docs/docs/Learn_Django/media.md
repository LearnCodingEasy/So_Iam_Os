# Media

## settings.py

```python
# Access path for media files (such as images and files uploaded by users)
MEDIA_URL = "media/"
# Specify a "media" folder in the project to store uploaded media files
MEDIA_ROOT = BASE_DIR / "media"
```

## urls.py

```python
from django.conf import settings
from django.conf.urls.static import static

```

```python
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
