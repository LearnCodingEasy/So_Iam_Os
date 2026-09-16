from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        "email",
        "name",
        "surname",
        "is_active",
        "is_staff",
        "is_online",
        "date_joined",
    )

    search_fields = (
        "email",
        "name",
        "surname",
    )

    list_filter = (
        "is_active",
        "is_staff",
        "is_online",
    )

    ordering = (
        "-date_joined",
    )
