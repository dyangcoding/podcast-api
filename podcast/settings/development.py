from .base import *
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
CLIENT_AUTH_URL = 'http://localhost:3000/auth/'