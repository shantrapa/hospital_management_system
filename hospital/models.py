from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Patient(models.Model):
    user = models.OneToOneField(User, null=True, blank = True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50, null = True, blank = True)
    date_of_birth = models.DateField(null = True, blank = True)
    gender = models.CharField(max_length = 15, null = True, choices=[
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Rather not say', 'Rather not say'),
    ])
    email = models.CharField(max_length = 50, null = True, blank = True)
    contact_number = models.CharField(max_length=20, null = True, blank = True)
    profile_pic = models.ImageField(default = "profile.png", null=True, blank=True)

    def __str__(self):
        return self.first_name

class Doctor(models.Model):
    user = models.OneToOneField(User, null=True, blank = True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    specialization = models.CharField(max_length = 20, choices=[
        ('Surgery', 'Surgery'),
        ('Dermatology', 'Dermatology'),
        ('Psychiatry', 'Psychiatry')
    ])
    email = models.CharField(max_length = 50, null = True)
    contact_number = models.CharField(max_length = 20, null = True)

    def __str__(self):
        return self.first_name

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete = models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete = models.CASCADE)
    appointment_date = models.DateTimeField()
    reason = models.TextField(null = True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
    ], default='Pending')

class TimeSlot(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"