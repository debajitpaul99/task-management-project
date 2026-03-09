from django.contrib import admin
from users.models import UserProfile
from django.contrib.auth.admin import UserAdmin

# Register your models here.
@admin.register(UserProfile)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {
            "fields": (
                ["username", "password"]
            ),
        }),
        ("Personal Info", {
            "fields": (
                ["first_name", "last_name", "email", "bio", "profile_image"]
            )
        }),
        ("Permissions", {
            "fields": (
                ["is_staff", "is_active", "is_superuser", "groups", "user_permissions"]
            )
        }),
        ("Important Dates", {
            "fields": (
                ["last_login", "date_joined"]
            )
        })
    )

    search_fields = ["username", "email", "first_name", "last_name"]
    ordering = ["username"]