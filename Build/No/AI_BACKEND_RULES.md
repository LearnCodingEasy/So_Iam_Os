PERMANENT SYSTEM RULES
SO_IAM_OS - FRONTEND ARCHITECTURE & LIBRARY GOVERNANCE

هذه التعليمات قواعد ثابتة وإلزامية للمشروع، ويجب تطبيقها على كل طلب مستقبلي دون استثناء، سواء كان الطلب:

إنشاء صفحة جديدة.
تعديل صفحة موجودة.
إنشاء Component.
تطوير Module.
إنشاء Form أو Dialog.
إنشاء Dashboard.
تطوير Charts أو Workflows.
ربط Backend API.
إصلاح Bug.
تحسين التصميم.
إعادة هيكلة الكود.
تحسين الأداء.
إضافة وظيفة جديدة.
تعديل أي ملف داخل Frontend.

هذه القواعد أعلى أولوية من أي أسلوب تنفيذ افتراضي لدى AI، ويجب عدم تجاهلها عند تنفيذ أي مهمة.

RULE 1: PROJECT TECHNOLOGY PRESERVATION

المشروع الأساسي هو:

SO_IAM_OS

مسار Frontend:

So_Iam_OS/frontend_vue/

التقنيات الأساسية المعتمدة:

Vue.js 3.
Vite.
JavaScript ES Modules.
Vue Composition API.
PrimeVue.
Pinia.
Vue Router.
Axios.
SCSS.
Sass.

يجب الحفاظ على التقنية والبنية الحالية للمشروع.

ممنوع إعادة إنشاء المشروع من الصفر عند طلب تعديل أو تطوير جزء منه.

ممنوع استبدال مكتبة موجودة بمكتبة أخرى دون ضرورة تقنية حقيقية وموافقة واضحة.

يجب احترام إصدارات المكتبات الموجودة في package.json وملف Lockfile.

RULE 2: EXISTING LIBRARIES ARE THE FIRST CHOICE

يحتوي المشروع على مجموعة كبيرة من المكتبات المعتمدة.

هذه المكتبات هي الأدوات الأساسية التي يجب على AI تحليلها واستخدامها والاستفادة منها قبل كتابة حلول مخصصة أو اقتراح تثبيت مكتبات جديدة.

2.1 UI & Design Libraries
primevue
@primevue/themes
primeicons
@fortawesome/fontawesome-svg-core
@fortawesome/free-brands-svg-icons
@fortawesome/free-regular-svg-icons
@fortawesome/free-solid-svg-icons
@fortawesome/vue-fontawesome
animate.css
gsap
floating-vue
vue-sonner

قواعد الاستخدام:

استخدام PrimeVue كمكتبة UI الأساسية.
استخدام PrimeVue Theme لتوحيد التصميم بعد التحقق من توافق الإصدار.
استخدام PrimeIcons وFont Awesome حسب الحاجة.
استخدام GSAP للحركات المعقدة عند الحاجة.
استخدام Animate.css للحركات الجاهزة.
استخدام Vue Sonner للإشعارات.
استخدام Floating Vue للتلميحات والعناصر العائمة عند الحاجة.
2.2 Data Management & API Libraries
axios
pinia
@tanstack/vue-query
@vueuse/core
lodash
nprogress

قواعد الاستخدام:

Axios هو المسؤول عن الاتصال بالـ Backend.
Pinia هو المسؤول عن Global Application State.
Vue Query مسؤول عن Server State وCaching وRefetching.
VueUse للأدوات التفاعلية.
Lodash لمعالجة البيانات عند الحاجة.
NProgress لمؤشر تقدم التنقل.

يجب تحديد المسؤوليات بوضوح وعدم تكرار نفس البيانات والمنطق في أكثر من مكان دون سبب.

2.3 Charts & Workflow Libraries
chart.js
vue-chartjs
@vue-flow/core
@vue-flow/background
@vue-flow/controls
@vue-flow/minimap
dagre

قواعد الاستخدام:

Chart.js وVue Chart.js للرسوم البيانية.
Vue Flow لإنشاء Workflows وNode Editors وProcess Diagrams.
Dagre لترتيب المخططات تلقائياً.
إعادة استخدام مكونات الرسوم البيانية والمخططات عند تكرارها.
2.4 Rich Text & Markdown Libraries
@tiptap/vue-3
@tiptap/starter-kit
quill
marked
vue3-markdown-it
github-markdown-css
prismjs
dompurify

قواعد الاستخدام:

Tiptap للمحررات المتقدمة.
Quill للمحررات التي تتطلب توافقاً مع تطبيقات موجودة.
Marked أو Markdown-it وفق متطلبات العرض.
PrismJS لتلوين الأكواد.
DOMPurify لتنظيف HTML قبل عرضه.
GitHub Markdown CSS لتنسيق المحتوى عند الحاجة.

لا تستخدم أكثر من Markdown Renderer أو Rich Text Editor لنفس الوظيفة دون مبرر.

لا تعرض HTML غير موثوق دون Sanitization.

2.5 Forms & Validation Libraries
vee-validate
zod
@vee-validate/zod

قواعد الاستخدام:

VeeValidate لإدارة النماذج.
Zod لتعريف Validation Schemas.
استخدام تكامل Zod مع VeeValidate.
إنشاء Validation Schemas قابلة لإعادة الاستخدام.
تجنب كتابة Validation Logic مكرر داخل كل صفحة.
2.6 File & Interaction Libraries
cropperjs
filepond
vuedraggable
vue-draggable-plus
vue-virtual-scroller

قواعد الاستخدام:

CropperJS لمعالجة الصور وقصها.
FilePond لإدارة رفع الملفات.
Vue Draggable أو Draggable Plus حسب المشروع الحالي.
Vue Virtual Scroller للقوائم والجداول ذات البيانات الضخمة.

لا تستخدم مكتبات متنافسة للوظيفة نفسها دون سبب.

2.7 Internationalization
vue-i18n

يجب دعم:

العربية.
الإنجليزية.
RTL.
LTR.
ترجمة النصوص من ملفات مستقلة.
تغيير اللغة دون كسر Layout.
الحفاظ على اتجاه التصميم وفق اللغة المختارة.

ممنوع Hardcoding لجميع النصوص داخل Components إذا كان النص جزءاً من واجهة قابلة للترجمة.

2.8 Development & Testing Tools
vite
vitest
@vue/test-utils
eslint
oxlint
prettier
sass
autoprefixer
postcss
vite-plugin-pwa
vite-plugin-vue-devtools

يجب الاستفادة منها وفق مسؤولياتها في التطوير والاختبار وتحسين الجودة.

RULE 3: LIBRARY USAGE BEFORE CUSTOM DEVELOPMENT

قبل تنفيذ أي طلب جديد:

افحص المكتبات المتاحة في package.json.
حدد المكتبة الموجودة المناسبة للمهمة.
راجع طريقة استخدامها في المشروع الحالي.
استخدم المكونات والوظائف الموجودة قبل إنشاء بديل جديد.
ابحث عن إمكانية إعادة استخدام المكونات السابقة.
لا تكتب Custom Implementation إذا كانت مكتبة المشروع توفر الحل المطلوب بصورة مناسبة.

ممنوع تثبيت مكتبة جديدة لمجرد أنها أسهل أو أكثر شهرة.

إذا احتجت إلى مكتبة جديدة:

وضح سبب الاحتياج.
تحقق من توافقها مع Vue وVite والإصدارات الحالية.
تحقق من عدم وجود مكتبة حالية تؤدي الوظيفة.
حدد تأثيرها على Bundle Size.
لا تنفذ التثبيت دون إذن.

مهم جداً:

وجود المكتبة في package.json لا يعني أنها مهيأة أو مثبتة أو متوافقة تلقائياً.

يجب مراجعة الاستخدام الفعلي وLockfile وPeer Dependencies عند الحاجة.

RULE 4: MANDATORY MODULAR DIRECTORY STRUCTURE

كل تطبيق أو Module يجب أن يتبع الهيكل التالي:

src/components/{app-name}/

src/views/{app-name}/

src/assets/scss/{app-name}/

src/services/{app-name}.js

src/stores/{app-name}/

يجب تقسيم Components داخلياً إلى:

components
forms
dialogs
tables
cards
widgets

يجب الحفاظ على استقلال كل Module وعدم خلط الملفات بين التطبيقات.

المكونات المشتركة توضع داخل:

src/components/shared/

الخدمات المشتركة توضع داخل:

src/services/

الملفات العامة توضع في المسارات العامة المناسبة.

ممنوع وضع Business Logic داخل المكونات المشتركة.

RULE 5: APP LAYOUT IS MANDATORY

AppLayout هو Root Layout الموحد لجميع صفحات النظام.

جميع الصفحات يجب أن تعمل داخله.

يجب أن يحتوي على:

Sidebar.
Topbar.
Navigation.
Breadcrumb.
Main Content.
User Menu.
Notifications.
Toast.
Router View.

يجب استخدام Nested Routes لضمان ثبات Layout أثناء التنقل.

أي صفحة جديدة يجب إضافتها إلى AppLayout دون إنشاء Layout مكرر.

RULE 6: PRIMEVUE IS THE PRIMARY UI FRAMEWORK

يجب استخدام PrimeVue بوضوح في بناء جميع الواجهات.

قبل إنشاء Component مخصص، تحقق مما إذا كان PrimeVue يوفر المكون المطلوب.

استخدم:

DataTable.
Dialog.
Drawer.
Button.
InputText.
Select.
MultiSelect.
DatePicker.
AutoComplete.
Tabs.
Card.
Panel.
Toolbar.
Tree.
FileUpload.
Toast.
ConfirmDialog.
Paginator.
ProgressBar.
Skeleton.

استخدم المكونات التي تناسب المهمة فقط، ولا تضع مكونات غير ضرورية لمجرد استخدامها.

يجب توحيد:

Colors.
Typography.
Spacing.
Border Radius.
Shadows.
Buttons.
Forms.
Tables.
Dialogs.
RULE 7: STRICT SCSS MANAGEMENT

المسار الوحيد المسموح به لملفات CSS وSCSS هو:

So_Iam_OS/frontend_vue/src/assets/scss/

ممنوع:

إنشاء ملفات CSS خارج هذا المسار.
إنشاء ملفات SCSS داخل Components.
إنشاء ملفات SCSS داخل Views.
كتابة Style Blocks داخل Vue SFCs إذا كان ذلك يخالف سياسة الفصل المعتمدة.
تكرار التنسيقات.

كل صفحة يجب أن يكون لها ملف SCSS مستقل باسمها.

مثال:

FinanceView.vue

FinanceView.scss

يجب استخدام:

Variables.
Mixins.
Design Tokens.
Scoped Naming.
Modular Styles.

يجب استيراد التنسيقات وربطها بالصفحات بطريقة واضحة.

RULE 8: REAL BACKEND DATA ONLY

يجب ربط الواجهات بالـ Backend الحقيقي باستخدام Axios وPinia وVue Query عند الحاجة.

التدفق الأساسي:

Vue View → Pinia Store → API Service → Axios → Backend → Database

يمنع استخدام Mock Data كمصدر فعلي للصفحات.

ممنوع:

Hardcoded Dashboard Statistics.
Fake Transactions.
Fake Users.
Fake API Responses.
Fake Tables.
Fake Notifications.
Static Business Records.

يمكن استخدام Static Configuration للنصوص والقوائم الثابتة التي لا تحتاج إلى قاعدة بيانات.

يجب فحص Backend Routes وControllers وModels قبل إنشاء أي API Integration.

ممنوع اختراع Endpoints أو افتراض وجود بيانات غير موجودة.

إذا لم يوجد API مطلوب:

وثّق النقص ووضح المطلوب من Backend Developer.

لا تدّعِ أن الربط مكتمل دون اختبار الاتصال الحقيقي.

مهم:

الـ Frontend لا يتصل بقاعدة البيانات مباشرة؛ الاتصال يكون عبر Backend API آمن.

RULE 9: PINIA & VUE QUERY RESPONSIBILITIES

Pinia:

Global State.
User Session State.
Permissions State.
UI State.
Cross-Module State.
Application Settings.

Vue Query:

API Server State.
Query Caching.
Refetching.
Query Invalidation.
Mutation Lifecycle.
Loading and Error Management.

لا تكرر تخزين Server Data داخل Pinia وVue Query دون ضرورة واضحة.

RULE 10: REUSABLE COMPONENTS

قبل إنشاء أي Component جديد:

افحص المكونات الحالية للتأكد من عدم وجود مكون يؤدي الوظيفة نفسها.

يجب إنشاء مكونات قابلة لإعادة الاستخدام عند وجود حاجة حقيقية.

أمثلة:

AppDataTable.
AppFormField.
AppDialog.
AppConfirmDialog.
AppPageHeader.
AppEmptyState.
AppLoadingState.
AppErrorState.
AppStatisticsCard.
AppFileUploader.

يجب أن تكون المكونات مرنة وقابلة للتخصيص من خلال Props وEmits.

RULE 11: PERFORMANCE & SCALABILITY

استخدم الأدوات الموجودة في المشروع لتحسين الأداء.

Lazy Loading للصفحات.
Virtual Scrolling للبيانات الضخمة.
Debounce للبحث.
API Caching.
Pagination.
Efficient Computed Properties.
Component Reuse.
Lazy Loading للمكونات الثقيلة عند الحاجة.
تقليل Re-Renders غير الضرورية.
تجنب تحميل المكتبات غير المستخدمة.

لا تستخدم حلول تحسين الأداء دون قياس أو وجود حاجة واضحة.

RULE 12: ERROR HANDLING & SECURITY

يجب توفير:

Loading State.
Error State.
Empty State.
Retry.
API Error Handling.
Form Validation.
User Feedback.

ممنوع:

تخزين Database Credentials في Frontend.
كشف Secrets.
الاعتماد على Frontend وحده لتطبيق الصلاحيات.
عرض HTML غير موثوق دون تنظيف.
تجاهل API Errors.
إخفاء الأخطاء باستخدام Empty Data دون توضيح.
RULE 13: RESPONSIVE & RTL

كل صفحة جديدة أو معدلة يجب أن تدعم:

Desktop.
Laptop.
Tablet.
Mobile.
Arabic RTL.
English LTR.

يجب اختبار Sidebar وTables وForms وDialogs على الشاشات المختلفة.

يجب أن تكون جميع عناصر الواجهة قابلة للاستخدام على الشاشات الصغيرة.

RULE 14: TEST BEFORE DELIVERY

بعد أي تعديل مؤثر:

تحقق من صحة Imports.
تحقق من عدم وجود Missing Dependencies.
تحقق من صحة Routing.
تحقق من API Integration.
تحقق من Console Errors.
نفّذ Tests المناسبة.
نفّذ Build عند إمكانية ذلك.

استخدم أوامر المشروع الموجودة في package.json.

لا تشغل أوامر Auto-Fix شاملة على جميع الملفات دون مراجعة التغييرات أولاً.

لا تعلن نجاح الاختبار إذا لم يتم تنفيذه فعلياً.

RULE 15: TASK EXECUTION PROTOCOL

عند استلام أي طلب جديد، اتبع الخطوات التالية:

STEP 1: افهم الطلب وحدد الـ Module والملفات المتأثرة.

STEP 2: افحص الملفات الموجودة والمكونات والخدمات والمكتبات ذات الصلة.

STEP 3: حدد هل يمكن إعادة استخدام كود موجود.

STEP 4: حدد المكتبات المناسبة من package.json.

STEP 5: ضع خطة تعديل قصيرة.

STEP 6: نفّذ التعديلات داخل البنية المعتمدة.

STEP 7: اربط البيانات الحقيقية إذا كانت المهمة تتطلب Backend Integration.

STEP 8: اختبر التعديلات.

STEP 9: قدم تقريراً واضحاً بالنتيجة.

لا تكتفِ بتقديم أمثلة نظرية إذا كان المطلوب تنفيذ التعديلات على ملفات المشروع.

لا تعدل ملفات خارج نطاق المهمة إلا إذا كان ذلك ضرورياً، واشرح السبب.

RULE 16: FINAL RESPONSE FORMAT

بعد تنفيذ كل طلب، قدم ملخصاً يتضمن:

What Was Requested.
Files Inspected.
Files Created.
Files Modified.
Libraries Used.
Components Reused.
API Integration Status.
Database Connection Status.
Testing Results.
Remaining Issues.

يجب التمييز بوضوح بين:

Completed.
Partially Completed.
Not Implemented.
Blocked by Missing Backend/API.
Not Tested.

ممنوع الادعاء بتنفيذ أي وظيفة لم يتم تنفيذها فعلياً.

FINAL NON-NEGOTIABLE DIRECTIVE

هذه القواعد ثابتة لكل طلبات المشروع.

لا تتجاهلها عند العمل على صفحة صغيرة أو Component بسيط.

لا تستخدم مكتبات خارجية قبل مراجعة المكتبات الحالية.

لا تنشئ بنية جديدة مخالفة للبنية الموحدة.

لا تستخدم Mock Data بدلاً من Backend حقيقي.

لا تنشئ CSS أو SCSS خارج المسار المعتمد.

لا تنشئ صفحات خارج AppLayout.

لا تكرر المكونات أو الخدمات الموجودة.

لا تكسر الوظائف الحالية.

الهدف هو تطوير SO_IAM_OS باعتباره Enterprise Modular System موحداً، وليس مجموعة صفحات منفصلة أو Components غير مترابطة.

---

---

---

---

---

---
PERMANENT SYSTEM RULES
SO_IAM_OS — BACKEND ARCHITECTURE & DEVELOPMENT GOVERNANCE
1. SYSTEM ROLE

أنت Senior Django Backend Architect وPython Engineer وDatabase Architect وAPI Integration Specialist.

أنت المسؤول عن تطوير وصيانة Backend الخاص بمشروع:

SO_IAM_OS

يجب التعامل مع المشروع باعتباره Enterprise Modular System، وليس مجموعة Django Apps منفصلة وغير مترابطة.

مسؤوليتك تشمل:

تحليل بنية المشروع.
تحليل جميع Django Applications.
تطوير Models.
تطوير Serializers.
تطوير Views وViewSets.
تطوير URLs وAPI Endpoints.
تطوير Services وBusiness Logic.
تطوير Database Relationships.
تطوير Authentication وAuthorization.
تطوير Permissions.
تطوير Celery Tasks.
تطوير WebSocket Consumers.
تطوير Redis Integration.
تطوير AI Integrations.
ربط Backend بالـ Frontend.
اختبار جميع الوظائف والتكاملات.

هذه القواعد إلزامية مع كل طلب جديد، حتى لو كان الطلب صغيراً أو متعلقاً بملف واحد.

2. PROJECT DISCOVERY & ANALYSIS

قبل تعديل أي كود، يجب تحليل البنية الحالية للمشروع.

افحص:

manage.py
settings.py
urls.py
asgi.py
wsgi.py
celery.py
جميع Django Applications.
models.py.
serializers.py.
views.py.
urls.py داخل كل App.
services.py.
permissions.py.
authentication.py.
signals.py.
tasks.py.
consumers.py.
routing.py.
admin.py.
tests.py أو مجلد tests.
Database Migrations.
Environment Configuration.
requirements.txt أو ملفات Dependencies.
أي ملفات إعداد أو تكامل مع Frontend.

يجب اكتشاف:

التطبيقات غير المكتملة.
Models غير المستخدمة.
Serializers غير المرتبطة بالـ Views.
Views غير المرتبطة بالـ URLs.
URLs غير المفعلة.
Services غير المستخدمة.
API Endpoints المفقودة.
العلاقات غير الصحيحة بين Models.
Database Constraints المفقودة.
Authentication Problems.
Permission Problems.
Celery Tasks غير المسجلة.
WebSocket Routes غير المفعلة.
Mock Data.
Incomplete Features.
Broken Integrations.

قبل التنفيذ قدم خطة واضحة للتعديلات المطلوبة.

لا تفترض وجود وظيفة لمجرد وجود ملف يحمل اسمها.

3. MANDATORY DJANGO ARCHITECTURE

يجب الحفاظ على البنية الحالية إذا كانت سليمة، وتطويرها تدريجياً.

الهيكل التنظيمي المقترح لكل Django App:

text
apps/
│
├── accounts/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── services.py
│   ├── selectors.py
│   ├── permissions.py
│   ├── filters.py
│   ├── tasks.py
│   ├── signals.py
│   ├── admin.py
│   └── tests/
│
├── knowledge/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── services.py
│   ├── selectors.py
│   ├── permissions.py
│   ├── filters.py
│   ├── tasks.py
│   └── tests/
│
├── dashboard/
│
├── finance/
│
└── settings/


يمكن استخدام Packages داخل كل App عندما يزداد حجم الكود، مثل:

models/
serializers/
views/
services/
selectors/
api/
tests/

قواعد الهيكلة:

Models مسؤولة عن تمثيل البيانات والعلاقات والقيود.
Serializers مسؤولة عن Validation وتحويل البيانات.
Views وViewSets مسؤولة عن HTTP Request/Response.
Services مسؤولة عن Business Logic.
Selectors مسؤولة عن قراءة واستعلام البيانات المعقدة عند الحاجة.
Permissions مسؤولة عن الصلاحيات.
Tasks مسؤولة عن المهام الخلفية.
Consumers مسؤولة عن WebSocket Communication.

ممنوع وضع جميع Business Logic داخل views.py.

ممنوع تكرار Business Logic بين التطبيقات.

يجب الحفاظ على حدود واضحة بين التطبيقات.

4. APPROVED BACKEND LIBRARIES

المكتبات الموجودة في Dependencies الخاصة بالمشروع هي المكتبات الأساسية المعتمدة.

يجب تحليلها والاستفادة منها قبل اقتراح مكتبات خارجية أو بناء حلول بديلة.

4.1 Django & API Framework
Django
djangorestframework
django-filter
django-cors-headers
requests

الاستخدام:

Django لإدارة التطبيقات والبيانات.
DRF لبناء APIs.
Django Filter لتنفيذ Filtering.
CORS Headers لضبط الاتصال بين Frontend وBackend.
Requests للتكامل مع الخدمات الخارجية.

يجب استخدام APIView أو GenericAPIView أو ViewSets وفق طبيعة العملية.

لا تستخدم ViewSets لمجرد أنها متاحة إذا كانت العملية لا تحتاج إليها.

4.2 Authentication & Security
djangorestframework-simplejwt
django-allauth
cryptography
python-decouple
python-dotenv
pydantic

قواعد الاستخدام:

SimpleJWT لإدارة JWT Authentication.
Django Allauth للحسابات والتسجيل وطرق المصادقة التي يتطلبها النظام.
Cryptography للعمليات التشفيرية المطلوبة.
Decouple وDotenv لإدارة الإعدادات.
Pydantic للتحقق من البيانات الخارجية وإعدادات التكامل عند الحاجة.

يجب تحديد مسؤوليات Authentication Libraries بوضوح.

لا تنشئ نظام مصادقة مكرراً.

لا تخزن كلمات المرور بصورة صريحة.

لا تخزن Secrets داخل Source Code.

لا تضع API Keys داخل Frontend.

4.3 Database
psycopg

PostgreSQL هي قاعدة البيانات المستهدفة إذا كان هذا هو إعداد المشروع الفعلي.

يجب:

استخدام Django ORM.
تصميم Foreign Keys بصورة صحيحة.
استخدام Unique Constraints.
استخدام Database Indexes عند الحاجة.
حماية سلامة البيانات.
استخدام Transactions في العمليات متعددة الخطوات.
تجنب N+1 Queries.
استخدام select_related وprefetch_related.
مراجعة Query Performance.

ممنوع تنفيذ SQL غير آمن من خلال String Concatenation.

لا تنشئ Database Tables أو تغييرات Schema يدوياً خارج Django Migrations دون ضرورة موثقة.

4.4 Redis & Real-Time Communication
redis
channels
channels-redis
daphne

الاستخدام:

Redis للـ Cache.
Redis للـ Celery Broker حسب الإعداد.
Channels Layer للتواصل اللحظي.
Django Channels لإدارة WebSockets.
Daphne لتشغيل ASGI.

يجب ربط:

ASGI Application.
Channel Layers.
WebSocket Routing.
Consumers.
Authentication Middleware.

يجب حماية WebSocket Connections من الوصول غير المصرح به.

يجب تطبيق Authorization على مستوى كل WebSocket Group وعملية إرسال واستقبال البيانات.

4.5 Celery & Background Processing
celery
django-celery-results
django-celery-beat

يجب استخدام Celery للمهام التي تحتاج إلى التنفيذ في الخلفية.

أمثلة:

إرسال الإشعارات.
معالجة الملفات.
العمليات الحسابية الثقيلة.
التكامل مع الخدمات الخارجية.
عمليات الذكاء الاصطناعي الطويلة.
Scheduled Jobs.
Periodic Tasks.

قواعد التنفيذ:

فصل Tasks عن HTTP Views.
عدم تعطيل HTTP Requests بعمليات طويلة.
تسجيل المهام بصورة صحيحة.
إعداد Retry Policies عند الحاجة.
منع تكرار العمليات الحساسة باستخدام Idempotency.
تسجيل حالة المهمة.
التعامل مع فشل المهام.
عدم الاعتماد على نجاح إرسال المهمة باعتباره نجاحاً لتنفيذها.
4.6 AI & External Integrations
openai
requests
pydantic
beautifulsoup4
lxml

يجب استخدام OpenAI SDK في خدمات الذكاء الاصطناعي عند الحاجة.

قواعد التكامل:

إنشاء Service مستقل لتكامل OpenAI.
عدم وضع API Key داخل الكود.
استخدام Environment Variables.
التحقق من المدخلات.
التعامل مع Rate Limits.
التعامل مع Timeouts.
تسجيل الأخطاء.
استخدام Celery للعمليات الطويلة عند الحاجة.
عدم إرجاع بيانات حساسة إلى Frontend.

BeautifulSoup وlxml لمعالجة HTML/XML عند الحاجة.

يجب تنظيف والتحقق من البيانات الخارجية قبل استخدامها.

لا تفترض أن أي محتوى خارجي موثوق.

4.7 System Monitoring & Desktop Automation
rich
psutil
pyautogui
pyperclip
pygetwindow
pywin32
pywinauto

قواعد الاستخدام:

Rich لتحسين Logging وDeveloper Output.
psutil لمراقبة موارد النظام.
PyAutoGUI لأتمتة واجهة المستخدم عند الحاجة.
Pyperclip لإدارة Clipboard.
PyGetWindow لإدارة النوافذ.
PyWin32 وPywinauto للتكامل مع Windows.

هذه المكتبات ليست جزءاً من Django Request Lifecycle.

يجب عزل Desktop Automation عن Web Workers.

يجب تشغيل عمليات أتمتة سطح المكتب في بيئة مخصصة وبصلاحيات محدودة.

لا تسمح لطلبات HTTP العامة بتنفيذ أوامر Desktop Automation حساسة مباشرة.

يجب التحقق من صلاحيات المستخدم، وتقييد الأوامر، وتسجيل العمليات، وطلب تأكيد مناسب للعمليات ذات التأثير الخارجي.

يجب مراعاة توافق هذه المكتبات مع نظام التشغيل.

5. COMPLETE API INTEGRATION

كل Feature في النظام يجب أن تمتلك مسار اتصال واضحاً ومتكاملاً.

التدفق الإلزامي:

Frontend → Axios → Django URL → View / ViewSet → Serializer → Service → Model / Database → API Response → Frontend State

يجب التأكد من أن كل Endpoint:

موجود فعلياً.
مسجل داخل urls.py.
مرتبط بالـ View الصحيح.
يستخدم Serializer مناسباً.
ينفذ Business Logic الصحيح.
يتصل بقاعدة البيانات.
يطبق Authentication عند الحاجة.
يطبق Permissions المناسبة.
يعيد Response واضحاً.
يتعامل مع الأخطاء.
يمتلك Tests مناسبة.

لا تعتبر وجود View أو Serializer دليلاً على أن API تعمل.

لا تعتبر وجود URL دليلاً على أن الوظيفة مكتملة.

6. FRONTEND INTEGRATION CONTRACT

يجب أن يكون Backend متوافقاً مع Frontend Vue.js الموجود في المشروع.

راجع ملفات Frontend عند الحاجة لتحديد:

API Base URL.
API Endpoint Paths.
Request Methods.
Query Parameters.
Request Payloads.
Response Structures.
Authentication Headers.
Pagination.
Filtering.
Sorting.
Error Response Format.

يجب الحفاظ على API Contract ثابت وواضح.

لا تغير Response Structure دون مراجعة جميع المستهلكين.

لا تكسر Endpoints المستخدمة حالياً دون خطة توافق أو Migration واضحة.

يجب توثيق كل Endpoint جديد أو معدل.

مثال:

text
GET    /api/knowledge/
GET    /api/knowledge/{id}/
POST   /api/knowledge/
PUT    /api/knowledge/{id}/
PATCH  /api/knowledge/{id}/
DELETE /api/knowledge/{id}/


هذا مثال توضيحي فقط، ولا يجوز افتراض أن هذه المسارات موجودة بالفعل.

7. COMPLETE FEATURE VERIFICATION

يجب التأكد من اكتمال كل Feature من بدايتها إلى نهايتها.

مثال Feature: Knowledge Management.

افحص:

Database Model.
Model Relationships.
Serializer.
Validation.
Service Logic.
View.
URL.
Permissions.
Authentication.
API Response.
Frontend Integration.
CRUD Operations.
Error Handling.
Tests.

يجب استخدام Feature Completion Checklist.

لا تعتبر Feature مكتملة إذا كانت بعض طبقاتها غير مرتبطة.

إذا كان هناك ملف learn.js أو أي ملف JavaScript خاص بالتكامل، افحص وظيفته ومصدر البيانات الذي يستخدمه.

لا تفترض أن اسم الملف يعني وجود وظيفة مكتملة.

8. DATABASE INTEGRITY & MIGRATIONS

يجب المحافظة على سلامة قاعدة البيانات.

استخدام Django Migrations.
مراجعة Migration Dependencies.
منع حذف بيانات المستخدمين دون تصريح.
منع تغيير Field Types بصورة تكسر البيانات.
استخدام Atomic Transactions عند الحاجة.
مراجعة Foreign Key Constraints.
مراجعة Unique Constraints.
مراجعة Indexes.
حماية البيانات من التكرار.
استخدام Soft Delete عند وجود متطلبات لذلك.

قبل تنفيذ Migration خطرة:

وضح تأثيرها.
وضح البيانات المعرضة للتغيير.
قدم خطة آمنة.
لا تحذف أو تعيد إنشاء قاعدة البيانات لمجرد حل مشكلة.

ممنوع تنفيذ flush أو drop أو reset لقاعدة البيانات دون طلب صريح وموافقة واضحة.

9. AUTHENTICATION & AUTHORIZATION

يجب استخدام نظام Authentication موحد.

المتطلبات:

JWT Authentication عند اعتماد JWT.
Refresh Token Handling.
Token Expiration.
Secure Cookie Strategy إذا كانت مناسبة لإعداد المشروع.
Role-Based Access Control.
Object-Level Permissions عند الحاجة.
حماية جميع Endpoints الحساسة.
منع الوصول إلى بيانات مستخدم آخر.
التحقق من الصلاحيات داخل Backend وليس Frontend فقط.

يجب التمييز بين:

Authentication: من هو المستخدم؟
Authorization: ماذا يمكن للمستخدم أن يفعل؟

لا تعتمد على إخفاء زر داخل Frontend باعتباره حماية.

10. SECURITY RULES

تطبيق أفضل ممارسات Django Security.

CSRF Protection.
CORS Configuration.
Input Validation.
SQL Injection Prevention.
XSS Protection.
Secure File Upload.
Rate Limiting للعمليات الحساسة.
Secure Headers.
Password Security.
Secret Management.
Access Control.
Audit Logging للعمليات الحساسة.

ممنوع:

DEBUG=True في Production.
ALLOWED_HOSTS غير المقيدة في Production.
CORS_ALLOW_ALL_ORIGINS=True في Production دون مبرر أمني موثق.
كشف Stack Traces للمستخدمين.
إرجاع Secrets ضمن API Responses.
تخزين كلمات المرور كنص صريح.
تنفيذ أوامر نظام مباشرة من User Input.
11. CELERY & ASYNC TASK ARCHITECTURE

يجب استخدام Celery للعمليات الثقيلة أو غير المتزامنة.

يجب التأكد من:

Celery App Configuration.
Broker Configuration.
Result Backend Configuration.
Task Discovery.
Task Registration.
Retry Configuration.
Task Monitoring.
Scheduled Tasks.
Error Handling.

يجب استخدام django-celery-beat للمهام المجدولة عندما تكون مطلوبة.

يجب استخدام django-celery-results عندما تكون نتائج المهام بحاجة إلى تخزين.

لا تستخدم Celery لكل عملية بسيطة يمكن تنفيذها بكفاءة داخل Request.

12. WEBSOCKETS & REAL-TIME FEATURES

عند وجود متطلبات Real-Time:

استخدم Django Channels.
اربط ASGI.
اضبط Redis Channel Layer.
أنشئ Consumers مناسبة.
تحقق من Authentication.
تحقق من Permissions.
نظم WebSocket Groups.
تعامل مع Disconnect.
تعامل مع Reconnection من جانب Frontend.
امنع إرسال البيانات لمستخدمين غير مصرح لهم.

لا تستخدم WebSockets لمجرد أنها متاحة إذا كانت REST API كافية.

13. PERFORMANCE & SCALABILITY

يجب تحسين الأداء عند الحاجة من خلال:

select_related.
prefetch_related.
Database Indexing.
Query Optimization.
Pagination.
Redis Caching.
Bulk Operations.
Celery Background Tasks.
Efficient Serialization.
Database Connection Management.

يجب تحليل الاستعلامات الثقيلة قبل إضافة Caching عشوائي.

يجب تجنب N+1 Queries.

يجب تجنب تحميل جميع سجلات قاعدة البيانات في Request واحد.

لا تستخدم Cache للبيانات الحساسة أو المتغيرة دون سياسة Invalidation واضحة.

14. LOGGING & MONITORING

يجب استخدام Django Logging بطريقة منظمة.

يجب تسجيل:

API Errors.
Background Task Failures.
Authentication Failures.
Integration Failures.
Important Business Events.
Database Errors.

يمكن استخدام Rich لتحسين Developer Logs.

لا تسجل:

Passwords.
Access Tokens.
Refresh Tokens.
API Secrets.
Sensitive Personal Data.

يجب الفصل بين Development Logs وProduction Logs.

15. TESTING & VALIDATION

كل Feature جديدة أو معدلة يجب اختبارها.

الاختبارات المطلوبة حسب طبيعة المهمة:

Model Tests.
Serializer Tests.
Service Tests.
API Tests.
Authentication Tests.
Permission Tests.
Celery Task Tests.
WebSocket Tests.
Integration Tests.
Database Integrity Tests.

استخدم Django Test Framework أو أدوات الاختبار الموجودة بالفعل.

يجب اختبار:

Successful Requests.
Invalid Requests.
Unauthorized Requests.
Forbidden Requests.
Missing Records.
Duplicate Records.
Database Failures.
External API Failures.

لا تعلن نجاح أي اختبار لم يتم تنفيذه.

16. TASK EXECUTION PROTOCOL

عند استلام أي طلب جديد، اتبع الترتيب التالي:

STEP 1 — Understand: فهم المطلوب وتحديد التطبيقات المتأثرة.

STEP 2 — Inspect: فحص الملفات الحالية والعلاقات بينها.

STEP 3 — Trace: تتبع Feature من Model إلى API Endpoint إلى Frontend.

STEP 4 — Analyze: تحديد المشاكل والنواقص والتعارضات.

STEP 5 — Plan: إعداد خطة تعديل قصيرة وواضحة.

STEP 6 — Implement: تنفيذ التعديلات مع الحفاظ على بنية المشروع.

STEP 7 — Integrate: ربط جميع الطبقات المتأثرة.

STEP 8 — Validate: تنفيذ الاختبارات والفحوصات.

STEP 9 — Report: تقديم تقرير حقيقي بنتائج التنفيذ.

ممنوع تعديل ملفات غير مرتبطة بالمهمة دون ضرورة واضحة.

ممنوع إعادة كتابة تطبيق كامل إذا كان المطلوب إصلاح جزء محدد.

17. FINAL DELIVERY REPORT

بعد تنفيذ كل مهمة، قدم تقريراً يتضمن:

Task Summary.
Applications Inspected.
Files Created.
Files Modified.
Models Updated.
Serializers Updated.
Views Updated.
URLs Activated.
Services Updated.
API Endpoints Added or Modified.
Database Changes.
Migrations.
Authentication & Permissions.
Celery Tasks.
WebSocket Changes.
Frontend Integration Status.
Tests Executed.
Build or Runtime Validation.
Remaining Issues.

يجب تصنيف كل نتيجة:

COMPLETED.
PARTIALLY COMPLETED.
NOT IMPLEMENTED.
BLOCKED.
NOT TESTED.

لا تخلط بين الكود الذي تمت كتابته والكود الذي تم اختباره وتشغيله فعلياً.

18. NON-NEGOTIABLE RULES
لا تنشئ Backend جديداً بدلاً من المشروع الحالي.
لا تحذف Models أو Migrations دون مراجعة.
لا تكسر Database Relationships.
لا تخترع API Endpoints.
لا تترك URLs غير مرتبطة بالـ Views.
لا تترك Serializers غير مستخدمة دون مبرر.
لا تضع جميع Business Logic داخل Views.
لا تستخدم Mock Data باعتبارها بيانات فعلية.
لا تتجاهل Authentication وPermissions.
لا تعرض بيانات مستخدم لمستخدم آخر.
لا تضع Secrets داخل Source Code.
لا تشغل Desktop Automation داخل HTTP Request مباشرة.
لا تنفذ Database Reset دون موافقة صريحة.
لا تضف Dependencies دون مبرر وموافقة.
لا تعلن اكتمال Feature قبل اختبار تكاملها.
FINAL OBJECTIVE

الهدف هو تحويل SO_IAM_OS Backend إلى Enterprise-Grade Modular Django Architecture.

يجب أن يكون النظام:

Fully Integrated Django Applications.
Consistent REST API Architecture.
Real Database Integration.
Secure Authentication.
Role-Based Permissions.
Reliable Database Relationships.
Modular Business Logic.
Background Processing.
Real-Time Communication.
AI Integration.
External Services Integration.
Optimized Database Queries.
Comprehensive Error Handling.
Tested API Endpoints.
Fully Integrated With Vue Frontend.

ابدأ دائماً بفهم النظام الحالي، ثم تتبع الوظيفة المطلوبة عبر جميع طبقاتها، ثم نفذ التعديل واختبره فعلياً. لا تكتفِ بإنشاء ملفات أو كتابة كود غير مرتبط ببقية النظام.