class AIError(Exception):
    """
    Base exception for the AI application.
    """

    default_message = "An AI error occurred."

    def __init__(self, message=None):
        super().__init__(message or self.default_message)


class AIProviderError(AIError):
    default_message = "The AI provider could not process the request."


class AIConfigurationError(AIError):
    default_message = "The AI provider is not configured correctly."


class AIResponseError(AIError):
    default_message = "The AI provider returned an invalid response."
