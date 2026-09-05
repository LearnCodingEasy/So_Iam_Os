
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # 3️⃣ django-allauth [Allauth]
    path("accounts/", include("allauth.urls")),
    path('admin/', admin.site.urls),
]
