from rest_framework.routers import DefaultRouter

from .views import (
    KnowledgeItemViewSet,
    KnowledgeFileViewSet,
)


router = DefaultRouter()


# ====================================================
# 🧠 Knowledge
# ====================================================

router.register(
    r"items",
    KnowledgeItemViewSet,
    basename="knowledge-item",
)


# ====================================================
# 📎 Knowledge Files
# ====================================================

router.register(
    r"files",
    KnowledgeFileViewSet,
    basename="knowledge-file",
)


urlpatterns = router.urls
