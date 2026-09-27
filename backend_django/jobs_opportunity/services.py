from django.db import transaction
from django.utils import timezone
from learning.models import Skill
from .models import JobApplication, JobMatch, JobOpportunity, JobSource, JobSkillRequirement


class JobMatchingService:
    LEVELS = {"beginner": 1, "intermediate": 2, "advanced": 3, "expert": 4}

    @classmethod
    def calculate(cls, user, job):
        raw_skills = user.skills or []
        ids, names = [], []
        for item in raw_skills:
            if isinstance(item, dict):
                if item.get("id"):
                    ids.append(item["id"])
                if item.get("slug"):
                    names.append(item["slug"])
                if item.get("name"):
                    names.append(item["name"])
            elif isinstance(item, int) or (isinstance(item, str) and item.isdigit()):
                ids.append(int(item))
            elif isinstance(item, str):
                names.append(item)
        qs = Skill.objects.filter(is_active=True)
        user_skills = {s.slug: s for s in qs.filter(id__in=ids)}
        if names:
            for skill in qs.filter(slug__in=names) | qs.filter(name__in=names):
                user_skills[skill.slug] = skill
        # Learning goals are also evidence of active skills.
        for skill in qs.filter(learning_goals__user=user).distinct():
            user_skills.setdefault(skill.slug, skill)
        matched, missing, weighted, total = [], [], 0, 0
        for req in job.skill_requirements.select_related("skill"):
            weight = req.importance
            total += weight
            if req.skill.slug in user_skills:
                matched.append({"id": req.skill_id, "name": req.skill.name, "required_level": req.required_level})
                weighted += weight
            else:
                missing.append({"id": req.skill_id, "name": req.skill.name, "required_level": req.required_level})
        score = round(weighted / total * 100) if total else 0
        reasons = [f"Matched {len(matched)} of {len(matched) + len(missing)} required skills."]
        if job.is_remote:
            reasons.append("Remote opportunity.")
        match, _ = JobMatch.objects.update_or_create(user=user, job=job, defaults={"score": score, "matched_skills": matched, "missing_skills": missing, "reasons": reasons})
        return match

    @classmethod
    def refresh_for_user(cls, user):
        jobs = JobOpportunity.objects.filter(user=user, is_active=True).prefetch_related("skill_requirements__skill")
        return [cls.calculate(user, job) for job in jobs]


class JobService:
    @staticmethod
    @transaction.atomic
    def save_source(user, **data):
        return JobSource.objects.create(user=user, **data)

    @staticmethod
    @transaction.atomic
    def create_job(user, **data):
        requirements = data.pop("skill_ids", [])
        job = JobOpportunity.objects.create(user=user, **data)
        skills = Skill.objects.filter(id__in=requirements, is_active=True)
        JobSkillRequirement.objects.bulk_create([JobSkillRequirement(job=job, skill=s) for s in skills], ignore_conflicts=True)
        JobMatchingService.calculate(user, job)
        return job

    @staticmethod
    def apply(user, job, **data):
        return JobApplication.objects.update_or_create(user=user, job=job, defaults=data)
