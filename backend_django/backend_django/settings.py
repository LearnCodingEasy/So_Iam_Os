# 📄 [ settings.py ] ملف
import os

from pathlib import Path

# 1️⃣ Library Decouple & Dotenv
from decouple import config
from dotenv import load_dotenv

# 2️⃣ Library SimpleJWT
from datetime import timedelta


# ====================================================
# BASE DIRECTORY
# ====================================================

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent


# ====================================================
# ENVIRONMENT
# ====================================================

ENVIRONMENT = os.getenv(
    "DJANGO_ENV",
    "local"
)


# ====================================================
# ENVIRONMENT FILE
# ====================================================

if ENVIRONMENT == "production":
    ENV_FILE = PROJECT_ROOT / ".env.production"
else:
    ENV_FILE = PROJECT_ROOT / ".env.local"


# ====================================================
# LOAD ENVIRONMENT
# ====================================================

load_dotenv(ENV_FILE)


# ====================================================
# DJANGO SETTINGS
# ====================================================

SECRET_KEY = config("SECRET_KEY", default="dev-only-change-me")

DEBUG = config(
    "DEBUG",
    default=(ENVIRONMENT != "production"),
    cast=bool,
)


# 2️⃣ Library Simplejwt
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=180),
    "ROTATE_REFRESH_TOKENS": False,
}

# ====================================================
# 🔐 Django REST Framework
# ====================================================

REST_FRAMEWORK = {
    # 🔑 Authentication
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),

    # 🛡️ Default permissions
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}

# 3️⃣ Library django-allauth [Allauth]
SITE_ID = 1
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_SIGNUP_FIELDS = ["email", "name", ]
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'
SOCIALACCOUNT_AUTO_SIGNUP = True
ACCOUNT_LOGOUT_ON_GET = True

# 🔵 Google OAuth
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": config("GOOGLE_OAUTH_CLIENT_ID"),
            "secret": config("GOOGLE_OAUTH_CLIENT_SECRET"),
            "key": "",
        },
        "SCOPE": ["profile", "email", ],
        "AUTH_PARAMS": {"access_type": "online", },
        "OAUTH_PKCE_ENABLED": True,
    },
}
SOCIALACCOUNT_ADAPTER = (
    "users_accounts.adapter.MySocialAccountAdapter"
)
# 🔄 Redirect Configuration
# LOGIN_REDIRECT_URL = "/"
# LOGIN_REDIRECT_URL = 'http://localhost:5173/'
# LOGIN_REDIRECT_URL = 'http://localhost:5173/about/'
# LOGIN_REDIRECT_URL = '/accounts/google/login/callback/'
LOGIN_REDIRECT_URL = 'http://localhost:5173/auth/callback'
LOGOUT_REDIRECT_URL = "/accounts/login/"
ACCOUNT_LOGOUT_REDIRECT_URL = 'http://localhost:5173/login'
ACCOUNT_SIGNUP_REDIRECT_URL = 'http://localhost:5173'
SOCIALACCOUNT_LOGIN_REDIRECT_URL = 'http://localhost:5173/auth-callback/'

# 📧 Development Email Backend
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# 🕐 Session Configuration
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7  # 7 أيام
SESSION_SAVE_EVERY_REQUEST = True

SOCIALACCOUNT_AUTO_SIGNUP = True
ACCOUNT_UNIQUE_EMAIL = True


# 🌐 CORS Headers
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
CORS_EXPOSE_HEADERS = ['Content-Type', 'X-CSRFToken']


# 🧪 Development Debugging
print(f"✅ Settings loaded Django")
# print(f"✅ AUTH_USER_MODEL: {AUTH_USER_MODEL}")
print(f"✅ SOCIALACCOUNT_ADAPTER: {SOCIALACCOUNT_ADAPTER}")


# 1️⃣ Django_Core
# WEBSITE_URL = "http://127.0.0.1:8000"
WEBSITE_URL = config(
    "WEBSITE_URL",
    default="http://127.0.0.1:8000",
)

FRONTEND_URL = config(
    "FRONTEND_URL",
    default="http://localhost:5173",
)

CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in config("CORS_ALLOWED_ORIGINS", default=FRONTEND_URL).split(",")
    if origin.strip()
]
AUTH_USER_MODEL = "users_accounts.User"
ALLOWED_HOSTS = [h.strip() for h in config(
    "ALLOWED_HOSTS",
    default="localhost,127.0.0.1,192.168.1.5,172.23.232.133",
).split(",") if h.strip()]
CSRF_TRUSTED_ORIGINS = [o.strip() for o in config(
    "CSRF_TRUSTED_ORIGINS",
    default=FRONTEND_URL,
).split(",") if o.strip()]
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

CORS_ALLOW_ALL_ORIGINS = config("CORS_ALLOW_ALL_ORIGINS", default=False, cast=bool)
SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=False, cast=bool)
CSRF_COOKIE_SECURE = config("CSRF_COOKIE_SECURE", default=(ENVIRONMENT == "production"), cast=bool)
SESSION_COOKIE_SECURE = config("SESSION_COOKIE_SECURE", default=(ENVIRONMENT == "production"), cast=bool)
SECURE_HSTS_SECONDS = config("SECURE_HSTS_SECONDS", default=(31536000 if ENVIRONMENT == "production" else 0), cast=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = config("SECURE_HSTS_INCLUDE_SUBDOMAINS", default=(ENVIRONMENT == "production"), cast=bool)
SECURE_HSTS_PRELOAD = config("SECURE_HSTS_PRELOAD", default=(ENVIRONMENT == "production"), cast=bool)
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"

# 0️⃣ channels

ASGI_APPLICATION = "backend_django.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

SO_IAM_OS_DEBUG_CONSOLE = config(
    "SO_IAM_OS_DEBUG_CONSOLE",
    default=False,
    cast=bool,
)
LOGGING = {
    "version": 1,

    "disable_existing_loggers": False,

    "formatters": {
        "debug_console": {
            "format": (
                "{asctime} | "
                "{levelname} | "
                "{name} | "
                "{message}"
            ),
            "style": "{",
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "debug_console",
        },
    },

    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}


if SO_IAM_OS_DEBUG_CONSOLE:

    LOGGING["handlers"]["websocket"] = {
        "class": "core.debug_console.handlers.WebSocketLogHandler",
        "formatter": "debug_console",
    }

    LOGGING["root"]["handlers"].append(
        "websocket"
    )

#
AI_DEFAULT_PROVIDER = config(
    "AI_DEFAULT_PROVIDER",
    default="ollama",
)

OLLAMA_BASE_URL = config(
    "OLLAMA_BASE_URL",
    default="http://127.0.0.1:11434",
)

OLLAMA_MODEL = config(
    "OLLAMA_MODEL",
    default="gemma3:4b",
)

OPENROUTER_API_KEY = config(
    "OPENROUTER_API_KEY",
    default="",
)

OPENROUTER_BASE_URL = config(
    "OPENROUTER_BASE_URL",
    default="https://openrouter.ai/api/v1",
)

OPENROUTER_MODEL = config(
    "OPENROUTER_MODEL",
    default="openai/gpt-4o-mini",
)
# Application definition
INSTALLED_APPS = [
    # ================================================
    # 🔥 Daphne
    # ================================================
    "daphne",
    # ================================================
    # Django
    # ================================================
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # ================================================
    # 📚 Libraries
    # ================================================

    # 1️⃣ djangorestframework [DRF]
    'rest_framework',
    'rest_framework.authtoken',
    # 2️⃣ djangorestframework-simplejwt [Auth]
    "rest_framework_simplejwt",
    'rest_framework_simplejwt.token_blacklist',
    # 3️⃣ django-allauth [Allauth]
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    # 4️⃣ corsheaders
    "corsheaders",
    # 0️⃣ channels
    "channels",
    "django_celery_results",
    "django_celery_beat",
    # ================================================
    # 📚 Apps
    # ================================================

    "ai",
    "automation",
    "core",
    "codex",
    "goals",
    "jobs_opportunity",
    "knowledge",
    "learning",
    "memory",
    "notification",
    "projects",
    "social",
    "tasks",
    "users_accounts",
    "challenges",
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 4️⃣ corsheaders
    "corsheaders.middleware.CorsMiddleware",

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 3️⃣ django-allauth [Allauth]
    "allauth.account.middleware.AccountMiddleware"
]

ROOT_URLCONF = 'backend_django.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend_django.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.1/ref/settings/#databases

DATABASE_ENGINE = config("DATABASE_ENGINE", default="sqlite3")
if DATABASE_ENGINE == "postgresql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config("POSTGRES_DB"),
            "USER": config("POSTGRES_USER"),
            "PASSWORD": config("POSTGRES_PASSWORD"),
            "HOST": config("POSTGRES_HOST", default="127.0.0.1"),
            "PORT": config("POSTGRES_PORT", default=5432, cast=int),
            "CONN_MAX_AGE": config("POSTGRES_CONN_MAX_AGE", default=60, cast=int),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# Password validation
# https://docs.djangoproject.com/en/6.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.1/howto/static-files/

STATIC_URL = 'static/'
# Access path for media files (such as images and files uploaded by users)
MEDIA_URL = "media/"
# Specify a "media" folder in the project to store uploaded media files
MEDIA_ROOT = BASE_DIR / "media"


# Email
# https://docs.djangoproject.com/en/6.1/topics/email/#topic-email-configuration

EMAIL_BACKEND = config(
    "EMAIL_BACKEND",
    default="django.core.mail.backends.console.EmailBackend",
)
EMAIL_HOST = config("EMAIL_HOST", default="")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)



# ====================================================
# Redis / Celery / Cache
# ====================================================
REDIS_URL = config("REDIS_URL", default="redis://127.0.0.1:6379/0")
CELERY_BROKER_URL = config("CELERY_BROKER_URL", default=REDIS_URL)
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND", default=REDIS_URL)
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
CELERY_BEAT_SCHEDULE = {
    "generate-daily-learning-tasks": {
        "task": "tasks.tasks.generate_daily_learning_tasks_for_all_users",
        "schedule": 86400.0,
    },
}
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_URL,
        "TIMEOUT": 300,
    }
}
