# 🐍 Django — Virtual Environment

> بيئة Python معزولة خاصة بالمشروع، تُستخدم لفصل مكتبات وإصدارات المشروع عن باقي مشاريع Python الموجودة على الجهاز.

---

### 1. 🎯 Purpose

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

الـVirtual Environment بتعمل بيئة مستقلة للمشروع، بحيث مكتبات وإصدارات المشروع ما تتعارضش مع مشاريع Python تانية على الجهاز.

مثال:

</div>

```text
Project A
├── Django 4.x
│
Project B
└── Django 5.x
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

كل مشروع يقدر يشتغل بإصداراته الخاصة بدون تعارض.

</div>

---

### 2. 🧠 Concept

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

بدل ما كل مشاريع Python تستخدم نفس المكتبات الموجودة بشكل Global على الجهاز، بننشئ بيئة خاصة بكل مشروع.

بدون Virtual Environment:

</div>

```text
Computer
│
├── Python
├── Django
├── Requests
└── Other Libraries
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

مع Virtual Environment:

</div>

```text
Project
│
├── venv
│   ├── Scripts
│   ├── Lib
│   └── ...
│
├── manage.py
└── ...
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

الفكرة الأساسية:

</div>

```text
Project
   ↓
Virtual Environment
   ↓
Project Dependencies
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

وبالتالي كل مشروع بيكون عنده مساحة مستقلة للمكتبات والإصدارات الخاصة بيه.

</div>

---

### 3. 🔧 Requirements

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

قبل إنشاء البيئة الافتراضية، لازم نتأكد إن Python وpip موجودين على الجهاز.

</div>

#### 🐍 Python Version

```cmd
python --version
```

أو:

```cmd
py --version
```

#### 📦 Pip Version

```cmd
pip --version
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

كمان يُفضل تنفيذ الخطوات من داخل مجلد المشروع.

</div>

---

### 4. 🛠️ Installation / Setup

#### ⬆️ Upgrade Pip

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

لو محتاج تحدث pip، استخدم:

</div>

```cmd
py -m pip install --upgrade pip
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

مش محتاج تثبت virtualenv بشكل منفصل لو هتستخدم الأداة المدمجة في Python وهي venv.

</div>

#### 📦 Create Virtual Environment

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

داخل مجلد المشروع:

</div>

```cmd
python -m venv venv
```

أو:

```cmd
py -m venv venv
```

#### 🚀 Activate on Windows

```cmd
venv\Scripts\activate
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

بعد التفعيل، أوامر Python وpip هتتعامل مع البيئة الخاصة بالمشروع بدل البيئة الـGlobal.

</div>

---

### 5. 🚀 Usage

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

بعد إنشاء وتفعيل البيئة الافتراضية، بنستخدمها لتثبيت مكتبات المشروع وتشغيل أوامر Python الخاصة بالمشروع.

</div>

#### 📚 Show Installed Libraries

```cmd
pip list
```

#### 📋 Export Dependencies

```cmd
pip freeze
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

ويُفضل تسجيل dependencies داخل ملف requirements.txt:

</div>

```cmd
pip freeze > requirements.txt
```

#### ⛔ Deactivate

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

لإغلاق البيئة الافتراضية:

</div>

```cmd
deactivate
```

---

### 6. 📁 Structure

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

بعد إنشاء البيئة الافتراضية، شكل المشروع ممكن يكون كالتالي:

</div>

```text
Project/
│
├── .git/
│
├── venv/
│   ├── Include/
│   ├── Lib/
│   ├── Scripts/
│   │   ├── activate
│   │   └── ...
│   │
│   └── pyvenv.cfg
│
├── .gitignore
├── LICENSE
└── README.md
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

مجلد venv بيحتوي على ملفات البيئة والمكتبات الخاصة بالمشروع، ولذلك لا يتم رفعه إلى Git.

</div>

---

### 7. 🧩 Important Concepts

#### 🔹 Virtual Environment

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

بيئة Python مستقلة عن باقي مشاريع Python.

</div>

#### 🔹 Dependency Isolation

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

عزل مكتبات المشروع وإصداراتها عن المشاريع الأخرى.

</div>

#### 🔹 pip

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

أداة Python الأساسية لإدارة وتثبيت packages.

</div>

#### 🔹 requirements.txt

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

ملف بيتم فيه تسجيل dependencies المطلوبة للمشروع، بحيث يمكن إعادة تجهيز البيئة على جهاز آخر.

</div>

#### 🔹 .gitignore

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

ملف بيحدد الملفات والمجلدات التي لا يجب رفعها إلى Git، ومنها Virtual Environment.

</div>

---

### 8. 💻 Examples

#### Example 1 — Create Environment

```cmd
python -m venv venv
```

#### Example 2 — Activate

```cmd
venv\Scripts\activate
```

#### Example 3 — Install Django After Activation

```cmd
venv\Scripts\activate

pip install django
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

المهم إن تثبيت المكتبات يتم بعد التأكد إن البيئة الصحيحة مفعلة.

</div>

#### Example 4 — Save Dependencies

```cmd
pip freeze > requirements.txt
```

#### Example 5 — Recreate Dependencies

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

عند تجهيز بيئة جديدة للمشروع، يمكن تثبيت dependencies المسجلة في requirements.txt:

</div>

```cmd
pip install -r requirements.txt
```

---

### 9. ❌ Common Mistakes

#### 1. تثبيت المكتبات قبل تفعيل البيئة

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

من الأخطاء الشائعة تثبيت مكتبات المشروع بدون التأكد إن Virtual Environment مفعلة.

</div>

```cmd
pip install django
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

الأفضل:

</div>

```cmd
venv\Scripts\activate

pip install django
```

#### 2. رفع venv إلى Git

لا يتم رفع:

```text
venv/
```

ويجب إضافتها إلى:

```text
.gitignore
```

مثال:

```gitignore
venv/
```

#### 3. عدم تسجيل Dependencies

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

وجود المكتبات داخل جهازك مش كفاية.

لازم dependencies تكون مسجلة عشان تقدر تعيد بناء البيئة بسهولة.

</div>

```cmd
pip freeze > requirements.txt
```

#### 4. اعتبار venv جزءًا من Source Code

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

الـvenv نفسها مش المفروض تكون جزء من الكود الذي يتم مشاركته في Git.

الذي يتم مشاركته هو تعريف dependencies، وليس ملفات البيئة نفسها.

</div>

---

### 10. 🧠 Why?

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

نستخدم Virtual Environment لأن كل مشروع ممكن يعتمد على إصدارات معينة من المكتبات.

بدون العزل ممكن يحصل Version Conflict:

</div>

```text
Project A
    ↓
Global Python
    ↑
Project B
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

أما مع العزل:

</div>

```text
Project A
    ↓
  venv A


Project B
    ↓
  venv B
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

وبالتالي كل مشروع يقدر يحتفظ بالـdependencies الخاصة بيه بدون التأثير على المشاريع الأخرى.

</div>

---

### 11. 🔗 Project Usage

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

داخل مشروع So_Iam_OS، الـVirtual Environment تعتبر جزء أساسي من إعداد الـBackend.

التسلسل الأساسي:

</div>

```text
Python
   ↓
Virtual Environment
   ↓
Activate
   ↓
Upgrade pip
   ↓
Install Dependencies
   ↓
Django
   ↓
Project Setup
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

يعني قبل تثبيت Django وباقي مكتبات الـBackend، لازم تكون البيئة الافتراضية جاهزة ومفعلة.

</div>

---

### 12. 🤖 AI Reference

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

المعلومات التالية تعتبر قواعد مرجعية للـAI عند التعامل مع إعداد Backend المشروع.

</div>

```text
Project:
So_Iam_OS

Technology:
Python / Django

Domain:
Backend

Topic:
Virtual Environment

Purpose:
Dependency Isolation

Environment:
venv

Activation:
venv\Scripts\activate

Dependency File:
requirements.txt

Version Control:
Git

Ignored Directory:
venv/

Rules:
- يجب تشغيل Virtual Environment قبل تثبيت مكتبات المشروع.
- لا يتم تثبيت Dependencies الخاصة بالمشروع Global بدون سبب.
- venv لا يتم رفعها إلى Git.
- Dependencies يجب تسجيلها.
- requirements.txt هو ملف تعريف Dependencies للمشروع.
- Virtual Environment جزء من Backend Setup.
- حذف venv لا يعني حذف Source Code للمشروع.
```

---

### 13. 📊 Current Status

| Task                          | Status |
| ----------------------------- | ------ |
| Python Installed              | ✅     |
| Pip Available                 | ✅     |
| Virtual Environment Created   | ✅     |
| Virtual Environment Activated | ✅     |
| Dependencies Setup            | ⬜     |
| Django Installation           | ⬜     |
| requirements.txt              | ⬜     |
| venv added to .gitignore      | ⬜     |

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

الحالة هنا خاصة بمرحلة Virtual Environment. بعد تنفيذ الخطوات فعليًا داخل المشروع، يتم تحديث الـStatus حسب الواقع.

</div>

---

### 14. ✅ Checklist

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

استخدم القائمة دي للتأكد إن مرحلة Virtual Environment خلصت بشكل صحيح.

</div>

- [x] التأكد من Python
- [x] التأكد من pip
- [x] إنشاء Virtual Environment
- [x] تفعيل البيئة
- [x] إضافة venv إلى `.gitignore`
- [ ] تثبيت Django
- [ ] تثبيت باقي dependencies
- [ ] إنشاء `requirements.txt`

---

### 15. 🔗 Related Documentation

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

الملفات والتقنيات المرتبطة بالموضوع:

</div>

- Python
- pip
- Django
- `requirements.txt`
- Git
- `.gitignore`
- Backend Setup

---

### 16. 📝 Notes

#### 🔹 اسم البيئة

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

`venv` هو اسم شائع للـVirtual Environment، لكن ممكن تسمي البيئة بأي اسم مناسب.

</div>

مثال:

```cmd
python -m venv .venv
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

في الحالة دي هيكون مسار البيئة:

</div>

```text
.venv/
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

ولازم يتم تحديث `.gitignore` وفقًا للاسم المستخدم.

</div>

```gitignore
.venv/
```

#### 🔹 حذف Virtual Environment

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

لحذف البيئة على Windows:

</div>

```cmd
rmdir /S /Q venv
```

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

حذف `venv` لا يحذف ملفات المشروع الأساسية، لكنه يحذف البيئة والمكتبات المثبتة بداخلها.

بعد حذفها يمكن إنشاء بيئة جديدة وتثبيت dependencies مرة أخرى.

</div>

---

## 📌 Quick Reference

```cmd
python --version

py --version

pip --version

py -m pip install --upgrade pip

python -m venv venv

venv\Scripts\activate

pip list

pip freeze

pip freeze > requirements.txt

pip install -r requirements.txt

deactivate

rmdir /S /Q venv
```

---

## 🧠 AI Rules

<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">

- Virtual Environment هي أول مرحلة في Backend Setup.
- يجب تفعيل البيئة قبل تثبيت Dependencies.
- لا يتم رفع `venv/` إلى Git.
- يتم مشاركة `requirements.txt` بدلًا من مشاركة ملفات `venv`.
- عند إعادة بناء المشروع على جهاز جديد، يتم إنشاء Virtual Environment جديدة.
- يتم تثبيت Dependencies من `requirements.txt`.
- لا يتم افتراض أن حذف `venv` يؤدي إلى حذف المشروع.
- إذا تغير اسم البيئة من `venv` إلى `.venv`، يجب تحديث أوامر التفعيل و`.gitignore`.
- حالة المشروع يجب أن تعكس ما تم تنفيذه فعليًا، وليس ما هو مخطط له فقط.

</div>
