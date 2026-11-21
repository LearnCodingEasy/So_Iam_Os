from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from jobs_opportunity.models import JobCoverLetter, JobOpportunity, JobResume
from jobs_opportunity.api.serializers import JobApplicationSerializer, JobCoverLetterSerializer, JobMatchSerializer, JobOpportunitySerializer, JobReadinessSerializer
from jobs_opportunity.services import JobMatchingService, JobParserService, JobService, ReadinessService
from jobs_opportunity.api.views.user_owned_views import UserOwnedViewSet


class JobOpportunityViewSet(UserOwnedViewSet):
    serializer_class = JobOpportunitySerializer

    def get_queryset(self):
        qs = JobOpportunity.objects.filter(user=self.request.user).select_related(
            "source", "company_profile").prefetch_related("skill_requirements__skill", "matches", "readiness_records")
        p = self.request.query_params
        q = p.get("q")
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(company__icontains=q) | Q(
                description__icontains=q) | Q(location__icontains=q))
        if p.get("remote") == "true":
            qs = qs.filter(is_remote=True)
        if p.get("job_type"):
            qs = qs.filter(job_type=p["job_type"])
        if p.get("experience"):
            qs = qs.filter(experience_level=p["experience"])
        if p.get("location"):
            qs = qs.filter(location__icontains=p["location"])
        if p.get("skill"):
            qs = qs.filter(
                skill_requirements__skill__slug__iexact=p["skill"]).distinct()
        if p.get("salary_min"):
            qs = qs.filter(salary_max__gte=p["salary_min"])
        if p.get("salary_max"):
            qs = qs.filter(salary_min__lte=p["salary_max"])
        if p.get("source"):
            qs = qs.filter(source_id=p["source"])
        if p.get("active") in {"true", "false"}:
            qs = qs.filter(is_active=p["active"] == "true")
        if p.get("fresh") == "true":
            qs = qs.order_by("-published_at", "-discovered_at")
        return qs.distinct()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)
        data["skill_ids"] = request.data.get("skill_ids", [])
        job = JobService.create_job(request.user, **data)
        return Response(self.get_serializer(job).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def refresh_match(self, request, pk=None):
        match = JobMatchingService.calculate(request.user, self.get_object())
        return Response(JobMatchSerializer(match, context={"request": request}).data)

    @action(detail=True, methods=["post"])
    def analyze(self, request, pk=None):
        job = JobParserService.analyze(self.get_object(), user=request.user, use_ai=True)
        JobMatchingService.calculate(request.user, job)
        return Response(self.get_serializer(job).data)

    @action(detail=True, methods=["get"])
    def readiness(self, request, pk=None):
        readiness = ReadinessService.calculate(request.user, self.get_object())
        return Response(JobReadinessSerializer(readiness).data)

    @action(detail=True, methods=["get"])
    def similar(self, request, pk=None):
        job = self.get_object()
        terms = [x for x in [job.company, job.location, job.job_type] if x]
        qs = self.get_queryset().exclude(pk=job.pk)
        if terms:
            qs = qs.filter(Q(company__icontains=job.company) | Q(
                location__icontains=job.location) | Q(job_type=job.job_type))
        return Response(self.get_serializer(qs[:20], many=True).data)

    @action(detail=False, methods=["get"])
    def compare(self, request):
        ids = [x for x in request.query_params.get("ids", "").split(",") if x]
        return Response(self.get_serializer(self.get_queryset().filter(id__in=ids), many=True).data)

    @action(detail=True, methods=["post"], url_path="generate_cover_letter")
    def generate_cover_letter(self, request, pk=None):
        """Generate and persist a cover letter using the user's configured AI provider."""
        job = self.get_object()
        from jobs_opportunity.models import JobResume, JobCoverLetter
        from ai.models import AISettings
        from ai.providers import AIProviderFallbackChain

        resume_id = request.data.get("resume_id")
        resume = None
        if resume_id:
            resume = JobResume.objects.filter(
                pk=resume_id, user=request.user).first()
            if not resume:
                return Response({"detail": "Resume not found for this user."}, status=400)
        else:
            resume = JobResume.objects.filter(
                user=request.user, is_default=True).first()

        settings_obj, _ = AISettings.objects.get_or_create(user=request.user)
        provider_name = settings_obj.preferred_provider or "ollama"
        resume_text = (resume.content if resume else "")[:10000]
        prompt = (
            "Write a tailored, truthful professional cover letter. Do not invent qualifications. "
            "Use the candidate resume and job details below. Return only the letter text.\n\n"
            f"JOB TITLE: {job.title}\nCOMPANY: {job.company}\nLOCATION: {job.location}\n"
            f"JOB DESCRIPTION: {job.description[:12000]}\n"
            f"CANDIDATE RESUME: {resume_text or 'No resume content supplied; avoid asserting specific experience.'}\n"
            f"ADDITIONAL USER CONTEXT: {str(request.data.get('context', ''))[:3000]}"
        )
        try:
            result = AIProviderFallbackChain(user=request.user).generate(
                provider=provider_name,
                messages=[
                    {"role": "system", "content": "You are a careful career-writing assistant. Be specific, professional, concise, and truthful."},
                    {"role": "user", "content": prompt},
                ],
                model=settings_obj.preferred_model or None,
            )
        except Exception as exc:
            return Response({"detail": f"AI provider failed to generate the letter: {str(exc)[:300]}"}, status=502)
        content = (result.get("content") or "").strip()
        if not content:
            return Response({"detail": "The configured AI provider returned an empty response."}, status=502)
        letter = JobCoverLetter.objects.create(
            user=request.user, job=job, resume=resume,
            title=f"Cover Letter — {job.title}", content=content, generated=True,
        )
        return Response(JobCoverLetterSerializer(letter, context={"request": request}).data, status=201)

    @action(detail=True, methods=["post"])
    def apply(self, request, pk=None):
        application = JobService.apply(request.user, self.get_object(), status=request.data.get("status", "saved"), notes=request.data.get("notes", ""), resume_id=request.data.get(
            "resume"), cover_letter_id=request.data.get("cover_letter"), deadline=request.data.get("deadline"), expected_salary=request.data.get("expected_salary"))
        return Response(JobApplicationSerializer(application, context={"request": request}).data)
