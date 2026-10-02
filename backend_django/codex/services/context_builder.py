from ..models import ProjectRegistry,Feature,FileRegistry,APIEndpoint,ProtectedFeature,ArchitectureNode,ArchitectureEdge,CodexPolicy,CodexTool,CodexFinding

class ContextBuilder:
    @staticmethod
    def build(project):
        return {
            "project":{"key":project.key,"name":project.name,"root_path":project.root_path},
            "features":list(Feature.objects.filter(project=project).values("key","name","app_label","status","protected")),
            "files":list(FileRegistry.objects.filter(project=project).values("path","kind","app_label","protected")),
            "apis":list(APIEndpoint.objects.filter(project=project).values("method","path","name","app_label","frontend_route","frontend_section","frontend_service","coverage_status")),
            "protected":list(ProtectedFeature.objects.filter(project=project,enabled=True).values("key","reason","paths","rules")),
            "architecture":{"nodes":ArchitectureNode.objects.filter(project=project).count(),"edges":ArchitectureEdge.objects.filter(project=project).count()},
            "tools":list(CodexTool.objects.filter(project=project,enabled=True).values("key","name","capability")),
            "security_findings":list(CodexFinding.objects.filter(project=project,resolved=False).values("category","severity","title","path","line","message")[:100]),
        }
