from django.shortcuts import render

# Create your views here.
import requests
from django.http import JsonResponse
from django.conf import settings
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64

# Get access token
def get_access_token():
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = r.json()['access_token']
    return mpesa_access_token

# Lipa na M-Pesa Online
def lipa_na_mpesa_online(request, amount, phone_number):
    access_token = get_access_token()
    api_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    headers = {'Authorization': f'Bearer {access_token}'}
    
    # Generate timestamp
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    
    # Password - base64 encoded string
    password = base64.b64encode(f"{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{timestamp}".encode()).decode('utf-8')

    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,  # Customer's phone number
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": "https://yourdomain.com/payment/callback/",
        "AccountReference": "TelehealthConsultation",
        "TransactionDesc": "Payment for Telehealth Services"
    }

    response = requests.post(api_url, json=payload, headers=headers)
    return JsonResponse(response.json())

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def mpesa_callback(request):
    data = request.body
    # Process the callback and update the payment status in the database
    return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})

def mpesa_payment_view(request):
    return render(request, 'payments/mpesa_payment.html')