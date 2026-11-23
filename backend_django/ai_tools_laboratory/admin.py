from django.contrib import admin

from ai_tools_laboratory.models import ToolCategory, Tool, ToolConfiguration, ToolExecution

@admin.register(ToolCategory)
class ToolCategoryAdmin(admin.ModelAdmin):
    list_per_page = 50


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_per_page = 50


@admin.register(ToolConfiguration)
class ToolConfigurationAdmin(admin.ModelAdmin):
    list_per_page = 50


@admin.register(ToolExecution)
class ToolExecutionAdmin(admin.ModelAdmin):
    list_per_page = 50
