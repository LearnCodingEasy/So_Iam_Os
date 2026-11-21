from rest_framework import serializers
from jobs_opportunity.models import JobSkillRequirement


class JobSkillRequirementSerializer(serializers.ModelSerializer):
    skill_name = serializers.CharField(source="skill.name", read_only=True)

    class Meta:
        model = JobSkillRequirement
        fields = ["id", "skill", "skill_name",
                  "required_level", "importance", "requirement_type"]
