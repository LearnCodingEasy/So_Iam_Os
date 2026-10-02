# 👥 Users Accounts

## 📦 Models (النماذج)

```python
# 📄 [users_accounts/models.py] صفحة

from django.db import models

# uuid: يُستخدم لإنشاء معرّفات فريدة عالمياً
# 🔑 uuid: (Unique IDs) يُستخدم لإنشاء معرّفات فريدة عالمياً
import uuid

# ⚙️ settings: Django لاستيراد إعدادات الخاصة بالمشروع
from django.conf import settings

# 👤 AbstractBaseUser, PermissionsMixin: لإنشاء نموذج مستخدم مخصص (Custom User Model)
# 👨‍💻 UserManager: (superusers) لإدارة وإنشاء المستخدمين والمشرفين
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager

# 🏗️ Django داخل (Models) لإنشاء النماذج
from django.db import models

# 🕒 timezone: (Dates & Times) للتعامل مع التوقيتات
from django.utils import timezone
# ⏳ timesince: لحساب الفرق بين وقتين بصيغة مفهومة (مثلاً: "منذ ساعتين")
from django.utils.timesince import timesince

# 👥 Dedicated manager to create and manage users
# 👥 مدير مخصص لإنشاء وإدارة المستخدمين
class CustomUserManager(UserManager):
    def _create_user(self, name, email, password, **extra_fields):
        # ✉️ Verify email entry
        # ✉️ تحقق من إدخال البريد الإلكتروني
        if not email:
            raise ValueError("You have not provided a valid e-mail address")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # 👤 Create a regular user
    # 👤 إنشاء مستخدم عادي
    def create_user(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(name, email, password, **extra_fields)

    # 🛡️ Create an administrative user (super user)
    # 🛡️ إنشاء مستخدم إداري (سوبر يوزر)
    def create_superuser(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(name, email, password, **extra_fields)


# 🧑 Custom User Form 🧑 نموذج المستخدم المخصص
class User(AbstractBaseUser, PermissionsMixin):
    # ___________________
    # حقل يتم تعبئة تلقائي
    # ___________________
    # 🔑 Define the primary field to be UUID  تعريف الحقل الأساسي ليكون
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # ⚙️ User Status  حالة المستخدم
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    # 📋 Custom Admin Link ربط المدير المخصص
    objects = CustomUserManager()
    # 👥 Friends and Characteristics of Friendships الأصدقاء وخصائص الصداقات
    friends = models.ManyToManyField("self")
    friends_count = models.IntegerField(default=0)
    people_you_may_know = models.ManyToManyField("self")
    # 📅 Join Date & Last Login تاريخ الانضمام وآخر تسجيل دخول
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(auto_now=True, blank=True, null=True)

    # ___________________
    # حقل يتم تعبئة من المستخدام
    # ___________________
    # 📛 User Data Properties خصائص بيانات المستخدم
    name = models.CharField(max_length=255, blank=True, null=True, default="")
    surname = models.CharField(max_length=255, blank=True, default="")
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(default=timezone.now)
    gender = models.CharField(max_length=15, blank=True, null=True)
    # 🖼️ Profile Picture صورة شخصية
    avatar = models.ImageField(upload_to="avatars", blank=True, null=True)
    # 🖼️ Cover Photo صورة الغلاف
    cover = models.ImageField(upload_to="covers", blank=True, null=True)
    # مهارات
    skills = models.JSONField(default=list, blank=True, null=True)
    # 📋 Tasks and Their Number المهام وعددها
    task_count = models.IntegerField(default=0)
    # 📅 User Is Online  حالة الاتصال
    is_online = models.BooleanField(default=False)

    # 🔒 إعدادات تسجيل الدخول: البريد الإلكتروني كمحدد رئيسي لتسجيل الدخول
    # يحدد الحقل الذي سيتم استخدامه لتسجيل الدخول. في هذه الحالة، هو email.
    USERNAME_FIELD = "email"
    # يحدد الحقل الذي يتم استخدامه كالبريد الإلكتروني الرئيسي للمستخدم. في هذه الحالة، هو email.
    EMAIL_FIELD = "email"
    # 📝 لا توجد حقول إضافية مطلوبة بجانب البريد الإلكتروني وكلمة المرور عند إنشاء مستخدم جديد عبر الأوامر الإدارية.
    REQUIRED_FIELDS = []

    # 🖼️ Function to get cover image link With default link if none exists
    # 🖼️ دالة للحصول على رابط صورة الغلاف مع رابط افتراضي إذا لم تكن موجودة
    def get_avatar(self):
        if self.avatar:
            return settings.WEBSITE_URL + self.avatar.url
        else:
            return "https://picsum.photos/200/200"

    def get_cover(self):
        if self.cover:
            return settings.WEBSITE_URL + self.cover.url
        else:
            return "https://picsum.photos/200/200"

    def date_joined_formatted(self):
        return timesince(self.date_joined)

    def last_login_formatted(self):
        return timesince(self.last_login)


# 📬 Friend Request Form نموذج طلب الصداقة
class FriendshipRequest(models.Model):
    # 📝 Friend request cases  حالات طلب الصداقة
    NOTSEND = "notsend"  # 🚫 لم يتم الإرسال
    SEND = "send"  # ✉️ تم الإرسال
    WAITING = "waiting"  # ⏳ في انتظار الرد
    ACCEPTED = "accepted"  # ✅ تم القبول
    REJECTED = "rejected"  # ❌ تم الرفض
    CANCEL = "cancel"  # 🔄 تم الإلغاء
    UNFRIEND = "unfriend"  # 🔄 تم الإلغاء الصداقة
    BLOCKED = "blocked"  # 🚫 الحظر
    MUTED = "muted"  # 🔕 الكتم
    FROZEN = "frozen"  # 🧊 تجميد
    ARCHIVED = "archived"  # 📦 مؤرشف
    FOLLOWING = "following"  # 👥 متابعة
    UNFOLLOWED = "unfollowed"  # 🚫 إلغاء المتابعة
    REPORTED = "reported"  # 🚨 تم الإبلاغ عنه
    SPAM = "spam"  # 🗑️ بريد مزعج
    DELETED = "deleted"  # 🗑️ محذوف
    FAVORITE = "favorite"  # 🌟 مفضل
    TEMPORARILY_BLOCKED = "temporarily_blocked"  # ⏳ حظر مؤقت
    VERIFIED = "verified"  # ✔️ تم التحقق
    REQUEST_RESENT = "request_resent"  # 🔄 تم إعادة الإرسال
    SUGGESTED = "suggested"  # 💡 مقترح
    IGNORED = "ignored"  # 🛑 تم التجاهل
    INACTIVE = "inactive"  # ⚠️ غير نشط
    LIMITED = "limited"  # 🚫 محدود

    # 📜 قائمة الحالات الممكنة مع النصوص المقابلة
    STATUS_CHOICES = (
        (NOTSEND, "NotSent"),  # 🚫 لم يتم الإرسال
        (SEND, "Send"),  # ✉️ تم الإرسال
        (WAITING, "Waiting"),  # ⏳ في انتظار الرد
        (ACCEPTED, "Accepted"),  # ✅ تم القبول
        (REJECTED, "Rejected"),  # ❌ تم الرفض
        (CANCEL, "Cancel"),  # 🔄 تم الإلغاء
        (UNFRIEND, "Unfriend"),  # 🔄 تم الإلغاء
        (BLOCKED, "Blocked"),  # 🚫 الحظر
        (MUTED, "Muted"),  # 🔕 الكتم
        (FROZEN, "Frozen"),  # 🧊 تجميد
        (ARCHIVED, "Archived"),  # 📦 مؤرشف
        (FOLLOWING, "Following"),  # 👥 متابعة
        (UNFOLLOWED, "Unfollowed"),  # 🚫 إلغاء المتابعة
        (REPORTED, "Reported"),  # 🚨 تم الإبلاغ عنه
        (SPAM, "Spam"),  # 🗑️ بريد مزعج
        (DELETED, "Deleted"),  # 🗑️ محذوف
        (FAVORITE, "Favorite"),  # 🌟 مفضل
        (TEMPORARILY_BLOCKED, "TemporarilyBlocked"),  # ⏳ حظر مؤقت
        (VERIFIED, "Verified"),  # ✔️ تم التحقق
        (REQUEST_RESENT, "RequestResent"),  # 🔄 تم إعادة الإرسال
        (SUGGESTED, "Suggested"),  # 💡 مقترح
        (IGNORED, "Ignored"),  # 🛑 تم التجاهل
        (INACTIVE, "Inactive"),  # ⚠️ غير نشط
        (LIMITED, "Limited"),  # 🚫 محدود
    )

    # 🔑 Friend Request UUID Essential Field حقل أساسي UUID لطلب الصداقة
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # 🧑 User receiving the request  المستخدم المستلم للطلب
    created_for = models.ForeignKey(
        User, related_name="received_friendshiprequests", on_delete=models.CASCADE
    )
    # 🧑 The user who sent the request  المستخدم المرسل للطلب
    created_by = models.ForeignKey(
        User, related_name="created_friendshiprequests", on_delete=models.CASCADE
    )
    # 📅 Creation date تاريخ الإنشاء
    created_at = models.DateTimeField(auto_now_add=True)
    # 📝 Order Status  حالة الطلب
    # 🚫 الحالة الافتراضية: "لم يتم الإرسال"
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=NOTSEND)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return "%s" % self.status

    # 🔍 Retrieve All Friend Requests by User and Status 🔍
    # 🧑‍🤝‍🧑 جلب جميع طلبات الصداقة بناءً على المستخدم والحالة
    @staticmethod
    def get_friends_by_status(user, status):
        """جلب الأصدقاء بناءً على حالة محددة"""
        if status == FriendshipRequest.ACCEPTED:
            return User.objects.filter(
                received_friendshiprequests__created_by=user,
                received_friendshiprequests__status=status,
            ) | User.objects.filter(
                created_friendshiprequests__created_for=user,
                created_friendshiprequests__status=status,
            )
        return User.objects.filter(
            received_friendshiprequests__created_by=user,
            received_friendshiprequests__status=status,
        )

```

## 👨‍💼 Admin (لوحة الإدارة)

```python
# 📄 [users_accounts/admin.py] صفحة
# 🛠️ استيراد أدوات الإدارة
from django.contrib import admin

# 🌐 استيراد نموذج موقع الويب
from .models import User, FriendshipRequest

# admin.site.register(FriendshipRequest)

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
    # fields = ("name", "surname", "email", "is_online")


# 🖥️ تخصيص عرض النموذج في لوحة الإدارة
@admin.register(FriendshipRequest)
class FriendshipRequestAdmin(admin.ModelAdmin):
    # 🌟 الحقول التي ستظهر في قائمة الإدارة
    list_display = (
        "created_for",
        "created_by",
        "status",
    )

    # 🔍 تمكين البحث عبر الحقول
    search_fields = ("created_for", "created_by", "status")

    # 🗂️ إضافة فلاتر حسب اللغة
    list_filter = ("status",)

    # 🔃 ترتيب النتائج حسب الاسم
    ordering = ("status",)

    # 📝 تحديد الحقول التي يمكن تعديلها داخل شاشة تحرير المستخدم
    fields = ("created_at", "created_for", "created_by", "status")

```

## 📨 Serializers (المسلسلات)

```python
# 📝 [users_accounts/serializers.py] صفحة
#
# 🔄 هذا الملف يحتوي على السيريالايزر (Serializers)، والتي تُستخدم لتحويل البيانات بين النماذج (Models) و JSON.
# 🌟 السيريالايزر مهم في Django Rest Framework لتسهيل التعامل مع البيانات عند إنشاء واجهات برمجة التطبيقات (APIs).

# 🌟 1️⃣ استيراد الإطار لتحويل البيانات
# - يتم استيراد الوحدة `serializers` من مكتبة Django Rest Framework.
from rest_framework import serializers

# 🌟 2️⃣ استيراد النماذج
# - استيراد نماذج البيانات `User` و `FriendshipRequest` من ملف `models.py`.
# - هذه النماذج تمثل جداول البيانات التي سيتم تحويلها عبر السيريالايزر.
from .models import User, FriendshipRequest


# 🧑 3️⃣ **UserSerializer**
# - السيريالايزر المستخدم لتحويل بيانات نموذج `User` إلى JSON والعكس.
# - يستخدم لتحليل البيانات المتعلقة بالمستخدمين عند إرسالها أو استقبالها.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        # ✨ النموذج المرتبط بالسيريالايزر
        model = User
        # 🔍 الحقول المراد تضمينها في الاستجابة
        fields = (
            "id",  # 🆔 المعرف الفريد للمستخدم
            "name",  # 👤 الاسم الأول
            "surname",  # 👥 اسم العائلة
            "email",  # 📧 البريد الإلكتروني
            "date_of_birth",  # 🎂 تاريخ الميلاد
            "gender",  # ⚧ الجنس
            "get_avatar",  # 🖼️ رابط صورة الملف الشخصي
            "get_cover",  # 🖼️ رابط صورة الغلاف
            "friends_count",  # 👫 عدد الأصدقاء
            "task_count",  # 📋 عدد المهام
            "date_joined",  # 📅 تاريخ الانضمام
            "date_joined_formatted",  # 🗓️ تنسيق تاريخ الانضمام
            "last_login",  # ⏱️ آخر تسجيل دخول
            "last_login_formatted",  # 🕒 تنسيق تاريخ آخر تسجيل دخول
            "is_online",  # 🔵 حالة الاتصال (متصل أم لا)
            "skills",  #
        )


# 👫 4️⃣ **FriendshipRequestSerializer**
# - السيريالايزر المستخدم لتحويل بيانات طلبات الصداقة إلى JSON والعكس.
# - يحتوي على بيانات المرسل والمعلومات الأساسية عن الطلب.


class FriendshipRequestSerializer(serializers.ModelSerializer):
    # 👤 استخدام `UserSerializer` لعرض معلومات المرسل (قراءة فقط).
    created_by = UserSerializer(read_only=True)

    class Meta:
        # ✨ النموذج المرتبط بالسيريالايزر
        model = FriendshipRequest
        # 🔍 الحقول المراد تضمينها في الاستجابة
        fields = (
            "id",  # معرف الطلب
            "created_by",  # بيانات المرسل
            "status",  # حالة الطلب (مقبول، مرفوض، قيد الانتظار)
        )

```

## 📝 Forms (النماذج)

```python
# 📄 [users_accounts/forms.py] ملف
#
# 🔄 هذا الملف يحتوي على نماذج Django Forms التي تُستخدم لإنشاء النماذج التي يتفاعل معها المستخدمون.
# 🌟 هذه النماذج تعمل كوسيط بين واجهة المستخدم وقاعدة البيانات.

# 🌟 1️⃣ استيراد النماذج الأساسية
# - يتم استيراد نموذج إنشاء المستخدم `UserCreationForm` من مكتبة `django.contrib.auth.forms`.
# - استيراد `forms` من مكتبة Django لإنشاء النماذج.
from django.contrib.auth.forms import UserCreationForm
from django import forms

# 🌟 2️⃣ استيراد نموذج البيانات
# - يتم استيراد نموذج `User` المعرَّف مسبقًا في ملف `models.py`.
from .models import User

# 📝 3️⃣ **SignupForm**
# - نموذج تسجيل المستخدمين الجدد.
# - يرث من `UserCreationForm` لتوفير الحقول اللازمة لإنشاء مستخدم جديد مع الحقول المخصصة.
class SignupForm(UserCreationForm):
    # 🔧 إعدادات النموذج: يتم تحديد النموذج المرتبط والحقول التي سيتم عرضها.
    class Meta:
        model = User  # 🌟 النموذج المرتبط هو `User`.
        fields = (
            # 🧑 الاسم الأول
            "name",
            # 🧑 اللقب
            "surname",
            # 📧 البريد الإلكتروني
            "email",
            # 📅 تاريخ الميلاد
            "date_of_birth",
            # ⚧ الجنس
            "gender",
            # 🔑 كلمة المرور
            "password1",
            # 🔑 تأكيد كلمة المرور
            "password2",
        )


# 🖋️ 4️⃣ **ProfileForm**
# - نموذج تعديل بيانات المستخدم الشخصية.
# - يرث من `forms.ModelForm` لتوفير واجهة سهلة لتعديل البيانات.
class ProfileForm(forms.ModelForm):
    # 🔧 إعدادات النموذج: يتم تحديد النموذج المرتبط والحقول التي يمكن تعديلها.
    class Meta:
        model = User  # 🌟 النموذج المرتبط هو `User`.
        fields = (
            # 🧑 الاسم الأول
            "name",
            # 🧑 اللقب
            "surname",
            # 📧 البريد الإلكتروني
            "email",
            # 📅 تاريخ الميلاد
            "date_of_birth",
            # ⚧ الجنس
            "gender",
            # 🖼️ صورة الملف الشخصي
            "avatar",
            # 🖼️ صورة الغلاف
            "cover",
            "skills",
            "is_online",
        )

```

## 🌐 API (واجهة برمجة التطبيقات)

```python
# 📄 ملف [ messenger/messenger_django/account/api.py ]

# 🌐 API for User Signup and Profile Info Retrieval
# 🌐 API لتسجيل المستخدم واسترجاع معلومات الحساب

# Django إستيراد إعدادات المشروع في
from django.conf import settings

# إستيراد نموذج تغيير كلمة المرور
from django.contrib.auth.forms import PasswordChangeForm

# إستيراد دالة إرسال البريد الإلكتروني
from django.core.mail import send_mail

# JSON لإرجاع استجابات JsonResponse إستيراد
from django.http import JsonResponse

# إستيراد الديكورات لتعريف وحدات الواجهة البرمجية
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)

# إستيراد النماذج المخصصة لتسجيل المستخدم وتعديل الملف الشخصي
from .forms import SignupForm, ProfileForm

# إستيراد النماذج المخصصة للمستخدم وطلبات الصداقة
from .models import User, FriendshipRequest

# إستيراد المسلسلات للمستخدم وطلبات الصداقة
from .serializers import UserSerializer, FriendshipRequestSerializer

# 🛠️ استيراد مكتبة التسجيل لتتبع العمليات
import logging

# 🚫 استيراد استثناء الرفض
from django.core.exceptions import PermissionDenied

## 🌐 إعداد مكتبة التسجيل
# 🛠️ إعداد المستوى الأساسي للتسجيل
logging.basicConfig(level=logging.INFO)
# 📝 إنشاء مُسجل مرتبط باسم الوحدة
logger = logging.getLogger(__name__)

from rest_framework.parsers import JSONParser

# إستيراد دالة إنشاء الإشعارات
from notification.utils import create_notification

# 📜 استيراد نموذج الإشعار
from notification.models import Notification


# 📝 Signup API Endpoint
# 📝 واجهة برمجية للتسجيل
@api_view(["POST"])  # 📬 السماح فقط بالطلبات من نوع POST.
@authentication_classes([])  # 🚫 لا تتطلب مصادقة
@permission_classes([])  # 🚫 لا تتطلب أذونات
def signup(request):
    """
    وظيفة للتعامل مع تسجيل المستخدم.
    """
    # 🗃️ البيانات المُرسلة مع الطلب.
    data = request.data
    message = "success"

    # 🧾 Initialize signup form with request data
    # 🧾 تهيئة نموذج التسجيل باستخدام بيانات الطلب
    form = SignupForm(
        {
            "name": data.get("name"),
            "surname": data.get("surname"),
            "email": data.get("email"),
            "date_of_birth": data.get("date_of_birth"),
            "gender": data.get("gender"),
            "password1": data.get("password1"),
            "password2": data.get("password2"),
        }
    )

    # ✅ Check if form is valid ✅ التحقق من صحة النموذج
    if form.is_valid():
        # 🛠️ Save the new user 🛠️ حفظ المستخدم الجديد
        user = form.save()
        # 🔓 Activate the account 🔓 تنشيط الحساب مباشرة
        user.is_active = True
        user.save()

        # 📤 إرجاع رسالة نجاح.
        return JsonResponse({"message": message, "email_sent": True}, safe=False)
    else:
        # ❌ If errors exist, return them ❌ إذا كان هناك أخطاء
        message = form.errors.as_json()
    # 🔍 Print errors for debugging 🔍 طباعة الأخطاء لأغراض التصحيح
    print(message)
    return JsonResponse({"message": message}, safe=False)


# 👤 User Info API Endpoint 👤 واجهة برمجية لاسترجاع معلومات المستخدم
@api_view(["GET", "POST"])
def me(request):
    """
    وظيفة لاسترجاع بيانات المستخدم الحالي.
    """
    # ✅ إذا كان المستخدم مصادقًا.
    if request.user.is_authenticated:
        # 📜 تحويل بيانات المستخدم إلى JSON.
        user_serializer = UserSerializer(request.user)
        return JsonResponse(user_serializer.data, safe=False)
    # ❌ إرجاع رسالة خطأ إذا كان المستخدم غير مصادق.
    return JsonResponse({"error": "User not authenticated"}, status=401)


# 📝 Profile API Endpoint
# 📝 واجهة برمجية لاسترجاع بيانات المستخدم
@api_view(["GET"])  # 🌐 السماح فقط بطلبات GET.
def profile(request, id):
    """
    وظيفة لاسترجاع بيانات ملف المستخدم بناءً على معرفه الفريد (ID).
    """
    user = User.objects.get(pk=id)
    # print("Profile User By Id 👉️", user)

    # 📜 تسلسل بيانات المستخدم باستخدام السيريالايزر المخصص.
    user_serializer = UserSerializer(user)
    # 🟢 افتراض أن المستخدم يمكنه إرسال طلب صداقة.
    can_send_friendship_request = True
    # 🔒 التحقق مما إذا كان المستخدم بالفعل صديقًا.
    if request.user in user.friends.all():
        can_send_friendship_request = False  # 🛑 لا يمكن إرسال طلب صداقة.

    # 🔍 Check if a request already exists between the users
    # 🔍 التحقق مما إذا كان هناك طلب صداقة موجود بالفعل بين المستخدمين
    check1 = FriendshipRequest.objects.filter(created_for=request.user).filter(
        created_by=user
    )
    check2 = FriendshipRequest.objects.filter(created_for=user).filter(
        created_by=request.user
    )
    # 🔴 إذا كان هناك طلب صداقة موجود، لا يمكن إرسال طلب جديد.
    if check1 or check2:
        can_send_friendship_request = False

    # 📤 إرجاع بيانات المستخدم وصلاحية إرسال طلب الصداقة كاستجابة JSON.
    return JsonResponse(
        {
            "user": user_serializer.data,  # بيانات المستخدم المسلسلة.
            "can_send_friendship_request": can_send_friendship_request,  # صلاحية إرسال طلب الصداقة.
        },
        safe=False,  # ⚠️ يتيح إرجاع البيانات غير المهيكلة كـ JSON.
    )


# 📝 واجهة برمجية لتعديل الملف الشخصي
@api_view(["POST"])  # 🌐 هذه الدالة تستجيب فقط لطلبات POST
def editprofile(request):
    # 👤 استرجاع بيانات المستخدم الحالي من الطلب
    # 👤 `request.user` تمثل المستخدم الذي أرسل الطلب
    user = request.user

    # 📧 الحصول على البريد الإلكتروني الجديد المرسل مع الطلب
    # 📧 يتم استخدام `request.data.get` للحصول على قيمة الحقل "email"
    email = request.data.get("email")

    # 📧 التحقق إذا كان البريد الإلكتروني مستخدمًا بالفعل من قبل مستخدم آخر
    # 📧 يتم استبعاد المستخدم الحالي من البحث باستخدام `exclude(id=user.id)`
    if User.objects.exclude(id=user.id).filter(email=email).exists():
        # 🔴 إذا تم العثور على البريد الإلكتروني بالفعل، يتم إرجاع رسالة خطأ
        return JsonResponse({"message": "email already exists"})
    else:
        # 📝 تهيئة نموذج تعديل الملف الشخصي
        # 📝 يتم تمرير البيانات من الطلب (`request.POST`) وأي ملفات (`request.FILES`)
        # 📝 `instance=user` يربط النموذج بالمستخدم الحالي لتعديل بياناته
        form = ProfileForm(request.POST, request.FILES, instance=user)

        # ✅ Validate and save profile if valid
        # ✅ التحقق من صحة النموذج
        # ✅ إذا كانت البيانات صالحة، يتم حفظ التعديلات في قاعدة البيانات
        if form.is_valid():
            form.save()

        # 🔄 تسلسل بيانات المستخدم المحدثة
        # 🔄 يتم استخدام `UserSerializer` لتحويل بيانات المستخدم إلى صيغة JSON
        serializer = UserSerializer(user)

        # 🔄 إرجاع رسالة نجاح تحتوي على بيانات المستخدم المحدثة
        return JsonResponse({"message": "information updated", "user": serializer.data})


# 🛠️ واجهة برمجية لتغيير كلمة المرور
@api_view(["POST"])  # 🌐 الدالة تقبل فقط طلبات POST
def editpassword(request):
    # 🔒 تهيئة نموذج تغيير كلمة المرور
    # 🔒 `PasswordChangeForm` هو نموذج افتراضي من Django لتغيير كلمة المرور
    # 🔒 يتم تمرير بيانات الطلب (`request.POST`) والمستخدم الحالي (`user`)
    user = request.user
    form = PasswordChangeForm(data=request.POST, user=user)

    # ✅ Validate and save new password if valid
    # ✅ التحقق من صحة البيانات في النموذج
    if form.is_valid():
        # 🛠️ إذا كانت البيانات صالحة، يتم حفظ كلمة المرور الجديدة
        form.save()
        # 🟢 إرجاع استجابة نجاح للعميل
        return JsonResponse({"message": "success"})
    else:
        # ❌ Return errors if form is invalid
        # ❌ إذا كانت البيانات غير صالحة، يتم إرجاع الأخطاء
        # 🔍 يتم استخدام `form.errors.as_json()` لتحويل الأخطاء إلى صيغة JSON
        return JsonResponse({"message": form.errors.as_json()}, safe=False)


# ___________________________
# ___________________________
# ___________________________


# 🌐 واجهة برمجية لجلب الأصدقاء وطلبات الصداقة لمستخدم معين
@api_view(["GET"])  # 🌐 الدالة تقبل فقط طلبات GET
def friends(request, pk):
    # 👤🎯 pk المستخدم اللى فاتح صفحة البروافيل عن طريق
    # User Pk [Id 🔑 ] الايدى الخاص بى المستخدام اللى انا بجيب الاصدقاء الخاصين بية
    user = User.objects.get(pk=pk)
    # print(f"👥 [Friends] User By Id : {user}")
    # print("_________________________________👥_______________________________")
    # ✅ التحقق مما إذا كان المستخدم الحالي هو نفسه المستخدم الهدف

    # 🟢 افتراض أن المستخدم يمكنه إرسال طلب صداقة.
    can_send_friendship_request = True
    # 🔒 التحقق مما إذا كان المستخدم بالفعل صديقًا.
    if request.user in user.friends.all():
        # 📡 تسجيل حالة الإرسال
        # logger.info(f"✅ [Friends] User Is Friend Yes: {request.user}")
        # print("_________________________________🔒_______________________________")
        # 🛑 لا يمكن إرسال طلب صداقة
        can_send_friendship_request = False

    is_current_user = user == request.user
    # print(f"request.user {request.user}")
    # print(f"💪 [Friends] User In Page Profile Is Owner  {is_current_user}")
    # print("_________________________________💪_______________________________")
    # 📝 جلب طلبات الصداقة إذا كان المستخدم الحالي هو نفسه الهدف
    requests = []
    if is_current_user:
        requests = FriendshipRequest.objects.filter(
            created_for=request.user,
            status=FriendshipRequest.WAITING,
        )
        # logger.info(f"💪 [Friends] If User Is Owner  {requests}")
        # print("_________________________________✅_______________________________")
        # 🔄 تحويل الطلبات إلى JSON باستخدام Serializer 🔄 تحويل الطلبات إلى بيانات JSON باستخدام السيريالايزر
        requests = FriendshipRequestSerializer(requests, many=True).data

    # 👫 Retrieve all friends of the user
    # 👫 جلب جميع أصدقاء المستخدم
    friendsAll = user.friends.all()
    # 📡 تسجيل حالة الإرسال
    # logger.info(f"👫 All Friends  {friendsAll}")
    # print("_________________________________✅_______________________________")
    # إضافة الأشخاص الذين لا يوجد بينهم طلب صداقة
    # اضافة جميع المستخدمين اللى سجلو الدخول فى الموقع
    notsend_users = User.objects.exclude(id__in=[friend.id for friend in friendsAll])
    # logger.info(f"👫 Not Send Friends  {notsend_users}")
    # print("_________________________________✅_______________________________")
    send = FriendshipRequest.get_friends_by_status(user, FriendshipRequest.SEND)
    # logger.info(f"👫 Send Friends  {send}")
    # print("_________________________________✅_______________________________")
    waiting_friends = FriendshipRequest.get_friends_by_status(
        user, FriendshipRequest.WAITING
    )
    # logger.info(f"👫 Send Friends  {send}")
    # print("_________________________________✅_______________________________")
    accepted_friends = FriendshipRequest.get_friends_by_status(
        user, FriendshipRequest.ACCEPTED
    )
    # logger.info(f"👫 [Friends] Accepted Friends  {accepted_friends}")
    # print("_________________________________✅_______________________________")
    rejected_friends = FriendshipRequest.get_friends_by_status(
        user, FriendshipRequest.REJECTED
    )
    # logger.info(f"👫 [Friends] Rejected Friends  {rejected_friends}")
    # print("_________________________________✅_______________________________")
    cancelled_requests = FriendshipRequest.get_friends_by_status(
        user, FriendshipRequest.CANCEL
    )
    # logger.info(f"👫 [Friends] Cancelled Requests Friends  {cancelled_requests}")
    # print("_________________________________✅_______________________________")
    unfriend_requests = FriendshipRequest.get_friends_by_status(
        user, FriendshipRequest.UNFRIEND
    )
    # logger.info(f"👫 [Friends] Unfriend Friends  {unfriend_requests}")
    # print("_________________________________✅_______________________________")

    # 📤 إرجاع البيانات كاستجابة JSON تحتوي على بيانات المستخدم، الأصدقاء، والطلبات
    return JsonResponse(
        {
            "user": UserSerializer(user).data,  # بيانات المستخدم
            # "friends": UserSerializer(friends, many=True).data,  # بيانات الأصدقاء
            "friends": {
                "all": UserSerializer(friendsAll, many=True).data,
                "notsend": UserSerializer(notsend_users, many=True).data,
                "send": UserSerializer(send, many=True).data,
                "waiting": UserSerializer(waiting_friends, many=True).data,
                "accepted": UserSerializer(accepted_friends, many=True).data,
                "rejected": UserSerializer(rejected_friends, many=True).data,
                "cancel": UserSerializer(cancelled_requests, many=True).data,
                "unfriend": UserSerializer(unfriend_requests, many=True).data,
            },
            # طلبات الصداقة (إذا كانت موجودة)
            "requests": requests,
            # صلاحية إرسال طلب الصداقة.
            "can_send_friendship_request": can_send_friendship_request,
        },
        safe=False,  # السماح بتمرير كائنات ليست من نوع القاموس
    )


@api_view(["POST"])  # 🌐 الدالة تقبل فقط طلبات POST
def send_friendship_request(request, pk):
    try:
        # 👤 استرجاع بيانات المستخدم المستهدف
        user = User.objects.get(pk=pk)

        # 🙏 🔍 التحقق إذا كان هناك طلب صداقة مرسل
        send_request = FriendshipRequest.objects.filter(
            created_for=user, created_by=request.user
        ).first()
        print(f"🙏 send_request.id  {send_request}")
        # 🤝 🔍 التحقق إذا كان هناك طلب صداقة مستلم
        received_request = FriendshipRequest.objects.filter(
            created_for=request.user, created_by=user
        ).first()

        # ✅ إذا لم يكن هناك أي طلبات صداقة موجودة
        if not send_request and not received_request:
            # ✉️ إنشاء طلب صداقة جديد
            new_send_request = FriendshipRequest.objects.create(
                created_for=user, created_by=request.user, status=FriendshipRequest.SEND
            )
            # 📡 تسجيل حالة الإرسال
            logger.info(f"👉️ new_send_request {new_send_request}")

            # Notsend أخرجه من
            FriendshipRequest.objects.filter(
                created_for=user,
                created_by=request.user,
                status=FriendshipRequest.NOTSEND,
            ).delete()
            # _______________________________________
            # إنشاء طلب من المتلقي إلى المرسل مع انتظار الحالة
            # FriendshipRequest.objects.create(
            #     created_for=request.user,
            #     created_by=user,
            #     status=FriendshipRequest.WAITING,
            # )
            # تحديث حالة المستخدم المستلم (Waiting)
            FriendshipRequest.objects.update_or_create(
                created_for=request.user,
                created_by=user,
                defaults={"status": FriendshipRequest.WAITING},
            )

            # Notsend أخرج من
            FriendshipRequest.objects.filter(
                created_for=request.user,
                created_by=user,
                status=FriendshipRequest.NOTSEND,
            ).delete()
            # إنشاء إشعار طلب الصداقة للمستلم
            notification = create_notification(
                # 👥 نوع الإشعار (طلب صداقة جديد)
                "new_friendrequest",
                # 👤 الشخص الذي أرسل طلب الصداقة
                created_by=request.user,
                # 👤 الشخص الذي استلم الطلب
                created_for=user,
                # 📩 معرف خاص لطلب الصداقة إذا كان موجود
                friendrequest_id=new_send_request.id,
            )
            # 🛑 لا يمكن إرسال طلب صداقة
            can_send_friendship_request = False
            return JsonResponse(
                {
                    "message": "Friendship request send successfully",
                    # صلاحية إرسال طلب الصداقة.
                    "can_send_friendship_request": can_send_friendship_request,
                }
            )

        # ⚠️ إذا كان الطلب موجوداً بالفعل
        if send_request and send_request.status == FriendshipRequest.SEND:
            # 🛑 لا يمكن إرسال طلب صداقة
            can_send_friendship_request = False
            datatroorfalse = (
                send_request and send_request.status == FriendshipRequest.SEND
            )
            # 📡 تسجيل حالة الإرسال
            logger.info(f"🚀 Request already send: {datatroorfalse} 🙏")

            return JsonResponse(
                {
                    "message": "Request already send",
                    # صلاحية إرسال طلب الصداقة.
                    "can_send_friendship_request": can_send_friendship_request,
                }
            )

        # 🔄 تحديث حالة الطلبات الحالية
        if send_request:
            send_request.status = FriendshipRequest.SEND
            send_request.save()
            logger.info(f"🙏 Send Status {send_request.status} ")

        if received_request:
            received_request.status = FriendshipRequest.WAITING
            received_request.save()
            logger.info(f"🤝 Send Received  {received_request.status} ")

        # 💬 إرجاع رسالة النجاح
        return JsonResponse(
            {
                "message": "Friendship request updated successfully",
                "status": (
                    send_request.status if send_request else received_request.status
                ),
            }
        )

    except User.DoesNotExist:
        return JsonResponse({"message": "User not found"}, status=404)
    except Exception as e:
        return JsonResponse(
            {"message": "An unexpected error occurred", "error": str(e)}, status=500
        )


# 🌐 واجهة برمجية لمعالجة وتحديث حالة طلب الصداقة
@api_view(["POST"])  # 🌐 الدالة تستقبل فقط طلبات POST
def handle_request(request, pk, status):
    try:
        # 🛠️ التحقق من إذن المستخدم
        if not request.user.is_authenticated:
            logger.warning("🚫 An unauthorized user has attempted to access.")
            raise PermissionDenied("You must be logged in to perform this action.")
        # 🧑‍🤝‍🧑 [ الصفحة اللى انا فيهاء ID الحصول على المستخدم المستهدف [اللى هو
        user = User.objects.get(pk=pk)
        # 🟢 افتراض أن المستخدم يمكنه إرسال طلب صداقة.
        can_send_friendship_request = True
        # 🔒 التحقق مما إذا كان المستخدم بالفعل صديقًا.
        if request.user in user.friends.all():
            # 🛑 لا يمكن إرسال طلب صداقة
            can_send_friendship_request = False
            # ✅ في حالة القبول، إضافة الأصدقاء
            if status == "unfriend":
                logger.info(
                    f"❌ remove {request.user.name} And {user.name} As Unfriends."
                )
                remove_friends(request.user, user)
                return JsonResponse(
                    {
                        "message": f"Friendship request {status} successfully",
                        "status": status,
                    }
                )

        # 🔍 🙏 [ صلاحيات المستخدم المرسل للطلب ] جلب طلب الصداقة المرسل
        friendship_request_send = FriendshipRequest.objects.filter(
            created_by=request.user, created_for=user
        ).first()
        # 🚫 🙏 [ صلاحيات المستخدم المرسل للطلب ] الغاء طلب الصداقة
        if friendship_request_send:
            # 💬 تحديث الحالة وتخزينها
            update_request_status(friendship_request_send, status)
            # 🚫 في حالة الإلغاء، تحديث المستخدم إلى حالة NOTSEND
            if status == "cancel":
                friendship_request_send.created_for.friendship_status = (
                    FriendshipRequest.NOTSEND
                )
                friendship_request_send.created_for.friendship_status = (
                    FriendshipRequest.CANCEL
                )
                friendship_request_send.created_for.save()
                logger.info(
                    f"🚫 The order has been cancelled and the user status has been restored. {user.name} To NOTSEND."
                )

        # _______________________________________
        # 🔍 🤝 [ صلاحيات المستخدم المستلم للطلب ] جلب طلب الصداقة المرسل
        friendship_request_waiting = FriendshipRequest.objects.filter(
            created_for=request.user, created_by=user
        ).first()
        # 🚫 🙏 [ صلاحيات المستخدم المرسل للطلب ] قبول او رفض طلب الصداقة
        if friendship_request_waiting:
            # 💬 تحديث الحالة وتخزينها
            update_request_status(friendship_request_waiting, status)
            # ✅ في حالة القبول، إضافة الأصدقاء
            if status == "accepted":
                add_friends(request.user, user)
                logger.info(f"✅ Added {request.user.name} And {user.name} As friends.")
                # ارسال اشعار الى المرسال بقبول طلب الصداقة
                notificationWaiting = create_notification(
                    # 👥 نوع الإشعار (طلب صداقة جديد)
                    "accepted_friendrequest",
                    # 👤 الشخص الذي أرسل طلب الصداقة
                    created_by=request.user,
                    # 👤 الشخص الذي استلم الطلب
                    created_for=user,
                    # 📩 معرف خاص لطلب الصداقة إذا كان موجود
                    friendrequest_id=friendship_request_send.id,
                )
                # 🔔 تحديث الإشعار كـ "مقروء"
                notificationSendAll = Notification.objects.all()
                print(f"notificationSendAll {notificationSendAll}")
                notificationSendId = Notification.objects.filter(
                    created_for=request.user
                )
                # notificationSendId = Notification.objects.filter(
                #     created_for=request.user
                # ).get(pk=pk)

                # notificationSend = Notification.objects.filter(
                #     created_for=request.user, friendrequest_id=FriendshipRequest.id
                # ).first()
                # if notificationSend:
                #     notificationSend.is_read = True
                #     notificationSend.save()
                print(f"notificationSendId {notificationSendId}")
                """
                "notification_id": (
                        notificationSend.id if notificationSend else None
                    ),
                """
            return JsonResponse(
                {
                    "message": f"Friendship request {status} successfully",
                    "status": status,
                }
            )
        # 🔴 ❌ [ صلاحيات المستخدم المرسل للطلب ] اذا حدث أخطاء
        if not friendship_request_waiting:
            logger.error(
                f"❌ Friendship request between {request.user.name} And {user.name} unavailable."
            )
            return JsonResponse({"error": "Friendship request not found"}, status=404)

    # _______________________________________
    except PermissionDenied as e:
        return JsonResponse({"error": str(e)}, status=403)
    except User.DoesNotExist:
        logger.error("❌ User not found.")
        return JsonResponse({"error": "User not found"}, status=404)
    except Exception as e:
        logger.exception("❌ An unexpected error occurred.")
        return JsonResponse({"error": "An unexpected error occurred"}, status=500)

    # 🟢 افتراض أن المستخدم يمكنه إرسال طلب صداقة.
    # can_send_friendship_request = True
    # # 🔒 التحقق مما إذا كان المستخدم بالفعل صديقًا.
    # if request.user in user.friends.all():
    #     can_send_friendship_request = False  # 🛑 لا يمكن إرسال طلب صداقة.
    #         "can_send_friendship_request": can_send_friendship_request,  # صلاحية إرسال طلب الصداقة.
    # # _____________________________________________
    # # _____________________________________________
    # # _____________________________________________
    # # _____________________________________________
    # # _____________________________________________


# 🛠️ وظيفة لتحديث حالة طلب الصداقة
def update_request_status(friendship_request, status):
    friendship_request.status = status
    friendship_request.save()
    logger.info(f"🔄 The order status has been updated to {status}.")

    # ❌ حذف الطلب في حالات معينة
    if status in [
        FriendshipRequest.WAITING,
        FriendshipRequest.SEND,
        FriendshipRequest.CANCEL,
    ]:
        friendship_request.delete()
        logger.info(
            f"❌ The request was deleted between {friendship_request.created_by.surname} And {friendship_request.created_for.surname}."
        )


# 👫 وظيفة لإضافة الأصدقاء
def add_friends(user1, user2):
    user1.friends.add(user2)
    user1.friends_count += 1
    user1.save()

    user2.friends.add(user1)
    user2.friends_count += 1
    user2.save()


# 👫 وظيفة لإضافة الأصدقاء
def remove_friends(user1, user2):
    user1.friends.remove(user2)
    user1.friends_count -= 1
    user1.save()

    user2.friends.remove(user1)
    user2.friends_count -= 1
    user2.save()


# 🌐 واجهة برمجية لاقتراح المستخدمين الذين قد يعرفهم المستخدم الحالي
@api_view(["GET"])  # 🌐 الدالة تقبل فقط طلبات GET
def my_friendship_suggestions(request):

    # 🤝 Suggest users the current user may know
    # 🤝 اقتراح المستخدمين الذين قد يعرفهم المستخدم الحالي
    # 🧑‍🤝‍🧑 السيريالايزر يقوم بتحويل قائمة المستخدمين الذين قد يعرفهم المستخدم إلى صيغة JSON
    serializer = UserSerializer(request.user.people_you_may_know.all(), many=True)
    # print("🤝 Suggest users", serializer)

    # 📤 إرجاع البيانات كاستجابة JSON
    return JsonResponse(serializer.data, safe=False)

```

## 🔗 Urls (الروابط)

```python
# 📄 [ users_accounts/urls.py ] ملف

# 🌐 تكوين الروابط لواجهة برمجية لإدارة المستخدم والأصدقاء
# 🌐 URL Configuration for User and Friend Management API

# 📦 استيراد path من مكتبة Django لتحديد الروابط
from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)  # 🛡️ استيراد عرض الحصول على رمز JWT وتحديثه
from . import api  # 🔧 استيراد الوظائف من ملف api

urlpatterns = [
    # 👤 استرجاع معلومات المستخدم الحالي
    # 🌐 Retrieve current user's information
    path(
        "me/", api.me, name="me"
    ),  # 👥 رابط لاسترجاع معلومات المستخدم الذي قام بتسجيل الدخول
    # 📝 تسجيل مستخدمين جدد
    # 🌐 Signup for new users
    # 📝 رابط لتسجيل مستخدمين جدد
    path("signup/", api.signup, name="signup"),
    # 🔑 الحصول على رمز JWT لتسجيل الدخول
    # 🌐 Obtain JWT token for login
    path(
        "login/", TokenObtainPairView.as_view(), name="token_obtain"
    ),  # 🔑 رابط للحصول على رمز JWT لتسجيل الدخول
    # ♻️ تحديث رمز JWT
    # 🌐 Refresh JWT token
    path(
        "refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # 🔄 رابط لتحديث رمز JWT
    # ___________________________
    # ___________________________
    # ___________________________
    # ** إدارة الملف الشخصي للمستخدم **
    # 📝 استرجاع الملف الشخصي للمستخدم بناءً على معرفه
    # 🌐 Retrieve user profile by ID
    path(
        "profile/<uuid:id>/", api.profile, name="profile"
    ),  # 👤 رابط لعرض الملف الشخصي للمستخدم باستخدام المعرف (ID)
    # ✏️ تعديل الملف الشخصي للمستخدم
    # 🌐 Edit user profile
    path(
        "editprofile/", api.editprofile, name="editprofile"
    ),  # 📝 رابط لتعديل الملف الشخصي للمستخدم
    # 🔒 تغيير كلمة مرور المستخدم
    # 🌐 Change user password
    path(
        "editpassword/", api.editpassword, name="editpassword"
    ),  # 🔑 رابط لتغيير كلمة مرور المستخدم
    # ___________________________
    # ___________________________
    # ___________________________
    # ** إدارة الأصدقاء **
    # 👫 استرجاع أصدقاء المستخدم
    # 🌐 Retrieve friends of a user
    path(
        "friends/<uuid:pk>/", api.friends, name="friends"
    ),  # 👥 رابط لاسترجاع أصدقاء المستخدم بناءً على المعرف (ID)
    # 🤝 استرجاع الأصدقاء المقترحين للمستخدم
    # 🌐 Retrieve suggested friends for the user
    path(
        "friends/suggested/",
        api.my_friendship_suggestions,
        name="my_friendship_suggestions",
    ),  # 👫 رابط لاسترجاع الأصدقاء المقترحين بناءً على الصداقات السابقة
    # ✉️ إرسال طلب صداقة
    # 🌐 Send a friendship request
    path(
        "friends/<uuid:pk>/request/",
        api.send_friendship_request,
        name="send_friendship_request",
    ),  # 💌 رابط لإرسال طلب صداقة إلى مستخدم آخر
    # 🛠️ معالجة طلب الصداقة (قبول/رفض)
    # 🌐 Handle a friendship request (accept/reject)
    path(
        "friends/<uuid:pk>/<str:status>/", api.handle_request, name="handle_request"
    ),  # 👥 رابط لمعالجة طلب الصداقة (قبول أو رفض)
]

```
