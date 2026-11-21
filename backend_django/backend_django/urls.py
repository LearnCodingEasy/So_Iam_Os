
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from codex.api.views import BuildWorkspaceView, BuildManifestView

urlpatterns = [
    # Keep the Build workspace endpoints explicit at the project URL layer as well
    # as in codex.api.urls. This makes the expected public API contract unambiguous and
    # avoids deployment configurations accidentally omitting the nested Codex URLs.
    path("api/codex/build/workspace/", BuildWorkspaceView.as_view(),
         name="codex-build-workspace"),
    path("api/codex/build/manifest/", BuildManifestView.as_view(),
         name="codex-build-manifest"),
    path("api/codex/", include("codex.api.urls")),
    # 3️⃣ django-allauth [Allauth]
    path("accounts/", include("allauth.urls")),
    path('admin/', admin.site.urls),

    path(
        "api/users/",
        include(
            "users_accounts.api.urls"
        ),
    ),

    path(
        "api/core/",
        include("core.api.urls"),
    ),
    path(
        "api/knowledge/",
        include("knowledge.api.urls"),
    ),
    path(
        "api/learning/",
        include("learning.api.urls"),
    ),
    path(
        "api/scraper/",
        include("scraper.api.urls"),
    ),
    path(
        "api/ai/",
        include("ai.api.urls"),
    ),


    path(
        "api/goals/",
        include("goals.api.urls"),
    ),
    path(
        "api/tasks/",
        include("tasks.api.urls"),
    ),
    path(
        "api/jobs/",
        include("jobs_opportunity.api.urls"),
    ),
    path(
        "api/social/",
        include(
            "social.api.urls"
        ),
    ),
    path(
        "api/automation/",
        include("automation.api.urls"),
    ),
    path(
        "api/notifications/",
        include("notification.api.urls"),
    ),
    path("api/memory/", include("memory.api.urls")),
    path("api/projects/", include("projects.api.urls")),
    path("api/challenges/", include("challenges.api.urls")),
    path("api/finance/", include("personal_finance.api.urls")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
