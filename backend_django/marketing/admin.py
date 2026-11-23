from django.contrib import admin

from marketing.models import MarketingChannel, Campaign, MarketingContent, LeadSource

@admin.register(MarketingChannel)
class MarketingChannelAdmin(admin.ModelAdmin):
    list_per_page = 50


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_per_page = 50


@admin.register(MarketingContent)
class MarketingContentAdmin(admin.ModelAdmin):
    list_per_page = 50


@admin.register(LeadSource)
class LeadSourceAdmin(admin.ModelAdmin):
    list_per_page = 50
