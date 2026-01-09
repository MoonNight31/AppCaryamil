from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Roles', {'fields': ('is_parent', 'is_teacher')}),
    )
    list_display = ['username', 'email', 'is_parent', 'is_teacher', 'is_staff']
    list_filter = ['is_parent', 'is_teacher', 'is_staff', 'is_superuser']
