# 🔌 Django REST Framework

> مكتبة مبنية فوق Django لإنشاء وبناء Web APIs وREST APIs باستخدام Python وDjango.

---

### 1. 🎯 Purpose

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

Django REST Framework أو DRF هو الـFramework اللي بنستخدمه لبناء الـAPI داخل مشروع Django.

هو مسؤول عن توفير الأدوات اللازمة لإنشاء API، مثل:

- استقبال HTTP Requests.
- إرسال API Responses.
- التعامل مع Serializers.
- التعامل مع Models.
- إنشاء API Views.
- بناء CRUD APIs.
- التعامل مع Authentication وPermissions.

لكن الـDRF نفسه مش معناه إن أي Domain أو User مسموح له يدخل الـAPI؛ التحكم في السماح والمنع بيتم من خلال Authentication وPermissions وطبقات الحماية المناسبة.

</div>

---

### 2. 🧠 Concept

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

الفكرة الأساسية إن Django مسؤول عن بناء الـWeb Application، بينما Django REST Framework بيضيف طبقة متخصصة لبناء الـAPIs.

التدفق الأساسي:

</div>

```text
Client
   │
   │ HTTP Request
   ↓
Django REST Framework
   │
   ├── Authentication
   ├── Permissions
   ├── Views / ViewSets
   ├── Serializers
   │
   ↓
Django Models
   │
   ↓
Database
   │
   ↓
Response
   │
   ↓
Client
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

يعني DRF بيكون حلقة مهمة بين الـClient والـDjango Backend والـDatabase.

</div>

---

### 3. 🔧 Requirements

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

قبل تثبيت Django REST Framework، لازم يكون عندك مشروع Django شغال وVirtual Environment مفعلة.

</div>

```text
Python
   ↓
Virtual Environment
   ↓
Django
   ↓
Django Project
   ↓
Django REST Framework
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

في مشروع So_Iam_OS، DRF جزء من Backend Layer.

</div>

---

### 4. 🛠️ Installation / Setup

#### 📦 Install Django REST Framework

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

افتح الـTerminal داخل بيئة المشروع الافتراضية، ثم ثبت Django REST Framework:

</div>

```cmd
pip install djangorestframework
```

#### ⚙️ Add to `INSTALLED_APPS`

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

بعد التثبيت، أضف `rest_framework` إلى `INSTALLED_APPS` داخل `settings.py`.

</div>

```python
INSTALLED_APPS = [
    # Libraries
    'rest_framework',
]
```

#### 📋 Save Dependency

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

بعد تثبيت المكتبة، لازم يتم تسجيلها ضمن dependencies الخاصة بالمشروع.

</div>

```cmd
pip freeze > requirements.txt
```

---

### 5. 🚀 Usage

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

DRF بيوفر أكثر من طريقة لبناء الـAPI.

من أهم الطرق:

1. APIView
2. Generic Views
3. ViewSets
4. Routers

</div>

#### 🔹 APIView

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

`APIView` بتديك تحكم كبير جدًا في كل HTTP Method.

مناسبة لما تكون محتاج تتحكم في منطق الـEndpoint بشكل يدوي وواضح.

</div>

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Post
from .serializers import PostSerializer


class PostListCreateView(APIView):

    def get(self, request):
        posts = Post.objects.all()

        serializer = PostSerializer(
            posts,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

في المثال:

`GET` بتجيب Posts الموجودة.

`POST` بتستقبل بيانات جديدة، تعمل Validation، وبعدها تحفظ الـPost.

</div>

---

#### 🔹 ViewSets

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

`ViewSet` بتوفر طريقة أكثر اختصارًا وتنظيمًا لبناء CRUD APIs، وخصوصًا لما يكون عندك عدد كبير من الـEndpoints.

</div>

```python
from rest_framework import viewsets

from .models import Post
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all()

    serializer_class = PostSerializer
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

`ModelViewSet` بتوفر عمليات CRUD الأساسية مثل:

</div>

```text
GET     → List
GET     → Detail
POST    → Create
PUT     → Update
PATCH   → Partial Update
DELETE  → Delete
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

وده بيقلل كمية الكود المطلوبة مقارنة بكتابة كل عملية بشكل منفصل.

</div>

---

### 6. 📁 Structure

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

شكل App بسيطة تستخدم Django REST Framework ممكن يكون:

</div>

```text
social/
│
├── migrations/
│
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── serializers.py
├── views.py
├── urls.py
└── tests.py
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

أهم الملفات المرتبطة بالـAPI:

</div>

```text
models.py
    ↓
serializers.py
    ↓
views.py
    ↓
urls.py
    ↓
API Endpoint
```

---

### 7. 🧩 Important Concepts

#### 🔹 API

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

واجهة تسمح للـFrontend أو أي Client آخر بالتواصل مع الـBackend من خلال HTTP Requests وResponses.

</div>

#### 🔹 Serializer

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

الـSerializer مسؤول عن تحويل البيانات بين Python/Django Objects والبيانات المناسبة للإرسال والاستقبال عبر الـAPI، بالإضافة إلى Validation للبيانات المدخلة.

</div>

#### 🔹 APIView

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

Class بتسمح لك بكتابة منطق كل HTTP Method بشكل مباشر.

</div>

#### 🔹 ViewSet

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

طريقة لتنظيم مجموعة من العمليات الخاصة بـResource واحد داخل Class واحدة.

</div>

#### 🔹 ModelViewSet

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

ViewSet جاهزة توفر عمليات CRUD الأساسية اعتمادًا على Django Model وSerializer.

</div>

#### 🔹 Router

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

أداة تساعد في إنشاء URLs الخاصة بالـViewSets تلقائيًا بدل كتابة كل Route يدويًا.

</div>

#### 🔹 Authentication

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

تحديد هوية المستخدم الذي يرسل الـRequest.

</div>

#### 🔹 Permissions

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

تحديد هل المستخدم الذي تم التعرف عليه مسموح له بتنفيذ العملية أم لا.

</div>

---

### 8. 💻 Examples

#### Example — APIView

```python
from rest_framework.views import APIView
from rest_framework.response import Response


class HelloAPIView(APIView):

    def get(self, request):
        return Response({
            "message": "Hello So_Iam_OS"
        })
```

#### Example — ViewSet

```python
from rest_framework import viewsets

from .models import Post
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
```

#### Example — Basic Router

```python
from rest_framework.routers import DefaultRouter

from .views import PostViewSet


router = DefaultRouter()

router.register(
    r'posts',
    PostViewSet,
    basename='posts'
)

urlpatterns = router.urls
```

---

### 9. ❌ Common Mistakes

#### 1. نسيان إضافة DRF

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

تثبيت المكتبة فقط مش كفاية؛ لازم إضافتها إلى `INSTALLED_APPS`.

</div>

```python
INSTALLED_APPS = [
    'rest_framework',
]
```

#### 2. الخلط بين Authentication وPermissions

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

Authentication بتجاوب على سؤال:

مين المستخدم؟

Permissions بتجاوب على سؤال:

هل المستخدم ده مسموح له يعمل العملية دي؟

</div>

#### 3. استخدام ViewSet بدون فهم الـCRUD

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

`ModelViewSet` بتوفر عمليات كثيرة تلقائيًا، لكن لازم تفهم العمليات اللي بيتم توفيرها قبل استخدامها.

</div>

#### 4. نسيان Serializer

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

في أغلب APIs التي تتعامل مع Models، الـSerializer بيكون جزء أساسي من عملية تحويل البيانات والتحقق منها.

</div>

#### 5. عدم تحديث `requirements.txt`

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

بعد تثبيت DRF، لازم تسجيل dependency الخاصة بالمشروع.

</div>

```cmd
pip freeze > requirements.txt
```

---

### 10. 🧠 Why?

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

بنستخدم Django REST Framework لأن Django الأساسي مش مصمم لوحده لتوفير كل الأدوات المتخصصة اللي محتاجينها لبناء REST APIs بشكل مريح ومنظم.

DRF بيوفر abstraction جاهز للـAPI، وبيخلينا نقدر نبني:

- CRUD APIs
- Serializers
- Validation
- Authentication
- Permissions
- API Views
- ViewSets
- Routers

وده بيقلل كمية الـBoilerplate Code وبيخلي بناء الـBackend APIs أكثر تنظيمًا.

</div>

---

### 11. 🔗 Project Usage

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

داخل مشروع So_Iam_OS، Django REST Framework هو طبقة الـAPI الأساسية التي تسمح للـFrontend وباقي Clients بالتواصل مع الـBackend.

مثال على الـSocial App:

</div>

```text
Vue.js Frontend
       ↓
     HTTP
       ↓
Django REST Framework
       ↓
   View / ViewSet
       ↓
   Serializer
       ↓
    Django Model
       ↓
    Database
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

وبالتالي DRF هي نقطة مهمة جدًا في الاتصال بين Vue.js والـDjango Backend.

</div>

---

### 12. 🤖 AI Reference

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

المعلومات التالية تعتبر مرجع للـAI عند التعامل مع Django REST Framework داخل المشروع.

</div>

```text
Project:
So_Iam_OS

Technology:
Django REST Framework

Domain:
Backend / API

Package:
djangorestframework

Installed App:
rest_framework

Primary Usage:
Building REST APIs

Main Components:
- APIView
- Generic Views
- ViewSets
- ModelViewSet
- Serializers
- Routers
- Authentication
- Permissions

Project Integration:
Vue.js → DRF → Django → Database

Rules:
- DRF مسؤول عن بناء API layer.
- Authentication يحدد هوية المستخدم.
- Permissions تحدد صلاحية تنفيذ العملية.
- Serializers مسؤولة عن تحويل/Validation البيانات.
- ModelViewSet مناسب لتقليل Boilerplate في CRUD APIs.
- يجب تسجيل dependency داخل requirements.txt.
```

---

### 13. 📊 Current Status

| Task                                       | Status |
| ------------------------------------------ | ------ |
| Django Installed                           | ✅     |
| Django REST Framework Installed            | ⬜     |
| `rest_framework` Added to `INSTALLED_APPS` | ⬜     |
| Serializer Setup                           | ⬜     |
| APIView Setup                              | ⬜     |
| ViewSet Setup                              | ⬜     |
| Router Setup                               | ⬜     |
| Authentication Setup                       | ⬜     |
| Permissions Setup                          | ⬜     |
| requirements.txt Updated                   | ⬜     |

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

الحالة هنا بتوصف Knowledge/Setup الخاصة بـDRF. يتم تحديثها بعد تنفيذ الخطوات فعليًا داخل مشروع So_Iam_OS.

</div>

---

### 14. ✅ Checklist

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

قائمة مراجعة إعداد Django REST Framework:

</div>

- [x] تثبيت `djangorestframework`
- [x] إضافة `rest_framework` إلى `INSTALLED_APPS`
- [x] تحديث `requirements.txt`
- [ ] إنشاء `serializers.py`
- [ ] إنشاء API Views
- [ ] اختيار APIView أو Generic Views أو ViewSet حسب الحاجة
- [ ] إعداد URLs
- [ ] إعداد Routers عند استخدام ViewSets
- [ ] إعداد Authentication
- [ ] إعداد Permissions
- [ ] اختبار الـAPI

---

### 15. 🔗 Related Documentation

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

التقنيات والملفات المرتبطة:

</div>

- Python
- Virtual Environment
- Django
- Django Models
- Django URLs
- Django REST Framework
- Serializers
- APIView
- Generic Views
- ViewSets
- Routers
- Authentication
- Permissions
- Vue.js
- PostgreSQL
- `requirements.txt`

---

### 16. 📝 Notes

#### 🔹 APIView vs ViewSet

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

استخدم `APIView` لما تحتاج تحكم تفصيلي في كل Request وHTTP Method.

استخدم `ViewSet` أو `ModelViewSet` لما تكون بتبني CRUD API واضحة وممكن تستفيد من العمليات الجاهزة وتقليل الكود.

</div>

```text
Custom / Complex Logic
        ↓
     APIView


Standard CRUD
        ↓
   ModelViewSet
```

#### 🔹 DRF لا يساوي Authentication

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

وجود DRF في المشروع لا يعني تلقائيًا إن كل الـAPI محمية.

الحماية لازم يتم تصميمها باستخدام Authentication وPermissions والسياسات المناسبة لكل Endpoint.

</div>

#### 🔹 Dependency

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

اسم الحزمة التي يتم تثبيتها باستخدام pip هو:

</div>

```text
djangorestframework
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

بينما الاسم الذي يتم وضعه في `INSTALLED_APPS` هو:

</div>

```python
'rest_framework',
```

---

## 📌 Quick Reference

```cmd
pip install djangorestframework

pip freeze > requirements.txt
```

```python
INSTALLED_APPS = [
    'rest_framework',
]
```

```python
from rest_framework.views import APIView
from rest_framework.response import Response


class ExampleAPIView(APIView):

    def get(self, request):
        return Response({
            "message": "Hello"
        })
```

```python
from rest_framework import viewsets


class ExampleViewSet(viewsets.ModelViewSet):

    queryset = Model.objects.all()
    serializer_class = ModelSerializer
```

---

## 🤖 AI Rules

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

- Django REST Framework هو طبقة بناء الـAPI في Backend المشروع.
- لا يتم اعتبار DRF نظام Authentication بحد ذاته.
- Authentication لتحديد هوية المستخدم.
- Permissions لتحديد صلاحيات المستخدم.
- Serializer جزء أساسي من التعامل مع بيانات الـAPI.
- `APIView` تستخدم عند الحاجة لتحكم أكبر في الـRequest Logic.
- `ModelViewSet` مناسبة للـCRUD APIs القياسية.
- عند استخدام ViewSets يمكن استخدام Routers لتنظيم الـURLs.
- أي Dependency جديدة يتم تثبيتها يجب تسجيلها في `requirements.txt`.
- عند تصميم API جديدة داخل So_Iam_OS، يجب تحديد Authentication وPermissions المناسبة وعدم الاعتماد على وجود DRF وحده للحماية.

</div>
