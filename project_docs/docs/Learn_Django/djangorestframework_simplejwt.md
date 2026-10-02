# 🔐 Django REST Framework SimpleJWT

> مكتبة لإضافة JWT Authentication إلى Django REST Framework، واستخدام Access Token وRefresh Token للتحقق من هوية المستخدم وحماية الـAPI.

---

### 1. 🎯 Purpose

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

SimpleJWT بنستخدمها لإضافة نظام Authentication قائم على JSON Web Tokens داخل Django REST Framework.

الهدف الأساسي هو إن المستخدم بعد تسجيل الدخول يحصل على:

- Access Token
- Refresh Token

وبعد كده يستخدم الـAccess Token للوصول إلى الـAPI المحمية.

</div>

```text id="jwtflow1"
User
  ↓
Login
  ↓
SimpleJWT
  ↓
Access Token + Refresh Token
  ↓
Authenticated API Requests
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

وفي مشروع So_Iam_OS، JWT هي جزء أساسي من نظام Identity & Authentication.

</div>

---

### 2. 🧠 Concept

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

بدل ما الـServer يعتمد فقط على Session لتحديد المستخدم، SimpleJWT بتستخدم Tokens.

عند تسجيل الدخول:

</div>

```text id="jwtflow2"
Username / Email
        +
    Password
        ↓
   Login API
        ↓
   SimpleJWT
        ↓
 ┌─────────────────┐
 │ Access Token    │
 │ Refresh Token   │
 └─────────────────┘
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

الـAccess Token بيستخدم للوصول إلى الـAPI.

والـRefresh Token بيستخدم للحصول على Access Token جديد عند انتهاء صلاحية الـAccess Token.

</div>

```text id="jwtflow3"
Access Token
    ↓
API Request
    ↓
JWTAuthentication
    ↓
Authenticated User
```

---

### 3. 🔧 Requirements

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

قبل استخدام SimpleJWT، لازم يكون عندك:

- Python
- Virtual Environment
- Django
- Django REST Framework
- User Model
- API Layer

</div>

```text id="jwtrequirements"
Python
   ↓
Virtual Environment
   ↓
Django
   ↓
Django REST Framework
   ↓
User Model
   ↓
SimpleJWT
```

---

### 4. 🛠️ Installation / Setup

#### 📦 Install SimpleJWT

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

داخل Virtual Environment الخاصة بالمشروع:

</div>

```cmd id="jwtinstall"
pip install djangorestframework-simplejwt
```

#### ⚙️ Add Authentication Configuration

```python id="jwtsettings1"
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

الإعداد السابق معناه إن الـAPI بشكل افتراضي هتستخدم JWT للتحقق من هوية المستخدم، والـEndpoints هتحتاج User Authenticated.

</div>

#### 🔐 SimpleJWT Configuration

```python id="jwtsettings2"
from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=180),
    "ROTATE_REFRESH_TOKENS": False,
}
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

الإعدادات الحالية:

`ACCESS_TOKEN_LIFETIME` → Access Token صالح لمدة 30 يوم.

`REFRESH_TOKEN_LIFETIME` → Refresh Token صالح لمدة 180 يوم.

`ROTATE_REFRESH_TOKENS` → عند ضبطها على `False`، لا يتم إصدار Refresh Token جديد تلقائيًا عند استخدام Refresh Token.

</div>

> ⚠️ ملاحظة أمنية: مدد 30 يوم للـAccess Token و180 يوم للـRefresh Token طويلة نسبيًا، لذلك يجب مراجعتها وفق نموذج الأمان الخاص بالمشروع، خصوصًا لو النظام سيتعامل مع بيانات حساسة.

#### 📦 Token Blacklist

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

لو المشروع محتاج إبطال Refresh Tokens عند Logout، لازم تفعيل تطبيق الـBlacklist الخاص بـSimpleJWT.

</div>

```python id="jwtblacklist"
INSTALLED_APPS = [
    # Libraries
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
]
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

بعد إضافة Blacklist App، يجب تشغيل migrations:

</div>

```cmd id="jwtmigrate"
python manage.py migrate
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

أما `djangorestframework-simplejwt` فهي الحزمة التي يتم تثبيتها باستخدام pip، بينما `rest_framework_simplejwt.token_blacklist` هو التطبيق المستخدم لتخزين وإدارة الـBlacklisted Tokens.

</div>

#### 📋 Update Dependencies

```cmd id="jwtfreeze"
pip freeze > requirements.txt
```

---

### 5. 🚀 Usage

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

في So_Iam_OS، SimpleJWT مستخدمة في دورة حياة المستخدم الأساسية:

</div>

```text id="jwtlifecycle"
Login
  ↓
Issue Tokens
  ↓
Authenticated Requests
  ↓
Refresh Access Token
  ↓
Logout
  ↓
Blacklist Refresh Token
```

---

#### 🔑 Login

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

بنستخدم `TokenObtainPairView` لإنشاء Access Token وRefresh Token.

ولأن المشروع محتاج تحديث `is_online` عند تسجيل الدخول، تم إنشاء Serializer مخصص.

</div>

```python id="jwtlogin"
# users_accounts/views.py

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        # تحديث is_online عند تسجيل الدخول
        user = self.user

        user.is_online = True
        user.save(
            update_fields=["is_online"]
        )

        return data


class MyTokenObtainPairView(TokenObtainPairView):

    serializer_class = MyTokenObtainPairSerializer
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

عند نجاح Login، الـSerializer بيعمل:

1. تنفيذ عملية JWT الأصلية.
2. الحصول على المستخدم.
3. تغيير `is_online` إلى `True`.
4. حفظ التغيير.
5. إرجاع الـTokens.

</div>

---

#### 🔄 Refresh Token

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

عند انتهاء Access Token، الـClient يقدر يستخدم Refresh Token للحصول على Access Token جديد.

</div>

```text id="jwtrefresh"
Refresh Token
      ↓
Refresh API
      ↓
New Access Token
```

---

#### 🚪 Logout

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

عند تسجيل الخروج، المشروع بيستقبل Refresh Token، ثم يحاول عمل Blacklist له، وبعدها يغير حالة المستخدم إلى Offline.

</div>

```python id="jwtlogout"
# users_accounts/views.py

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class LogoutAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"error": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Blacklist refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()

            # تحديث حالة المستخدم
            user = request.user

            if user and user.is_authenticated:
                user.is_online = False
                user.save(
                    update_fields=["is_online"]
                )

            return Response(
                {"message": "تم تسجيل الخروج بنجاح"},
                status=status.HTTP_200_OK
            )

        except Exception as e:

            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

هنا Logout بيعمل حاجتين رئيسيتين:

1. إبطال Refresh Token عن طريق Blacklist.
2. تحديث حالة المستخدم إلى `is_online = False`.

</div>

---

### 6. 📁 Structure

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

الجزء الخاص بـJWT ممكن يكون موزع بالشكل التالي:

</div>

```text id="jwtstructure"
backend_django/
│
├── settings.py
├── urls.py
│
├── users_accounts/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── signals.py
│   └── ...
│
└── requirements.txt
```

#### JWT Architecture

```text id="jwtarchitecture"
Frontend
   │
   ├── Login
   │
   ↓
users_accounts
   │
   ↓
SimpleJWT
   │
   ├── Access Token
   └── Refresh Token
   │
   ↓
Protected API
```

---

### 7. 🧩 Important Concepts

#### 🔹 Access Token

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

Token قصير أو متوسط العمر يستخدمه الـClient للوصول إلى الـProtected APIs.

في الإعداد الحالي مدته 30 يوم.

</div>

#### 🔹 Refresh Token

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

Token أطول عمرًا يستخدم للحصول على Access Token جديد.

في الإعداد الحالي مدته 180 يوم.

</div>

#### 🔹 JWT Authentication

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

آلية تستخدم الـJWT Token لتحديد المستخدم الذي يرسل الـRequest.

</div>

#### 🔹 IsAuthenticated

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

Permission تمنع المستخدم غير المسجل من الوصول إلى الـAPI.

</div>

#### 🔹 Token Blacklist

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

آلية تسمح بإبطال Refresh Token بحيث لا يمكن استخدامه مرة أخرى بعد تسجيل الخروج.

</div>

#### 🔹 Token Rotation

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

عند تفعيل Refresh Token Rotation، يمكن إصدار Refresh Token جديد عند استخدام الـRefresh Token القديم، مع إمكانية إبطال القديم حسب الإعدادات.

في المشروع الحالي:

</div>

```python
"ROTATE_REFRESH_TOKENS": False,
```

#### 🔹 `is_online`

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

حقل داخل User Model يستخدمه المشروع لتسجيل حالة المستخدم Online أو Offline.

لكن مهم جدًا: وجود JWT Token صالح لا يعني بالضرورة أن المستخدم Online فعليًا في هذه اللحظة.

</div>

---

### 8. 💻 Examples

#### Example — Protected API

```python id="jwtprotected"
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class ProfileAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response({
            "user_id": request.user.id,
            "username": request.user.username,
            "is_online": request.user.is_online,
        })
```

#### Example — JWT URLs

```python id="jwturls"
# backend_django/urls.py

from django.contrib import admin
from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from users_accounts.views import (
    MyTokenObtainPairView,
    LogoutAPIView,
)


urlpatterns = [

    # JWT
    path(
        "api/login/",
        MyTokenObtainPairView.as_view(),
        name="token_obtain",
    ),

    path(
        "api/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),

    path(
        "api/logout/",
        LogoutAPIView.as_view(),
        name="logout",
    ),

    # Admin
    path(
        "admin/",
        admin.site.urls,
    ),
]
```

#### API Endpoints

```text id="jwtendpoints"
POST /api/login/
        ↓
Access + Refresh Token


POST /api/refresh/
        ↓
New Access Token


POST /api/logout/
        ↓
Blacklist Refresh Token
        ↓
is_online = False
```

---

### 9. ❌ Common Mistakes

#### 1. نسيان Blacklist App

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

لو هتستخدم:

</div>

```python
token.blacklist()
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

لازم يكون Token Blacklist App متفعل ومigrations متطبقة.

</div>

```python
"rest_framework_simplejwt.token_blacklist",
```

ثم:

```cmd
python manage.py migrate
```

---

#### 2. الاعتقاد أن Logout يحذف JWT من كل مكان

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

JWT مش Session تقليدية.

عمل Logout من الـBackend لا يعني أن Access Token الموجود بالفعل عند الـClient اختفى تلقائيًا.

لذلك تصميم Logout لازم يحدد بوضوح كيفية التعامل مع Access Token وRefresh Token.

</div>

---

#### 3. استخدام Access Token طويل جدًا بدون مراجعة الأمان

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

Access Token لمدة 30 يوم يعتبر طويلًا نسبيًا.

لو الـAccess Token اتسرق، يظل صالحًا لفترة طويلة حسب إعدادات المشروع.

</div>

---

#### 4. الخلط بين Authentication وOnline Status

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

المستخدم ممكن يكون عنده JWT صالح، لكن ده لا يثبت أنه Online حاليًا.

`is_online` هو Business State وليس بديلًا عن Authentication.

</div>

---

#### 5. الاعتماد على Django Login Signals مع JWT بدون فهم دورة التنفيذ

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

`user_logged_in` و`user_logged_out` مرتبطة بدورة تسجيل الدخول والخروج الخاصة بـDjango Authentication.

استخدام SimpleJWT لا يعني تلقائيًا أن كل Login أو Logout عبر JWT سيؤدي إلى تشغيل نفس Signals.

لذلك تحديث `is_online` في JWT Login/Logout يتم بشكل أوضح داخل منطق الـJWT نفسه، مثل الـCustom Serializer والـLogout API الموجودين في المشروع.

</div>

---

### 10. 🧠 Why?

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

بنستخدم SimpleJWT لأن So_Iam_OS محتاج نظام Authentication مناسب للـAPI والـFrontend.

الـFrontend مثل Vue.js يقدر يعمل Login، يستلم Tokens، وبعدها يستخدم Access Token في Requests.

</div>

```text id="jwtwhy"
Vue.js
   ↓
Login
   ↓
Django SimpleJWT
   ↓
Access Token
   ↓
Protected API
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

وده مناسب جدًا للـAPI-first architecture لأن الـFrontend والـBackend بيتواصلوا من خلال HTTP APIs.

</div>

---

### 11. 🔗 Project Usage

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

داخل So_Iam_OS، SimpleJWT موجودة في طبقة Identity & Authentication.

التدفق الأساسي:

</div>

```text id="jwtprojectflow"
Vue.js Frontend
       │
       ↓
   Login API
       │
       ↓
  SimpleJWT
       │
       ├──────────────┐
       ↓              ↓
Access Token    Refresh Token
       │
       ↓
Protected APIs
       │
       ↓
Django REST Framework
       │
       ↓
Users / Applications
```

#### User Online State

```text id="jwtonline"
Login
  ↓
is_online = True
  ↓
Authenticated Session State


Logout
  ↓
Blacklist Refresh Token
  ↓
is_online = False
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

المشروع يستخدم `is_online` كحالة إضافية للمستخدم، وليس كوسيلة Authentication.

</div>

---

### 12. 🤖 AI Reference

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

المعلومات التالية تعتبر المرجع الأساسي للـAI عند التعامل مع JWT Authentication داخل So_Iam_OS.

</div>

```text id="jwtairef"
Project:
So_Iam_OS

Technology:
Django REST Framework

Authentication:
SimpleJWT

Package:
djangorestframework-simplejwt

Domain:
Identity / Authentication / Backend

Authentication Class:
JWTAuthentication

Default Permission:
IsAuthenticated

Tokens:
- Access Token
- Refresh Token

Current Lifetimes:
- Access Token: 30 days
- Refresh Token: 180 days

Refresh Rotation:
False

Blacklist:
Enabled for Refresh Tokens

User State:
is_online

Login:
Custom TokenObtainPairSerializer

Logout:
Custom LogoutAPIView

Login Endpoint:
POST /api/login/

Refresh Endpoint:
POST /api/refresh/

Logout Endpoint:
POST /api/logout/
```

#### AI Rules

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

- SimpleJWT هي طبقة JWT Authentication للمشروع.
- `JWTAuthentication` مسؤولة عن التحقق من Access Token.
- `IsAuthenticated` تحمي الـAPI من المستخدم غير المصادق عليه.
- Access Token يستخدم للوصول إلى الـProtected APIs.
- Refresh Token يستخدم للحصول على Access Token جديد.
- Logout يجب أن يتعامل مع Refresh Token بطريقة آمنة.
- Blacklist مطلوب عند استخدام `RefreshToken.blacklist()`.
- لا يتم اعتبار JWT Authentication مساوية لـOnline Status.
- `is_online` حالة Business داخل User Model.
- لا يتم الاعتماد على Django Auth Signals وحدها لتحديث حالة المستخدم عند JWT Login/Logout.
- أي تغيير في JWT configuration يجب أن يتم توثيقه.
- أي تغيير في Token Lifetime يجب مراجعته أمنيًا.
- لا يتم تخزين Tokens في أماكن غير آمنة داخل الـFrontend.
- يجب التعامل مع Access وRefresh Tokens كبيانات حساسة.

</div>

---

### 13. 📊 Current Status

| Task                           | Status |
| ------------------------------ | ------ |
| SimpleJWT Installed            | ⬜     |
| `JWTAuthentication` Configured | ⬜     |
| `IsAuthenticated` Configured   | ⬜     |
| JWT Lifetime Configured        | ⬜     |
| Token Blacklist App Enabled    | ⬜     |
| Blacklist Migrations Applied   | ⬜     |
| Custom Login Serializer        | ⬜     |
| Custom Login View              | ⬜     |
| Refresh Endpoint               | ⬜     |
| Logout Endpoint                | ⬜     |
| `is_online` Login Update       | ⬜     |
| `is_online` Logout Update      | ⬜     |
| `requirements.txt` Updated     | ⬜     |
| JWT Flow Tested                | ⬜     |

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

الحالة هنا يجب تحديثها بناءً على التنفيذ الفعلي داخل المشروع، وليس مجرد وجود الكود في Documentation.

</div>

---

### 14. ✅ Checklist

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

قائمة مراجعة إعداد SimpleJWT:

</div>

- [x] تثبيت `djangorestframework-simplejwt`
- [x] إضافة `JWTAuthentication`
- [x] إضافة `IsAuthenticated`
- [x] إعداد `SIMPLE_JWT`
- [ ] تحديد Access Token Lifetime
- [ ] تحديد Refresh Token Lifetime
- [ ] تحديد Refresh Token Rotation
- [ ] إضافة Token Blacklist
- [ ] تشغيل migrations
- [ ] إنشاء Custom Login Serializer
- [ ] تحديث `is_online` عند Login
- [ ] إنشاء Logout API
- [ ] Blacklist للـRefresh Token
- [ ] تحديث `is_online` عند Logout
- [ ] إنشاء Refresh Endpoint
- [ ] تسجيل dependency في `requirements.txt`
- [ ] اختبار Login
- [ ] اختبار Refresh
- [ ] اختبار Protected API
- [ ] اختبار Logout
- [ ] اختبار Blacklisted Refresh Token

---

### 15. 🔗 Related Documentation

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

المواضيع المرتبطة:

</div>

- Python
- Virtual Environment
- Django
- Django REST Framework
- Django Authentication
- Custom User Model
- JWT
- Access Token
- Refresh Token
- Authentication
- Permissions
- Token Blacklist
- User Online Status
- Vue.js
- API Security
- `requirements.txt`

---

### 16. 📝 Notes

#### 🔐 Security Note

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

الـJWT Tokens تعتبر بيانات حساسة.

لا يجب تسجيلها في Logs أو وضعها داخل Documentation أو Git أو مشاركتها بشكل عام.

</div>

#### ⏱️ Token Lifetime

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

الإعداد الحالي يستخدم:

</div>

```python
"ACCESS_TOKEN_LIFETIME": timedelta(days=30),
"REFRESH_TOKEN_LIFETIME": timedelta(days=180),
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

هذه المدد جزء من Architecture الخاصة بالمشروع ويجب إعادة تقييمها عند الانتقال إلى Production.

</div>

#### 🟢 Online Status

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

`is_online = True` عند Login و`is_online = False` عند Logout لا تعني بالضرورة أن حالة الاتصال الحقيقية للمستخدم دقيقة في كل لحظة.

لو المشروع مستقبلًا محتاج Presence System حقيقي، ممكن يحتاج Heartbeat / Last Seen / Connection Tracking بدل الاعتماد على Boolean فقط.

</div>

#### 🔄 Authentication Flow

```text id="jwtfinalflow"
LOGIN
  │
  ↓
Credentials
  │
  ↓
TokenObtainPair
  │
  ├── Access Token
  └── Refresh Token
  │
  ↓
is_online = True


API REQUEST
  │
  ↓
Access Token
  │
  ↓
JWTAuthentication
  │
  ↓
IsAuthenticated
  │
  ↓
Protected API


REFRESH
  │
  ↓
Refresh Token
  │
  ↓
New Access Token


LOGOUT
  │
  ↓
Refresh Token
  │
  ↓
Blacklist
  │
  ↓
is_online = False
```

---

## 📌 Quick Reference

### Install

```cmd
pip install djangorestframework-simplejwt
```

### Authentication

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}
```

### JWT

```python
from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=180),
    "ROTATE_REFRESH_TOKENS": False,
}
```

### Blacklist

```python
INSTALLED_APPS = [
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
]
```

```cmd
python manage.py migrate
```

### Dependency

```cmd
pip freeze > requirements.txt
```

### Endpoints

```text
POST /api/login/
POST /api/refresh/
POST /api/logout/
```

---

## 🧠 AI Rules

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

SimpleJWT هي المسؤولة عن JWT Authentication داخل Backend مشروع So_Iam_OS.

أي API محمية تستخدم `JWTAuthentication` و`IsAuthenticated` حسب احتياج الـEndpoint.

Login يتم من خلال Custom `TokenObtainPairSerializer` لتحديث `is_online`.

Logout يتم من خلال `LogoutAPIView` ويجب أن يعمل على إبطال Refresh Token باستخدام Blacklist.

`is_online` ليست بديلًا عن Authentication.

لا يتم اعتبار وجود JWT صالح دليلًا كافيًا على أن المستخدم Online فعليًا.

أي تعديل على Token Lifetime أو Rotation أو Blacklist يجب اعتباره تعديلًا في Security Architecture ويجب توثيقه.

</div>
