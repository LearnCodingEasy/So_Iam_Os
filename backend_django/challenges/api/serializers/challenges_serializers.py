from rest_framework import serializers
from challenges.models import Challenge, ChallengeStep, ChallengeAttempt, ChallengeProgress


class UserOwnedChallengeSerializer(serializers.ModelSerializer):
    """Prevent nested challenge records from crossing user ownership."""

    def validate_challenge(self, challenge):
        request = self.context.get("request")
        if request and challenge.user_id != request.user.pk:
            raise serializers.ValidationError(
                "You can only use challenges that belong to your account."
            )
        return challenge


class ChallengeStepSerializer(UserOwnedChallengeSerializer):
    class Meta: model=ChallengeStep; fields='__all__'


class ChallengeSerializer(serializers.ModelSerializer):
    steps=ChallengeStepSerializer(many=True,read_only=True)
    class Meta: model=Challenge; fields='__all__'; read_only_fields=['user','created_at','updated_at']


class ChallengeAttemptSerializer(UserOwnedChallengeSerializer):
    class Meta: model=ChallengeAttempt; fields='__all__'; read_only_fields=['user','created_at']


class ChallengeProgressSerializer(UserOwnedChallengeSerializer):
    class Meta: model=ChallengeProgress; fields='__all__'; read_only_fields=['user','updated_at']
