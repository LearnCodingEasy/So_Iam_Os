from django.contrib import admin

from sales.models import Offer, Deal, Sale, SalesActivity

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_per_page = 50


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_per_page = 50


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_per_page = 50


@admin.register(SalesActivity)
class SalesActivityAdmin(admin.ModelAdmin):
    list_per_page = 50
