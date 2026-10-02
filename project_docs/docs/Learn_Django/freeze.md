### ❄️ freeze

```cmd
cd backend_django
```

<div dir="rtl" style="font-size:1.5vw; margin:1.5rem 0">
  الأمر ده بيعمل تصدير لكل المكتبات اللي مثبتها في البيئة الافتراضية بتاعتك (virtual environment) ويحطهم في ملف اسمه requirements.txt.
</div>

```cmd
pip freeze > requirements.txt
```

<div dir="rtl" style="font-size:1.5vw; margin:1.5rem 0">
  الأمر ده بيعرض قائمة المكتبات المثبتة حاليًا في البيئة الافتراضية مع إصداراتها، لكن مش بيحفظهم في ملف.
</div>

```cmd
pip freeze
```

<div dir="rtl" style="font-size:1.5vw; margin:1.5rem 0">
  يقدر أي حد يثبت نفس المكتبات بالظبط باستخدام:
</div>

```cmd
pip install -r requirements.txt
```
