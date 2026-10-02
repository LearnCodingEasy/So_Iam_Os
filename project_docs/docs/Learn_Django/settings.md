# Setting

## Path

```python
from pathlib import Path
```

## BASE_DIR

```python
BASE_DIR = Path(__file__).resolve().parent.parent
```

## SECRET_KEY

<div class="" dir="rtl"></div>

```python
# Default
SECRET_KEY = '************'
```

<div class="" dir="rtl">
المكتبة دي مفيدة جدًا عشان تفصل المعلومات الحساسة (زي الـ SECRET_KEY، بيانات قواعد البيانات، API keys، …) عن كود المشروع نفسه.
</div>

[Decouple](decouple.md)

```python
from decouple import config

SECRET_KEY = config('SECRET_KEY')
```

## DEBUG

<div class="" dir="rtl">
تحذير أمني: لا تعمل مع تشغيل تصحيح الأخطاء في الإنتاج!

</div>

```python
# Default
DEBUG = True
```

<div class="" dir="rtl">
المكتبة دي مفيدة جدًا عشان تفصل المعلومات الحساسة (زي الـ SECRET_KEY، بيانات قواعد البيانات، API keys، …) عن كود المشروع نفسه.
</div>

[Decouple](decouple.md)

```python
from decouple import config
DEBUG = config('DEBUG', default=True, cast=bool)
```

## ALLOWED_HOSTS

<div class="" dir="rtl">

ALLOWED_HOSTS ده المتغير اللي بنحدد فيه الدومينات أو الآيبيهات اللي مسموح لها تشغل المشروع

للسماح بكل الطلبات أثناء التطوير

استبدل 192.168.1.5 بعنوان IP لجهاز الكمبيوتر.

</div>

```python
# Default
ALLOWED_HOSTS = []
# ______________ 📺 __________________
# My Code
# ALLOWED_HOSTS = ['*']
# ALLOWED_HOSTS = ['127.0.0.1']
# ALLOWED_HOSTS = [
#     "localhost",
#     "127.0.0.1",
#     "192.168.1.5",
#     '0.0.0.0'
## Firebase يسمح بجميع نطاقات
#     ".firebaseapp.com",
## Firebase Hosting يسمح باستضافة
#     ".web.app",
# ]
```

## INSTALLED_APPS

```python
INSTALLED_APPS = [
  # Default
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',

    # ...
    # My Apps
    'users_accounts',
    # ...
    # Libraries
    'rest_framework',
    'corsheaders',
    # ...
]
```

## MIDDLEWARE

```python
MIDDLEWARE = [
    # Default
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

## ROOT_URLCONF

```python
ROOT_URLCONF = 'backend_django.urls'

```

## TEMPLATES

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Default
        'DIRS': [],
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
```

## WSGI_APPLICATION

```python
WSGI_APPLICATION = 'backend.wsgi.application'
```

## DATABASES

```python
DATABASES = {
    # Default
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

## AUTH_PASSWORD_VALIDATORS

```python
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
```

## Internationalization

```python
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
```

## STATIC_URL

```python
STATIC_URL = 'static/'
```

## DEFAULT_AUTO_FIELD

```python
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```
