from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Project,ProjectMember,ProjectContext
from .serializers import ProjectSerializer,ProjectMemberSerializer,ProjectContextSerializer
class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]; serializer_class=ProjectSerializer
    def get_queryset(self): return Project.objects.filter(user=self.request.user).prefetch_related('members')
    def perform_create(self,s): s.save(user=self.request.user)
    @action(detail=True,methods=['get','put','patch'])
    def context(self,request,pk=None):
        project=self.get_object(); obj,_=ProjectContext.objects.get_or_create(project=project)
        if request.method=='GET': return Response(ProjectContextSerializer(obj).data)
        ser=ProjectContextSerializer(obj,data=request.data,partial=True); ser.is_valid(raise_exception=True); ser.save(); return Response(ser.data)
class ProjectMemberViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]; serializer_class=ProjectMemberSerializer
    def get_queryset(self): return ProjectMember.objects.filter(project__user=self.request.user)
class ProjectContextViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes=[IsAuthenticated]; serializer_class=ProjectContextSerializer
    def get_queryset(self): return ProjectContext.objects.filter(project__user=self.request.user)
