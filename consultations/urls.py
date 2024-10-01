from django.urls import path
from .import views
from .views import video_consultation

app_name = "consultations"
urlpatterns = [
    path('video/<str:room_name>/', video_consultation, name='video_consultation'),
    path('chat/<str:room_name>/', views.chat_room, name='chat_room'),

]
