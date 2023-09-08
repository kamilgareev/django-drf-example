from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .forms import *


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'first_name', 'last_name', 'password']
    list_filter = ['is_admin']
    ordering = ['email']

    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'groups',
                                    'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'fields': (
                'email', 'first_name', 'last_name', 'password1',
                'password2', 'is_staff', 'groups', 'user_permissions'
            )}
         ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
