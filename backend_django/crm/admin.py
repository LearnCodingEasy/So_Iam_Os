from django.contrib import admin

from crm.models import Company, Contact, Interaction, CustomerRelationship

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_per_page = 50


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_per_page = 50


@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_per_page = 50


@admin.register(CustomerRelationship)
class CustomerRelationshipAdmin(admin.ModelAdmin):
    list_per_page = 50
