## Django

### 1️⃣ Install

<div dir="rtl" style="font-size:1.5vw">

- مكتبة متكاملة لإدارة تسجيل الدخول/التسجيل والدعم الكامل لطرق المصادقة الاجتماعية (OAuth) مثل Google، Facebook، Twitter.

- تدعم التسجيل عبر البريد الإلكتروني، تأكيد البريد، إعادة تعيين كلمة المرور.

</div>

#### 1️⃣ Install 📚

```cmd
pip install djoser
```

### 2️⃣ Setup 🛠️

```python
INSTALLED_APPS = [
  # Libraries
  "djoser",
]
```

```python
from django.urls import path, include
urlpatterns = [
    # djoser
    # تسجيل الدخول، تسجيل الخروج، المستخدمين
    path('api/auth/', include('djoser.urls')),
    # JWT token (access/refresh)
    path('api/auth/', include('djoser.urls.jwt')),
] 
```

```python

```

```python

```

```python

```
