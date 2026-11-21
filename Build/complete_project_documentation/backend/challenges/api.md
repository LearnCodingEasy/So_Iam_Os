# challenges API

Project prefix: /api/challenges/ (source: backend_django/backend_django/urls.py). Route rows below are declarations; DRF router methods are implicit and not runtime-verified.


## Routes: challenges/api/urls.py

- L3: router=DefaultRouter(); router.register('challenges',ChallengeViewSet,basename='challenge'); router.register('steps',ChallengeStepViewSet,basename='challenge-step'); router.register('attempts',ChallengeAttemptViewSet,basename='challenge-attempt'); router.register('progress',ChallengeProgressViewSet,basename='challenge-progress')

## Handler declarations: challenges/api/views/challenges_views.py
L7: class Owned(viewsets.ModelViewSet): permission_classes=[IsAuthenticated]
L10: class ChallengeViewSet(Owned):
L11: serializer_class=ChallengeSerializer
L12: def get_queryset(self): return Challenge.objects.filter(user=self.request.user).prefetch_related('steps')
L13: def perform_create(self,s): s.save(user=self.request.user)
L16: class ChallengeStepViewSet(Owned):
L17: serializer_class=ChallengeStepSerializer
L18: def get_queryset(self): return ChallengeStep.objects.filter(challenge__user=self.request.user)
L21: class ChallengeAttemptViewSet(Owned):
L22: serializer_class=ChallengeAttemptSerializer
L23: def get_queryset(self): return ChallengeAttempt.objects.filter(user=self.request.user)
L24: def perform_create(self,s): s.save(user=self.request.user)
L27: class ChallengeProgressViewSet(viewsets.ModelViewSet):
L28: permission_classes=[IsAuthenticated]; serializer_class=ChallengeProgressSerializer
L29: def get_queryset(self): return ChallengeProgress.objects.filter(user=self.request.user)
L30: def perform_create(self,s): s.save(user=self.request.user)


Full payload/response compatibility remains UNKNOWN until handlers, serializers and active frontend consumers are traced. See [cross-project API catalog](../../05-complete-api-catalog.md).
