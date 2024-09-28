"""
Handles the functionality for booking appointments, managing appointment video chats, and displaying appointment lists and details.

The `book_appointment` function allows users to create new appointments by filling out an appointment form. It also creates a Twilio video room and chat service for the appointment.

The `appointment_video_chat` function generates a Twilio access token for the video chat and chat service associated with a specific appointment, and renders the video chat page.

The `appointment_list` function retrieves and displays a list of appointments for the currently logged-in user.

The `appointment_detail` function retrieves and displays the details of a specific appointment for the currently logged-in user.
"""
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Appointment, DoctorProfile, PatientProfile
from .forms import AppointmentForm
from twilio.rest import Client
from django.conf import settings



# Initialize Twilio Client
# Initialize a Twilio client using the API key, API secret, and account SID from the Django settings.
# This Twilio client is used to interact with the Twilio API,
# such as creating video rooms and chat services for appointments.
client = Client(settings.TWILIO_API_KEY, settings.TWILIO_API_SECRET, settings.TWILIO_ACCOUNT_SID)
@login_required
def book_appointment(request):
    """
    Handles the appointment booking process. Creates a new appointment, Twilio video room, and chat service.

    Parameters:
    request (HttpRequest): The request object containing the user's input data.

    Returns:
    HttpResponseRedirect: If the request method is POST and the form is valid, redirects to the appointment list page.
    render: If the request method is GET, renders the appointment booking form.
    """
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

    """
    Handles the appointment video chat functionality by generating an access token 
    for the given appointment and rendering the video chat template with the 
    required parameters.

    Parameters:
        request (HttpRequest): The request object containing the user's input data.
        appointment_id (int): The ID of the appointment for which the video chat is being initiated.

    Returns:
        render: The rendered video chat template with the access token, appointment, and room name.
    """

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
