from rest_framework.routers import DefaultRouter

from architecture.api.views import ArchitectureViewSet, ComponentViewSet, DependencyViewSet, ArchitectureDecisionViewSet

router = DefaultRouter()
router.register('architectures', ArchitectureViewSet, basename='architecture')
router.register('components', ComponentViewSet, basename='component')
router.register('dependencies', DependencyViewSet, basename='dependency')
router.register('decisions', ArchitectureDecisionViewSet, basename='decision')

urlpatterns = router.urls
