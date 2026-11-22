"""Social account mapping for the project's custom user model."""

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    """Map provider identity data onto the required custom ``User.name``."""

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)

        full_name = (
            data.get("name")
            or " ".join(
                part
                for part in (data.get("first_name"), data.get("last_name"))
                if part
            )
            or data.get("given_name")
            or (data.get("email") or "").split("@", 1)[0]
            or "User"
        )
        first_name, _, surname = full_name.strip().partition(" ")
        user.name = first_name or "User"
        if hasattr(user, "surname"):
            user.surname = surname
        return user
