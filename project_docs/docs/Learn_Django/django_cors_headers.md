## Django

### 1️⃣ Install

<div dir="rtl" style="font-size:2vw">

هي المسؤولة عن التحكم في الـ CORS (Cross-Origin Resource Sharing) — السماح أو منع الطلبات اللي جاية من دومينات مختلفة.

</div>

#### 1️⃣ Install 📚

```cmd
pip install django-cors-headers
```

### 2️⃣ Setup 🛠️

```python
# corsheaders إعدادات
# Allow CORS requests from specific addresses
# Allow requests from this origin
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://192.168.1.5:5173",
]
```

```python
INSTALLED_APPS = [
  # Libraries
  "corsheaders",
]
```

```python
MIDDLEWARE = [
# Libraries [ Django Cors Headers ]
"corsheaders.middleware.CorsMiddleware",
]
```
