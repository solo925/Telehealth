from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User
from .models import DoctorProfile, PatientProfile
from accounts.decorators import role_required

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.groups.filter(name='Doctors').exists():
            DoctorProfile.objects.get_or_create(user=instance)
        elif instance.groups.filter(name='Patients').exists():
            PatientProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'doctor_profile'):
        instance.doctor_profile.save()
    elif hasattr(instance, 'patient_profile'):
        instance.patient_profile.save()
