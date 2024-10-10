from django.urls import path
from . import views
from .views import create_paypal_payment, execute_payment, cancel_payment

app_name ="payment"
urlpatterns = [
    path('', views.payment, name='mpesa_payment'),
    path('paypal/create/', create_paypal_payment, name='paypal-create'),
    path('paypal/execute/', execute_payment, name='paypal-execute'),
    path('paypal/cancel/', cancel_payment, name='paypal-cancel'),
    # path('mpesa/', views.lipa_na_mpesa_online, name='lipa_na_mpesa'),
    # path('callback/', views.mpesa_callback, name='mpesa_callback'),
]


