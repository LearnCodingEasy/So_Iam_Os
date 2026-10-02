# django-allauth

> إعداد متقدم لـ `django-allauth` لإدارة Email Authentication وGoogle OAuth وSessions وRedirects داخل مشروع So_Iam_OS.

---

### 1. 🎯 Purpose

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

الجزء ده مسؤول عن إعداد `django-allauth` داخل مشروع Django بحيث نقدر ندير نظام الحسابات والمصادقة باستخدام:

- Email Authentication.
- Google OAuth.
- Email Verification.
- Social Account Signup.
- Session Management.
- Login Redirect.
- Logout Redirect.
- Custom Social Account Adapter.
- CORS Headers المطلوبة للتعامل مع الـFrontend.

الهدف النهائي هو ربط نظام Authentication الموجود في Django بالـFrontend الخاص بـ **So_Iam_OS**.

</div>

---

### 2. 🧠 Concept

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

الفكرة هنا إن `django-allauth` بيكون طبقة مسؤولة عن هوية المستخدم والحسابات.

في البداية كان Google OAuth معمول بشكل مباشر داخل `settings.py` باستخدام:

`client_id`

و

`secret`

لكن الإعداد المتقدم بيستخدم `python-decouple` لقراءة البيانات الحساسة من Environment Variables بدل كتابتها مباشرة داخل الكود.

الـFlow:

Frontend
↓
Django / allauth
↓
Email أو Google OAuth
↓
User Identity
↓
users_accounts
↓
Authentication

</div>

```text
Frontend
   │
   ▼
Django
   │
   ▼
django-allauth
   │
   ├── Email
   │
   └── Google OAuth
           │
           ▼
      User Identity
           │
           ▼
     users_accounts
```

---

### 3. 🔧 Requirements

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

قبل تطبيق الإعدادات دي، المشروع محتاج:

- Django.
- `django-allauth`.
- `python-decouple`.
- Django Sites Framework.
- تطبيق `users_accounts`.
- Google OAuth Application.
- Frontend شغال.
- Environment Variables تحتوي على Google OAuth credentials.
- إعداد CORS مناسب للتواصل مع الـFrontend.

</div>

---

### 4. 🛠️ Installation / Setup

#### 📚 Install django-allauth

```cmd
pip install django-allauth
```

#### 📚 Install python-decouple

```cmd
pip install python-decouple
```

#### 📦 INSTALLED_APPS

```python
INSTALLED_APPS = [
    # Libraries

    "django.contrib.sites",

    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
]
```

#### ⚙️ AccountMiddleware

```python
MIDDLEWARE = [
    # Add AccountMiddleware for allauth

    "allauth.account.middleware.AccountMiddleware",
]
```

#### 🌐 URLs

```python
# 📄 backend_django/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("accounts/", include("allauth.urls")),
]
```

#### 🔐 Google OAuth Configuration

```python
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": config("GOOGLE_OAUTH_CLIENT_ID"),
            "secret": config("GOOGLE_OAUTH_CLIENT_SECRET"),
            "key": "",
        },
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
        "OAUTH_PKCE_ENABLED": True,
    },
}
```

> لا يتم تخزين `GOOGLE_OAUTH_CLIENT_SECRET` الحقيقي داخل ملف المعرفة أو Git.

#### 📧 Account Configuration

```python
ACCOUNT_LOGOUT_ON_GET = True

ACCOUNT_EMAIL_VERIFICATION = "optional"

ACCOUNT_USER_MODEL_USERNAME_FIELD = None

ACCOUNT_SIGNUP_FIELDS = [
    "email",
    "name",
]

ACCOUNT_LOGIN_METHODS = {
    "email",
}

ACCOUNT_UNIQUE_EMAIL = True

ACCOUNT_EMAIL_REQUIRED = True
```

#### 🔄 Redirect Configuration

```python
LOGIN_REDIRECT_URL = "http://localhost:5173/auth/callback"

LOGOUT_REDIRECT_URL = "/accounts/login/"

ACCOUNT_LOGOUT_REDIRECT_URL = (
    "http://localhost:5173/login"
)

ACCOUNT_SIGNUP_REDIRECT_URL = (
    "http://localhost:5173"
)

SOCIALACCOUNT_LOGIN_REDIRECT_URL = (
    "http://localhost:5173/auth-callback/"
)
```

#### 📧 Development Email Backend

```python
EMAIL_BACKEND = (
    "django.core.mail.backends.console.EmailBackend"
)
```

#### 🕐 Session Configuration

```python
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7  # 7 أيام

SESSION_SAVE_EVERY_REQUEST = True
```

#### 🌐 CORS Headers

```python
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

CORS_EXPOSE_HEADERS = [
    "Content-Type",
    "X-CSRFToken",
]
```

---

### 5. 🚀 Usage

#### 📧 Email Authentication

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

النظام هنا يعتمد على Email كطريقة تسجيل الدخول بدل Username.

</div>

```python
ACCOUNT_USER_MODEL_USERNAME_FIELD = None

ACCOUNT_SIGNUP_FIELDS = [
    "email",
    "name",
]

ACCOUNT_LOGIN_METHODS = {
    "email",
}

ACCOUNT_UNIQUE_EMAIL = True

ACCOUNT_EMAIL_REQUIRED = True
```

#### ✉️ Email Verification

```python
ACCOUNT_EMAIL_VERIFICATION = "optional"
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

القيم المذكورة في الإعدادات:

- `none` → من غير تحقق.
- `optional` → التحقق اختياري.
- `mandatory` → لازم المستخدم يتحقق عشان الحساب يتفعل.

الإعداد المستخدم حاليًا في المحتوى هو:

`optional`

</div>

#### 🔵 Google OAuth

```python
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": config("GOOGLE_OAUTH_CLIENT_ID"),
            "secret": config("GOOGLE_OAUTH_CLIENT_SECRET"),
            "key": "",
        },
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
        "OAUTH_PKCE_ENABLED": True,
    },
}
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

الـGoogle Provider يستخدم:

- `profile`
- `email`

والـOAuth configuration مفعّل فيها PKCE.

</div>

#### 👤 Automatic Signup

```python
SOCIALACCOUNT_AUTO_SIGNUP = True
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

ده يسمح بإنشاء الحساب تلقائيًا عند استخدام Social Authentication.

</div>

#### 🔌 Custom Adapter

```python
SOCIALACCOUNT_ADAPTER = (
    "users_accounts.adapter.MySocialAccountAdapter"
)
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

الـCustom Adapter موجود ضمن تطبيق `users_accounts` ويتم استخدامه لتخصيص التعامل مع Social Accounts.

</div>

---

### 6. 📁 Structure

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

الملفات المرتبطة بالإعداد:

</div>

```text
So_Iam_OS/
│
├── backend_django/
│   ├── settings.py
│   └── urls.py
│
├── users_accounts/
│   └── adapter.py
│
├── .env
│
└── ...
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

المسؤوليات:

`settings.py`

إعداد django-allauth وGoogle OAuth والـSession والـRedirects.

`urls.py`

ربط URLs الخاصة بـallauth.

`users_accounts/adapter.py`

الـCustom Social Account Adapter.

`.env`

تخزين Environment Variables الحساسة.

</div>

---

### 7. 🧩 Important Concepts

#### 🔐 Environment Variables

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

بدل ما نحط Google credentials مباشرة داخل `settings.py`، بنقرأها باستخدام `config()`.

</div>

```python
client_id = config("GOOGLE_OAUTH_CLIENT_ID")

secret = config("GOOGLE_OAUTH_CLIENT_SECRET")
```

#### 🔑 OAuth PKCE

```python
"OAUTH_PKCE_ENABLED": True
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

الإعداد ده بيفعّل PKCE ضمن OAuth flow المستخدم مع Google.

</div>

#### 🌐 Redirect URLs

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

بعد نجاح Login أو Logout، المستخدم يتم توجيهه إلى Frontend routes محددة.

</div>

```text
Login
  ↓
http://localhost:5173/auth/callback

Logout
  ↓
http://localhost:5173/login

Signup
  ↓
http://localhost:5173

Social Login
  ↓
http://localhost:5173/auth-callback/
```

#### 🕐 Sessions

```python
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7

SESSION_SAVE_EVERY_REQUEST = True
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

الإعدادات دي مرتبطة بإدارة Django Session.

</div>

#### 🌍 CORS

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

CORS يسمح للـFrontend والـBackend بالتعامل مع بعض عبر HTTP عندما تكون origins مختلفة.

</div>

---

### 8. 💻 Examples

#### 🔐 Environment Configuration

```env
GOOGLE_OAUTH_CLIENT_ID=YOUR_GOOGLE_CLIENT_ID
GOOGLE_OAUTH_CLIENT_SECRET=YOUR_GOOGLE_CLIENT_SECRET
```

#### 🐍 Django Settings

```python
from decouple import config

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": config("GOOGLE_OAUTH_CLIENT_ID"),
            "secret": config("GOOGLE_OAUTH_CLIENT_SECRET"),
            "key": "",
        },
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
        "OAUTH_PKCE_ENABLED": True,
    },
}
```

#### 🔄 Redirects

```python
LOGIN_REDIRECT_URL = (
    "http://localhost:5173/auth/callback"
)

ACCOUNT_LOGOUT_REDIRECT_URL = (
    "http://localhost:5173/login"
)

ACCOUNT_SIGNUP_REDIRECT_URL = (
    "http://localhost:5173"
)

SOCIALACCOUNT_LOGIN_REDIRECT_URL = (
    "http://localhost:5173/auth-callback/"
)
```

#### 🧪 Development Debugging

```python
print("✅ Settings loaded Django")
print(f"✅ AUTH_USER_MODEL: {AUTH_USER_MODEL}")
print(
    f"✅ SOCIALACCOUNT_ADAPTER: "
    f"{SOCIALACCOUNT_ADAPTER}"
)
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

الـprint statements دي مفيدة أثناء Development للتأكد إن `settings.py` اتحمل وإن الإعدادات الأساسية موجودة.

</div>

---

### 9. ❌ Common Mistakes

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

أهم الأخطاء:

1. وضع Google Client Secret مباشرة داخل `settings.py`.
2. رفع `.env` إلى Git.
3. نسيان `allauth.socialaccount.providers.google`.
4. نسيان `django.contrib.sites`.
5. نسيان `SITE_ID`.
6. نسيان `AccountMiddleware`.
7. نسيان ربط `allauth.urls`.
8. استخدام Redirect URL مختلف عن المسجل في Google OAuth.
9. استخدام `localhost` URLs في Production بدون تعديلها.
10. عدم ضبط CORS عند وجود Frontend منفصل.
11. عدم وجود `users_accounts.adapter.MySocialAccountAdapter` مع تفعيل هذا المسار.
12. الاعتماد على Console Email Backend في Production.

</div>

---

### 10. 🧠 Why?

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

ليه بنستخدم `config()`؟

عشان نفصل الـSecrets عن Source Code.

بدل:

</div>

```python
"secret": "REAL_SECRET"
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

نستخدم:

</div>

```python
"secret": config("GOOGLE_OAUTH_CLIENT_SECRET")
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

وبالتالي الـSecret يكون خارج الكود.

وليه بنستخدم Redirect URLs؟

لأن Authentication Flow محتاج يعرف المستخدم يرجع لفين بعد انتهاء العملية.

وليه بنستخدم Custom Adapter؟

لأن المشروع ممكن يحتاج Logic خاص أثناء إنشاء أو ربط Social Account، بدل الاعتماد على السلوك الافتراضي فقط.

</div>

---

### 11. 🔗 Project Usage

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

داخل **So_Iam_OS**، الإعدادات دي بتربط Backend Django بالـFrontend Vue عن طريق Authentication Flow.

</div>

```text
Vue Frontend
     │
     ▼
Django Backend
     │
     ▼
django-allauth
     │
     ├──────────────┐
     ▼              ▼
   Email         Google
     │              │
     └──────┬───────┘
            ▼
       User Identity
            │
            ▼
     users_accounts
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

الـFrontend المستخدم في الإعدادات الحالية يعمل على:

`http://localhost:5173`

</div>

---

### 12. 🤖 AI Reference

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

عند تعامل الـAI مع إعدادات `django-allauth` داخل المشروع، لازم يعرف الآتي:

- `django-allauth` مسؤول عن Account + Social Authentication.
- Login Method هو Email.
- Google هو Social Provider.
- Google credentials يتم قراءتها من Environment Variables.
- `python-decouple` مستخدم لقراءة الـEnvironment Variables.
- PKCE مفعّل في Google OAuth.
- `SOCIALACCOUNT_AUTO_SIGNUP = True`.
- يوجد Custom Adapter.
- الـCustom Adapter مساره `users_accounts.adapter.MySocialAccountAdapter`.
- Frontend Development URL هو `http://localhost:5173`.
- Email Backend الحالي هو Console Email Backend.
- Session Age مضبوطة على 7 أيام.
- CORS Headers محددة في settings.
- `settings.py` هو مركز إعدادات allauth.
- `urls.py` يربط `allauth.urls` تحت `/accounts/`.

</div>

```text
Project:
So_Iam_OS

Technology:
django-allauth

Dependency:
python-decouple

Authentication:
- Email
- Google OAuth

Google Credentials:
- Environment Variables

Google Scope:
- profile
- email

OAuth:
- PKCE Enabled
- access_type = online

Frontend:
http://localhost:5173

Custom Adapter:
users_accounts.adapter.MySocialAccountAdapter

Email Backend:
django.core.mail.backends.console.EmailBackend

Session:
- 7 Days
- SAVE_EVERY_REQUEST = True

URL Prefix:
 /accounts/
```

---

### 13. 📊 Current Status

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

الحالة هنا تمثل التنفيذ الفعلي داخل المشروع، وليس مجرد وجود الكود داخل ملف المعرفة.

</div>

| Task                                   | Status |
| -------------------------------------- | ------ |
| Install `django-allauth`               | ⬜     |
| Install `python-decouple`              | ⬜     |
| Configure `INSTALLED_APPS`             | ⬜     |
| Add `AccountMiddleware`                | ⬜     |
| Configure Email Authentication         | ⬜     |
| Configure Email Verification           | ⬜     |
| Configure Google OAuth                 | ⬜     |
| Configure Google Environment Variables | ⬜     |
| Enable OAuth PKCE                      | ⬜     |
| Configure `SITE_ID`                    | ⬜     |
| Configure Social Auto Signup           | ⬜     |
| Configure Custom Adapter               | ⬜     |
| Configure Redirect URLs                | ⬜     |
| Configure Session                      | ⬜     |
| Configure CORS Headers                 | ⬜     |
| Configure Email Backend                | ⬜     |
| Connect `allauth.urls`                 | ⬜     |
| Test Email Authentication              | ⬜     |
| Test Google Authentication             | ⬜     |
| Test Frontend Callback                 | ⬜     |
| Production Configuration               | ⬜     |

---

### 14. ✅ Checklist

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

قائمة تنفيذ ومراجعة `django-allauth`:

</div>

- [ ] Install `django-allauth`
- [ ] Install `python-decouple`
- [ ] Add `django.contrib.sites`
- [ ] Add `allauth`
- [ ] Add `allauth.account`
- [ ] Add `allauth.socialaccount`
- [ ] Add Google Provider
- [ ] Add `AccountMiddleware`
- [ ] Configure Email Authentication
- [ ] Configure Email Verification
- [ ] Configure Google OAuth
- [ ] Add Google credentials to Environment Variables
- [ ] Enable PKCE
- [ ] Configure `SITE_ID`
- [ ] Enable Social Auto Signup
- [ ] Configure Custom Adapter
- [ ] Configure Login Redirect
- [ ] Configure Logout Redirect
- [ ] Configure Signup Redirect
- [ ] Configure Social Login Redirect
- [ ] Configure Session
- [ ] Configure CORS
- [ ] Configure Development Email Backend
- [ ] Connect `allauth.urls`
- [ ] Run migrations
- [ ] Test Email Authentication
- [ ] Test Google OAuth
- [ ] Test Frontend Callback
- [ ] Review Production Security

---

### 15. 🔗 Related Documentation

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

الملفات والمواضيع المرتبطة:

</div>

- `backend_django/settings.py`
- `backend_django/urls.py`
- `users_accounts/`
- `users_accounts/adapter.py`
- Django Authentication
- Django Sites Framework
- Google OAuth
- OAuth PKCE
- `python-decouple`
- Environment Variables
- CORS
- Django Sessions
- Django REST Framework
- SimpleJWT

---

### 16. 📝 Notes

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

الإعداد الحالي يمثل Development Configuration لأن الـFrontend يستخدم:

`http://localhost:5173`

وكمان Email Backend الحالي هو Console Backend.

لذلك لا يتم اعتبار الإعداد الحالي Production Configuration.

كمان الـGoogle Client ID والـClient Secret الموجودين في النص الأصلي تم استبدالهم في ملف المعرفة بـPlaceholders.

لو كانت القيم الأصلية حقيقية وتم نشرها أو مشاركتها، الأفضل اعتبار الـSecret مكشوفًا وعمل Rotation / Regeneration له.

المعماريًا، `django-allauth` مسؤول عن:

**Account + Social Authentication**

بينما Authentication الخاصة بالـREST API يمكن فصلها في طبقة أخرى مثل:

**SimpleJWT**

</div>

```text
So_Iam_OS
    │
    ├── Frontend
    │      └── Vue
    │
    └── Backend
           │
           └── Django
                 │
                 └── django-allauth
                       │
                       ├── Email
                       │
                       └── Google OAuth
                              │
                              ▼
                         User Identity
                              │
                              ▼
                       users_accounts
```
