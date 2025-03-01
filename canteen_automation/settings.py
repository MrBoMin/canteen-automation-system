"""
Django settings for canteen_automation project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-cc=nk3iw=-f3g#7ub7&^7%*+)319xpm+zg%r)abx5l*he$hlzz'


DEBUG = True  # Disable debug mode in production
ALLOWED_HOSTS = ['*']  # Make sure to specify allowed hosts for production

# Application definition

INSTALLED_APPS = [
    # 'grappelli',
    # 'unfold',
    'django_daisy',    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pages',
    'users',
    'menu',
    'orders',
    'payments',
    'inventory',
    'notification',
    'admin_custom',
]

MIDDLEWARE = [
   
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',

    
]


ROOT_URLCONF = 'canteen_automation.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'orders.context_processors.cart_count',
                'orders.context_processors.base_view',
                'admin_custom.context_processors.admin_dashboard_data'
            ],
        },
    },
]

WSGI_APPLICATION = 'canteen_automation.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'canteen_db',
        'USER': 'postgres',
        'PASSWORD': 'felix',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


AUTH_USER_MODEL = 'users.User'

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/


STATIC_URL = '/static/'

# If you have custom static files
STATICFILES_DIRS = [
    BASE_DIR / "static",  # Your custom static files
]

# The location where `collectstatic` will collect files
STATIC_ROOT = BASE_DIR / "staticfiles"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [
    'users.backends.EmailBackend', 
    'django.contrib.auth.backends.ModelBackend',  # Optional for fallback
]



# Redirect users to the login page or any other page after logout
LOGIN_URL = 'login'  # Name of your login URL pattern
LOGIN_REDIRECT_URL = 'home'  # Redirect to home page after login
LOGOUT_REDIRECT_URL = '/users/login/'  # Or any URL of your choice

# Media Settings for Menu Items 

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')




# settings.py

APPS_REORDER = {
    "Inventory": ["Inventorys"],
    "Menu": ["Categorys", "Menu items", "Reviews"],
    "Notification": ["Notifications"],
    "Orders": ["Orders"],
    "Payments": ["Payments"],
    "Users": ["Roles", "Users"],
}


ADMIN_MENU_ORDER = [
    {"label": "Menu", "models": ["menu.Category", "menu.MenuItem", "menu.Review"]},
    {"label": "Notification", "models": ["notification.Notification"]},
    {"label": "Orders", "models": ["orders.Order"]},
    {"label": "Payments", "models": ["payments.Payment"]},
    {"label": "Users", "models": ["users.User"]},
]
