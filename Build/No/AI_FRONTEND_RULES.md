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
