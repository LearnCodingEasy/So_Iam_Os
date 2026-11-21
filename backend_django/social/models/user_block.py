import uuid
from django.db import models
from social.models.common import User


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
