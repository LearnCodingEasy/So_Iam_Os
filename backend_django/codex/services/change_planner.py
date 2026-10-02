from ..models import ChangeSet,ProjectRegistry,ProtectedFeature

class ChangePlanner:
    @staticmethod
    def plan(*,user,title,objective,paths=None):
        project=ProjectRegistry.objects.get(key="so_iam_os")
        paths=paths or []
        protected=[]
        for rule in ProtectedFeature.objects.filter(project=project,enabled=True):
            protected += [p for p in rule.paths if any(p==x or x.startswith(p.rstrip("/")+"/") for x in paths)]
        impact={"requested_paths":paths,"protected_hits":protected,"requires_approval":bool(protected),"execution":"not_exposed_in_foundation"}
        plan=[{"step":1,"action":"analyze","paths":paths},{"step":2,"action":"review_impact"},{"step":3,"action":"approval_required" if protected else "ready_for_future_executor"}]
        return ChangeSet.objects.create(project=project,created_by=user,title=title,objective=objective,impact=impact,plan=plan)
