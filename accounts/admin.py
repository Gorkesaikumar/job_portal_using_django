from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Employer, Jobseeker

class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'user_type', 'is_active', 'is_staff', 'date_joined']
    list_filter = ['user_type', 'is_active', 'is_staff']
    search_fields = ['email']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('User Type', {'fields': ('user_type',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_type', 'password1', 'password2'),
        }),
    )

class EmployerAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'location', 'phone', 'user']
    search_fields = ['company_name', 'location']

class JobseekerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone', 'location', 'user']
    search_fields = ['full_name', 'skills']

admin.site.register(User, UserAdmin)
admin.site.register(Employer, EmployerAdmin)
admin.site.register(Jobseeker, JobseekerAdmin)