# users_accounts/serializers.py

from rest_framework import serializers

from .models import User


class PublicUserSerializer(serializers.ModelSerializer):

    full_name = serializers.ReadOnlyField()
    avatar_url = serializers.ReadOnlyField()

    class Meta:
        model = User

        fields = [
            "id",
            "name",
            "surname",
            "full_name",
            "avatar_url",
            "skills",
            "is_online",
        ]


class UserSerializer(serializers.ModelSerializer):

    full_name = serializers.ReadOnlyField()
    avatar_url = serializers.ReadOnlyField()
    cover_url = serializers.ReadOnlyField()

    class Meta:
        model = User

        fields = [
            "id",
            "name",
            "surname",
            "full_name",
            "email",
            "date_of_birth",
            "gender",
            "avatar_url",
            "cover_url",
            "skills",
            "task_count",
            "is_online",
            "date_joined",
        ]
