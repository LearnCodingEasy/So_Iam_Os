
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("api/codex/", include("codex.urls")),
    # 3️⃣ django-allauth [Allauth]
    path("accounts/", include("allauth.urls")),
    path('admin/', admin.site.urls),

    path(
        "api/users/",
        include(
            "users_accounts.urls"
        ),
    ),

    path(
        "api/core/",
        include("core.urls"),
    ),
    path(
        "api/knowledge/",
        include("knowledge.urls"),
    ),
    path(
        "api/learning/",
        include("learning.urls"),
    ),
    path(
        "api/ai/",
        include("ai.urls"),
    ),


    path(
        "api/goals/",
        include("goals.urls"),
    ),
    path(
        "api/tasks/",
        include("tasks.urls"),
    ),
    path(
        "api/jobs/",
        include("jobs_opportunity.urls"),
    ),
    path(
        "api/social/",
        include(
            "social.urls"
        ),
    ),
    path(
        "api/automation/",
        include("automation.urls"),
    ),
    path(
        "api/notifications/",
        include("notification.urls"),
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
