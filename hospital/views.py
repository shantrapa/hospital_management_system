from django.shortcuts import render, redirect
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
    context = {}
    return render(request, 'hospital/index.html', context)

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['patient'])
def userPage(request):
    context = {}
    return render(request, 'hospital/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def patient_list(request):
    patients = Patient.objects.all()
    context = {'patients': patients}
    return render(request, 'hospital/patient_list.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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