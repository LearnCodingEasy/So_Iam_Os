from rest_framework.routers import DefaultRouter
from .views import ChallengeViewSet,ChallengeStepViewSet,ChallengeAttemptViewSet,ChallengeProgressViewSet
router=DefaultRouter(); router.register('challenges',ChallengeViewSet,basename='challenge'); router.register('steps',ChallengeStepViewSet,basename='challenge-step'); router.register('attempts',ChallengeAttemptViewSet,basename='challenge-attempt'); router.register('progress',ChallengeProgressViewSet,basename='challenge-progress')
urlpatterns=router.urls
