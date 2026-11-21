


# ===================================================
# Base Mixins
# ===================================================


class UserOwnedQuerysetMixin:
    """
    Base queryset protection.

    Models that directly contain a `user` ForeignKey
    can use this mixin.
    """

    def get_queryset(self):
        queryset = super().get_queryset()

        model = queryset.model

        if hasattr(model, "user"):
            return queryset.filter(
                user=self.request.user
            )

        return queryset
