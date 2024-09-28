"""
Generates a Twilio Access Token for a video consultation session with the given room name.

Args:
    request (django.http.request.HttpRequest): The Django HTTP request object.
    room_name (str): The name of the Twilio video room.

Returns:
    django.http.response.HttpResponse: A rendered template with the generated Twilio Access Token.
"""
from django.conf import settings
from django.shortcuts import render
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant

def video_consultation(request, room_name):
    twilio_account_sid = settings.TWILIO_ACCOUNT_SID
    twilio_api_key = settings.TWILIO_API_KEY
    twilio_api_secret = settings.TWILIO_API_SECRET

    # Generate Access Token
    token = AccessToken(twilio_account_sid, twilio_api_key, twilio_api_secret, identity=request.user.username)

    # Create Video Grant
    video_grant = VideoGrant(room=room_name)
    token.add_grant(video_grant)

    context = {
        'room_name': room_name,
        'token': token.to_jwt()
    }
    return render(request, 'consultations/video_call.html', context)
