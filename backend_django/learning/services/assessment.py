from learning.models import AssessmentAttempt


class AssessmentService:

    @staticmethod
    def submit_attempt(
        *,
        user,
        assessment,
        score,
        feedback="",
    ):
        if assessment.topic.path.user_id != user.id:
            raise ValueError(
                "Assessment does not belong to this user."
            )

        passed = score >= assessment.passing_score

        return AssessmentAttempt.objects.create(
            user=user,
            assessment=assessment,
            score=score,
            passed=passed,
            feedback=feedback,
        )
