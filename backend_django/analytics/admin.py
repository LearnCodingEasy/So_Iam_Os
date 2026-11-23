from django.contrib import admin

from analytics.models import Metric, MetricSnapshot, AnalyticsEvent, Report

@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_per_page = 50


@admin.register(MetricSnapshot)
class MetricSnapshotAdmin(admin.ModelAdmin):
    list_per_page = 50


@admin.register(AnalyticsEvent)
class AnalyticsEventAdmin(admin.ModelAdmin):
    list_per_page = 50


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_per_page = 50
