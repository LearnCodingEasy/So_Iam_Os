# Django Page Api

<div dir="rtl" style="font-size:1.2vw; padding: 1rem 0; font-weight: 900;">
  إنشاء العناصر المراية و طريقة العرض و الفلاتر
</div>

## Normal

### All

<div style="font-size:1.2vw; padding: 2rem 0 0 0; font-weight: 900;">
</div>

```python
# views.py
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from django.http import JsonResponse
from .models import Product
from .serializers import ProductSerializer

# 🏷️ دالة لجلب جميع الفئات
# 🛠️ فقط GET تعريف هذه الدالة كواجهة برمجية تدعم طلبات
@api_view(["GET"])
# 🔓 عدم استخدام مصادقة
@authentication_classes([])
# 🔓 عدم استخدام تصاريح
@permission_classes([])
def product_list(request):
    # 📚 جلب كل الفئات
    products = Product.objects.all()
    # 🔄 serializer باستخدام  JSON تحويل البيانات إلى صيغة
    serializer = ProductSerializer(products, many=True)
    # 📤 JSON إعادة البيانات بصيغة
    # return Response(serializer.data)
    return JsonResponse(serializer.data, safe=False)
```

```python
# views.py
from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer

class product_list(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer

```

### Single

```python

```

```python
# 🧐 Django كائن يُستخدم لبناء استعلامات معقدة في
from django.db.models import Q

# 📚 دالة لجلب بيانات دورة معينة باستخدام المعرف (pk)
@api_view(["GET"])
def course_detail(request, pk):
    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id)

    # 📦 جلب الدورة إذا كان منشؤها موجودًا ضمن معرفات المستخدمين
    # 🔍 البحث عن الدورة المحددة باستخدام شرط أن تكون منشأة بواسطة المستخدم أو أصدقائه.
    course = Course.objects.filter(Q(created_by_id__in=list(user_ids))).get(pk=pk)

    # 🎨 تحويل بيانات الدورة إلى JSON باستخدام الـ Serializer
    course_serializer = CourseDetailSerializer(course)
    course_data = course_serializer.data

    # 🔐 التحقق من إذا كان المستخدم مصرحًا له
    # 🔐 التحقق من إذا كان المستخدم قد سجل الدخول
    if request.user.is_authenticated:
        # ✅ إذا كان مصرحًا له، يتم استخدام بيانات الدورة كما هي
        course_data = course_serializer.data
    else:
        # 🚫 إذا لم يكن مصرحًا له، تكون بيانات الدورة فارغة
        course_data = {}

    # 📚 جلب جميع الدروس المرتبطة بالدورة
    lesson = course.lessons.all()
    # 🎨 تحويل بيانات الدروس إلى JSON باستخدام الـ Serializer
    lesson_serializer = LessonListSerializer(lesson, many=True)
    lesson_data = lesson_serializer.data

    # 📝 إرجاع بيانات الدورة والدروس في صيغة JSON
    return JsonResponse(
        {
            "course": course_data,  # 📝 بيانات الدورة
            "lessons": lesson_data,  # 📚 بيانات الدروس
        }
    )

```

## viewsets

##### Rest Framework viewsets

### All

```python
# Get All Data List By viewsets

# Rest Framework
from rest_framework import viewsets

# Element
from .models import Vendor
from .serializers import VendorSerializer

class categoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
```

### Search & Ordering

```python
# Get All Data List And Search & Ordering By viewsets

# Rest Framework
from rest_framework import viewsets, filters

# Element
from .models import Vendor
from .serializers import VendorSerializer

class categoryView(viewsets.ModelViewSet):
    serializer_class = VendorSerializer
    queryset = Vendor.objects.all()

    # ✨ Search & Ordering
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['created_at', 'name']

```

### Permissions

```python
# Get All Data List And Permissions By viewsets

# Rest Framework
from rest_framework import viewsets, filters, permissions

# Element
from .models import Vendor
from .serializers import VendorSerializer

class categoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    # ✨ Search & Ordering
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['created_at', 'name']

    # ✨ Permissions
    permission_classes = [permissions.IsAuthenticated]
    # ده للتجربة بس، مش Production.
    # permission_classes = [permissions.AllowAny]

```

### List

```python
# Get All Data List And Permissions By viewsets

# Rest Framework
from rest_framework import viewsets, filters, permissions, status
from rest_framework.response import Response

# Element
from .models import Vendor
from .serializers import VendorSerializer

class categoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    # ✨ Search & Ordering
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['created_at', 'name']

    # ✨ Permissions
    permission_classes = [permissions.IsAuthenticated]

    # -------- LIST --------
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)

        # ✅ Create Table
        console.rule("[bold green]All Category Table")
        table = Table(
            title="All Categories",
            box=box.SIMPLE_HEAVY,
            header_style="bold magenta"
        )
        table.add_column("Name", style="green")
        table.add_column("Slug", style="yellow")
        table.add_column("Created At", style="red")
        for item in serializer.data:
            table.add_row(
                str(item.get("name", "")),
                str(item.get("slug", "")),
                str(item.get("created_at_formatted", item.get("created_at", ""))),
            )
        console.print(table)
        console.rule()

        return Response(
            {
              "message": "Categories list",
              "data": serializer.data
            },
            status=status.HTTP_200_OK,
        )

```

### Control user View

```python
# 📄 [ Product/api.py ] ملف

# Rest Framework
from rest_framework import viewsets, filters, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

# Element
from .models import Category
from .serializers import CategorySerializer

# Console
from rich.console import Console
from rich.table import Table
from rich import box
from rich import print
console = Console()


class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    # ✨ Search & Ordering
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['created_at', 'name']

    # ✨ Permissions
    permission_classes = [permissions.IsAuthenticated]

    # -------- LIST --------
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)

        # ✅ Create Table
        console.rule("[bold green]All Category Table")
        table = Table(
            title="All Categories",
            box=box.SIMPLE_HEAVY,
            header_style="bold magenta"
        )
        table.add_column("Name", style="green")
        table.add_column("Slug", style="yellow")
        table.add_column("Created At", style="red")
        for item in serializer.data:
            table.add_row(
                str(item.get("name", "")),
                str(item.get("slug", "")),
                str(item.get("created_at_formatted", item.get("created_at", ""))),
            )
        console.print(table)
        console.rule()

        return Response(
            {
                "message": "Categories List",
                "data": serializer.data
            },
            status=status.HTTP_200_OK,
        )

    # -- Control user View --
    def get_queryset(self):
        # admin يشوف كل حاجة
        if self.request.user.is_staff:
            return Category.objects.all()
        # الباقي يشوف الحاجات اللي هو عملها بس
        return Category.objects.filter(created_by=self.request.user)

```

### Single

### Create

#### Create Data By viewsets

```python
# 📄 [ Product/api.py ] ملف

# Rest Framework
from rest_framework import viewsets, filters, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.decorators import action

# Element
from .models import Category
from .serializers import CategorySerializer

# Console
from rich.console import Console
from rich.table import Table
from rich import box
from rich import print
console = Console()


class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    # ✨ Search & Ordering
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['created_at', 'name']

    # ✨ Permissions
    permission_classes = [permissions.IsAuthenticated]

    # -------- CREATE --------
    def perform_create(self, serializer):
        """
        When creating the item
        Created_by = current user
        """
        instance = serializer.save(created_by=self.request.user)

        # Print in console
        console.rule("[bold green]New Category Created")
        console.print(f"[yellow]Name:[/yellow] {instance.name}")
        console.print(f"[cyan]Created By:[/cyan] {instance.created_by}")
        console.print(f"[magenta]ID:[/magenta] {instance.id}")
        console.rule()

    # ✅ عند التحديث

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                "message": "Category Created Successfully",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED,
        )

```

```python

```
