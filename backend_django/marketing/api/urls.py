from rest_framework.routers import DefaultRouter

from marketing.api.views import MarketingChannelViewSet, CampaignViewSet, MarketingContentViewSet, LeadSourceViewSet

router = DefaultRouter()
router.register('channels', MarketingChannelViewSet, basename='marketing-channel')
router.register('campaigns', CampaignViewSet, basename='campaign')
router.register('content', MarketingContentViewSet, basename='marketing-content')
router.register('lead-sources', LeadSourceViewSet, basename='lead-source')

urlpatterns = router.urls
