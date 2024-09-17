from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import DoctorProfile, PatientProfile

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
    if created:  # Only create profiles for new users
        if instance.groups.filter(name='Doctors').exists():
            DoctorProfile.objects.get_or_create(user=instance)
        elif instance.groups.filter(name='Patients').exists():
            PatientProfile.objects.get_or_create(user=instance)
