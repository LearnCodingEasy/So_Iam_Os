# core security and testing

## Permission/ownership evidence

- core/api/views/core_views.py:L1: from rest_framework.permissions import AllowAny, IsAuthenticated
- core/api/views/core_views.py:L11: permission_classes = [AllowAny]
- core/api/views/core_views.py:L17: permission_classes = [IsAuthenticated]
- core/api/views/core_views.py:L19: return Response(DashboardService.get_data(user=request.user))
- core/api/views/core_views.py:L23: permission_classes = [IsAuthenticated]
- core/api/views/core_views.py:L25: obj, _ = UserLearningSettings.objects.get_or_create(user=request.user)
- core/api/views/core_views.py:L26: if obj.current_learning_goal_id and obj.current_learning_goal.user_id != request.user.id:


## Tests
- core/tests/tests_learning_settings.py
- core/tests/test_api_contract.py
- core/tests/test_core.py
- core/tests/__init__.py


Tests were not run. This scan is not a complete authorization/security review. Shared guidance: [authentication and permissions](../../07-authentication-and-permissions.md).
