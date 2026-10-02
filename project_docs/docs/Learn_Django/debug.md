# Debug

## Why

<div class="" dir="rtl">

1️⃣ لماذا نستخدم Django Debug Toolbar؟

تحليل الأداء: بيوريك الوقت المستغرق لكل view و SQL queries.

تصحيح الأخطاء: يوضح تفاصيل request/response headers، context variables، templates المستخدمة.

تحسين الاستعلامات: بتشوف استعلامات الـ ORM وتقدر تقلل الـ queries الغير ضرورية.

مفيد أثناء التطوير فقط: لا تستخدمه في الإنتاج (security & performance).

</div>

## Need

<div class="" dir="rtl">
  2️⃣ ما المطلوب لتشغيله؟

مشروع Django شغال محليًا (Backend فقط).

Python environment مفعل.

Vue frontend ممكن شغال على dev server (localhost:5173 أو port آخر).

DEBUG = True في settings.py.

ملاحظة: Django Debug Toolbar يعمل فقط مع Django، فهو لا يتكامل مباشرة مع Vue لأنه لا يتحكم في واجهة Vue، لكنه يعرض كل request/response من Django REST API لو Vue تطلب البيانات منه.

</div>

## Install

<div class="" dir="rtl">
  3️⃣ خطوات تثبيت وإعداد Django Debug Toolbar

A) تثبيت الحزمة

</div>

```cmd
pip install django-debug-toolbar

```

## settings

<div class="" dir="rtl">
  B) تحديث settings.py
</div>

```python
# settings.py

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE = [
    # لازم قبل CommonMiddleware
    'debug_toolbar.middleware.DebugToolbarMiddleware',

]

# Debug Toolbar settings
INTERNAL_IPS = [
    '127.0.0.1',  # لو شغال محلي
    'localhost',
]

```

## urls

```python
# 📄 [ backend_django/urls.py ] ملف

from django.contrib import admin

from debug_toolbar.toolbar import debug_toolbar_urls


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

] + debug_toolbar_urls()

```
