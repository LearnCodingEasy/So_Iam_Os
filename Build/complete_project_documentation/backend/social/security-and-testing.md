# social security and testing

## Permission/ownership evidence

- social/api/views/social_views.py:L4: from rest_framework.decorators import api_view, permission_classes
- social/api/views/social_views.py:L5: from rest_framework.permissions import IsAuthenticated
- social/api/views/social_views.py:L21: @permission_classes([IsAuthenticated])
- social/api/views/social_views.py:L52: if user == request.user:
- social/api/views/social_views.py:L55: receiver=request.user,
- social/api/views/social_views.py:L82: @permission_classes([IsAuthenticated])
- social/api/views/social_views.py:L90: current_user = request.user
- social/api/views/social_views.py:L170: @permission_classes([IsAuthenticated])
- social/api/views/social_views.py:L180: receiver=request.user,
- social/api/views/social_views.py:L201: user1 = request.user
- social/api/views/social_views.py:L239: if friendship_request.sender != request.user:
- social/api/views/social_views.py:L273: @permission_classes([IsAuthenticated])
- social/api/views/social_views.py:L281: user1 = request.user
- social/api/views/social_views.py:L315: @permission_classes([IsAuthenticated])
- social/api/views/social_views.py:L318: current_user = request.user
- social/api/views/social_views.py:L363: @permission_classes([IsAuthenticated])
- social/api/views/social_views.py:L367: rows = recommendations_for(request.user, limit=limit)
- social/api/views/social_views.py:L372: @permission_classes([IsAuthenticated])
- social/api/views/social_views.py:L376: obj, _ = SocialProfile.objects.get_or_create(user=request.user)


## Tests
- social/tests/test_social.py
- social/tests/__init__.py


Tests were not run. This scan is not a complete authorization/security review. Shared guidance: [authentication and permissions](../../07-authentication-and-permissions.md).
