import uuid
from django.db import models
from social.models.common import User


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
