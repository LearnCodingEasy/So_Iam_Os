from django.contrib import admin

from revenue.models import RevenueSource, RevenueStream, RevenueRecord, RecurringRevenue

@admin.register(RevenueSource)
class RevenueSourceAdmin(admin.ModelAdmin):
    list_per_page = 50


@admin.register(RevenueStream)
class RevenueStreamAdmin(admin.ModelAdmin):
    list_per_page = 50


@admin.register(RevenueRecord)
class RevenueRecordAdmin(admin.ModelAdmin):
    list_per_page = 50


@admin.register(RecurringRevenue)
class RecurringRevenueAdmin(admin.ModelAdmin):
    list_per_page = 50
