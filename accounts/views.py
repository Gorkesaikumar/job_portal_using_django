from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import EmployerRegistrationForm, JobseekerRegistrationForm, EmployerProfileForm, JobseekerProfileForm
from .models import Employer, Jobseeker

def select_user_type(request):
    return render(request, 'accounts/select_user_type.html')

def select_login(request):
    return render(request, 'accounts/select_login.html')

def employer_register(request):
    if request.method == 'POST':
        form = EmployerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Job Portal.')
            return redirect('employer_dashboard')
    else:
        form = EmployerRegistrationForm()
    return render(request, 'accounts/employer_register.html', {'form': form})

def jobseeker_register(request):
    if request.method == 'POST':
        form = JobseekerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Job Portal.')
            return redirect('jobseeker_dashboard')
    else:
        form = JobseekerRegistrationForm()
    return render(request, 'accounts/jobseeker_register.html', {'form': form})

def employer_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        
        if user is not None and user.user_type == 'employer':
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('employer_dashboard')
        else:
            messages.error(request, 'Invalid credentials or not an employer account.')
    
    return render(request, 'accounts/employer_login.html')

def jobseeker_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        
        if user is not None and user.user_type == 'jobseeker':
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('jobseeker_dashboard')
        else:
            messages.error(request, 'Invalid credentials or not a job seeker account.')
    
    return render(request, 'accounts/jobseeker_login.html')

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('home')

@login_required
def employer_dashboard(request):
    if request.user.user_type != 'employer':
        messages.error(request, 'Access denied. Employers only.')
        return redirect('home')
    
    employer = request.user.employer_profile
    jobs = employer.jobs.all()
    total_applications = sum(job.application_count() for job in jobs)
    
    context = {
        'employer': employer,
        'jobs': jobs,
        'total_applications': total_applications,
    }
    return render(request, 'accounts/employer_dashboard.html', context)

@login_required
def jobseeker_dashboard(request):
    if request.user.user_type != 'jobseeker':
        messages.error(request, 'Access denied. Job seekers only.')
        return redirect('home')
    
    jobseeker = request.user.jobseeker_profile
    applications = jobseeker.applications.all()
    
    context = {
        'jobseeker': jobseeker,
        'applications': applications,
    }
    return render(request, 'accounts/jobseeker_dashboard.html', context)

@login_required
def employer_profile(request):
    if request.user.user_type != 'employer':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    employer = request.user.employer_profile
    
    if request.method == 'POST':
        form = EmployerProfileForm(request.POST, request.FILES, instance=employer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('employer_dashboard')
    else:
        form = EmployerProfileForm(instance=employer)
    
    return render(request, 'accounts/employer_profile.html', {'form': form, 'employer': employer})

@login_required
def jobseeker_profile(request):
    if request.user.user_type != 'jobseeker':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    jobseeker = request.user.jobseeker_profile
    
    if request.method == 'POST':
        form = JobseekerProfileForm(request.POST, request.FILES, instance=jobseeker)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('jobseeker_dashboard')
    else:
        form = JobseekerProfileForm(instance=jobseeker)
    
    return render(request, 'accounts/jobseeker_profile.html', {'form': form, 'jobseeker': jobseeker})