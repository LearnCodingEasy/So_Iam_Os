import re
from collections import Counter
from decimal import Decimal

from django.db import transaction
from django.db.models import Avg, Count, Q
from django.utils import timezone

from learning.models import LearningGoal, LearningPath, Skill
from .feature_catalog import FEATURES
from .models import (
    CompanyProfile, JobAlert, JobAnalyticsSnapshot, JobApplication, JobApplicationEvent,
    JobCoverLetter, JobInterview, JobMatch, JobOpportunity, JobPreference,
    JobRecommendation, JobReadiness, JobResume, JobSavedSearch, JobSkillGap,
    JobSkillRequirement, JobSource,
)


class JobMatchingService:
    LEVELS = {"beginner": 1, "intermediate": 2, "advanced": 3, "expert": 4}

    @classmethod
    def _user_skill_levels(cls, user):
        levels = {}
        for item in user.skills or []:
            if isinstance(item, dict):
                name = item.get("slug") or item.get("name")
                if name:
                    levels[str(name).lower()] = cls.LEVELS.get(item.get("level", "intermediate"), 2)
        for goal in user.learning_goals.select_related("skill").filter(status__in=["active", "paused"]):
            if not goal.skill:
                continue
            key = goal.skill.slug.lower()
            level = cls.LEVELS.get(goal.current_level or "beginner", 1)
            levels[key] = max(levels.get(key, 0), level)
        return levels

    @classmethod
    def calculate(cls, user, job):
        levels = cls._user_skill_levels(user)
        matched, missing, weighted, total = [], [], 0.0, 0.0
        for req in job.skill_requirements.select_related("skill"):
            weight = req.importance * (1.25 if req.requirement_type == "required" else 0.65)
            total += weight
            user_level = levels.get(req.skill.slug.lower(), 0)
            required_level = cls.LEVELS.get(req.required_level, 2)
            user_level_name = next((k for k, v in cls.LEVELS.items() if v == user_level), None)
            item = {"id": req.skill_id, "name": req.skill.name, "required_level": req.required_level, "user_level": user_level_name, "requirement_type": req.requirement_type, "importance": req.importance}
            if user_level >= required_level:
                matched.append(item)
                weighted += weight
            elif user_level:
                missing.append({**item, "reason": "skill level below requirement"})
                weighted += weight * (user_level / required_level) * 0.5
            else:
                missing.append({**item, "reason": "skill not found"})

        skill_score = round(weighted / total * 100) if total else 0
        pref = getattr(user, "job_preference", None)
        location_score = 50
        salary_score = 50
        preference_score = 50
        reasons = []
        if job.is_remote:
            reasons.append("Remote opportunity.")
        if pref:
            if pref.remote_preference == JobPreference.RemotePreference.REMOTE:
                location_score = 100 if job.location_type == "remote" or job.is_remote else 25
            elif pref.remote_preference == JobPreference.RemotePreference.HYBRID:
                location_score = 100 if job.location_type == "hybrid" else 50
            elif pref.remote_preference == JobPreference.RemotePreference.ONSITE:
                location_score = 100 if job.location_type == "onsite" else 35
            if pref.locations:
                location_score = max(location_score, 100 if any(x.lower() in job.location.lower() for x in pref.locations) else 30)
            if pref.min_salary is not None and job.salary_max is not None:
                salary_score = 100 if job.salary_max >= pref.min_salary else 20
            if pref.max_salary is not None and job.salary_min is not None:
                salary_score = min(salary_score, 100 if job.salary_min <= pref.max_salary else 40)
            if pref.preferred_companies:
                preference_score = 100 if any(x.lower() in job.company.lower() for x in pref.preferred_companies) else 60
            if pref.excluded_companies and any(x.lower() in job.company.lower() for x in pref.excluded_companies):
                preference_score = 0
                reasons.append("Company is in your excluded-company list.")
        goal_score = 50
        goals = list(user.learning_goals.filter(status__in=["active", "paused"]).select_related("skill"))
        goal_slugs = {g.skill.slug.lower() for g in goals if g.skill}
        job_slugs = {r.skill.slug.lower() for r in job.skill_requirements.select_related("skill")}
        if goal_slugs and job_slugs:
            overlap = len(goal_slugs & job_slugs)
            goal_score = round(overlap / max(len(job_slugs), 1) * 100)
            if overlap:
                reasons.append(f"Matches {overlap} active learning goal skill(s).")
        experience_score = 50
        if job.experience_level == "entry": experience_score = 100
        elif job.experience_level in {"junior", "mid", "senior", "lead", "executive"}: experience_score = 75
        weights = (pref.score_weights if pref else {}) or {}
        default_weights = {"skill": 0.45, "experience": 0.12, "preference": 0.13, "goal": 0.12, "salary": 0.08, "location": 0.10}
        merged = {**default_weights, **{k: float(v) for k, v in weights.items() if k in default_weights}}
        total_weight = sum(merged.values()) or 1
        score = round((skill_score * merged["skill"] + experience_score * merged["experience"] + preference_score * merged["preference"] + goal_score * merged["goal"] + salary_score * merged["salary"] + location_score * merged["location"]) / total_weight)
        if matched:
            reasons.append(f"Matched {len(matched)} required/preferred skill(s) at the requested level.")
        if missing:
            reasons.append(f"There are {len(missing)} skill gap(s) to improve.")
        breakdown = {"skill": skill_score, "experience": experience_score, "preference": preference_score, "goal": goal_score, "salary": salary_score, "location": location_score}
        match, _ = JobMatch.objects.update_or_create(user=user, job=job, defaults={"score": max(0, min(100, score)), "skill_score": skill_score, "experience_score": experience_score, "preference_score": preference_score, "goal_score": goal_score, "salary_score": salary_score, "location_score": location_score, "matched_skills": matched, "missing_skills": missing, "reasons": reasons, "breakdown": breakdown})
        JobGapService.sync_from_match(user, match)
        ReadinessService.calculate(user, job, match=match)
        return match

    @classmethod
    def refresh_for_user(cls, user):
        jobs = JobOpportunity.objects.filter(user=user, is_active=True).prefetch_related("skill_requirements__skill")
        return [cls.calculate(user, job) for job in jobs]


class JobGapService:
    @staticmethod
    def sync_from_match(user, match):
        existing = {g.name: g for g in JobSkillGap.objects.filter(user=user, job=match.job)}
        for item in match.missing_skills:
            severity = "critical" if item.get("requirement_type") == "required" and item.get("importance", 1) >= 4 else "high" if item.get("requirement_type") == "required" else "medium"
            skill = Skill.objects.filter(pk=item.get("id")).first()
            JobSkillGap.objects.update_or_create(user=user, job=match.job, name=item["name"], defaults={"skill": skill, "required_level": item.get("required_level", "intermediate"), "current_level": item.get("user_level") or "", "severity": severity})
        for name, gap in existing.items():
            if name not in {x.get("name") for x in match.missing_skills} and gap.status != "ready":
                gap.status = "ready"
                gap.save(update_fields=["status", "updated_at"])

    @staticmethod
    @transaction.atomic
    def create_learning_goal(user, gap):
        if gap.learning_goal_id:
            return gap.learning_goal
        goal = LearningGoal.objects.create(user=user, skill=gap.skill, title=f"Become job-ready: {gap.name}", description=f"Close the skill gap for {gap.job.title} at {gap.job.company or 'the target company'}.", reason=f"Required for job opportunity #{gap.job_id}", current_level=gap.current_level or "beginner", target_level=gap.required_level)
        gap.learning_goal = goal
        gap.status = JobSkillGap.Status.LEARNING
        gap.save(update_fields=["learning_goal", "status", "updated_at"])
        return goal


class JobParserService:
    LEVEL_PATTERNS = [("executive", r"\b(vp|vice president|chief|director|head of)\b"), ("lead", r"\b(lead|principal|staff)\b"), ("senior", r"\b(senior|sr\.?|5\+ years|6\+ years|7\+ years)\b"), ("mid", r"\b(mid|middle|3\+ years|4\+ years)\b"), ("junior", r"\b(junior|jr\.?|1\+ years|2\+ years)\b"), ("entry", r"\b(entry|graduate|intern|trainee)\b")]
    REMOTE_WORDS = ("remote", "work from home", "wfh", "hybrid")

    @classmethod
    def analyze(cls, job):
        text = f"{job.title}\n{job.description}".lower()
        level = "unknown"
        for candidate, pattern in cls.LEVEL_PATTERNS:
            if re.search(pattern, text):
                level = candidate
                break
        location_type = "remote" if any(x in text for x in ("fully remote", "100% remote", "remote position", "remote job")) else "hybrid" if "hybrid" in text else "onsite" if any(x in text for x in ("on-site", "onsite", "office-based")) else ("remote" if job.is_remote else "unknown")
        if location_type == "remote": job.is_remote = True
        skills = []
        for skill in Skill.objects.filter(is_active=True):
            if re.search(rf"\b{re.escape(skill.name.lower())}\b", text) or re.search(rf"\b{re.escape(skill.slug.lower())}\b", text):
                skills.append(skill)
        responsibilities = [x.strip(" -•\t") for x in re.split(r"[\n.]", job.description) if any(w in x.lower() for w in ("responsibil", "develop", "build", "design", "maintain", "implement"))][:12]
        benefits = [x.strip(" -•\t") for x in re.split(r"[\n.]", job.description) if any(w in x.lower() for w in ("benefit", "insurance", "vacation", "bonus", "health"))][:12]
        red_flags = []
        if not job.company: red_flags.append("Company name is missing")
        if not job.url: red_flags.append("Application URL is missing")
        if not job.description: red_flags.append("Job description is missing")
        job.experience_level = level
        job.location_type = location_type
        job.responsibilities = responsibilities
        job.benefits = benefits
        job.extracted_requirements = [s.name for s in skills]
        job.tags = list(dict.fromkeys([job.job_type, location_type, level] + [s.slug for s in skills]))
        job.red_flags = red_flags
        job.ai_summary = (job.description[:700] + ("..." if len(job.description) > 700 else "")) if job.description else "No description available."
        job.last_checked_at = timezone.now()
        job.freshness_score = max(0, min(100, 100 - max(0, (timezone.now() - (job.published_at or job.discovered_at)).days * 3)))
        job.save(update_fields=["experience_level", "location_type", "is_remote", "responsibilities", "benefits", "extracted_requirements", "tags", "red_flags", "ai_summary", "last_checked_at", "freshness_score", "updated_at"])
        for skill in skills:
            JobSkillRequirement.objects.get_or_create(job=job, skill=skill, defaults={"required_level": "intermediate", "importance": 1})
        return job


class ReadinessService:
    @staticmethod
    def calculate(user, job, match=None):
        match = match or JobMatch.objects.filter(user=user, job=job).first()
        gaps = list(JobSkillGap.objects.filter(user=user, job=job, status__in=["open", "learning"]))
        score = match.score if match else 0
        level = "ready" if score >= 85 and not gaps else "almost_ready" if score >= 70 else "preparing" if score >= 45 else "not_ready"
        actions = [f"Improve {g.name} ({g.severity})" for g in gaps[:6]]
        if not job.url: actions.append("Add or verify the application URL")
        if not job.description: actions.append("Add a complete job description")
        breakdown = match.breakdown if match else {}
        readiness, _ = JobReadiness.objects.update_or_create(user=user, job=job, defaults={"score": score, "level": level, "breakdown": breakdown, "next_actions": actions})
        return readiness


class JobRecommendationService:
    @staticmethod
    def refresh(user, limit=50):
        jobs = JobOpportunity.objects.filter(user=user, is_active=True).exclude(applications__user=user).prefetch_related("skill_requirements__skill")[:300]
        rows = []
        for job in jobs:
            match = JobMatchingService.calculate(user, job)
            reasons = match.reasons[:5]
            recommendation, _ = JobRecommendation.objects.update_or_create(user=user, job=job, defaults={"score": match.score, "reasons": reasons})
            rows.append(recommendation)
        return sorted(rows, key=lambda x: x.score, reverse=True)[:limit]


class JobAnalyticsService:
    @staticmethod
    def dashboard(user):
        jobs = JobOpportunity.objects.filter(user=user)
        apps = JobApplication.objects.filter(user=user)
        interviews = JobInterview.objects.filter(application__user=user)
        offers = apps.filter(status__in=["offer", "accepted"]).count()
        applied = apps.exclude(status="saved").count()
        interview_count = interviews.count()
        skills = Counter()
        for job in jobs.prefetch_related("skill_requirements__skill"):
            for req in job.skill_requirements.all(): skills[req.skill.name] += 1
        salaries = list(jobs.exclude(salary_min__isnull=True).values_list("salary_min", flat=True))
        snapshot = {"jobs": jobs.count(), "active_jobs": jobs.filter(is_active=True).count(), "saved": apps.filter(status="saved").count(), "applied": applied, "interviews": interview_count, "offers": offers, "rejected": apps.filter(status="rejected").count(), "application_conversion_rate": round(interview_count / applied * 100) if applied else 0, "interview_rate": round(interview_count / applied * 100) if applied else 0, "offer_rate": round(offers / applied * 100) if applied else 0, "avg_salary_min": round(float(sum(salaries) / len(salaries)), 2) if salaries else None, "remote_jobs": jobs.filter(is_remote=True).count(), "top_skills": skills.most_common(10), "sources": list(jobs.values("source__name").annotate(count=Count("id")).order_by("-count")[:10])}
        JobAnalyticsSnapshot.objects.update_or_create(user=user, snapshot_date=timezone.localdate(), defaults={"metrics": snapshot})
        return snapshot


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
        JobParserService.analyze(job)
        JobMatchingService.calculate(user, job)
        return job

    @staticmethod
    def apply(user, job, **data):
        status = data.get("status", "saved")
        resume_id = data.get("resume_id")
        cover_letter_id = data.get("cover_letter_id")
        if resume_id and not JobResume.objects.filter(pk=resume_id, user=user).exists():
            data.pop("resume_id", None)
        if cover_letter_id and not JobCoverLetter.objects.filter(pk=cover_letter_id, user=user, job=job).exists():
            data.pop("cover_letter_id", None)
        if status == "applied" and not data.get("applied_at"):
            data["applied_at"] = timezone.now()
        application, created = JobApplication.objects.update_or_create(user=user, job=job, defaults=data)
        JobApplicationEvent.objects.create(application=application, event_type="status", title=f"Application status: {application.get_status_display()}", metadata={"status": application.status})
        return application
