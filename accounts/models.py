from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    department = models.CharField(max_length=100,default="General")
    firstname = models.CharField(max_length=50,default='firstname')
    middlename = models.CharField(max_length=50,default="middlename"),
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    surname = models.CharField(max_length=50, blank=True)  # Full name
    other_details = models.TextField(blank=True)  # Additional optional info

    def __str__(self):
        return self.user.email

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    firstname = models.CharField(max_length=50,default='firstname')
    middlename = models.CharField(max_length=50,default="middlename")
    surname = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=255,default="address")
    physical_address = models.CharField(max_length=255,default="physical_address")
    blood_group = models.CharField(max_length=5,default="blood_group")
    age = models.IntegerField(default=20)
    
    def __str__(self):
        return self.user.email
