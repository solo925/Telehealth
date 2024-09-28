# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Appointment, DoctorProfile, PatientProfile
from .forms import AppointmentForm
from twilio.rest import Client
from django.conf import settings



# Initialize Twilio Client
client = Client(settings.TWILIO_API_KEY, settings.TWILIO_API_SECRET, settings.TWILIO_ACCOUNT_SID)
@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)

            # Create Twilio Video Room
            rooms = client.video.rooms.list(unique_name=f"Appointment_{appointment.id}")

            if not rooms:
               room = client.video.rooms.create(unique_name=f"Appointment_{appointment.id}")
            else:
              room = rooms[0]  # Use the existing room


            # Create Twilio Chat Service
            chat_service = client.chat.services.create(friendly_name=f"AppointmentChat_{appointment.id}")
            appointment.chat_service_sid = chat_service.sid

            appointment.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
    return render(request, 'appointments/book_appointment.html', {'form': form})


def appointment_video_chat(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)

    # Generate Access Token for Video
    from twilio.jwt.access_token import AccessToken
    from twilio.jwt.access_token.grants import VideoGrant, ChatGrant

    # Create Access Token
    token = AccessToken(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_API_KEY, settings.TWILIO_API_SECRET, identity=str(request.user))
    video_grant = VideoGrant(room=appointment.room_name)
    chat_grant = ChatGrant(service_sid=appointment.chat_service_sid)
    
    token.add_grant(video_grant)
    token.add_grant(chat_grant)

    access_token = token.to_jwt()

    return render(request, 'appointments/video_chat.html', {
        'appointment': appointment,
        'access_token': access_token,
        'room_name': appointment.room_name,
    })

@login_required
def appointment_list(request):
    appointments = Appointment.objects.filter(patient__user=request.user)
    # appointments = Appointment.objects.all()
    return render(request, 'appointments/appointment_list.html', {'appointments': appointments})

@login_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, patient__user=request.user)
    return render(request, 'appointments/appointment_detail.html', {'appointment': appointment})
