from django.urls import path

from .views import CoreHealthView, DashboardView


urlpatterns = [
    path(
        "health/",
        CoreHealthView.as_view(),
        name="core-health",
    ),

    path(
        "dashboard/",
        DashboardView.as_view(),
        name="core-dashboard",
    ),
]
