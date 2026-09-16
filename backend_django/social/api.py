# social/api.py

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework.decorators import (
    api_view,
    permission_classes,
)

from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response

from rest_framework import status

from .models import (
    Friendship,
    FriendshipRequest,
)

from .serializers import (
    FriendshipRequestSerializer,
    FriendshipSerializer,
)

from users_accounts.serializers import (
    UserSerializer,
    PublicUserSerializer,
)


User = get_user_model()


# ============================================================
# 🧑‍🤝‍🧑 FRIENDS
# ============================================================

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def friends(request, pk):

    user = get_object_or_404(
        User,
        pk=pk,
    )

    friendships = Friendship.objects.filter(
        Q(user1=user) |
        Q(user2=user)
    ).select_related(
        "user1",
        "user2",
    )

    friend_users = []

    for friendship in friendships:

        if friendship.user1_id == user.id:
            friend_users.append(
                friendship.user2
            )
        else:
            friend_users.append(
                friendship.user1
            )

    incoming_requests = []

    if user == request.user:

        incoming_requests = FriendshipRequest.objects.filter(
            receiver=request.user,
            status=FriendshipRequest.Status.PENDING,
        )

    return Response(
        {
            "user": PublicUserSerializer(user).data,

            "friends": PublicUserSerializer(
                friend_users,
                many=True,
            ).data,

            "requests": FriendshipRequestSerializer(
                incoming_requests,
                many=True,
            ).data,

        }
    )


# ============================================================
# 📤 SEND FRIEND REQUEST
# ============================================================

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_friendship_request(request, pk):

    target_user = get_object_or_404(
        User,
        pk=pk,
    )

    current_user = request.user

    # 🚫 Can't send to yourself
    if target_user == current_user:

        return Response(
            {
                "message": "You cannot send a request to yourself."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # 🤝 Already friends?
    already_friends = Friendship.objects.filter(
        Q(user1=current_user, user2=target_user) |
        Q(user1=target_user, user2=current_user)
    ).exists()

    if already_friends:

        return Response(
            {
                "message": "Users are already friends."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # 🔍 Existing request
    friendship_request = FriendshipRequest.objects.filter(
        sender=current_user,
        receiver=target_user,
    ).first()

    if friendship_request:

        if friendship_request.status == FriendshipRequest.Status.PENDING:

            return Response(
                {
                    "message": "Request already sent."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        friendship_request.status = (
            FriendshipRequest.Status.PENDING
        )

        friendship_request.save()

    else:

        friendship_request = FriendshipRequest.objects.create(
            sender=current_user,
            receiver=target_user,
            status=FriendshipRequest.Status.PENDING,
        )

    return Response(
        {
            "message": "Friendship request sent successfully.",
            "request": FriendshipRequestSerializer(
                friendship_request
            ).data,
        },
        status=status.HTTP_201_CREATED,
    )


# ============================================================
# 🤝 HANDLE FRIEND REQUEST
# ============================================================

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def handle_request(request, pk, action):

    target_user = get_object_or_404(
        User,
        pk=pk,
    )

    friendship_request = FriendshipRequest.objects.filter(
        sender=target_user,
        receiver=request.user,
        status=FriendshipRequest.Status.PENDING,
    ).first()

    if not friendship_request:

        return Response(
            {
                "message": "Friendship request not found."
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    if action == "accept":

        friendship_request.status = (
            FriendshipRequest.Status.ACCEPTED
        )

        friendship_request.save()

        user1 = request.user
        user2 = target_user

        # ترتيب UUIDs لمنع إنشاء
        # نفس العلاقة مرتين
        if str(user1.id) > str(user2.id):
            user1, user2 = user2, user1

        friendship, created = Friendship.objects.get_or_create(
            user1=user1,
            user2=user2,
        )

        return Response(
            {
                "message": "Friendship request accepted.",
                "friendship": FriendshipSerializer(
                    friendship
                ).data,
            }
        )

    if action == "reject":

        friendship_request.status = (
            FriendshipRequest.Status.REJECTED
        )

        friendship_request.save()

        return Response(
            {
                "message": "Friendship request rejected."
            }
        )

    if action == "cancel":

        if friendship_request.sender != request.user:

            return Response(
                {
                    "message": "You cannot cancel this request."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        friendship_request.status = (
            FriendshipRequest.Status.CANCELLED
        )

        friendship_request.save()

        return Response(
            {
                "message": "Friendship request cancelled."
            }
        )

    return Response(
        {
            "message": "Invalid action."
        },
        status=status.HTTP_400_BAD_REQUEST,
    )


# ============================================================
# ❌ UNFRIEND
# ============================================================

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def unfriend(request, pk):

    target_user = get_object_or_404(
        User,
        pk=pk,
    )

    user1 = request.user
    user2 = target_user

    if str(user1.id) > str(user2.id):
        user1, user2 = user2, user1

    friendship = Friendship.objects.filter(
        user1=user1,
        user2=user2,
    ).first()

    if not friendship:

        return Response(
            {
                "message": "Friendship not found."
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    friendship.delete()

    return Response(
        {
            "message": "Users are no longer friends."
        }
    )


# ============================================================
# 💡 FRIEND SUGGESTIONS
# ============================================================

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_friendship_suggestions(request):

    current_user = request.user

    friend_ids = Friendship.objects.filter(
        Q(user1=current_user) |
        Q(user2=current_user)
    ).values_list(
        "user1",
        "user2",
    )

    suggestions = User.objects.exclude(
        id=current_user.id
    )

    # استبعاد الأصدقاء الحاليين
    for friend_id_pair in friend_ids:
        pass

    friends = []

    friendships = Friendship.objects.filter(
        Q(user1=current_user) |
        Q(user2=current_user)
    )

    for friendship in friendships:

        if friendship.user1_id == current_user.id:
            friends.append(friendship.user2_id)
        else:
            friends.append(friendship.user1_id)

    suggestions = suggestions.exclude(
        id__in=friends
    )

    return Response(
        PublicUserSerializer(
            suggestions[:50],
            many=True,
        ).data
    )
