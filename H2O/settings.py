"""
Django settings for H2O project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import os

SYSTEM_CURRENCY = 'usd'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get('SECRET_KEY', '50@=z3-bw$acojx%4ans=c*y8$fn0_wii$1_071+k**o=i2sbk')

DEBUG = os.environ.get('H2O_DEBUG', 'True') == 'True'

FACEBOOK_CLIENT_ID = '401193696737876'
FACEBOOK_TIMEOUT = 4

INVITES_COUNT_FOR_NEW_USER = 0

ENTRANCE_GIFT_AMOUNT = 10.0

ALLOWED_HOSTS = []

REFRESH_TOKEN_EXPIRES_IN = 300 # 86400
ACCESS_TOKEN_EXPIRES_IN = 60 # 3600

ANDROID_PUSH_TOKEN_EXPIRES_IN = 7 * 86400
IOS_PUSH_TOKEN_EXPIRES_IN =  7 * 86400

# see send_alert_task
DEVELOPER_EMAIL = 'milovanov@octabrain.com'

#
TEST_INVITE_CODE = 'TEST_INVITE_CODE1'

#
PAYPAL_MODE = 'sandbox' if DEBUG else 'live'
PAYPAL_CLIENT_ID = os.environ.get('PAYPAL_CLIENT_ID', 'AWGLmmsBsfBLu8ZqogVZp3SroEpHPLcyLsFTt9gvHIs0h-m-mqG0LaokDEPyDwgr6sIb4aDGeRIqj0pk')
PAYPAL_CLIENT_SECRET = os.environ.get('PAYPAL_CLIENT_SECRET', 'EIvwAxzFZ57ZI38Tfr9lHWWMi33_a_XCGfjkn_Xf8U4ULnTKB8Du1_o_TdslL2uCVq7hKnm4Q2al7mfs')
PAYPAL_SANDBOX_TRANSACTION_ID = 'PAY-2G3660958Y2828046KX352DQ'

#
STRIPE_CLIENT_ID = os.environ.get('STRIPE_CLIENT_ID', 'pk_test_A4E5DX6OPfdZJnFEprqeEOjJ')
STRIPE_CLIENT_SECRET = os.environ.get('STRIPE_CLIENT_SECRET', 'sk_test_9Hc6zpdwLTZkbINTeuVZ6NP9')
STRIPE_SANDBOX_CARD = '4242424242424242'
STRIPE_FEE_PERCENT = 2.9
STRIPE_FEE_FLAT = 0.30

import paypalrestsdk
paypalrestsdk.configure({
    'mode': PAYPAL_MODE,
    'client_id': PAYPAL_CLIENT_ID,
    'client_secret': PAYPAL_CLIENT_SECRET,
})

import stripe
stripe.api_key = STRIPE_CLIENT_SECRET

# to have test queues prefixed
from components.queue import Queue
Queue.test = DEBUG

#
APNS_USE_SANDBOX = False
if APNS_USE_SANDBOX:
    __APNS_SUFFIX = 'Dev'
else:
    __APNS_SUFFIX = 'Prod'

APNS_CERT_FILE = BASE_DIR + '/resources/certs/push_H2O_' + __APNS_SUFFIX + '.pem'
APNS_KEY_FILE = BASE_DIR + '/resources/certs/push_H2O_' + __APNS_SUFFIX + '.key'

INSTALLED_APPS = (
    'api',
    'daemons',
    #'admin',
    #'django.contrib.auth',
    'django.contrib.contenttypes',
    #'django.contrib.staticfiles',
    'rest_framework',
)

MIDDLEWARE_CLASSES = (
)

ROOT_URLCONF = 'H2O.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'H2O.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'h2o_main',
        'USER': 'h2o_front',
        'PASSWORD': os.environ.get('DB_PASSWORD', '1g2Az8_lJ'),
        'HOST': '127.0.0.1',
        'PORT': os.environ.get('DB_PORT', 5432),
    },
}

RABBITMQ_USER =  'rabbitmq_user'
RABBITMQ_PASSWORD = os.environ.get('RABBITMQ_PASSWORD', '1Gh_7*2aS#+2K')
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'EXCEPTION_HANDLER': 'api.views_helpers.custom_exception_handler',
}

GCM_API_KEY = 'AIzaSyDl8iM7UK3rIBlefHx6Ofh173TZdDVltxs'
MANDRILL_API_KEY = 'zbAi_yqI1IkJ9WKhKky-8A'

URL = 'http://localhost:8000'
API_URL = URL

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

TEST_RUNNER = 'tests.no_db.NoDbTestRunner'



