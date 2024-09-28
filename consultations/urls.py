from django.urls import path
from .views import video_consultation

urlpatterns = [
    path('video/<str:room_name>/', video_consultation, name='video_consultation'),
]
