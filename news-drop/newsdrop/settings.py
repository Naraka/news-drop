"""
Django settings for newsdrop project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from dotenv import load_dotenv
from pathlib import Path
try:
    load_dotenv()
except: pass

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drops',
    'storages',
    'users'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'newsdrop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'users.context_processors.profile_image',
            ],
        },
    },
]

WSGI_APPLICATION = 'newsdrop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/


# #nombre de la carpeta en la que estan los estaticos cuando los carga la web
# STATIC_URL = "https://storage.googleapis.com/newsdropstatic/staticfiles3/"

#path donde esta referenciada los staticos en local
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

#donde deberia star el buket
#cuando collecstatic path y nombre de la carpeta donde se van
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


from google.oauth2 import service_account

if 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ:
    GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
        os.environ['GOOGLE_APPLICATION_CREDENTIALS']
    )
else:
    GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
        os.path.join(BASE_DIR, 'news-drop-796857b8eb91.json')
    )

GS_PROJECT_ID = 'news-drop'
GS_MEDIA_BUCKET_NAME = 'djangobucket-newsdropped'
GS_STATIC_BUCKET_NAME = 'djangostatic-bucket'

STORAGES = {
    'default': {
        'BACKEND': 'storages.backends.gcloud.GoogleCloudStorage',
        'OPTIONS': {
            'bucket_name': GS_MEDIA_BUCKET_NAME,
            'project_id': GS_PROJECT_ID,
            'credentials': GS_CREDENTIALS,
        },
    },
    'staticfiles': {
        'BACKEND': 'storages.backends.gcloud.GoogleCloudStorage',
        'OPTIONS': {
            'bucket_name': GS_STATIC_BUCKET_NAME,
            'project_id': GS_PROJECT_ID,
            'credentials': GS_CREDENTIALS,
        },
    },
}

MEDIA_URL = f'https://storage.googleapis.com/{GS_MEDIA_BUCKET_NAME}/media/'

STATIC_URL = f'https://storage.googleapis.com/{GS_STATIC_BUCKET_NAME}/static/'






# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login required redirect path
LOGIN_URL = '/signin/'


SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_DOMAIN = 'app.newsdropped.com'
CSRF_TRUSTED_ORIGINS = ['https://app.newsdropped.com']
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_AGE = 3600