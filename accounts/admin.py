from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm

from .models import User, Profile


# Register your models here.

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)


class CustomUserAdmin(UserAdmin):
    model = User
    add_form = CustomUserCreationForm
    list_display = ['email', 'is_staff', 'is_active', 'is_superuser', 'is_verified']
    list_filter = ['is_staff', 'is_active', 'is_superuser', 'is_verified']
    search_fields = ['email']
    ordering = ('email',)
    fieldsets = [
        ('Authentication', {
            'fields': [
                'email', 'password'
            ],
        }),
        ('Permissions', {
            'fields': [
                'is_staff', 'is_active', 'is_superuser',
            ],
        }),
        ('group permissions', {
            'fields': [
                'groups', 'user_permissions',
            ],
        }),
        ('important date', {
            'fields': [
                'last_login',
            ],
        }),
    ]
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff", "is_active", "is_superuser", "is_verified"
            )}
         ),
    )


admin.site.register(Profile)
admin.site.register(User, CustomUserAdmin)
