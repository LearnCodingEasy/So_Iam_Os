from django.test import SimpleTestCase
from allauth.socialaccount.models import SocialLogin

from users_accounts.adapter import MySocialAccountAdapter
from users_accounts.models import User


class SocialAccountAdapterTests(SimpleTestCase):
    def test_maps_provider_name_to_custom_user_fields(self):
        sociallogin = SocialLogin(user=User())

        user = MySocialAccountAdapter().populate_user(
            None,
            sociallogin,
            {"name": "Ada Lovelace", "email": "ada@example.test"},
        )

        self.assertEqual(user.name, "Ada")
        self.assertEqual(user.surname, "Lovelace")
        self.assertEqual(user.email, "ada@example.test")

    def test_uses_email_local_part_when_provider_has_no_name(self):
        sociallogin = SocialLogin(user=User())

        user = MySocialAccountAdapter().populate_user(
            None,
            sociallogin,
            {"email": "ada@example.test"},
        )

        self.assertEqual(user.name, "ada")
