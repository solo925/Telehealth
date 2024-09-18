from django.contrib.auth.models import User, Group
from accounts.models import DoctorProfile

# Ensure the 'Doctors' group exists
doctors_group, created = Group.objects.get_or_create(name='Doctors')

# Create a user and assign them to the 'Doctors' group
user = User.objects.create_user(username='doctor1', password='password')
user.groups.add(doctors_group)

# Check if DoctorProfile is created
print(DoctorProfile.objects.filter(user=user).exists())  # Should return True
