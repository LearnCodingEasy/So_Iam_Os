# social API

Project prefix: /api/social/ (source: backend_django/backend_django/urls.py). Route rows below are declarations; DRF router methods are implicit and not runtime-verified.


## Routes: social/api/urls.py

- L9: path("recommendations/", api.recommendations, name="recommendations"),

- L10: path("profile/", api.my_profile, name="my-social-profile"),

- L14: path(

- L21: path(

- L28: path(

- L35: path(

- L42: path(

## Handler declarations: social/api/views/social_views.py
L4: from rest_framework.decorators import api_view, permission_classes
L21: @permission_classes([IsAuthenticated])
L82: @permission_classes([IsAuthenticated])
L170: @permission_classes([IsAuthenticated])
L273: @permission_classes([IsAuthenticated])
L315: @permission_classes([IsAuthenticated])
L363: @permission_classes([IsAuthenticated])
L372: @permission_classes([IsAuthenticated])


Full payload/response compatibility remains UNKNOWN until handlers, serializers and active frontend consumers are traced. See [cross-project API catalog](../../05-complete-api-catalog.md).
