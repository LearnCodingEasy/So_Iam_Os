from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from jobs_opportunity.models.job_opportunity import JobOpportunity


class JobSkillRequirement(models.Model):
    job = models.ForeignKey(JobOpportunity, on_delete=models.CASCADE, related_name="skill_requirements")
    skill = models.ForeignKey("learning.Skill", on_delete=models.CASCADE, related_name="job_requirements")
    required_level = models.CharField(max_length=20, choices=[(x.value, x.label) for x in __import__("learning.models", fromlist=["Skill"]).Skill.Level], default="intermediate")
    importance = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    requirement_type = models.CharField(max_length=20, choices=[("required", "Required"), ("preferred", "Preferred"), ("optional", "Optional")], default="required")

    class Meta:
        constraints = [models.UniqueConstraint(fields=["job", "skill"], name="jobs_job_skill_unique")]
