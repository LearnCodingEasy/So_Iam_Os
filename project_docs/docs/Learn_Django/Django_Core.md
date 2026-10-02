## Django

<div dir="rtl" style="font-size:2vw">

1. الاعدادات الخاصة بمشروع Django الأساسي

</div>

<div dir="rtl" style="font-size:1.5vw">

- قائمة النطاقات أو العناوين المسموح للسيرفر يستقبل طلبات منها (لحماية الأمان).

- Backends - إعدادات المصادقة

  - هذه قائمة طرق المصادقة التي يقبلها النظام.

  - ModelBackend يدير تسجيل الدخول التقليدي بالبريد أو اسم المستخدم.

  - AuthenticationBackend من allauth يدير تسجيل الدخول الاجتماعي (Google، Facebook...).

- CSRF_TRUSTED_ORIGINS : عناوين يُسمح لها بتجاوز حماية CSRF (مهمة لتجربة الAPI من المتصفح).

- CORS_ALLOW_ALL_ORIGINS = True : تسمح لجميع المواقع بطلبات CORS (غير آمن للإنتاج).

- CSRF_COOKIE_SECURE و SESSION_COOKIE_SECURE: تعطيل خاصية التشفير على الكوكيز (مناسب للتطوير فقط).

</div>

### 2️⃣ Setup 🛠️

```python
# ______________ 📺 __________________
# أثناء التطوير
# للسماح بكل الطلبات أثناء التطوير
# لجهاز الكمبيوتر. IP استبدل 192.168.1.5 بعنوان

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "192.168.1.5"]
```

```python
# (AUTHENTICATION_BACKENDS) إعداد المصادقة

AUTHENTICATION_BACKENDS = (
    # تسجيل الدخول التقليدي
    "django.contrib.auth.backends.ModelBackend",
    # تسجيل الدخول عبر مواقع التواصل
    "allauth.account.auth_backends.AuthenticationBackend",
)
```

```python
# Allow CSRF requests from specific addresses

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://192.168.1.5:5173",
    "http://192.168.1.5:5174",
]

CORS_ALLOW_ALL_ORIGINS = True

CSRF_COOKIE_SECURE = False


SESSION_COOKIE_SECURE = False

```
