# core API

Project prefix: /api/core/ (source: backend_django/backend_django/urls.py). Route rows below are declarations; DRF router methods are implicit and not runtime-verified.


## Routes: core/api/urls.py

- L4: path("health/", CoreHealthView.as_view(), name="core-health"),

- L5: path("dashboard/", DashboardView.as_view(), name="core-dashboard"),

- L6: path("learning-settings/", UserLearningSettingsView.as_view(), name="user-learning-settings"),

## Handler declarations: core/api/views/core_views.py
L10: class CoreHealthView(APIView):
L11: permission_classes = [AllowAny]
L16: class DashboardView(APIView):
L17: permission_classes = [IsAuthenticated]
L22: class UserLearningSettingsView(APIView):
L23: permission_classes = [IsAuthenticated]


Full payload/response compatibility remains UNKNOWN until handlers, serializers and active frontend consumers are traced. See [cross-project API catalog](../../05-complete-api-catalog.md).
