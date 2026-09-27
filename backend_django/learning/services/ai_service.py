from learning.models import (
    KnowledgeApplication,
    LearningTopic,
)


class LearningAIService:
    """
    AI abstraction layer for the learning system.

    Currently this provides a deterministic local analysis.

    Later it can be connected to:
        - OpenAI
        - internal AI service
        - knowledge analysis engine
        - external LLM provider
    """

    # ========================================================
    # 🤖 Analyze Application
    # ========================================================

    @staticmethod
    def analyze_application(
        *,
        topic,
        application,
    ):
        """
        Analyze a KnowledgeApplication.

        Returns data compatible with ApplicationReview.
        """

        if not topic:
            raise ValueError(
                "Topic is required for AI analysis."
            )

        if not application:
            raise ValueError(
                "Application is required for AI analysis."
            )

        # ----------------------------------------------------
        # Ownership / consistency
        # ----------------------------------------------------

        if application.topic_id != topic.id:
            raise ValueError(
                "Application does not belong to this topic."
            )

        # ----------------------------------------------------
        # Content
        # ----------------------------------------------------

        content = (
            application.content
            or ""
        ).strip()

        # ====================================================
        # Empty Application
        # ====================================================

        if not content:

            score = 0

            return {
                "score": score,

                "mastery_level": (
                    LearningAIService
                    .calculate_mastery(score)
                ),

                "understood": [],

                "applied": [],

                "strengths": [],

                "weaknesses": [
                    "No application content was provided."
                ],

                "errors": [],

                "needs_review": [
                    topic.title
                ],

                "knowledge_gaps": [
                    topic.title
                ],

                "recommendations": [
                    "Add a practical explanation "
                    "of how the topic was applied."
                ],

                "feedback": (
                    "The application does not contain "
                    "enough information for evaluation."
                ),

                "ai_metadata": {
                    "provider": "local",
                    "version": "v2",
                    "mode": "deterministic",
                },

                "reviewed_by": "ai",
            }

        # ====================================================
        # Temporary baseline analysis
        # ====================================================

        score = 50

        return {
            "score": score,

            "mastery_level": (
                LearningAIService
                .calculate_mastery(score)
            ),

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
                topic.title
            ],

            "knowledge_gaps": [
                "A deeper practical understanding "
                "of the topic is recommended."
            ],

            "recommendations": [
                "Provide a more detailed explanation "
                "of the practical implementation."
            ],

            "feedback": (
                "The application was submitted successfully. "
                "A full AI analysis should be connected "
                "through the AI application."
            ),

            "ai_metadata": {
                "provider": "local",
                "version": "v2",
                "mode": "deterministic",
            },

            "reviewed_by": "ai",
        }

    # ========================================================
    # 🧠 Calculate Mastery
    # ========================================================

    @staticmethod
    def calculate_mastery(score):
        """
        Convert numeric score into mastery level.
        """

        try:
            score = float(score or 0)
        except (
            TypeError,
            ValueError,
        ):
            score = 0

        if score < 30:
            return "beginner"

        if score < 50:
            return "developing"

        if score < 70:
            return "competent"

        if score < 90:
            return "advanced"

        return "mastered"
