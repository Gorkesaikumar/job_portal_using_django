from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Job, Application
from .forms import JobForm, ApplicationForm

def home(request):
    recent_jobs = Job.objects.filter(is_active=True)[:6]
    total_jobs = Job.objects.filter(is_active=True).count()
    return render(request, 'home.html', {'recent_jobs': recent_jobs, 'total_jobs': total_jobs})

def job_list(request):
    jobs = Job.objects.filter(is_active=True)
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(location__icontains=query)
        )
    
    # Filter by job type
    job_type = request.GET.get('job_type')
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    
    # Filter by location
    location = request.GET.get('location')
    if location:
        jobs = jobs.filter(location__icontains=location)
    
    context = {
        'jobs': jobs,
        'query': query,
        'job_type': job_type,
        'location': location,
    }
    return render(request, 'jobs/job_list.html', context)

def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    has_applied = False
    
    if request.user.is_authenticated and request.user.user_type == 'jobseeker':
        has_applied = Application.objects.filter(
            job=job, 
            jobseeker=request.user.jobseeker_profile
        ).exists()
    
    return render(request, 'jobs/job_detail.html', {'job': job, 'has_applied': has_applied})

@login_required
def job_create(request):
    if request.user.user_type != 'employer':
        messages.error(request, 'Only employers can create jobs.')
        return redirect('home')
    
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user.employer_profile
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('employer_dashboard')
    else:
        form = JobForm()
    
    return render(request, 'jobs/job_create.html', {'form': form})

@login_required
def job_edit(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    
    if request.user.user_type != 'employer' or job.employer != request.user.employer_profile:
        messages.error(request, 'You do not have permission to edit this job.')
        return redirect('home')
    
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('employer_dashboard')
    else:
        form = JobForm(instance=job)
    
    return render(request, 'jobs/job_edit.html', {'form': form, 'job': job})

@login_required
def job_delete(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    
    if request.user.user_type != 'employer' or job.employer != request.user.employer_profile:
        messages.error(request, 'You do not have permission to delete this job.')
        return redirect('home')
    
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted successfully!')
        return redirect('employer_dashboard')
    
    return render(request, 'jobs/job_delete_confirm.html', {'job': job})

@login_required
def apply_job(request, job_id):
    if request.user.user_type != 'jobseeker':
        messages.error(request, 'Only job seekers can apply for jobs.')
        return redirect('home')
    
    job = get_object_or_404(Job, id=job_id)
    jobseeker = request.user.jobseeker_profile
    
    # Check if already applied
    if Application.objects.filter(job=job, jobseeker=jobseeker).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('job_detail', job_id=job_id)
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.jobseeker = jobseeker
            application.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('jobseeker_dashboard')
    else:
        form = ApplicationForm()
    
    return render(request, 'jobs/apply_job.html', {'form': form, 'job': job})

@login_required
def my_applications(request):
    if request.user.user_type != 'jobseeker':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    applications = request.user.jobseeker_profile.applications.all()
    return render(request, 'jobs/my_applications.html', {'applications': applications})

@login_required
def job_applications(request, job_id):
    if request.user.user_type != 'employer':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    job = get_object_or_404(Job, id=job_id)
    
    if job.employer != request.user.employer_profile:
        messages.error(request, 'You do not have permission to view these applications.')
        return redirect('home')
    
    applications = job.applications.all()
    return render(request, 'jobs/job_applications.html', {'job': job, 'applications': applications})

@login_required
def update_application_status(request, application_id):
    if request.user.user_type != 'employer':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    application = get_object_or_404(Application, id=application_id)
    
    if application.job.employer != request.user.employer_profile:
        messages.error(request, 'You do not have permission to update this application.')
        return redirect('home')
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['pending', 'reviewed', 'accepted', 'rejected']:
            application.status = status
            application.save()
            messages.success(request, 'Application status updated successfully!')
        else:
            messages.error(request, 'Invalid status.')
    
    return redirect('job_applications', job_id=application.job.id)