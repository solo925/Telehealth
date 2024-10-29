from django.shortcuts import render, redirect
import paypalrestsdk
import requests
from django.http import JsonResponse
from django.conf import settings
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64
from . forms import PaymentForm
from .mpesa_utils import standardize_phone_number
from .mpesa_utils import is_valid_phone_number
from payments.models import Invoice
from django.conf import settings


# PAYPAL VIEWS
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # 'sandbox' or 'live'
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

def create_paypal_payment(request):
    if request.method == "POST":
        amount = request.POST.get('amount')
        if not amount or float(amount) <= 0:
            return JsonResponse({"error": "Invalid amount"})

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": "http://localhost:8000/payment/execute/",
                "cancel_url": "http://localhost:8000/payment/cancel/"
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "Telehealth Consultation",
                        "sku": "item",
                        "price": amount,  # Use the input amount here
                        "currency": "USD",
                        "quantity": 1
                    }]
                },
                "amount": {
                    "total": amount,  # Use the input amount here
                    "currency": "USD"
                },
                "description": "Payment for Telehealth Services"
            }]
        })

        if payment.create():
            print("Payment created successfully")
            for link in payment.links:
                if link.rel == "approval_url":
                    approval_url = str(link.href)
                    return redirect(approval_url)
        else:
            print(payment.error)
            return JsonResponse({"error": "Payment creation failed."})
    else:
        return render(request, 'payments/paypal.html')

def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        print("Payment executed successfully")
        return JsonResponse({"status": "Payment completed."})
    else:
        print(payment.error)
        return JsonResponse({"error": "Payment execution failed."})

def cancel_payment(request):
    return JsonResponse({"status": "Payment canceled."})


# M-PESA PAYMNET VIEWS
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





# Get access token FOR mPEAS
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


# def mpesa_payment_view(request):
#     return render(request, 'payments/mpesa_payment.html')

# INVOICES
def create_invoice(user, payment_method, transaction_id, amount, description):
    # Create the invoice in the database
    invoice = Invoice.objects.create(
        user=user,
        payment_method=payment_method,
        transaction_id=transaction_id,
        amount=amount,
        description=description
    )
    return invoice


# M-Pesa callback - payments/views.py

# payments/views.py

import json
from decimal import Decimal

@csrf_exempt
def mpesa_callback(request):
    data = json.loads(request.body.decode('utf-8'))  # Decode the JSON body from M-Pesa
    
    # Extract relevant fields from the M-Pesa response
    transaction_id = data.get("Body", {}).get("stkCallback", {}).get("CheckoutRequestID")
    amount = data.get("Body", {}).get("stkCallback", {}).get("CallbackMetadata", {}).get("Item", [])[0].get("Value", 0)
    
    # Ensure amount is converted to a Decimal
    amount = Decimal(amount)
    
    user = request.user  # Assuming you know the user based on the request
    
    # Create an invoice with the correct amount
    create_invoice(
        user=user,
        payment_method="mpesa",
        transaction_id=transaction_id,
        amount=amount,
        description="Payment for Telehealth Services"
    )
    
    return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})
