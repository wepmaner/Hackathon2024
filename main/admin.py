from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import UserInfo
from django.contrib.auth import get_user_model
Team = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Team
    list_display = ("login", "email","photo","is_staff", "is_active",)
    list_filter = ("login", "email","photo","is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("login", "email","name","password","photo")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "login", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(Team, CustomUserAdmin)
admin.site.register(UserInfo)