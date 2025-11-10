from django.urls import path
from . import views

urlpatterns = [
    path('select-type/', views.select_user_type, name='select_user_type'),
    path('select-login/', views.select_login, name='select_login'),
    path('employer/register/', views.employer_register, name='employer_register'),
    path('jobseeker/register/', views.jobseeker_register, name='jobseeker_register'),
    path('employer/login/', views.employer_login, name='employer_login'),
    path('jobseeker/login/', views.jobseeker_login, name='jobseeker_login'),
    path('logout/', views.user_logout, name='logout'),
    path('employer/dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('jobseeker/dashboard/', views.jobseeker_dashboard, name='jobseeker_dashboard'),
    path('employer/profile/', views.employer_profile, name='employer_profile'),
    path('jobseeker/profile/', views.jobseeker_profile, name='jobseeker_profile'),
]