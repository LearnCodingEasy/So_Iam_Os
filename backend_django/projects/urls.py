from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet,ProjectMemberViewSet,ProjectContextViewSet
router=DefaultRouter(); router.register('projects',ProjectViewSet,basename='project'); router.register('members',ProjectMemberViewSet,basename='project-member'); router.register('contexts',ProjectContextViewSet,basename='project-context')
urlpatterns=router.urls
