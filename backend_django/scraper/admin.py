from django.contrib import admin
from .models import Website, ParentSelector, ScrapingConfig, ScrapingJob, ScrapedData


class ScrapingConfigInline(admin.StackedInline):
    model = ScrapingConfig
    extra = 1


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ("name", "source_type", "base_url", "is_active",
                    "last_status", "last_run_at", "created_by")
    search_fields = ("name", "base_url")
    list_filter = ("is_active", "source_type", "last_status", "created_at")
    readonly_fields = ("last_run_at", "last_status", "last_error")
    # inlines = [ScrapingConfigInline]


@admin.register(ParentSelector)
class ParentSelectorAdmin(admin.ModelAdmin):
    list_display = ("website", "name", "created_at")
    search_fields = ("name", "website__name")
    list_filter = ("created_at",)
    # inlines = [ScrapingConfigInline]


@admin.register(ScrapingJob)
class ScrapingJobAdmin(admin.ModelAdmin):
    list_display = ("website", "status", "items_scraped",
                    "trigger_type", "started_at", "completed_at")
    list_filter = ("status", "trigger_type", "started_at")
    readonly_fields = ("started_at", "completed_at",
                       "error_message", "items_scraped")


@admin.register(ScrapedData)
class ScrapedDataAdmin(admin.ModelAdmin):
    list_display = ("job", "source_url", "scraped_at")
    list_filter = ("scraped_at",)
    search_fields = ("source_url",)
