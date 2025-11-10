from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Employer, Jobseeker

class EmployerRegistrationForm(UserCreationForm):
    company_name = forms.CharField(max_length=200, required=True)
    company_description = forms.CharField(widget=forms.Textarea, required=False)
    website = forms.URLField(required=False)
    location = forms.CharField(max_length=200, required=True)
    phone = forms.CharField(max_length=20, required=True)
    
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'employer'
        if commit:
            user.save()
            Employer.objects.create(
                user=user,
                company_name=self.cleaned_data['company_name'],
                company_description=self.cleaned_data['company_description'],
                website=self.cleaned_data['website'],
                location=self.cleaned_data['location'],
                phone=self.cleaned_data['phone']
            )
        return user

class JobseekerRegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=200, required=True)
    skills = forms.CharField(widget=forms.Textarea, required=True, 
                            help_text='Enter skills separated by commas')
    experience = forms.CharField(widget=forms.Textarea, required=False)
    phone = forms.CharField(max_length=20, required=True)
    location = forms.CharField(max_length=200, required=False)
    resume = forms.FileField(required=False)
    
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'jobseeker'
        if commit:
            user.save()
            Jobseeker.objects.create(
                user=user,
                full_name=self.cleaned_data['full_name'],
                skills=self.cleaned_data['skills'],
                experience=self.cleaned_data['experience'],
                phone=self.cleaned_data['phone'],
                location=self.cleaned_data['location'],
                resume=self.cleaned_data.get('resume')
            )
        return user

class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ['company_name', 'company_description', 'website', 'location', 'phone', 'logo']

class JobseekerProfileForm(forms.ModelForm):
    class Meta:
        model = Jobseeker
        fields = ['full_name', 'skills', 'experience', 'phone', 'location', 'resume']