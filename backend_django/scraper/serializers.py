from rest_framework import serializers
from .models import Website, ParentSelector, ScrapingConfig, ScrapingJob, ScrapedData


class WebsiteSerializer(serializers.ModelSerializer):
    last_run_id = serializers.SerializerMethodField()

    class Meta:
        model = Website
        fields = ["id", "name", "base_url", "description", "is_active", "source_type",
                  "config", "request_timeout", "last_run_at", "last_status", "last_error",
                  "created_at", "updated_at", "last_run_id"]
        read_only_fields = ["id", "created_at", "updated_at", "last_run_at", "last_status", "last_error", "last_run_id"]

    def get_last_run_id(self, obj):
        run = obj.scrapingjob_set.order_by("-started_at").first()
        return str(run.pk) if run else None

    def validate_base_url(self, value):
        from .services import validate_public_url
        validate_public_url(value)
        return value

    def validate_config(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("config must be an object.")
        if len(str(value)) > 12000:
            raise serializers.ValidationError("config is too large.")
        return value


class ParentSelectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentSelector
        fields = "__all__"


class ScrapingConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapingConfig
        fields = "__all__"


class ScrapedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapedData
        fields = ["id", "job", "data", "scraped_at", "source_url"]


class ScrapingJobSerializer(serializers.ModelSerializer):
    website_name = serializers.CharField(source="website.name", read_only=True)

    class Meta:
        model = ScrapingJob
        fields = ["id", "website", "website_name", "target_url", "status", "started_at",
                  "completed_at", "error_message", "items_scraped", "items_created",
                  "items_updated", "items_duplicate", "trigger_type"]
        read_only_fields = fields
