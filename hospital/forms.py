from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *

class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
        exclude = ['user']

class DoctorForm(ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'

class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'

class PatientAppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date', 'reason']
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
                'placeholder': 'YYYY-MM-DD HH:MM',
            }),
        }        

class DoctorAppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'appointment_date', 'reason', 'status']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

