from rest_framework.routers import DefaultRouter

from crm.api.views import CompanyViewSet, ContactViewSet, InteractionViewSet, CustomerRelationshipViewSet

router = DefaultRouter()
router.register('companies', CompanyViewSet, basename='company')
router.register('contacts', ContactViewSet, basename='contact')
router.register('interactions', InteractionViewSet, basename='interaction')
router.register('relationships', CustomerRelationshipViewSet, basename='customer-relationship')

urlpatterns = router.urls
