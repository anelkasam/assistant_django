from .settings import *


ALLOWED_HOSTS = ['0.0.0.0']


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!c7pu9ym3w094pj$^xhm4afcj5o@q!0hu9!sr@5hh_we@h(qqo'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DATABASE_NAME', 'assistant'),
        'USER': os.environ.get('DATABASE_USER', 'elena'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', '3414269'),
        'HOST': 'postgres',
        'PORT': os.environ.get('DATABASE_PORT', 5432)
    }
}

# Email configurations
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'anelka.dmytriieva@gmail.com'
EMAIL_HOST_PASSWORD = 'orofluido16'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

