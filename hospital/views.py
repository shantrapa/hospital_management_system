from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *
from .decorators import *

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'hospital/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')
    context = {} 
    return render(request, 'hospital/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
    context = {
        'is_doctor': request.user.groups.filter(name='doctor').exists(),
    }
    return render(request, 'hospital/index.html', context)

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['patient'])
def userPage(request):
    context = {
        'is_doctor': request.user.groups.filter(name='doctor').exists(),
    }
    return render(request, 'hospital/user.html', context)

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['doctor'])
def doctorPage(request):
    context = {
        'is_doctor': request.user.groups.filter(name='doctor').exists(),
    }
    return render(request, 'hospital/doctor.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['doctor'])
def patient_list(request):
    patients = Patient.objects.all()
    context = {
        'patients': patients, 
        'is_doctor': request.user.groups.filter(name='doctor').exists(),}
    return render(request, 'hospital/patient_list.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['doctor'])
def add_patient(request):
    if request.user.groups.filter(name='doctor').exists():
        appointments = Appointment.objects.filter(doctor__user=request.user)
        context = {
            'appointments': appointments,
            'is_doctor': request.user.groups.filter(name='doctor').exists(),
        }
        return render(request, 'hospital/add_patient.html', context)
    else:
        return redirect('home')

# Appointments
@login_required(login_url='login')
@allowed_users(allowed_roles=['patient'])
def patient_appointment(request):
    doctors = Doctor.objects.all()
    if request.method == 'POST':
        form = PatientAppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.patient
            appointment.created_by = request.user
            appointment.save()
            return redirect('home')
    else:
        form = PatientAppointmentForm()
    context = {
        'form': form, 
        'doctors': doctors,
        'is_doctor': request.user.groups.filter(name='doctor').exists(),
    }
    return render(request, 'hospital/patient_appointment.html', context)
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['patient'])
def accountSettings(request):
	patient = request.user.patient
	form = PatientForm(instance=patient)

	if request.method == 'POST':
		form = PatientForm(request.POST, request.FILES,instance=patient)
		if form.is_valid():
			form.save()

	context = {
        'form': form,
        'is_doctor': request.user.groups.filter(name='doctor').exists(),
    }
	return render(request, 'hospital/account_settings.html', context)

def update_appointment_status(request, appointment_id):
    if request.method == 'POST':
        appointment = get_object_or_404(Appointment, id=appointment_id)
        new_status = request.POST.get('status')
        appointment.status = new_status
        appointment.save()
        return redirect('add_patient')  # Redirect to the page where appointments are listed

    return render(request, 'hospital/add_patient.html')