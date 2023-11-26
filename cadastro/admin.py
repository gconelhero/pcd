from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm, MemberForm
from .models import CustomUser, Member


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "name", "last_name", "birthday", "phone", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password", "name", "last_name", "birthday", "phone",)}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)

class MemberAdmin(admin.ModelAdmin):
    add_form = MemberForm
    form = MemberForm
    model = Member
    list_display = ("member", "state", "city", "address")
    list_filter = ("member", "state", "city", "address")
    fieldsets = (
        (None, {"fields": ("state", "city", "address", "file_report", "profile_image")}),
        
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("member", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("member",)
    ordering = ("member",)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Member, MemberAdmin)