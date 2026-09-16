# users_accounts/urls.py

from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import api


urlpatterns = [

    # 👤 Account
    path(
        "me/",
        api.me,
        name="me",
    ),

    # 📝 Authentication
    path(
        "signup/",
        api.signup,
        name="signup",
    ),

    path(
        "login/",
        TokenObtainPairView.as_view(),
        name="token_obtain",
    ),

    path(
        "refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),

    # 👤 Profile
    path(
        "profile/<uuid:id>/",
        api.profile,
        name="profile",
    ),

    path(
        "editprofile/",
        api.editprofile,
        name="editprofile",
    ),

    path(
        "editpassword/",
        api.editpassword,
        name="editpassword",
    ),
]
