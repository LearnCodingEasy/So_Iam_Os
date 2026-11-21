from rest_framework import serializers
from social.models import FriendshipRequest, Friendship, Follow
from users_accounts.api.serializers import PublicUserSerializer
from social.models import SocialProfile, SocialRecommendation


class FriendshipRequestSerializer(
    serializers.ModelSerializer
):

    sender = PublicUserSerializer(
        read_only=True
    )

    receiver = PublicUserSerializer(
        read_only=True
    )

    class Meta:
        model = FriendshipRequest

        fields = [
            "id",
            "sender",
            "receiver",
            "status",
            "created_at",
            "updated_at",
        ]


class FriendshipSerializer(
    serializers.ModelSerializer
):

    user1 = PublicUserSerializer(
        read_only=True
    )

    user2 = PublicUserSerializer(
        read_only=True
    )

    class Meta:
        model = Friendship

        fields = [
            "id",
            "user1",
            "user2",
            "created_at",
        ]


class FollowSerializer(
    serializers.ModelSerializer
):

    follower = PublicUserSerializer(
        read_only=True
    )

    following = PublicUserSerializer(
        read_only=True
    )

    class Meta:
        model = Follow

        fields = [
            "id",
            "follower",
            "following",
            "created_at",
        ]


class SocialProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialProfile
        fields = ["id", "learning_interests", "professional_interests", "topics", "looking_for", "bio", "discoverable", "updated_at"]
        read_only_fields = ["id", "updated_at"]


class SocialRecommendationSerializer(serializers.ModelSerializer):
    candidate = PublicUserSerializer(read_only=True)
    class Meta:
        model = SocialRecommendation
        fields = ["id", "candidate", "score", "reasons", "breakdown", "status", "created_at", "updated_at"]
        read_only_fields = fields
