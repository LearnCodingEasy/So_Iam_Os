from django.contrib import admin
from .models import JobApplication, JobMatch, JobOpportunity, JobSkillRequirement, JobSource
admin.site.register([JobSource, JobOpportunity, JobSkillRequirement, JobMatch, JobApplication])
