from django.urls import path
from . import views

app_name = "appointments"
urlpatterns = [
    path('book/', views.book_appointment, name='book_appointment'),
    path('', views.appointment_list, name='appointment_list'),
    path('<int:pk>/', views.appointment_detail, name='appointment_detail'),
    # path('<int:appointment_id>/video/', views.appointment_video_chat, name='appointment_video_chat'),
]
