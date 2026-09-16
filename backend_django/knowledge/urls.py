from rest_framework.routers import DefaultRouter

from .views import (
    KnowledgeFileViewSet,
    KnowledgeItemViewSet,
)


router = DefaultRouter()

router.register(
    r"items",
    KnowledgeItemViewSet,
    basename="knowledge-item",
)

router.register(
    r"files",
    KnowledgeFileViewSet,
    basename="knowledge-file",
)


urlpatterns = router.urls
