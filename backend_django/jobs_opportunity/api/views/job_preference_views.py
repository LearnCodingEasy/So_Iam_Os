from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from jobs_opportunity.models import JobPreference
from jobs_opportunity.api.serializers import JobPreferenceSerializer


class JobPreferenceViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        obj, _ = JobPreference.objects.get_or_create(user=request.user)
        return Response(JobPreferenceSerializer(obj).data)

    def create(self, request):
        obj, _ = JobPreference.objects.get_or_create(user=request.user)
        serializer = JobPreferenceSerializer(
            obj, data=request.data, partial=True, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data)

    @action(detail=False, methods=["patch", "put"])
    def update_preferences(self, request):
        obj, _ = JobPreference.objects.get_or_create(user=request.user)
        serializer = JobPreferenceSerializer(
            obj, data=request.data, partial=True, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data)
