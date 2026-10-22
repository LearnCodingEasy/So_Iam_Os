
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from codex.views import BuildWorkspaceView, BuildManifestView

urlpatterns = [
    # Keep the Build workspace endpoints explicit at the project URL layer as well
    # as in codex.urls. This makes the expected public API contract unambiguous and
    # avoids deployment configurations accidentally omitting the nested Codex URLs.
    path("api/codex/build/workspace/", BuildWorkspaceView.as_view(),
         name="codex-build-workspace"),
    path("api/codex/build/manifest/", BuildManifestView.as_view(),
         name="codex-build-manifest"),
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
        "api/scraper/",
        include("scraper.urls"),
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
    path("api/memory/", include("memory.urls")),
    path("api/projects/", include("projects.urls")),
    path("api/challenges/", include("challenges.urls")),
    path("api/finance/", include("personal_finance.urls")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
