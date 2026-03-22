import os

basedir = os.path.abspath(os.path.dirname(__file__))

def get_db_uri():
    uri = os.getenv('DATABASE_URL', 'sqlite:///../database/app.db')
    if uri.startswith('postgres://'):
        uri = uri.replace('postgres://', 'postgresql://', 1)
    return uri

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret')
    SQLALCHEMY_DATABASE_URI = get_db_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Daraja M-Pesa
    MPESA_CONSUMER_KEY = os.getenv('MPESA_CONSUMER_KEY')
    MPESA_CONSUMER_SECRET = os.getenv('MPESA_CONSUMER_SECRET')
    MPESA_PASSKEY = os.getenv('MPESA_PASSKEY')
    MPESA_SHORTCODE = os.getenv('MPESA_SHORTCODE', '174379')
    MPESA_CALLBACK_URL = os.getenv('MPESA_CALLBACK_URL')

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', 'sqlite:///../database/test.db')

class ProductionConfig(Config):
    DEBUG = False
