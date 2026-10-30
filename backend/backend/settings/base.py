import os
from datetime import timedelta
from pathlib import Path

import sentry_sdk
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env.local")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
SECRET_KEY = os.getenv("SECRET_KEY")
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
INTERNAL_IPS = ["127.0.0.1"]

# Application definition

INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.events",
    "apps.accounts",
    "corsheaders",
    'rest_framework',
    'drf_spectacular',
    "rest_framework_simplejwt.token_blacklist",
    'channels',
    "debug_toolbar",
]

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    # To customize collected data (user info, request bodies, AI inputs/outputs),
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/
    # data_collection={"user_info": False},
)

# Tell Django to use ASGI instead of WSGI
ASGI_APPLICATION = 'backend.asgi.application'

# Channel layer configuration (In-Memory for dev/pet project)
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    },
}

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1', 'v2'],
    'VERSION_PARAM': 'version',
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": os.getenv("DEFAULT_DB_ENGINE"),
        "NAME": os.getenv("DEFAULT_DB_NAME"),
        "USER": os.getenv("DEFAULT_DB_USER"),
        "PASSWORD": os.getenv("DEFAULT_DB_PASSWORD"),
        "HOST": os.getenv("DEFAULT_DB_HOST"),
        "PORT": os.getenv("DEFAULT_DB_PORT"),
    },
    "social_event": {
        "ENGINE": os.getenv("SOCIAL_EVENT_DB_ENGINE"),
        "NAME": os.getenv("SOCIAL_EVENT_DB_NAME"),
        "USER": os.getenv("SOCIAL_EVENT_DB_USER"),
        "PASSWORD": os.getenv("SOCIAL_EVENT_DB_PASSWORD"),
        "HOST": os.getenv("SOCIAL_EVENT_DB_HOST"),
        "PORT": os.getenv("SOCIAL_EVENT_DB_PORT"),
        "TEST": {"DEPENDENCIES": []},
    },
}

# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"  # The absolute path to the directory where collectstatic will collect static files for deployment.
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"  # Use a storage backend that appends a unique hash to filenames.

DATABASE_ROUTERS = ["backend.router.ExternalDatabaseRouter"]

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",

]
CORS_ALLOW_CREDENTIALS = True  # For a real app, explicitly list the frontend origins.
CORS_ALLOWED_ORIGINS = ["http://localhost:5173"]

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}
