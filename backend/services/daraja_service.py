import requests
import base64
from datetime import datetime
from flask import current_app

class DarajaService:
    @staticmethod
    def get_token():
        consumer_key = current_app.config.get('MPESA_CONSUMER_KEY')
        consumer_secret = current_app.config.get('MPESA_CONSUMER_SECRET')
        
        if not consumer_key or not consumer_secret:
            return None

        url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        response = requests.get(url, auth=(consumer_key, consumer_secret))
        
        if response.status_code == 200:
            return response.json().get('access_token')
        return None

    @staticmethod
    def initiate_stk_push(phone_number, amount, account_reference, transaction_desc):
        token = DarajaService.get_token()
        if not token:
            return {'error': 'Failed to get access token'}, 500

        passkey = current_app.config.get('MPESA_PASSKEY')
        shortcode = current_app.config.get('MPESA_SHORTCODE')
        callback_url = current_app.config.get('MPESA_CALLBACK_URL')
        
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode(f"{shortcode}{passkey}{timestamp}".encode()).decode()

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        payload = {
            "BusinessShortCode": shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": callback_url,
            "AccountReference": account_reference,
            "TransactionDesc": transaction_desc
        }

        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/query" # This should be the process request URL, wait
        # Correction: STK Push process URL
        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        
        response = requests.post(url, json=payload, headers=headers)
        return response.json(), response.status_code

    @staticmethod
    def query_stk_status(checkout_request_id):
        token = DarajaService.get_token()
        if not token:
            return {'error': 'Failed to get access token'}, 500

        passkey = current_app.config.get('MPESA_PASSKEY')
        shortcode = current_app.config.get('MPESA_SHORTCODE')
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode(f"{shortcode}{passkey}{timestamp}".encode()).decode()

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        payload = {
            "BusinessShortCode": shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "CheckoutRequestID": checkout_request_id
        }

        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/query"
        response = requests.post(url, json=payload, headers=headers)
        return response.json(), response.status_code
