#TRAVIS CI SETTINGS

# SECURITY WARNING: don't run with debug turned on in production!
from ecommerce_backend.settings.base import *
import os
DEBUG = True

ALLOWED_HOSTS = []
           
# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         # sqlite database
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',

#     }
# }
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'USER': 'mydatabaseuser',
#         'NAME': 'mydatabase',
#         'TEST': {
#             'NAME': 'mytestdatabase',
#         },
#     },
# }
# DATABASES = {
#     'default': {
#         'ENGINE':'django.db.backends.mysql',
#         'USER': 'mydatabaseuser',
#         'NAME': 'mydatabase',
#         'TEST': {
#             'NAME': 'mytestdatabase',
#         },
#     },
# }
DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': os.environ['DATABASE_NAME'],
    'USER': os.environ['DATABASE_USER'],
    'PASSWORD': '',
    'HOST': '127.0.0.1',
    # 'PASSWORD': os.environ['DATABASE_PASSWORD'],
    }
}




#EMAIL CONFIGURATIONS
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL="EcommerceTeam"
