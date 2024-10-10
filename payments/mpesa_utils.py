import requests
from django.conf import settings
from requests.auth import HTTPBasicAuth

def get_mpesa_access_token():
    url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    
    response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    
    if response.status_code == 200:
        access_token = response.json().get('access_token')
        return access_token
    else:
        raise Exception("Failed to obtain M-Pesa access token")

def standardize_phone_number(phone_number):
    """
    Standardizes phone number to the format 2547XXXXXXXX.
    """
    # Strip any leading or trailing whitespace
    phone_number = phone_number.strip()

    if phone_number.startswith("+"):
        phone_number = phone_number[1:]  # Remove the '+' sign
    elif phone_number.startswith("0"):
        phone_number = "254" + phone_number[1:]  # Replace leading '0' with '254'
    elif not phone_number.startswith("254"):
        # If it doesn't start with '254', assume it needs to be standardized
        phone_number = "254" + phone_number

    # Log the standardized phone number for debugging
    print(f"Standardized phone number: {phone_number}")

    return phone_number

def is_valid_phone_number(phone_number):
    """
    Validates if the phone number is in the correct format.
    """
    return phone_number.isdigit() and len(phone_number) == 12 and phone_number.startswith("2547")
