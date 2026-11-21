# challenges security and testing

## Permission/ownership evidence

- challenges/api/views/challenges_views.py:L2: from rest_framework.permissions import IsAuthenticated
- challenges/api/views/challenges_views.py:L7: class Owned(viewsets.ModelViewSet): permission_classes=[IsAuthenticated]
- challenges/api/views/challenges_views.py:L12: def get_queryset(self): return Challenge.objects.filter(user=self.request.user).prefetch_related('steps')
- challenges/api/views/challenges_views.py:L13: def perform_create(self,s): s.save(user=self.request.user)
- challenges/api/views/challenges_views.py:L18: def get_queryset(self): return ChallengeStep.objects.filter(challenge__user=self.request.user)
- challenges/api/views/challenges_views.py:L23: def get_queryset(self): return ChallengeAttempt.objects.filter(user=self.request.user)
- challenges/api/views/challenges_views.py:L24: def perform_create(self,s): s.save(user=self.request.user)
- challenges/api/views/challenges_views.py:L28: permission_classes=[IsAuthenticated]; serializer_class=ChallengeProgressSerializer
- challenges/api/views/challenges_views.py:L29: def get_queryset(self): return ChallengeProgress.objects.filter(user=self.request.user)
- challenges/api/views/challenges_views.py:L30: def perform_create(self,s): s.save(user=self.request.user)


## Tests
- challenges/tests/test_challenges.py
- challenges/tests/__init__.py


Tests were not run. This scan is not a complete authorization/security review. Shared guidance: [authentication and permissions](../../07-authentication-and-permissions.md).
