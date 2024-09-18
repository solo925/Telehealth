from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import DoctorProfile, PatientProfile

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
    if created:
        try:
            if instance.groups.filter(name='Doctors').exists():
                DoctorProfile.objects.get_or_create(user=instance)
            elif instance.groups.filter(name='Patients').exists():
                PatientProfile.objects.get_or_create(user=instance)
        except Exception as e:
            # Log the exception or handle it as needed
            print(f"Error creating profile for user {instance.username}: {e}")




