import uuid

from django.db import models


class BaseModel(models.Model):
    """
    Base model shared by the So_Iam_OS applications.

    Provides:
    - UUID primary key
    - created_at
    - updated_at
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.id)
