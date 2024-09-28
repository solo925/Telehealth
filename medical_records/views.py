from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import MedicalRecord
from .forms import MedicalRecordForm

@login_required
def upload_medical_record(request):
    """
    This function handles the uploading of medical records by doctors.
    It uses Django's form handling and authentication decorators.

    Parameters:
    request (HttpRequest): The incoming request object. Contains data about the request.

    Returns:
    HttpResponse: The rendered template with the form or a redirect to the 'view_medical_records' page.
    """
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, request.FILES)
        if form.is_valid():
            # Create an unsaved instance of the MedicalRecord model
            medical_record = form.save(commit=False)
            # Validate that the user is a doctor and not a patient
            if not request.user.is_doctor:
                medical_record.doctor = request.user  # Automatically set the logged-in user as the doctor
                medical_record.save()
            return redirect('view_medical_records')
    else:
        form = MedicalRecordForm()

    return render(request, 'medical_records/upload_record.html', {'form': form})

@login_required
def view_medical_records(request):
    """
    This function handles viewing medical records by both doctors and patients.
    It checks the user's group membership to determine which records to display.

    Parameters:
    request (HttpRequest): The incoming request object. Contains data about the request.

    Returns:
    HttpResponse: The rendered template with a list of medical records.
    """
    if request.user.groups.filter(name='Doctors').exists():
        # Doctors can view all records they created
        records = MedicalRecord.objects.filter(doctor=request.user)
    else:
        # Patients can only view their own records
        records = MedicalRecord.objects.filter(patient=request.user)

    return render(request, 'medical_records/record_list.html', {'records': records})
