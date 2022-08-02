import dj_database_url

from softskillspace.base_settings import *
# from softskillspace.settings.local.mailhog_settings import *
from softskillspace.utils.settings import get_env_variable

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-e1jb$w%@5d^3&lv%0@r@ccu+gkv())12a&obao#wzqtcaqrn9_"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

APPEND_SLASH = True

CSRF_TRUSTED_ORIGINS = ["http://*"]

X_FRAME_OPTIONS = "SAMEORIGIN"

DATABASES["default"] = dj_database_url.parse(
    f"sqlite:////{BASE_DIR.joinpath(BASE_DIR.name)}.db",
    conn_max_age=600,
)

DISABLE_SERVER_SIDE_CURSORS = True

INSTALLED_APPS += [
    "debug_toolbar",
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

if not DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

INTERNAL_IPS = [
    "127.0.0.1",
]

STATIC_ROOT = BASE_DIR / "assets"
