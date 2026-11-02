from .base import *  # noqa: F403

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
INTERNAL_IPS = ["127.0.0.1"]
INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
CORS_ALLOWED_ORIGINS = ["http://localhost:5173"]
CSRF_TRUSTED_ORIGINS = ["http://localhost:5173", "http://localhost:8000"]