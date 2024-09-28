from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import MedicalRecord
from .forms import MedicalRecordForm

@login_required
def upload_medical_record(request):
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, request.FILES)
        if form.is_valid():
            medical_record = form.save(commit=False)
            medical_record.doctor = request.user  # Automatically set the logged-in user as the doctor
            medical_record.save()
            return redirect('view_medical_records')
    else:
        form = MedicalRecordForm()

    return render(request, 'medical_records/upload_record.html', {'form': form})

@login_required
def view_medical_records(request):
    if request.user.groups.filter(name='Doctors').exists():
        # Doctors can view all records they created
        records = MedicalRecord.objects.filter(doctor=request.user)
    else:
        # Patients can only view their own records
        records = MedicalRecord.objects.filter(patient=request.user)

    return render(request, 'medical_records/record_list.html', {'records': records})
