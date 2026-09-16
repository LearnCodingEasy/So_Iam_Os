# users_accounts/api.py

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
    parser_classes,
)

from rest_framework.parsers import (
    MultiPartParser,
    FormParser,
)

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)

from rest_framework.response import Response
from rest_framework import status

from .forms import (
    SignupForm,
    ProfileForm,
)

from .serializers import (
    UserSerializer,
    PublicUserSerializer,
)


#
import logging

logger = logging.getLogger(__name__)

User = get_user_model()


# ====================================================
# 👤 SIGNUP
# ====================================================

@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def signup(request):
    logger.info("SIGNUP REQUEST | method=%s | path=%s",
                request.method, request.path, )
    logger.debug("SIGNUP DATA | keys=%s", list(request.data.keys()), )

    form = SignupForm(request.data)
    if not form.is_valid():
        logger.warning("SIGNUP FAILED | status=%s | errors=%s",
                       status.HTTP_400_BAD_REQUEST, form.errors.as_json(), )

        return Response(
            {
                "message": "Signup failed.",
                "errors": form.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = form.save()
    logger.info("SIGNUP SUCCESS | user_id=%s | status=%s",
                user.pk, status.HTTP_201_CREATED, )

    return Response(
        {
            "message": "success",
            "email_sent": False,
            "user": UserSerializer(user).data,
        },
        status=status.HTTP_201_CREATED,
    )


# ====================================================
# 👤 CURRENT USER
# ====================================================

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):

    logger.info("ME REQUEST | user_id=%s | email=%s | method=%s | path=%s",
                request.user.pk, request.user.email, request.method, request.path, )
    serializer = UserSerializer(request.user)
    logger.debug("ME RESPONSE | user_id=%s | status=%s",
                 request.user.pk, status.HTTP_200_OK, )

    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
    )


# ====================================================
# 👤 PUBLIC PROFILE
# ====================================================

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile(request, id):
    logger.info("PUBLIC PROFILE REQUEST | requester_id=%s | target_user_id=%s | method=%s | path=%s",
                request.user.pk, id, request.method, request.path, )

    user = get_object_or_404(
        User,
        pk=id,
    )
    logger.debug("PUBLIC PROFILE FOUND | target_user_id=%s", user.pk, )

    serializer = PublicUserSerializer(user)
    logger.info("PUBLIC PROFILE SUCCESS | target_user_id=%s | status=%s",
                user.pk, status.HTTP_200_OK, )

    return Response(
        {
            "user": serializer.data,
        },
        status=status.HTTP_200_OK,
    )


# ====================================================
# ✏️ EDIT PROFILE
# ====================================================

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@parser_classes([
    MultiPartParser,
    FormParser,
])
def editprofile(request):

    user = request.user
    logger.info("EDIT PROFILE REQUEST | user_id=%s | email=%s | method=%s | path=%s",
                user.pk, user.email, request.method, request.path, )
    logger.debug("EDIT PROFILE DATA | user_id=%s | fields=%s",
                 user.pk, list(request.data.keys()), )
    logger.debug("EDIT PROFILE FILES | user_id=%s | files=%s",
                 user.pk, list(request.FILES.keys()), )

    form = ProfileForm(
        request.data,
        request.FILES,
        instance=user,
    )

    if not form.is_valid():
        logger.warning("EDIT PROFILE FAILED | user_id=%s | status=%s | errors=%s",
                       user.pk, status.HTTP_400_BAD_REQUEST, form.errors.as_json(), )
        return Response(
            {
                "message": "Profile update failed.",
                "errors": form.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = form.save()
    serializer = UserSerializer(user)
    user_data = serializer.data
    logger.info("EDIT PROFILE SUCCESS | user_id=%s | status=%s",
                user.pk, status.HTTP_200_OK, )
    logger.debug("EDIT PROFILE RESULT | user_id=%s | data=%s",
                 user.pk, user_data, )

    return Response(
        {
            "message": "information updated",
            "user": UserSerializer(user).data,
        },
        status=status.HTTP_200_OK,
    )


# ==================================================== # 🔐 EDIT PASSWORD # ====================================================
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def editpassword(request):
    user = request.user
    logger.info("EDIT PASSWORD REQUEST | user_id=%s | email=%s | method=%s | path=%s",
                user.pk, user.email, request.method, request.path, )
    # مهم: #
    # لا نسجل password أو أي بيانات حساسة في الـ logs.
    form = PasswordChangeForm(user=user, data=request.data, )
    if not form.is_valid():
        logger.warning("EDIT PASSWORD FAILED | user_id=%s | status=%s | errors=%s",
                       user.pk, status.HTTP_400_BAD_REQUEST, form.errors.as_json(), )
        return Response({"message": "Password update failed.", "errors": form.errors, }, status=status.HTTP_400_BAD_REQUEST, )
    form.save()
    logger.info("EDIT PASSWORD SUCCESS | user_id=%s | status=%s",
                user.pk, status.HTTP_200_OK, )
    return Response({"message": "success", }, status=status.HTTP_200_OK, )
