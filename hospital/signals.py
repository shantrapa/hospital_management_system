from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from .models import Patient

def patient_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='patient')
        instance.groups.add(group)
        Patient.objects.create(
            user = instance,
            first_name = instance.username,
            )
        print("CREATED")
            
post_save.connect(patient_profile, sender = User)