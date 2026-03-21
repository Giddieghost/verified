import pytest
import responses
from backend.services.daraja_service import DarajaService

@responses.activate
def test_daraja_token_generation(app):
    responses.add(
        responses.GET,
        "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials",
        json={"access_token": "fake_token"},
        status=200
    )
    
    with app.app_context():
        app.config['MPESA_CONSUMER_KEY'] = 'key'
        app.config['MPESA_CONSUMER_SECRET'] = 'secret'
        token = DarajaService.get_token()
        assert token == "fake_token"
