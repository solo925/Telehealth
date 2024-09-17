from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm,LoginForm
from .models import DoctorProfile, PatientProfile

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            
            # Create profile based on the selected role
            if role == 'doctor':
                DoctorProfile.objects.create(user=user)
            elif role == 'patient':
                PatientProfile.objects.create(user=user)

            # Log the user in and redirect to the appropriate dashboard
            login(request, user)
            if role == 'doctor':
                return redirect('doctor_dashboard') 
            elif role == 'patient':
                return redirect('patient_dashboard')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})



def Login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)

                # octor or patient and redirect 
                
                if hasattr(user, 'doctor_profile'):
                    return redirect('doctor_dashboard')  
                elif hasattr(user, 'patient_profile'):
                    return redirect('patient_dashboard')  
                else:
                    return redirect('home')  
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout(request):
    auth_logout(request)
    return redirect('login') 


@login_required
def doctor_dashboard(request):
    return render(request, 'accounts/doctor_dashboard.html')

@login_required
def patient_dashboard(request):
    return render(request, 'accounts/patient_dashboard.html')

