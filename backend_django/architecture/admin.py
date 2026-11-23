from django.contrib import admin

from architecture.models import Architecture, Component, Dependency, ArchitectureDecision

@admin.register(Architecture)
class ArchitectureAdmin(admin.ModelAdmin):
    list_per_page = 50


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_per_page = 50


@admin.register(Dependency)
class DependencyAdmin(admin.ModelAdmin):
    list_per_page = 50


@admin.register(ArchitectureDecision)
class ArchitectureDecisionAdmin(admin.ModelAdmin):
    list_per_page = 50
