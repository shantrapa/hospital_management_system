from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Patient(models.Model):
    user = models.OneToOneField(User, null=True, blank = True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    date_of_birth = models.DateField(null = True)
    gender = models.CharField(max_length = 10, null = True)
    email = models.CharField(max_length = 50, null = True)
    contact_number = models.CharField(max_length=20, null = True)

    def __str__(self):
        return self.first_name

class Doctor(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    specialization = models.CharField(max_length = 50)
    email = models.CharField(max_length = 50, null = True)
    contact_number = models.CharField(max_length = 20, null = True)

    def __str__(self):
        return self.first_name

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete = models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete = models.CASCADE)
    appointment_date = models.DateTimeField()
    reason = models.TextField(null = True)