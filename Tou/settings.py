"""
Django settings for EasyShareWeb project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8ly(56vh4ib1y=r++y@&1#t6=fll$ra-278+ioel^oqyp@)2o='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = "toupiao.Person"

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'toupiao',
    'yzxweb',
    'ueditor',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'Tou.urls'

WSGI_APPLICATION = 'Tou.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
if 'mac' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'easyshareweb',                      # Or path to database file if using sqlite3.
            'USER': 'root',                      # Not used with sqlite3.
            'PASSWORD': '000000',                  # Not used with sqlite3.
            'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
        }
    }


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Shanghai'


USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Additional locations of static files
STATICFILES_DIRS = (
    ("css", os.path.join(STATIC_ROOT, 'css')),
    ("image", os.path.join(STATIC_ROOT, 'image')),
    ("images", os.path.join(STATIC_ROOT, 'images')),
    ("img", os.path.join(STATIC_ROOT, 'img')),
    ("ueditor", os.path.join(STATIC_ROOT, 'ueditor')),
    ("upload", os.path.join(STATIC_ROOT, 'upload')),
    ("js", os.path.join(STATIC_ROOT, 'js')),
    ("jquery-ui", os.path.join(STATIC_ROOT, 'jquery-ui')),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
