from django.db import models


class ActiveManager(models.Manager):
    """
    Manager that returns only active objects.

    Models using this manager must have an `is_active` field.
    """

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(is_active=True)
        )
