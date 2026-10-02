# Django Page Admin




<div dir="rtl" style="font-size:1.2vw; padding: 1rem 0; font-weight: 900;">
  الطريقة الطبيعية 
</div>

```python
# 🛠️ استيراد أدوات إدارة Django
from django.contrib import admin  

# 🌐 استيراد نموذج (Model) موقع الويب
from .models import Website  

# 🖥️ تسجيل نموذج Website في لوحة الإدارة
admin.site.register(Website)
```


<div dir="rtl" style="font-size:1.2vw; padding: 1rem 0; font-weight: 900;">
  تخصيص عرض الحقول وإضافة مميزات مثل البحث، الفلاتر، والترتيب 
</div>

```python
# 🛠️ استيراد أدوات الإدارة
from django.contrib import admin

# 🌐 استيراد نموذج موقع الويب
from .models import User


# 🖥️ تخصيص عرض النموذج في لوحة الإدارة
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # 🌟 الحقول التي ستظهر في قائمة الإدارة
    list_display = (
        "name",
        "surname",
        "is_online",
        "email",
    )

    # 🔍 تمكين البحث عبر الحقول
    search_fields = ("name", "surname")

    # 🗂️ إضافة فلاتر حسب اللغة
    list_filter = ("is_online",)

    # 🔃 ترتيب النتائج حسب الاسم
    ordering = ("name",)

    # 📝 تحديد الحقول التي يمكن تعديلها داخل شاشة تحرير المستخدم
    fields = ("name", "surname", "email", "is_online")

```
