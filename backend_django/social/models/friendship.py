import uuid
from django.db import models
from social.models.common import User


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
