from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Challenge,ChallengeStep,ChallengeAttempt,ChallengeProgress
from .serializers import ChallengeSerializer,ChallengeStepSerializer,ChallengeAttemptSerializer,ChallengeProgressSerializer
class Owned(viewsets.ModelViewSet): permission_classes=[IsAuthenticated]
class ChallengeViewSet(Owned):
    serializer_class=ChallengeSerializer
    def get_queryset(self): return Challenge.objects.filter(user=self.request.user).prefetch_related('steps')
    def perform_create(self,s): s.save(user=self.request.user)
class ChallengeStepViewSet(Owned):
    serializer_class=ChallengeStepSerializer
    def get_queryset(self): return ChallengeStep.objects.filter(challenge__user=self.request.user)
class ChallengeAttemptViewSet(Owned):
    serializer_class=ChallengeAttemptSerializer
    def get_queryset(self): return ChallengeAttempt.objects.filter(user=self.request.user)
    def perform_create(self,s): s.save(user=self.request.user)
class ChallengeProgressViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]; serializer_class=ChallengeProgressSerializer
    def get_queryset(self): return ChallengeProgress.objects.filter(user=self.request.user)
    def perform_create(self,s): s.save(user=self.request.user)
