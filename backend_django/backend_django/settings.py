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
    ENV_FILES = (PROJECT_ROOT / ".env.production", PROJECT_ROOT / ".env")
else:
    ENV_FILES = (PROJECT_ROOT / ".env.local", PROJECT_ROOT / ".env")


# ====================================================
# LOAD ENVIRONMENT
# ====================================================
# Prefer the environment-specific file, then fall back to the project's .env.
# Existing process/container variables always take precedence.
for _env_file in ENV_FILES:
    if _env_file.is_file():
        load_dotenv(_env_file, override=False)
        break


# ====================================================
# DJANGO SETTINGS
# ====================================================

SECRET_KEY = config("SECRET_KEY", default="dev-only-change-me")

# Keep this value stable in a secret manager. Existing credentials encrypted
# with SECRET_KEY remain readable when this optional key is introduced.
AI_CREDENTIAL_ENCRYPTION_KEY = config(
    "AI_CREDENTIAL_ENCRYPTION_KEY", default="")

if ENVIRONMENT == "production" and (
    not AI_CREDENTIAL_ENCRYPTION_KEY or len(AI_CREDENTIAL_ENCRYPTION_KEY) < 32
):
    from django.core.exceptions import ImproperlyConfigured
    raise ImproperlyConfigured(
        "Production requires AI_CREDENTIAL_ENCRYPTION_KEY with at least 32 characters."
    )

# Production must fail closed rather than silently booting with development secrets.
if ENVIRONMENT == "production" and (
    SECRET_KEY == "dev-only-change-me"
    or len(SECRET_KEY) < 50
    or "GENERATE_" in SECRET_KEY
    or "REPLACE" in SECRET_KEY
):
    from django.core.exceptions import ImproperlyConfigured
    raise ImproperlyConfigured(
        "Production requires a unique SECRET_KEY with at least 50 characters."
    )

DEBUG = config(
    "DEBUG",
    default=(ENVIRONMENT != "production"),
    cast=bool,
)


# 2️⃣ Library Simplejwt
SIMPLE_JWT = {
    # Short-lived access tokens reduce the impact of a leaked bearer token.
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=14),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
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
# Redirects follow the configured frontend origin rather than hard-coded localhost URLs.
_FRONTEND_REDIRECT_BASE = config(
    "FRONTEND_URL",
    default=("https://app.example.com" if ENVIRONMENT ==
             "production" else "http://localhost:5173"),
).rstrip("/")
LOGIN_REDIRECT_URL = config(
    "LOGIN_REDIRECT_URL", default=f"{_FRONTEND_REDIRECT_BASE}/auth/callback")
LOGOUT_REDIRECT_URL = config("LOGOUT_REDIRECT_URL", default="/accounts/login/")
ACCOUNT_LOGOUT_REDIRECT_URL = config(
    "ACCOUNT_LOGOUT_REDIRECT_URL", default=f"{_FRONTEND_REDIRECT_BASE}/login")
ACCOUNT_SIGNUP_REDIRECT_URL = config(
    "ACCOUNT_SIGNUP_REDIRECT_URL", default=_FRONTEND_REDIRECT_BASE)
SOCIALACCOUNT_LOGIN_REDIRECT_URL = config(
    "SOCIALACCOUNT_LOGIN_REDIRECT_URL", default=f"{_FRONTEND_REDIRECT_BASE}/auth-callback/")

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
    default=_FRONTEND_REDIRECT_BASE,
)

CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in config(
        "CORS_ALLOWED_ORIGINS",
        default=("" if ENVIRONMENT == "production" else FRONTEND_URL),
    ).split(",")
    if origin.strip()
]
AUTH_USER_MODEL = "users_accounts.User"
ALLOWED_HOSTS = [h.strip() for h in config(
    "ALLOWED_HOSTS",
    default=("" if ENVIRONMENT ==
             "production" else "localhost,127.0.0.1,192.168.1.5,172.23.232.133"),
).split(",") if h.strip()]
CSRF_TRUSTED_ORIGINS = [o.strip() for o in config(
    "CSRF_TRUSTED_ORIGINS",
    default=("" if ENVIRONMENT == "production" else FRONTEND_URL),
).split(",") if o.strip()]
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

CORS_ALLOW_ALL_ORIGINS = config(
    "CORS_ALLOW_ALL_ORIGINS", default=False, cast=bool)
SECURE_SSL_REDIRECT = config(
    "SECURE_SSL_REDIRECT", default=(ENVIRONMENT == "production"), cast=bool
)
CSRF_COOKIE_SECURE = config("CSRF_COOKIE_SECURE", default=(
    ENVIRONMENT == "production"), cast=bool)
SESSION_COOKIE_SECURE = config("SESSION_COOKIE_SECURE", default=(
    ENVIRONMENT == "production"), cast=bool)
SECURE_HSTS_SECONDS = config("SECURE_HSTS_SECONDS", default=(
    31536000 if ENVIRONMENT == "production" else 0), cast=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = config(
    "SECURE_HSTS_INCLUDE_SUBDOMAINS", default=(ENVIRONMENT == "production"), cast=bool)
SECURE_HSTS_PRELOAD = config("SECURE_HSTS_PRELOAD", default=(
    ENVIRONMENT == "production"), cast=bool)
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"

if ENVIRONMENT == "production":
    from django.core.exceptions import ImproperlyConfigured

    if DEBUG:
        raise ImproperlyConfigured("DEBUG must be False in production.")
    if not ALLOWED_HOSTS or "*" in ALLOWED_HOSTS:
        raise ImproperlyConfigured("Set explicit production ALLOWED_HOSTS.")
    if not CORS_ALLOWED_ORIGINS:
        raise ImproperlyConfigured(
            "Set explicit production CORS_ALLOWED_ORIGINS.")
    if any(not origin.startswith("https://") for origin in CORS_ALLOWED_ORIGINS):
        raise ImproperlyConfigured("Production CORS origins must use HTTPS.")
    if not CSRF_TRUSTED_ORIGINS or any(not origin.startswith("https://") for origin in CSRF_TRUSTED_ORIGINS):
        raise ImproperlyConfigured(
            "Set explicit HTTPS production CSRF_TRUSTED_ORIGINS.")
    if CORS_ALLOW_ALL_ORIGINS:
        raise ImproperlyConfigured(
            "CORS_ALLOW_ALL_ORIGINS must be False in production.")
    if not SECURE_SSL_REDIRECT or not CSRF_COOKIE_SECURE or not SESSION_COOKIE_SECURE:
        raise ImproperlyConfigured(
            "Production SSL redirect and secure cookies must be enabled.")
    if SECURE_HSTS_SECONDS < 1:
        raise ImproperlyConfigured(
            "Production requires a positive SECURE_HSTS_SECONDS value.")

# 0️⃣ channels

ASGI_APPLICATION = "backend_django.asgi.application"

CHANNEL_LAYERS_BACKEND = config("CHANNEL_LAYERS_BACKEND", default="memory")
if CHANNEL_LAYERS_BACKEND == "redis":
    CHANNEL_LAYERS = {"default": {"BACKEND": "channels_redis.core.RedisChannelLayer", "CONFIG": {
        "hosts": [config("REDIS_URL", default="redis://127.0.0.1:6379/0")]}}}
else:
    CHANNEL_LAYERS = {"default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"}}

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

# AI provider credentials are user-scoped in AIProviderCredential. These
# environment values are optional application-level fallbacks only.
OPENAI_API_KEY = config("OPENAI_API_KEY", default="")
OPENAI_BASE_URL = config(
    "OPENAI_BASE_URL", default="https://api.openai.com/v1")
OPENAI_MODEL = config("OPENAI_MODEL", default="gpt-4o-mini")
GEMINI_API_KEY = config("GEMINI_API_KEY", default="")
GOOGLE_API_KEY = config("GOOGLE_API_KEY", default="")
GEMINI_BASE_URL = config(
    "GEMINI_BASE_URL", default="https://generativelanguage.googleapis.com/v1beta")
GEMINI_MODEL = config("GEMINI_MODEL", default="gemini-2.5-flash")
DEEPSEEK_API_KEY = config("DEEPSEEK_API_KEY", default="")
DEEPSEEK_BASE_URL = config(
    "DEEPSEEK_BASE_URL", default="https://api.deepseek.com")
DEEPSEEK_MODEL = config("DEEPSEEK_MODEL", default="deepseek-chat")
AI_MAX_PROVIDER_ATTEMPTS = config(
    "AI_MAX_PROVIDER_ATTEMPTS", default=5, cast=int)
AI_MAX_RETRIES_PER_PROVIDER = config(
    "AI_MAX_RETRIES_PER_PROVIDER", default=1, cast=int)
AI_TOTAL_DEADLINE_SECONDS = config(
    "AI_TOTAL_DEADLINE_SECONDS", default=60, cast=int)
AI_RETRY_BACKOFF_SECONDS = config(
    "AI_RETRY_BACKOFF_SECONDS", default=0.75, cast=float)
AI_PROVIDER_TIMEOUT_SECONDS = config(
    "AI_PROVIDER_TIMEOUT_SECONDS", default=35, cast=int)
AI_PROVIDER_CONNECT_TIMEOUT_SECONDS = config(
    "AI_PROVIDER_CONNECT_TIMEOUT_SECONDS", default=5, cast=int)
AI_MODEL_DISCOVERY_TIMEOUT_SECONDS = config(
    "AI_MODEL_DISCOVERY_TIMEOUT_SECONDS", default=8, cast=int)
AI_PROVIDER_TEST_TIMEOUT_SECONDS = config(
    "AI_PROVIDER_TEST_TIMEOUT_SECONDS", default=20, cast=int)

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
    "agents",
    "ai",
    "ai_tools_laboratory",
    "analytics",
    "architecture",
    "automation",
    "challenges",
    "codex",
    "core",
    "crm",
    "goals",
    "jobs_opportunity",
    "knowledge",
    "learning",
    "marketing",
    "memory",
    "notification",
    "personal_finance",
    "projects",
    "revenue",
    "sales",
    "scraper",
    "social",
    "tasks",
    "users_accounts",
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
            "OPTIONS": {"timeout": 30},
        }
    }

if ENVIRONMENT == "production" and DATABASE_ENGINE != "postgresql":
    from django.core.exceptions import ImproperlyConfigured
    raise ImproperlyConfigured(
        "Production must use DATABASE_ENGINE=postgresql; SQLite is for local development only."
    )


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
# Fail fast when Redis is unavailable. A synchronous API request must never
# spend two minutes waiting for a broker/result-store reconnect.
CELERY_BROKER_CONNECTION_TIMEOUT = config(
    "CELERY_BROKER_CONNECTION_TIMEOUT", default=3, cast=int)
CELERY_BROKER_CONNECTION_RETRY = config(
    "CELERY_BROKER_CONNECTION_RETRY", default=False, cast=bool)
CELERY_BROKER_CONNECTION_MAX_RETRIES = config(
    "CELERY_BROKER_CONNECTION_MAX_RETRIES", default=1, cast=int)
CELERY_TASK_PUBLISH_RETRY = config(
    "CELERY_TASK_PUBLISH_RETRY", default=False, cast=bool)
CELERY_RESULT_BACKEND_ALWAYS_RETRY = config(
    "CELERY_RESULT_BACKEND_ALWAYS_RETRY", default=False, cast=bool)
CELERY_RESULT_BACKEND_MAX_RETRIES = config(
    "CELERY_RESULT_BACKEND_MAX_RETRIES", default=1, cast=int)
CELERY_TASK_IGNORE_RESULT = config(
    "CELERY_TASK_IGNORE_RESULT", default=False, cast=bool)
CELERY_TIMEZONE = TIME_ZONE

# AI provider resilience settings are defined once above the provider defaults.
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
