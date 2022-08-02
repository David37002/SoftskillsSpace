from pathlib import Path

from django.contrib import messages

from softskillspace.settings.packages.all_auth_settings import *
from softskillspace.settings.packages.ckeditor import *
from softskillspace.settings.packages.markdownify_settings import *
from softskillspace.settings.packages.resized_image_field import *
from softskillspace.settings.packages.rest_framework_settings import *
from softskillspace.settings.packages.stripe_settings import *
from softskillspace.utils.settings import get_env_variable

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.sites",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    # APP
    "blog",
    "chat",
    "faq",
    "home",
    "lesson",
    "location",
    "payment",
    "promotion",
    "student",
    "subject",
    "tutor",
    "career",
    # third party
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "channels",
    "ckeditor",
    "crispy_forms",
    # "ckeditor_uploader",
    # "hitcount",
    # "markdownify",
    # "rest_framework",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "softskillspace.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
                "django.template.context_processors.i18n",
                "softskillspace.utils.context_processors.page_data_filter",
                "softskillspace.utils.context_processors.user_stats",
            ],
        },
    },
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

WSGI_APPLICATION = "softskillspace.asgi.application"

ASGI_APPLICATION = "softskillspace.routing.application"

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

DATABASES = {}

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-gb"

TIME_ZONE = "Europe/London"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

LOGOUT_REDIRECT_URL = "home:index"

LOGIN_REDIRECT_URL = "home:index"

AUTH_USER_MODEL = "home.CustomUser"

STATIC_URL = "/assets/"

STATICFILES_DIRS = [
    BASE_DIR / "softskillspace/assets",
]

SITE_ID = 1

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_JQUERY_URL = "//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"

CKEDITOR_IMAGE_BACKEND = "pillow"

DJANGORESIZED_DEFAULT_QUALITY = 75

DJANGORESIZED_DEFAULT_KEEP_META = True

STATIC_ROOT = BASE_DIR / "assets"

MEDIA_URL = "/uploads/"

MEDIA_ROOT = get_env_variable(
    "MEDIA_ROOT",
    BASE_DIR /
    "softskillspace/uploads")

MESSAGE_TAGS = {messages.ERROR: "danger"}

CORS_ALLOW_ALL_ORIGINS = True

COMING_SOON = int(get_env_variable("COMING_SOON", "0"))

GOOGLE_ANALYTICS_ID = get_env_variable("GOOGLE_ANALYTICS_ID", "-")

CRISPY_TEMPLATE_PACK = "bootstrap4"
