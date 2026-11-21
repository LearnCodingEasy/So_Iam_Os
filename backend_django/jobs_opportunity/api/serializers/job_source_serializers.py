from rest_framework import serializers
from jobs_opportunity.models import JobSource


class JobSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSource
        fields = "__all__"
        read_only_fields = ["user", "last_synced_at", "last_sync_status",
                            "last_sync_error", "last_sync_count", "created_at", "updated_at"]

    def validate(self, attrs):
        source_type = attrs.get("source_type", getattr(
            self.instance, "source_type", None))
        if attrs.get("feed_url") and source_type not in {"rss", "api"}:
            raise serializers.ValidationError(
                {"source_type": "A feed URL requires RSS or API source type."})
        base_url = attrs.get("base_url", getattr(self.instance, "base_url", ""))
        feed_url = attrs.get("feed_url", getattr(self.instance, "feed_url", ""))
        enabled = attrs.get("enabled", getattr(self.instance, "enabled", True))
        if enabled and source_type in {"rss", "api", "scraper"} and not (base_url or feed_url):
            raise serializers.ValidationError({"base_url": "An enabled source needs a public URL."})
        if source_type == "scraper":
            config = attrs.get("config", getattr(
                self.instance, "config", {})) or {}
            if not config.get("terms_confirmed"):
                raise serializers.ValidationError(
                    {"config": "Confirm that this source permits scraping before enabling a scraper."})
            if not (attrs.get("base_url") or getattr(self.instance, "base_url", "")):
                raise serializers.ValidationError(
                    {"base_url": "Scraper sources require a URL."})
        return attrs
