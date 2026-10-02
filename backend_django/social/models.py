# social/models.py

import uuid

from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL


class FriendshipRequest(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"
        CANCELLED = "cancelled", "Cancelled"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_friendship_requests",
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_friendship_requests",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "sender",
                    "receiver",
                ],
                name="unique_friendship_request",
            )
        ]

    def __str__(self):
        return f"{self.sender} → {self.receiver}"


class Friendship(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    user1 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="friendships_as_user1",
    )

    user2 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="friendships_as_user2",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "user1",
                    "user2",
                ],
                name="unique_friendship",
            )
        ]

    def __str__(self):
        return f"{self.user1} ↔ {self.user2}"


class Follow(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
    )

    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="followers",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "follower",
                    "following",
                ],
                name="unique_follow",
            )
        ]

    def __str__(self):
        return f"{self.follower} → {self.following}"


class UserBlock(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    blocker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="blocked_users",
    )

    blocked = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="blocked_by_users",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "blocker",
                    "blocked",
                ],
                name="unique_user_block",
            )
        ]

    def __str__(self):
        return f"{self.blocker} blocks {self.blocked}"


class SocialProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="social_profile")
    learning_interests = models.JSONField(default=list, blank=True)
    professional_interests = models.JSONField(default=list, blank=True)
    topics = models.JSONField(default=list, blank=True)
    looking_for = models.JSONField(default=list, blank=True)
    bio = models.TextField(blank=True)
    discoverable = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["discoverable", "updated_at"])]


class SocialRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="social_recommendations")
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name="social_recommended_to")
    score = models.PositiveSmallIntegerField(default=0)
    reasons = models.JSONField(default=list, blank=True)
    breakdown = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=20, default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "candidate"], name="unique_social_recommendation")]
        indexes = [models.Index(fields=["user", "score"])]
