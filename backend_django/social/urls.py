# social/urls.py

from django.urls import path

from . import api


urlpatterns = [
    path("recommendations/", api.recommendations, name="recommendations"),
    path("profile/", api.my_profile, name="my-social-profile"),


    # 💡 Suggestions
    path(
        "friends/suggested/",
        api.my_friendship_suggestions,
        name="my_friendship_suggestions",
    ),

    # 👥 Friends
    path(
        "friends/<uuid:pk>/",
        api.friends,
        name="friends",
    ),

    # 📤 Send request
    path(
        "friends/<uuid:pk>/request/",
        api.send_friendship_request,
        name="send_friendship_request",
    ),

    # 🤝 Accept / Reject / Cancel
    path(
        "friends/<uuid:pk>/<str:action>/",
        api.handle_request,
        name="handle_request",
    ),

    # ❌ Unfriend
    path(
        "friends/<uuid:pk>/unfriend/",
        api.unfriend,
        name="unfriend",
    ),
]
