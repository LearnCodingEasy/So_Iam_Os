"""Encryption helpers for user-supplied AI provider credentials.

New deployments should set ``AI_CREDENTIAL_ENCRYPTION_KEY`` to a stable,
high-entropy secret kept outside source control. Existing ciphertexts created
with Django's SECRET_KEY remain readable for backward compatibility.
"""
import base64
import hashlib

from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings


_ENCRYPTION_PREFIX = "v2:"


def _fernet(secret):
    # Fernet requires a url-safe base64-encoded 32-byte key. Hashing gives us a
    # deterministic key while keeping the configured secret out of ciphertext.
    digest = hashlib.sha256(
        ("SO_IAM_OS:AI_CREDENTIALS:" + secret).encode("utf-8")
    ).digest()
    return Fernet(base64.urlsafe_b64encode(digest))


def _configured_fernet():
    secret = getattr(settings, "AI_CREDENTIAL_ENCRYPTION_KEY", "")
    if not secret:
        return None
    return _fernet(str(secret))


def _legacy_fernet():
    secret = getattr(settings, "SECRET_KEY", "")
    if not secret:
        raise ValueError("No credential encryption secret is configured.")
    return _fernet(str(secret))


def validate_encryption_configuration(*, production=False):
    secret = str(getattr(settings, "AI_CREDENTIAL_ENCRYPTION_KEY", "") or "")
    if production and not secret:
        raise RuntimeError("AI_CREDENTIAL_ENCRYPTION_KEY is required in production.")
    if secret and len(secret) < 32:
        raise RuntimeError("AI_CREDENTIAL_ENCRYPTION_KEY must contain at least 32 characters.")
    return True


def rotate_encryption_key(value, old_key):
    if not value:
        return ""
    old_fernet = _fernet(str(old_key))
    token = value[len(_ENCRYPTION_PREFIX):] if value.startswith(_ENCRYPTION_PREFIX) else value
    plaintext = old_fernet.decrypt(token.encode("utf-8")).decode("utf-8")
    return encrypt_secret(plaintext)


def encrypt_secret(value):
    if not value:
        return ""
    configured = _configured_fernet()
    if configured is not None:
        token = configured.encrypt(value.encode("utf-8")).decode("utf-8")
        return _ENCRYPTION_PREFIX + token
    # Preserve the legacy format when no dedicated key is configured.
    return _legacy_fernet().encrypt(value.encode("utf-8")).decode("utf-8")


def decrypt_secret(value):
    if not value:
        return ""
    try:
        if value.startswith(_ENCRYPTION_PREFIX):
            configured = _configured_fernet()
            if configured is None:
                raise ValueError(
                    "AI_CREDENTIAL_ENCRYPTION_KEY is required to decrypt this credential."
                )
            token = value[len(_ENCRYPTION_PREFIX):]
            return configured.decrypt(token.encode("utf-8")).decode("utf-8")

        # Backward compatibility for credentials encrypted before the dedicated
        # key was introduced. Do not rewrite old values implicitly on read.
        return _legacy_fernet().decrypt(value.encode("utf-8")).decode("utf-8")
    except InvalidToken as exc:
        raise ValueError(
            "Stored AI credential could not be decrypted. Check the configured "
            "AI_CREDENTIAL_ENCRYPTION_KEY and restore the original key if it changed."
        ) from exc
