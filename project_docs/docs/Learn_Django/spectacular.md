# Document

## spectacular

```cmd
pip install drf-spectacular
```

```python
# 3️⃣ rest_framework
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
# 0️⃣1️⃣ Document
SPECTACULAR_SETTINGS = {
    'TITLE': 'Your Project API',
    'DESCRIPTION': 'Your project description',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}
```

```python
    'drf_spectacular',

```

```python
SpectacularRedocView
urlpatterns = [
# 0️⃣1️⃣ Document
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/',
         SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + debug_toolbar_urls()
```
- swagger
```
http://localhost:8000/api/schema/swagger-ui
```
- redec
```
http://localhost:8000/api/schema/redoc/

```
