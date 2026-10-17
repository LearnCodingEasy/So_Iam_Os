from rest_framework import serializers
from .models import Challenge,ChallengeStep,ChallengeAttempt,ChallengeProgress
class ChallengeStepSerializer(serializers.ModelSerializer):
    class Meta: model=ChallengeStep; fields='__all__'
class ChallengeSerializer(serializers.ModelSerializer):
    steps=ChallengeStepSerializer(many=True,read_only=True)
    class Meta: model=Challenge; fields='__all__'; read_only_fields=['user','created_at','updated_at']
class ChallengeAttemptSerializer(serializers.ModelSerializer):
    class Meta: model=ChallengeAttempt; fields='__all__'; read_only_fields=['user','created_at']
class ChallengeProgressSerializer(serializers.ModelSerializer):
    class Meta: model=ChallengeProgress; fields='__all__'; read_only_fields=['user','updated_at']
