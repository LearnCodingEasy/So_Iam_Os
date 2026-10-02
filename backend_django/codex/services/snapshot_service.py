from django.utils.timezone import now
from ..models import ProjectRegistry,ProjectSnapshot,FileRegistry

class SnapshotService:
    @staticmethod
    def create(*,user,label):
        project=ProjectRegistry.objects.get(key="so_iam_os")
        manifest={"created_at":now().isoformat(),"files":list(FileRegistry.objects.filter(project=project).values("path","sha256","size"))}
        return ProjectSnapshot.objects.create(project=project,created_by=user,label=label,manifest=manifest)
