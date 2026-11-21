from rest_framework import serializers
from jobs_opportunity.models import CompanyProfile


class CompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = "__all__"
        read_only_fields = ["user", "created_at",
                            "updated_at", "normalized_name"]
