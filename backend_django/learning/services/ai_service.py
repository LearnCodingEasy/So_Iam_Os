class LearningAIService:
    """
    AI abstraction layer.

    Later this can connect to the project's AI app/provider.
    """

    @staticmethod
    def analyze_application(
        *,
        topic,
        application,
    ):

        # Temporary deterministic analysis.
        #
        # Replace this implementation with the real AI
        # integration when the AI app is connected.

        content = application.content.strip()

        if not content:
            return {
                "score": 0,
                "mastery_level": "beginner",
                "understood": [],
                "applied": [],
                "strengths": [],
                "weaknesses": [
                    "No application content was provided."
                ],
                "errors": [],
                "needs_review": [
                    topic.title,
                ],
                "feedback": (
                    "The application does not contain "
                    "enough information for evaluation."
                ),
                "ai_metadata": {
                    "provider": "local",
                    "version": "v1",
                },
                "reviewed_by": "ai",
            }

        # Temporary baseline.
        #
        # This is intentionally simple until the AI app
        # is connected.

        score = 50

        return {
            "score": score,
            "mastery_level": "developing",

            "understood": [
                "Application submitted for analysis."
            ],

            "applied": [
                "User provided a practical application."
            ],

            "strengths": [
                "The user attempted to apply the topic."
            ],

            "weaknesses": [
                "A deeper analysis is required."
            ],

            "errors": [],

            "needs_review": [
                topic.title,
            ],

            "feedback": (
                "The application was submitted successfully. "
                "A full AI analysis should be connected through "
                "the AI application."
            ),

            "ai_metadata": {
                "provider": "local",
                "version": "v1",
            },

            "reviewed_by": "ai",
        }
