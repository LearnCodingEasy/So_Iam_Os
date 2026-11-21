"""Normalized, credential-safe exceptions for shared AI execution."""


class AIError(Exception):
    """Base exception for the AI application."""
    default_message = "An AI error occurred."

    def __init__(self, message=None, *, category="unknown", retryable=False):
        super().__init__(message or self.default_message)
        self.category = category
        self.retryable = bool(retryable)


class AIProviderError(AIError):
    default_message = "The AI provider could not process the request."

    def __init__(self, message=None, *, category="provider_error", retryable=True,
                 status_code=None, retry_after=None):
        super().__init__(message, category=category, retryable=retryable)
        self.status_code = status_code
        self.retry_after = retry_after


class AIConfigurationError(AIError):
    default_message = "The AI provider is not configured correctly."

    def __init__(self, message=None, *, category="configuration_error"):
        super().__init__(message, category=category, retryable=False)


class AIResponseError(AIError):
    default_message = "The AI provider returned an invalid response."

    def __init__(self, message=None, *, category="invalid_provider_response"):
        # A malformed response can be recovered by trying another configured provider.
        super().__init__(message, category=category, retryable=True)
