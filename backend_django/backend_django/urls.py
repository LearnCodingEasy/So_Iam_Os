
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
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
        "api/social/",
        include(
            "social.urls"
        ),
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
