# Python modules
import os

from django.conf.global_settings import AUTH_USER_MODEL

# Project modules
from settings.conf import *

# ----------------------------------------------
# Path
#
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_URLCONF = 'settings.urls'
WSGI_APPLICATION = 'settings.wsgi.application'
ASGI_APPLICATION = "settings.asgi.application"

# ----------------------------------------------
# Apps
#
DJANGO_AND_THIRD_PARTY_APPS = [
    "daphne",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
]
PROJECT_APPS = [
    'apps.blog.apps.BlogConfig',
    'apps.users.apps.UsersConfig',
    'apps.abstracts.apps.AbstractsConfig',
    'apps.notifications.apps.NotificationsConfig',
]
INSTALLED_APPS = DJANGO_AND_THIRD_PARTY_APPS + PROJECT_APPS

# ----------------------------------------------
# Middleware | Templates | Validators
#
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'settings.middleware.DebugRequestLoggingMiddleware',
]
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
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

# ----------------------------------------------
# Internationalization
#
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ----------------------------------------------
# Static | Media
#
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
AUTH_USER_MODEL='users.CustomUser'


# ----------------------------------------------
# REST FRAMEWORK
#
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# -----------------------------------------------
# CHANNEL LAYERS
#
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [("127.0.0.1", 6379)]},
    }
}

# -----------------------------------------------
# CACHES
#
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


# ----------------------------------------------
# Celery Configuration
#
_celery_redis_url = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_DB}"  # noqa: F405
CELERY_BROKER_URL = _celery_redis_url
CELERY_RESULT_BACKEND = _celery_redis_url
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE


# -----------------------------------------------
# LOGGERS
#
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    # -------------------
    # FORMATTERS
    # -------------------
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
        'verbose': {
            'format': '%(asctime)s %(levelname)s [%(name)s] '
                      '%(module)s: %(message)s',
        },
    },

    # -------------------
    # FILTERS
    # -------------------
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },

    # -------------------
    # HANDLERS
    # -------------------
    'handlers': {
        # Console handler
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
        },

        # Main rotating file handler
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'WARNING',
            'formatter': 'verbose',
            'filename': os.path.join(BASE_DIR, 'logs/app.log'),
            'maxBytes': 5 * 1024 * 1024,  # 5 MB
            'backupCount': 3,
        },

        # Debug-only request logger
        'debug_requests': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'verbose',
            'filename': os.path.join(BASE_DIR, 'logs/debug_requests.log'),
            'filters': ['require_debug_true'],  # Only active when DEBUG=True
        },
    },

    # -------------------
    # LOGGERS
    # -------------------
    'loggers': {
        # Your apps
        'users': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'blog': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },

        # Django request errors
        'django.request': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': False,
        },

        # Debug request logger
        'debug_requests': {
            'handlers': ['debug_requests'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}