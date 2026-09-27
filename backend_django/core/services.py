from django.core.cache import cache
from django.db import transaction
from django.utils import timezone
from knowledge.models import KnowledgeFile, KnowledgeItem
from goals.models import Goal
from tasks.models import Task
from learning.models import LearningGoal, LearningPath, LearningProgress, Skill
from jobs_opportunity.models import JobOpportunity, JobMatch, JobApplication

class BaseService:
    @staticmethod
    @transaction.atomic
    def save(instance): instance.save(); return instance
    @staticmethod
    @transaction.atomic
    def delete(instance): instance.delete()

class DashboardService:
    @staticmethod
    def get_data(*, user):
        key=f"dashboard:{user.pk}"
        try:
            cached=cache.get(key)
            if cached: return cached
        except Exception:
            cached=None
        today=timezone.localdate()
        goals=Goal.objects.filter(user=user)
        tasks=Task.objects.filter(user=user)
        learning_goals=LearningGoal.objects.filter(user=user)
        paths=LearningPath.objects.filter(user=user)
        knowledge=KnowledgeItem.objects.filter(user=user,is_archived=False)
        jobs=JobOpportunity.objects.filter(user=user,is_active=True)
        matches=JobMatch.objects.filter(user=user)
        applications=JobApplication.objects.filter(user=user)
        recent_tasks=list(tasks.filter(scheduled_date=today).order_by("sort_order","-priority")[:8].values("id","title","status","priority","scheduled_date","due_at"))
        data={
            "user":{"id":str(user.id),"name":user.full_name,"email":user.email},
            "date":{"now":timezone.now(),"local_date":today},
            "stats":{
                "tasks":{"total":tasks.count(),"today":tasks.filter(scheduled_date=today).count(),"pending":tasks.filter(status__in=["pending","in_progress"]).count(),"completed":tasks.filter(status="completed").count()},
                "goals":{"total":goals.count(),"in_progress":goals.filter(status="active").count(),"completed":goals.filter(status="completed").count()},
                "learning":{"goals":learning_goals.count(),"paths":paths.count(),"active_paths":paths.filter(status="active").count()},
                "knowledge":{"total":knowledge.count(),"files":KnowledgeFile.objects.filter(knowledge__user=user,knowledge__is_archived=False).count()},
                "jobs":{"total":jobs.count(),"matches":matches.filter(score__gte=70).count(),"applications":applications.count()},
                "skills":{"total":Skill.objects.filter(learning_goals__user=user).distinct().count()},
            },
            "tasks":recent_tasks,
            "recent":{"knowledge":list(knowledge.order_by("-updated_at")[:5].values("id","title","knowledge_type","updated_at")),"jobs":list(jobs.order_by("-published_at","-discovered_at")[:5].values("id","title","company","is_remote","url"))},
            "system":{"online":True,"generated_at":timezone.now()},
        }
        try:
            cache.set(key,data,60)
        except Exception:
            pass
        return data
