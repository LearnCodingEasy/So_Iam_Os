from rest_framework.routers import DefaultRouter
from memory.api.views import MemoryItemViewSet
router=DefaultRouter(); router.register('items',MemoryItemViewSet,basename='memory-item')
urlpatterns=router.urls
