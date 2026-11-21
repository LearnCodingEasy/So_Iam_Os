from django.test import SimpleTestCase, override_settings

from ai.services.security import decrypt_secret, encrypt_secret


class AICredentialEncryptionTests(SimpleTestCase):
    @override_settings(AI_CREDENTIAL_ENCRYPTION_KEY="stable-test-key")
    def test_dedicated_key_encrypts_and_decrypts_credentials(self):
        encrypted = encrypt_secret("provider-secret")
        self.assertTrue(encrypted.startswith("v2:"))
        self.assertNotIn("provider-secret", encrypted)
        self.assertEqual(decrypt_secret(encrypted), "provider-secret")

    @override_settings(AI_CREDENTIAL_ENCRYPTION_KEY="")
    def test_legacy_secret_key_format_remains_supported(self):
        encrypted = encrypt_secret("legacy-secret")
        self.assertFalse(encrypted.startswith("v2:"))
        self.assertEqual(decrypt_secret(encrypted), "legacy-secret")

    @override_settings(AI_CREDENTIAL_ENCRYPTION_KEY="")
    def test_versioned_ciphertext_requires_dedicated_key(self):
        with self.assertRaisesMessage(ValueError, "AI_CREDENTIAL_ENCRYPTION_KEY"):
            decrypt_secret("v2:invalid")
