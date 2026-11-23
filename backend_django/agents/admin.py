from django.contrib import admin

from agents.models import Agent, AgentConfiguration, AgentRun, AgentExecution

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_per_page = 50


@admin.register(AgentConfiguration)
class AgentConfigurationAdmin(admin.ModelAdmin):
    list_per_page = 50


@admin.register(AgentRun)
class AgentRunAdmin(admin.ModelAdmin):
    list_per_page = 50


@admin.register(AgentExecution)
class AgentExecutionAdmin(admin.ModelAdmin):
    list_per_page = 50
