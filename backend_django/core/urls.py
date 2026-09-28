from django.urls import path
from .views import CoreHealthView, DashboardView, UserLearningSettingsView
urlpatterns = [
    path("health/", CoreHealthView.as_view(), name="core-health"),
    path("dashboard/", DashboardView.as_view(), name="core-dashboard"),
    path("learning-settings/", UserLearningSettingsView.as_view(), name="user-learning-settings"),
]
