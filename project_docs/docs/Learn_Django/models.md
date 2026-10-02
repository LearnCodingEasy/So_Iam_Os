## Models => إنشاء قاعدة البيانات

## ID

### UUIDField [ id ]

<div style="font-size:1.2vw; padding: 2rem 0 0 0; font-weight: 900;">
  📝 UUIDField()
</div>

<div dir="rtl" style="font-size:1.2vw; padding: 1rem 0; font-weight: 900;">
  id مُفتاح أساسي يستخدم كمُعرّف فريد لكل نموذج ويتم إنشاؤه بشكل تلقائي باستخدام
  uuid.uuid4.
</div>

```python
import uuid

# 🧑 Custom User Form  نموذج المستخدم المخصص
class User(AbstractBaseUser, PermissionsMixin):
    """
    # 🆔 معرّف فريد

    import uuid  # 📦 مكتبة لتوليد UUIDs

    # 🔑 الحقل هو المفتاح الأساسي للجدول يضمن أن القيم داخل الحقل تكون فريدة وغير مكررة
    primary_key=True,

    # 🌀 يولد UUID عشوائي تلقائيًا
    default=uuid.uuid4,

    # 🚫 غير قابل للتعديل
    editable=False,

    # 📋 الاسم الذي يظهر في لوحة الإدارة
    verbose_name="معرّف فريد 🆔",

    # 💬 مساعدة لتوضيح الهدف من الحقل
    help_text="معرّف فريد يُستخدم كرقم تسلسلي للعنصر 🎯."

    """

    # ___________________
    # حقل يتم تعبئة تلقائي
    # ___________________
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
```

---

## Text

### CharField [ Text ]

<div style="font-size: 2vw; padding: 2rem 0 0 0; font-weight: 900;">
  📝 CharField()
</div>

<div dir="rtl" style="font-size:1.5vw; padding: 0 0 1rem 0; ">
  🌾 حقل النص يُستخدم لتخزين النصوص

[ max_length=255 ]
⚙️ يمكن للخيار تحديد الحد الأقصى لعدد الأحرف في النص بحد أقصى 255 حرفًا

---

📝 [ null=False | null=True ]
أو لا(None) يحدد الحقل ما إذا كان يمكن أن يأخذ قيمة فارغة

📌 False القيمة الافتراضية هي

💭 يعني ذلك أن الحقل لا يمكن أن يكون فارغًا

🌟 True الحقل يمكن أن يكون فارغًا

👍 بمعنى أنه لا يحتوي على أي محتوى

---

📝 [ blank=False | blank=True ]

✔️ يحدد ما إذا كان يمكن ترك الحقل فارغًا عند إنشاء نموذج.

❌ False القيمة الافتراضية هي

💭 True مما يعني أنه يجب توفير قيمة لهذا الحقل

---

[ ... | default="Name" | default=5 ]

⚙️ يحدد القيمة الافتراضية للحقل عندما لا يتم تقديم قيمة له

⚙️ في هذه الحالة، ليس هناك قيمة افتراضية محددة

📌 في هذه الحالة، القيمة الافتراضية هي "اسم المنتج"

🌟 يمكن أن يكون هناك قيمة افتراضية محددة مثل الارقام

---

[ verbose_name="Name" ]

🏷️ يحدد الاسم الذي سيظهر في واجهة المستخدم كعنوان للحقل

🤔 يساعد في فهم المستخدم لغرض الحقل

---

[ help_text="Name" ]

🔍 يوفر نص توضيحي للمستخدمين بجانب الحقل

💡 يساعد في ملء الحقل بشكل صحيح

</div>

```python
# 🧑 Custom User Form  نموذج المستخدم المخصص
class User(AbstractBaseUser, PermissionsMixin):
    # ___________________
    # حقل يتم تعبئة من المستخدام
    # ___________________
    name = models.CharField(max_length=255)
    name = models.CharField(max_length=255, null=True, blank=True, default="Name",
        verbose_name="Name", help_text="Please Enter The Your Name Here",
        choices=[ ("available", "موجود"), ("sold_out", "خلص"), ("reserved", "محجوز"),],)
```

---

### TextField [ Text ]

<div style="font-size:1.5vw; padding: 2rem 0 0 0; font-weight: 900;">
  📝 TextField()
</div>

<div dir="rtl" style="font-size:1.5vw; padding: 0 0 1rem 0; ">
  
  🌾 حقل النص يُستخدم لتخزين النصوص الطويله
  
  ---
  [ max_length=255 ]
  
  ⚙️ يمكن للخيار تحديد الحد الأقصى لعدد الأحرف في النص بحد أقصى 255 حرفًا
  
  ---

📝 [ null=False | null=True ]

أو لا(None) يحدد الحقل ما إذا كان يمكن أن يأخذ قيمة فارغة

📌 False القيمة الافتراضية هي

💭 يعني ذلك أن الحقل لا يمكن أن يكون فارغًا

🌟 True الحقل يمكن أن يكون فارغًا

👍 بمعنى أنه لا يحتوي على أي محتوى

---

📝 [ blank=False | blank=True ]
<br>
✔️ يحدد ما إذا كان يمكن ترك الحقل فارغًا عند إنشاء نموذج.

❌ False القيمة الافتراضية هي

💭 True مما يعني أنه يجب توفير قيمة لهذا الحقل

---

[ ... | default="Name" | default=5 ]

⚙️ يحدد القيمة الافتراضية للحقل عندما لا يتم تقديم قيمة له

⚙️ في هذه الحالة، ليس هناك قيمة افتراضية محددة

📌 في هذه الحالة، القيمة الافتراضية هي "اسم المنتج"

🌟 يمكن أن يكون هناك قيمة افتراضية محددة مثل الارقام

---

[ verbose_name="Name" ]

🏷️ يحدد الاسم الذي سيظهر في واجهة المستخدم كعنوان للحقل

🤔 يساعد في فهم المستخدم لغرض الحقل

---

[ help_text="Name" ]

🔍 يوفر نص توضيحي للمستخدمين بجانب الحقل

💡 يساعد في ملء الحقل بشكل صحيح

</div>

```python
# 🧑 Custom User Form  نموذج المستخدم المخصص
class User(AbstractBaseUser, PermissionsMixin):
    # ___________________
    # حقل يتم تعبئة من المستخدام
    # ___________________
    long_description = models.TextField(null=True, blank=True)
    long_description = models.TextField(max_length=255, null=True, blank=True, default="Name",
        verbose_name="Name", help_text="Please Enter The Your Name Here",
        choices=[ ("available", "موجود"), ("sold_out", "خلص"), ("reserved", "محجوز"),],)
```

### SlugField

<div class="" dir="rtl">
  حقل لتخزين عناوين ال Url 
</div>

```
class Product(models.Model)
    slug = models.SlugField(max_length=255, unique=True)
```

```python
from django.utils.text import slugify

class Product(models.Model)
    name = models.CharField(max_length=255, blank=True, null=True, default="")
    slug = models.SlugField(max_length=255, editable=False, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

```

---

## Email

### EmailField [ Email ]

<div class="" dir="rtl">
  حقل لتخذين الريد و التحقق من صحتة 
</div>

```python
email = models.EmailField(unique=True)
```

---

## Url

### UrlField [ Url ]

<div class="" dir="rtl">
  حقل لتخذين  و التحقق من صحتة ال Url

يستخدم لتخزين روابط المواقع

</div>

```python
website = models.URLField(max_length=255)
```

---

## Number

### IntegerField

<div class="" dir="rtl">
  حقل تخزين الاعداد الصحيحة فقط
</div>

```python
price = models.IntegerField(default=0)
```

### FloatField

<div class="" dir="rtl">
  حقل تخزين الاعداد العشرية 
</div>

```python
price = models.FloatField(default=0.0)
```

### DecimalField

<div class="" dir="rtl">
  حقل تخزين الاعداد العشرية دقة عالية
</div>

```python
price = models.DecimalField(max_digits=10, decimal_places=2)
```

---

## Image

### ImageField [ Image ]

```python
class User(models.Model):
    """
    # 🖼️ حقل لتحميل صورة

    # 📁 تحديد مكان حفظ الصور داخل MEDIA_ROOT
    upload_to="avatars",

    # 🚫 الحقل اختياري في النماذج
    blank=True,

    # 🚫 الحقل يمكن أن يكون فارغًا في قاعدة البيانات
    null=True,

    # 📋 الاسم الودي للحقل في لوحة الإدارة
    verbose_name="صورة الملف الشخصي 🖼️",

    # 💬 نص المساعدة لشرح الحقل
    help_text="اختر صورة لملفك الشخصي 🎨.",
    """
    # ___________________
    # حقل يتم تعبئة من المستخدام
    # ___________________
    image = models.ImageField(
        upload_to="avatars",
        blank=True,
        null=True,
    )
```

## Date Time

### TimeField

<div class="" dir="rtl">

</div>

```python
created_at = models.TimeField(auto_now_add=True)
updated_at = models.TimeField(auto_now=True)
```

### DateField

<div class="" dir="rtl">
  
</div>

```python
created_at = models.DateField(auto_now_add=True)
updated_at = models.DateField(auto_now=True)
```

### DateTimeField

<div class="" dir="rtl">
  
</div>

```python
created_at = models.DateTimeField(auto_now_add=True)
updated_at = models.DateTimeField(auto_now=True)
```

## Boolean

### BooleanField

<div class="" dir="rtl">
</div>

```python
is_available = models.BooleanField(default=True)
```

## File [📂]

### FileField

<div class="" dir="rtl">
</div>

```python
file = models.FileField(upload_to='backgrounds/')
```

## Relationship

### ForeignKey

<div class="" dir="rtl">
  علاقة الكثير لى واحد

استخدمة فى علاقة مستخدم لية العديد من المقالات

</div>

```
category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
```

### OneToOneField

<div class="" dir="rtl">
</div>

```python
created_by = models.OneToOneField( User, related_name='vendor', on_delete=models.CASCADE)
```

### ManyToManyField

<div class="" dir="rtl">
</div>

```python
vendor = models.ManyToManyField(Vendor,  blank=True, null=True, )
```

---

## Setting & View

```python
class Product(models.Model):
    # ___________________
    # اعدادات خاصة بى الترتيب و الظهور
    # ___________________
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['-created_at']

    def created_at_formatted(self):
        return timesince(self.created_at)

    def __str__(self):
        return '%s' % self.name

    def __str__(self):
        return f"{self.name} - {'yes' if self.is_available else 'no'}"

```

## All

### User

```python
class User(models.Model):
    # ___________________
    # حقل يتم تعبئة تلقائي
    # ___________________
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, related_name="word", on_delete=models.CASCADE
    )

    # ___________________
    # حقل يتم تعبئة من المستخدام
    # ___________________
    name = models.CharField(max_length=255)
    long_description = models.TextField(null=True, blank=True)
```

### Product

```python
from django.db import models
import uuid
from django.utils.timesince import timesince
from users_accounts.models import User

class Product(models.Model):
    # ___________________
    # حقل يتم تعبئة تلقائي
    # ___________________
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, related_name="product", on_delete=models.CASCADE
    )

    # ___________________
    # حقل يتم تعبئة من المستخدام
    # ___________________
    name = models.CharField(max_length=255, blank=True, null=True, default="")
    description = models.TextField(blank=True, null=True, default="")
    price = models.FloatField(default=0)
    is_available = models.BooleanField(default=True)

    # ___________________
    # اعدادات خاصة بى الترتيب و الظهور
    # ___________________
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['-created_at']
    def created_at_formatted(self):
        return timesince(self.created_at)
    def updated_at_formatted(self):
        return timesince(self.updated_at)
    def __str__(self):
        # return '%s' % self.name
        return f"{self.name} - {'yes' if self.is_available else 'no'}"
```
