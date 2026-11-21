# users_accounts API

Project prefix: /api/users/ (source: backend_django/backend_django/urls.py). Route rows below are declarations; DRF router methods are implicit and not runtime-verified.


## Routes: users_accounts/api/urls.py

- L16: path(

- L23: path(

- L29: path(

- L35: path(

- L42: path(

- L48: path(

- L54: path(

## Handler declarations: users_accounts/api/views/users_accounts_views.py
L4: from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes
L26: @permission_classes([AllowAny])
L64: @permission_classes([IsAuthenticated])
L84: @permission_classes([IsAuthenticated])
L112: @permission_classes([IsAuthenticated])
L163: @permission_classes([IsAuthenticated])


Full payload/response compatibility remains UNKNOWN until handlers, serializers and active frontend consumers are traced. See [cross-project API catalog](../../05-complete-api-catalog.md).
