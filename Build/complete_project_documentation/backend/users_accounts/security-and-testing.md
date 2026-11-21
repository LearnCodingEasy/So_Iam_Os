# users_accounts security and testing

## Permission/ownership evidence

- users_accounts/api/views/users_accounts_views.py:L4: from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes
- users_accounts/api/views/users_accounts_views.py:L6: from rest_framework.permissions import AllowAny, IsAuthenticated
- users_accounts/api/views/users_accounts_views.py:L25: @authentication_classes([])
- users_accounts/api/views/users_accounts_views.py:L26: @permission_classes([AllowAny])
- users_accounts/api/views/users_accounts_views.py:L64: @permission_classes([IsAuthenticated])
- users_accounts/api/views/users_accounts_views.py:L68: request.user.pk, request.user.email, request.method, request.path, )
- users_accounts/api/views/users_accounts_views.py:L69: serializer = UserSerializer(request.user)
- users_accounts/api/views/users_accounts_views.py:L71: request.user.pk, status.HTTP_200_OK, )
- users_accounts/api/views/users_accounts_views.py:L84: @permission_classes([IsAuthenticated])
- users_accounts/api/views/users_accounts_views.py:L87: request.user.pk, id, request.method, request.path, )
- users_accounts/api/views/users_accounts_views.py:L112: @permission_classes([IsAuthenticated])
- users_accounts/api/views/users_accounts_views.py:L119: user = request.user
- users_accounts/api/views/users_accounts_views.py:L163: @permission_classes([IsAuthenticated])
- users_accounts/api/views/users_accounts_views.py:L165: user = request.user


## Tests
- users_accounts/tests/test_users_accounts.py
- users_accounts/tests/__init__.py


Tests were not run. This scan is not a complete authorization/security review. Shared guidance: [authentication and permissions](../../07-authentication-and-permissions.md).
