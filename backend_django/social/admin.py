from django.contrib import admin

from .models import (
    FriendshipRequest,
    Friendship,
    Follow,
    UserBlock,
)


@admin.register(FriendshipRequest)
class FriendshipRequestAdmin(admin.ModelAdmin):

    list_display = (
        "sender",
        "receiver",
        "status",
        "created_at",
    )

    search_fields = (
        "sender__email",
        "receiver__email",
    )

    list_filter = (
        "status",
    )

    ordering = (
        "-created_at",
    )


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):

    list_display = (
        "user1",
        "user2",
        "created_at",
    )

    search_fields = (
        "user1__email",
        "user2__email",
    )

    ordering = (
        "-created_at",
    )


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):

    list_display = (
        "follower",
        "following",
        "created_at",
    )

    search_fields = (
        "follower__email",
        "following__email",
    )

    ordering = (
        "-created_at",
    )


@admin.register(UserBlock)
class UserBlockAdmin(admin.ModelAdmin):

    list_display = (
        "blocker",
        "blocked",
        "created_at",
    )

    search_fields = (
        "blocker__email",
        "blocked__email",
    )

    ordering = (
        "-created_at",
    )
