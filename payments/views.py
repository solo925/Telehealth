from django.shortcuts import render

# Create your views here.
import requests
from django.http import JsonResponse
from django.conf import settings
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64
from . forms import PaymentForm
from .mpesa_utils import standardize_phone_number
from .mpesa_utils import is_valid_phone_number


def payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone_number']
            print(f"Cleaned phone number from form: {phone}")  # Log the raw phone input
            
            phone_number = standardize_phone_number(phone)
            print(f"Standardized phone number: {phone_number}")  # Log the standardized phone number

            # Validate the phone number format
            if not is_valid_phone_number(phone_number):
                print(f"Invalid phone number format: {phone_number}")  # Log invalid format
                return JsonResponse({"error": "Invalid phone number format"}, status=400)

            amount = form.cleaned_data['amount']
            response_data = lipa_na_mpesa_online(amount, phone_number)
            return JsonResponse(response_data, safe=False)
    else:
        form = PaymentForm()

    return render(request, 'payments/mpesa_payment.html', {'form': form})





# Get access token
def get_access_token():
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = r.json()['access_token']
    return mpesa_access_token

# Lipa na M-Pesa Online
def lipa_na_mpesa_online(amount, phone_number):
    access_token = get_access_token()
    api_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    headers = {'Authorization': f'Bearer {access_token}'}
    
    # Generate timestamp
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    
    # Password - base64 encoded string
    password = base64.b64encode(f"{settings.MPESA_SHORTCODE}{settings.LIPA_NA_MPESA_ONLINE_PASSKEY}{timestamp}".encode()).decode('utf-8')

    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,  # Customer's phone number
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": phone_number,  # Customer's phone number
        "CallBackURL": "https://yourdomain.com/payment/callback/",
        "AccountReference": "TelehealthConsultation",
        "TransactionDesc": "Payment for Telehealth Services"
    }

    print(f"M-Pesa payload: {payload}")  # Log the payload for debugging

    response = requests.post(api_url, json=payload, headers=headers)
    print(f"M-Pesa response: {response.json()}")  # Log the response
    return response.json()


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def mpesa_callback(request):
    data = request.body
    # Process the callback and update the payment status in the database
    return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})

# def mpesa_payment_view(request):
#     return render(request, 'payments/mpesa_payment.html')