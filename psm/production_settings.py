from .settings import *
import os

DEBUG = False
ALLOWED_HOSTS = ['brewbeauty.pythonanywhere.com']

# Security
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'brewbeauty$hosting',
        'USER': 'brewbeauty',
        'PASSWORD': os.getenv('DB_PASSWORD1'),
        'HOST': 'brewbeauty.mysql.pythonanywhere-services.com',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        }
    }
}

# Secret Key
SECRET_KEY = os.getenv('SECRET_KEY')