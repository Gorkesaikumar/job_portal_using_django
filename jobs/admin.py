from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Job, Application

class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'employer', 'location', 'job_type', 'posted_date', 'is_active']
    list_filter = ['job_type', 'is_active', 'posted_date']
    search_fields = ['title', 'description', 'employer__company_name']
    date_hierarchy = 'posted_date'

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['jobseeker', 'job', 'status', 'applied_date']
    list_filter = ['status', 'applied_date']
    search_fields = ['jobseeker__full_name', 'job__title']
    date_hierarchy = 'applied_date'

admin.site.register(Job, JobAdmin)
admin.site.register(Application, ApplicationAdmin)