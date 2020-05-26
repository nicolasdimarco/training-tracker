from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from authentication.models import User, TrainingGroup


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Custom Field Heading',
            {
                'fields': (
                    'training_group',
                    'is_trainer',
                ),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(TrainingGroup)
