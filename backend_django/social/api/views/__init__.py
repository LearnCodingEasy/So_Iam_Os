"""social views package (split from views.py)."""

from .social_views import User, friends, send_friendship_request, handle_request, unfriend, my_friendship_suggestions, recommendations, my_profile

__all__ = ['User', 'friends', 'send_friendship_request', 'handle_request', 'unfriend', 'my_friendship_suggestions', 'recommendations', 'my_profile']
