from django.shortcuts import render, redirect
from .models import Patient, Doctor, Appointment
from .forms import PatientForm, DoctorForm, AppointmentForm

def registerPage(request):
    context = {}
    return render(request, 'hospital/register.html', context)

def loginPage(request):
    context = {}
    return render(request, 'hospital/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def home(request):
    context = {}
    return render(request, 'hospital/index.html', context)

def patient_list(request):
    patients = Patient.objects.all()
    context = {'patients': patients}
    return render(request, 'hospital/patient_list.html', context)

def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm()
    context = {'form': form}
    return render(request, 'hospital/add_patient.html', context)