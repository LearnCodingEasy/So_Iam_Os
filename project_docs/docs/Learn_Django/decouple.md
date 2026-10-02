# 🔐 Django Environment Configuration — Decouple + Dotenv

> دمج `python-decouple` و`python-dotenv` لإدارة إعدادات وSecrets مشروع So_Iam_OS حسب بيئة التشغيل.

---

### 1. 🎯 Purpose

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

الهدف من النظام ده هو فصل إعدادات مشروع **So_Iam_OS** عن كود Django نفسه.

بدل ما نحط البيانات الحساسة مباشرة داخل `settings.py` مثل:

- `SECRET_KEY`
- `Database Password`
- Google OAuth Client ID
- Google OAuth Client Secret
- API Keys
- إعدادات البيئة

هنحطها داخل ملفات Environment، وبعد كده Django يقرأها وقت التشغيل.

في المشروع هنستخدم مكتبتين مع بعض:

**python-dotenv**

مسؤولة عن تحميل ملف `.env` المناسب إلى Environment Variables.

**python-decouple**

مسؤولة عن قراءة القيم داخل `settings.py` باستخدام `config()`، مع إمكانية تحديد Default Values وتحويل أنواع البيانات.

</div>

```text
Environment File
       ↓
python-dotenv
       ↓
Environment Variables
       ↓
python-decouple
       ↓
config()
       ↓
settings.py
       ↓
Django
       ↓
So_Iam_OS
```

---

### 2. 🧠 Concept

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

الفكرة الأساسية إن `settings.py` مايبقاش فيه Secrets حقيقية.

بدل:

</div>

```python
SECRET_KEY = "REAL_SECRET_KEY"
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

نستخدم:

</div>

```python
SECRET_KEY = config("SECRET_KEY")
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

لكن عندنا مشكلة إضافية في So_Iam_OS:

إحنا مش عايزين ملف Environment واحد فقط.

إحنا محتاجين نميز بين:

**Local Development**

و

**Production**

لذلك نستخدم:

</div>

```text
DJANGO_ENV
    │
    ├── local
    │      ↓
    │   .env.local
    │
    └── production
           ↓
      .env.production
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

بعد تحديد البيئة، `python-dotenv` يقوم بتحميل الملف المناسب.

وبعد تحميله، `python-decouple` يقرأ القيم باستخدام `config()`.

</div>

---

### 3. 🔧 Requirements

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

قبل استخدام النظام ده، المشروع يحتاج:

- Python.
- Django.
- Virtual Environment.
- `python-decouple`.
- `python-dotenv`.
- ملف `settings.py`.
- ملف `manage.py`.
- Environment File لكل بيئة تشغيل.

ويجب تثبيت المكتبات داخل الـVirtual Environment الخاصة بمشروع So_Iam_OS.

</div>

```cmd
venv\Scripts\activate
```

---

### 4. 🛠️ Installation / Setup

#### 📦 Install python-decouple

```cmd
pip install python-decouple
```

#### 📦 Install python-dotenv

```cmd
pip install python-dotenv
```

#### 📁 Environment Files

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

في So_Iam_OS هنستخدم ملفات منفصلة للبيئات.

</div>

```text
So_Iam_OS/
│
├── .env.local
├── .env.production
├── .gitignore
│
├── manage.py
│
└── backend_django/
    ├── settings.py
    ├── urls.py
    ├── asgi.py
    └── wsgi.py
```

#### 🏠 `.env.local`

```env
DJANGO_ENV=local

SECRET_KEY=YOUR_LOCAL_SECRET_KEY

DEBUG=True

DB_NAME=YOUR_LOCAL_DATABASE_NAME
DB_USER=YOUR_LOCAL_DATABASE_USER
DB_PASSWORD=YOUR_LOCAL_DATABASE_PASSWORD
DB_HOST=localhost
DB_PORT=5432

GOOGLE_OAUTH_CLIENT_ID=YOUR_LOCAL_GOOGLE_CLIENT_ID
GOOGLE_OAUTH_CLIENT_SECRET=YOUR_LOCAL_GOOGLE_CLIENT_SECRET
```

#### 🚀 `.env.production`

```env
DJANGO_ENV=production

SECRET_KEY=YOUR_PRODUCTION_SECRET_KEY

DEBUG=False

DB_NAME=YOUR_PRODUCTION_DATABASE_NAME
DB_USER=YOUR_PRODUCTION_DATABASE_USER
DB_PASSWORD=YOUR_PRODUCTION_DATABASE_PASSWORD
DB_HOST=YOUR_PRODUCTION_DATABASE_HOST
DB_PORT=5432

GOOGLE_OAUTH_CLIENT_ID=YOUR_PRODUCTION_GOOGLE_CLIENT_ID
GOOGLE_OAUTH_CLIENT_SECRET=YOUR_PRODUCTION_GOOGLE_CLIENT_SECRET
```

#### ⚙️ settings.py

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

الكود الأساسي المستخدم في المشروع لدمج المكتبتين:

</div>

```python
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

SECRET_KEY = config("SECRET_KEY")

DEBUG = config(
    "DEBUG",
    default=False,
    cast=bool
)
```

#### 🔐 Important Environment Rule

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

في الكود الحالي، `DJANGO_ENV` يتم قراءته **قبل** تشغيل `load_dotenv()`.

وده معناه إن `DJANGO_ENV` لازم يكون متوفر بالفعل في Environment الخاصة بالعملية لو عايزين نستخدمه لاختيار الملف.

يعني:

</div>

```text
DJANGO_ENV
    ↓
Choose Environment File
    ↓
load_dotenv()
    ↓
config()
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

لذلك لا نعتمد على وجود `DJANGO_ENV` داخل `.env.production` أو `.env.local` لاختيار الملف نفسه في هذا التصميم.

</div>

#### 🚫 .gitignore

```gitignore
.env
*.env
.env.local
.env.production

__pycache__/
*.py[cod]

venv/
.venv/

db.sqlite3
```

---

### 5. 🚀 Usage

#### 🔐 SECRET_KEY

```python
SECRET_KEY = config("SECRET_KEY")
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

Django يقرأ `SECRET_KEY` من Environment بدل كتابتها داخل Source Code.

</div>

#### 🐛 DEBUG

```python
DEBUG = config(
    "DEBUG",
    default=False,
    cast=bool
)
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

استخدام `cast=bool` مهم لأن Environment Variables يتم التعامل معها كنصوص، وإحنا محتاجين قيمة Boolean.

</div>

#### 🗄️ Database

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config(
            "DB_HOST",
            default="localhost"
        ),
        "PORT": config(
            "DB_PORT",
            default="5432"
        ),
    }
}
```

#### 🔵 Google OAuth

```python
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": config(
                "GOOGLE_OAUTH_CLIENT_ID"
            ),
            "secret": config(
                "GOOGLE_OAUTH_CLIENT_SECRET"
            ),
            "key": "",
        },
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online"
        },
        "OAUTH_PKCE_ENABLED": True,
    },
}
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

وبالتالي إعدادات Google OAuth نفسها لا تحتوي على الـSecrets الحقيقية.

</div>

---

### 6. 📁 Structure

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

الهيكل المستخدم في So_Iam_OS:

</div>

```text
So_Iam_OS/
│
├── .env.local
├── .env.production
├── .gitignore
│
├── manage.py
│
└── backend_django/
    │
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    ├── asgi.py
    └── wsgi.py
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

المسؤوليات:

`.env.local`

إعدادات بيئة التطوير المحلية.

`.env.production`

إعدادات بيئة Production.

`settings.py`

يحدد البيئة، يحمل ملف Environment، وبعدها يقرأ القيم.

`python-dotenv`

يحمل Environment File.

`python-decouple`

يقرأ القيم من خلال `config()`.

`.gitignore`

يمنع ملفات Environment من الصعود إلى Git.

</div>

---

### 7. 🧩 Important Concepts

#### 🔹 python-dotenv

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

مسؤولة في التصميم الحالي عن تحميل ملف `.env.local` أو `.env.production` إلى Environment Variables.

</div>

```python
from dotenv import load_dotenv

load_dotenv(ENV_FILE)
```

#### 🔹 python-decouple

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

مسؤولة عن قراءة القيم من خلال `config()`.

</div>

```python
from decouple import config

SECRET_KEY = config("SECRET_KEY")
```

#### 🔹 Environment Selection

```python
ENVIRONMENT = os.getenv(
    "DJANGO_ENV",
    "local"
)
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

السطر ده يحدد البيئة الحالية.

لو مفيش `DJANGO_ENV`، القيمة الافتراضية هي:

`local`

</div>

#### 🔹 Environment File Selection

```python
if ENVIRONMENT == "production":
    ENV_FILE = PROJECT_ROOT / ".env.production"
else:
    ENV_FILE = PROJECT_ROOT / ".env.local"
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

لو البيئة `production` يتم استخدام `.env.production`.

وأي قيمة أخرى تؤدي إلى استخدام `.env.local` حسب الكود الحالي.

</div>

#### 🔹 BASE_DIR

```python
BASE_DIR = Path(__file__).resolve().parent.parent
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

يمثل المسار الأساسي لمشروع Django.

</div>

#### 🔹 PROJECT_ROOT

```python
PROJECT_ROOT = BASE_DIR.parent
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

يستخدم الكود ده للوصول إلى جذر المشروع الذي توجد فيه ملفات `.env.local` و`.env.production`.

</div>

---

### 8. 💻 Examples

#### 🏠 Local Environment

```text
DJANGO_ENV=local
        ↓
.env.local
        ↓
load_dotenv()
        ↓
config()
        ↓
settings.py
```

#### 🚀 Production Environment

```text
DJANGO_ENV=production
        ↓
.env.production
        ↓
load_dotenv()
        ↓
config()
        ↓
settings.py
```

#### 🔐 Complete Configuration Example

```python
import os

from pathlib import Path

from decouple import config
from dotenv import load_dotenv

from datetime import timedelta


BASE_DIR = Path(__file__).resolve().parent.parent

PROJECT_ROOT = BASE_DIR.parent


ENVIRONMENT = os.getenv(
    "DJANGO_ENV",
    "local"
)


if ENVIRONMENT == "production":
    ENV_FILE = PROJECT_ROOT / ".env.production"
else:
    ENV_FILE = PROJECT_ROOT / ".env.local"


load_dotenv(ENV_FILE)


SECRET_KEY = config("SECRET_KEY")


DEBUG = config(
    "DEBUG",
    default=False,
    cast=bool
)
```

#### 🗄️ Database Example

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config(
            "DB_HOST",
            default="localhost"
        ),
        "PORT": config(
            "DB_PORT",
            default="5432"
        ),
    }
}
```

#### 🔵 Google OAuth Example

```python
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": config(
                "GOOGLE_OAUTH_CLIENT_ID"
            ),
            "secret": config(
                "GOOGLE_OAUTH_CLIENT_SECRET"
            ),
            "key": "",
        },
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online"
        },
        "OAUTH_PKCE_ENABLED": True,
    },
}
```

---

### 9. ❌ Common Mistakes

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

#### ❌ وضع Secrets داخل `settings.py`

لا نكتب:

</div>

```python
SECRET_KEY = "REAL_SECRET"
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

نستخدم:

</div>

```python
SECRET_KEY = config("SECRET_KEY")
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

#### ❌ رفع `.env` إلى Git

لازم ملفات Environment تكون موجودة في `.gitignore`.

#### ❌ وضع Secrets حقيقية في Knowledge Documentation

ملفات المعرفة تستخدم Placeholders فقط.

#### ❌ نسيان `cast=bool`

لازم نستخدم:

</div>

```python
DEBUG = config(
    "DEBUG",
    default=False,
    cast=bool
)
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

#### ❌ الخلط بين دور المكتبتين

لازم نفهم إن التصميم الحالي بيفصل الأدوار:

`dotenv`

تحميل ملف Environment.

`decouple`

قراءة القيم باستخدام `config()`.

#### ❌ محاولة استخدام `DJANGO_ENV` من ملف لم يتم تحميله بعد

في الكود الحالي، اختيار `.env` يحدث قبل `load_dotenv()`.

لذلك `DJANGO_ENV` المستخدم لاختيار الملف يجب أن يكون متوفرًا قبل عملية تحميل الملف.

</div>

---

### 10. 🧠 Why?

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

ليه So_Iam_OS محتاج النظام ده؟

لأن المشروع عنده أكثر من بيئة تشغيل.

في Development عندنا إعدادات مختلفة عن Production.

مثلًا:

- Database مختلفة.
- `DEBUG` مختلف.
- Google OAuth credentials مختلفة.
- `SECRET_KEY` مختلفة.
- إعدادات مستقبلية مختلفة.

بدل تغيير `settings.py` كل مرة، بنغير Environment فقط.

</div>

```text
                    So_Iam_OS
                        │
              ┌─────────┴─────────┐
              │                   │
           Local              Production
              │                   │
       .env.local        .env.production
              │                   │
              └─────────┬─────────┘
                        ↓
                 python-dotenv
                        ↓
                Environment Vars
                        ↓
                python-decouple
                        ↓
                    settings.py
```

---

### 11. 🔗 Project Usage

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

داخل مشروع **So_Iam_OS**، النظام ده جزء أساسي من Backend Configuration.

يتم استخدامه مع:

- Django.
- PostgreSQL.
- Google OAuth.
- django-allauth.
- SimpleJWT.
- أي API Keys مستقبلية.
- أي Secrets مستقبلية.

وبالتالي `settings.py` لا يكون مكان تخزين الأسرار، وإنما مكان استخدام الإعدادات.

</div>

```text
So_Iam_OS
│
├── Frontend
│
└── Backend
    │
    └── Django
        │
        └── settings.py
            │
            ├── Environment Selection
            │
            ├── python-dotenv
            │
            ├── python-decouple
            │
            ├── SECRET_KEY
            │
            ├── DEBUG
            │
            ├── PostgreSQL
            │
            ├── Google OAuth
            │
            ├── django-allauth
            │
            └── SimpleJWT
```

---

### 12. 🤖 AI Reference

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

عند تعامل الـAI مع إعدادات Environment في So_Iam_OS، يجب الالتزام بالتصميم الموجود.

الـAI لا يقوم بتغيير النظام إلى طريقة أخرى بدون طلب.

الـArchitecture الحالية تعتمد على دمج:

`python-dotenv`

مع:

`python-decouple`

`python-dotenv` مسؤول عن تحميل ملف Environment.

`python-decouple` مسؤول عن قراءة القيم باستخدام `config()`.

البيئة يتم تحديدها باستخدام:

`DJANGO_ENV`

القيمة الافتراضية هي:

`local`

إذا كانت البيئة:

`production`

يتم اختيار:

`.env.production`

وفي غير ذلك يتم اختيار:

`.env.local`

ملفات Environment تحتوي على Secrets ولا يجب رفعها إلى Git.

لا يتم وضع Secrets حقيقية داخل Documentation.

عند إضافة إعداد حساس جديد للمشروع، يجب استخدام Environment Variable بدل وضع القيمة السرية مباشرة داخل Source Code.

</div>

```text
Project:
So_Iam_OS

Backend:
Django

Environment Management:
python-dotenv + python-decouple

Environment Variable:
DJANGO_ENV

Default Environment:
local

Local File:
.env.local

Production File:
.env.production

Loader:
python-dotenv

Reader:
python-decouple

Reader Function:
config()

Main Configuration:
settings.py

Sensitive Configuration:
- SECRET_KEY
- Database Credentials
- Google OAuth Credentials
- API Keys
- Future Secrets

Git Rule:
Environment files must not be committed.

Security Rule:
Never expose real Secrets in documentation.
```

---

### 13. 📊 Current Status

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

الحالة هنا يجب أن تعكس ما تم تنفيذه فعليًا داخل المشروع، وليس مجرد وجود الكود في ملف المعرفة.

حسب حالة المشروع الحالية، `settings.py` و`urls.py` هما الملفات التي تم تنفيذها بالفعل، أما دمج كل إعدادات Environment الإضافية فيجب اعتباره منفذًا فقط بعد التأكد من تشغيله واختباره داخل المشروع.

</div>

| Task                                  | Status |
| ------------------------------------- | ------ |
| `settings.py` موجود                   | ✅     |
| `urls.py` موجود                       | ✅     |
| Install `python-decouple`             | ⬜     |
| Install `python-dotenv`               | ⬜     |
| Create `.env.local`                   | ⬜     |
| Create `.env.production`              | ⬜     |
| Configure `DJANGO_ENV`                | ⬜     |
| Configure Environment Selection       | ⬜     |
| Configure `load_dotenv()`             | ⬜     |
| Configure `config()`                  | ⬜     |
| Move `SECRET_KEY` to Environment      | ⬜     |
| Move `DEBUG` to Environment           | ⬜     |
| Move Database Configuration           | ⬜     |
| Move Google OAuth Configuration       | ⬜     |
| Add Environment files to `.gitignore` | ⬜     |
| Test Local Environment                | ⬜     |
| Test Production Environment           | ⬜     |
| Verify Django Settings                | ⬜     |

---

### 14. ✅ Checklist

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

قائمة مراجعة تنفيذ نظام Environment Configuration في So_Iam_OS:

</div>

- [x] `settings.py` موجود
- [x] `urls.py` موجود
- [ ] Install `python-decouple`
- [ ] Install `python-dotenv`
- [ ] Create `.env.local`
- [ ] Create `.env.production`
- [ ] Configure `DJANGO_ENV`
- [ ] Configure `BASE_DIR`
- [ ] Configure `PROJECT_ROOT`
- [ ] Configure Environment Selection
- [ ] Configure `load_dotenv()`
- [ ] Import `config`
- [ ] Configure `SECRET_KEY`
- [ ] Configure `DEBUG`
- [ ] Configure PostgreSQL
- [ ] Configure Google OAuth
- [ ] Add `.env` files to `.gitignore`
- [ ] Test Local Environment
- [ ] Test Database Configuration
- [ ] Test Google OAuth Configuration
- [ ] Test Production Environment
- [ ] Verify Secrets are not committed

---

### 15. 🔗 Related Documentation

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

المواضيع والملفات المرتبطة بالنظام ده داخل So_Iam_OS:

</div>

- `backend_django/settings.py`
- `backend_django/urls.py`
- `.env.local`
- `.env.production`
- `.gitignore`
- Python Virtual Environment
- Django Settings
- PostgreSQL
- `python-decouple`
- `python-dotenv`
- django-allauth
- Google OAuth
- SimpleJWT
- CORS
- Environment Variables
- Secrets Management

---

### 16. 📝 Notes

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

النظام الحالي مصمم على أساس وجود بيئتين رئيسيتين:

**Local**

و

**Production**

والفكرة الأساسية هي:

**نفس Source Code**

لكن:

**Environment مختلفة**

وبالتالي لا نحتاج إلى تعديل الكود في كل مرة ننتقل فيها من Development إلى Production.

النقطة المهمة في التصميم الحالي هي ترتيب التنفيذ:

أولًا يتم تحديد `DJANGO_ENV`.

بعدها يتم اختيار `.env.local` أو `.env.production`.

بعدها يتم تشغيل `load_dotenv()`.

بعدها يتم استخدام `config()` لقراءة القيم.

</div>

```text
DJANGO_ENV
    ↓
Environment Selection
    ↓
.env.local / .env.production
    ↓
load_dotenv()
    ↓
Environment Variables
    ↓
config()
    ↓
settings.py
    ↓
Django
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

كمان مهم إننا ملتزمين في So_Iam_OS بالفصل بين:

**Configuration**

و

**Secrets**

`settings.py` يحتوي على طريقة استخدام الإعدادات.

أما القيم الحساسة نفسها فتأتي من Environment.

ولا يتم وضع Google Client Secret أو Database Password أو Django Secret Key الحقيقية داخل Knowledge Documentation.

</div>

#### ⚡ Quick Reference

```cmd
pip install python-decouple
pip install python-dotenv
```

```python
import os

from pathlib import Path

from decouple import config
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

PROJECT_ROOT = BASE_DIR.parent


ENVIRONMENT = os.getenv(
    "DJANGO_ENV",
    "local"
)


if ENVIRONMENT == "production":
    ENV_FILE = PROJECT_ROOT / ".env.production"
else:
    ENV_FILE = PROJECT_ROOT / ".env.local"


load_dotenv(ENV_FILE)


SECRET_KEY = config("SECRET_KEY")

DEBUG = config(
    "DEBUG",
    default=False,
    cast=bool
)
```

```gitignore
.env
*.env
.env.local
.env.production
```

#### 🧠 Architecture Rule

```text
python-dotenv
      │
      │ Load
      ▼
Environment Variables
      │
      │ Read
      ▼
python-decouple
      │
      │ config()
      ▼
settings.py
      │
      ▼
Django
      │
      ▼
So_Iam_OS
```
