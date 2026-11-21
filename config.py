import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'solecraft-ultra-secure-key-2026-v1'
    
    # Database config: Support SQLite locally, or PostgreSQL/MySQL via env
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
        
    SQLALCHEMY_DATABASE_URI = database_url or f"sqlite:///{os.path.abspath(os.path.join(os.path.dirname(__file__), 'solecraft.db'))}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True
    } if database_url and not database_url.startswith('sqlite') else {}

    # Uploads
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # 16 MB max

    # Session & Security
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    # Razorpay Test Credentials (can be overridden via environment)
    RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID', 'rzp_test_solecraft_demo')
    RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET', 'solecraft_secret_test_2026')

    # Currency
    CURRENCY_SYMBOL = '$'
    CURRENCY_CODE = 'USD'
