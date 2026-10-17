# 🛠️ استيراد أدوات الإدارة
from django.contrib import admin

# 🌐 استيراد نموذج موقع الويب
from .models import MemoryItem


# 🖥️ تخصيص عرض النموذج في لوحة الإدارة
@admin.register(MemoryItem)
class MemoryItemAdmin(admin.ModelAdmin):
    # 🌟 الحقول التي ستظهر في قائمة الإدارة
    list_display = (
        "user",
        "type",
        "importance",
    )

    # 🔍 تمكين البحث عبر الحقول
    search_fields = ("user", "type")

    # 🗂️ إضافة فلاتر حسب اللغة
    list_filter = ("importance",)

    # 🔃 ترتيب النتائج حسب الاسم
    ordering = ("user",)

    # 📝 تحديد الحقول التي يمكن تعديلها داخل شاشة تحرير المستخدم
    fields = ("user", "type",  "importance")
