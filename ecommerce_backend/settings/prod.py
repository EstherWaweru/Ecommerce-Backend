#PRODUCTION SETTINGS
# SECURITY WARNING: don't run with debug turned on in production!
from ecommerce_backend.settings.base import *
DEBUG = False

ALLOWED_HOSTS = []



# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        sqlite database
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',

        

    }
}


#EMAIL CONFIGURATIONS
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = env.int('EMAIL_PORT')
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS')
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL=env.str('DEFAULT_FROM_EMAIL')
