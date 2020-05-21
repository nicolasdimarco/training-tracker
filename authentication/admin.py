from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from authentication.models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Custom Field Heading',
            {
                'fields': (
                    'is_trainer',
                ),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
