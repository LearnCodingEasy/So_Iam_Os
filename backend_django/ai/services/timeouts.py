"""Single source of truth for AI execution timeouts.

Hierarchy (first valid value wins):

    request  ->  agent  ->  provider  ->  global setting  ->  safe default

Every value is validated against ``AI_TIMEOUT_MIN_SECONDS`` and
``AI_TIMEOUT_MAX_SECONDS`` so that no caller can request unlimited execution.

The value returned here is the *read* (total wait for the model response)
timeout. The TCP connect timeout stays separate
(``AI_PROVIDER_CONNECT_TIMEOUT_SECONDS``) and Celery limits are derived from
the same maximum, see ``celery_limits``.
"""
from django.conf import settings

SAFE_DEFAULT_SECONDS = 60
SAFE_MIN_SECONDS = 5
SAFE_MAX_SECONDS = 600


def timeout_bounds():
    low = int(getattr(settings, "AI_TIMEOUT_MIN_SECONDS", SAFE_MIN_SECONDS) or SAFE_MIN_SECONDS)
    high = int(getattr(settings, "AI_TIMEOUT_MAX_SECONDS", SAFE_MAX_SECONDS) or SAFE_MAX_SECONDS)
    return max(1, low), max(low, high)


def validate_timeout(value, *, field="timeout"):
    """Return an int within bounds or raise ``ValueError`` with a clear message."""
    low, high = timeout_bounds()
    try:
        if isinstance(value, bool):
            raise TypeError
        number = int(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field} must be a whole number of seconds.")
    if number < low or number > high:
        raise ValueError(f"{field} must be between {low} and {high} seconds.")
    return number


def _coerce(value):
    """Lenient coercion for non-request layers; invalid/empty -> None."""
    if value in (None, "", 0):
        return None
    try:
        return validate_timeout(value)
    except ValueError:
        return None


def resolve_timeout(*, request=None, agent=None, provider=None):
    """Resolve the effective timeout and report which layer supplied it.

    ``request`` values are validated strictly (invalid -> ValueError) because
    they are caller input. Lower layers are configuration and are clamped to
    the bounds instead of failing.
    """
    if request not in (None, ""):
        return validate_timeout(request, field="timeout"), "request"

    low, high = timeout_bounds()

    def clamp(v):
        v = _coerce(v)
        return v

    candidates = [("agent", agent)]
    provider_map = getattr(settings, "AI_PROVIDER_TIMEOUTS", {}) or {}
    candidates.append(("provider", provider_map.get(str(provider or "").lower()) if provider else None))
    candidates.append(("global", getattr(settings, "AI_PROVIDER_TIMEOUT_SECONDS", None)))
    for source, raw in candidates:
        value = clamp(raw)
        if value is not None:
            return value, source
    return min(max(SAFE_DEFAULT_SECONDS, low), high), "default"


def celery_limits():
    """(soft, hard) Celery limits that always exceed the maximum AI timeout."""
    _, high = timeout_bounds()
    soft = int(getattr(settings, "AI_CELERY_SOFT_TIME_LIMIT", 0) or 0) or high + 30
    hard = int(getattr(settings, "AI_CELERY_TIME_LIMIT", 0) or 0) or soft + 30
    return soft, max(hard, soft + 5)


LEGACY_SETTINGS_DEFAULT = 35  # AISettings.timeout_seconds model default


def user_setting_timeout(settings_obj):
    """The user's saved timeout, or None when it is still the untouched model
    default (35s). Treating the untouched default as "unset" lets the
    provider-level default (e.g. Ollama 120s) apply instead of silently
    capping every user at 35s. A user can still force 35s per request."""
    value = getattr(settings_obj, "timeout_seconds", None)
    if value in (None, "", 0, LEGACY_SETTINGS_DEFAULT):
        return None
    return _coerce(value)
