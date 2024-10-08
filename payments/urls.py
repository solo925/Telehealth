from django.urls import path
from . import views
from .views import mpesa_payment_view

app_name ="payment"
urlpatterns = [
    path('', mpesa_payment_view, name='mpesa_payment'),
    path('mpesa/', views.lipa_na_mpesa_online, name='lipa_na_mpesa'),
    path('callback/', views.mpesa_callback, name='mpesa_callback'),
]


