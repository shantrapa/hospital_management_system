from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.validators import EmailValidator
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

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(validators=[EmailValidator()], required=True)  
    message = forms.CharField(widget=forms.Textarea, required=True)
