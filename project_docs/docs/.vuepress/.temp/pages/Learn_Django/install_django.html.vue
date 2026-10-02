<template><div><h1 id="🐍-django" tabindex="-1"><a class="header-anchor" href="#🐍-django"><span>🐍 Django</span></a></h1>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>Django هو إطار عمل مبني باستخدام Python، وبيستخدم لبناء تطبيقات الويب والـ Backend والـ APIs بطريقة منظمة وقابلة للتوسع.</p>
</div>
<hr>
<h3 id="_1-🎯-purpose" tabindex="-1"><a class="header-anchor" href="#_1-🎯-purpose"><span>1. 🎯 Purpose</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>الهدف من Django هو توفير Framework جاهز يساعدنا في بناء الـ Backend بدل ما نضطر نبني كل مكون من الصفر.</p>
<p>في مشروع So_Iam_OS، Django هو الـ Framework الأساسي المسؤول عن الـ Backend.</p>
</div>
<hr>
<h3 id="_2-🧠-concept" tabindex="-1"><a class="header-anchor" href="#_2-🧠-concept"><span>2. 🧠 Concept</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>Django مبني باستخدام Python، وبيوفر لنا مجموعة من الأدوات والمكونات الجاهزة لبناء تطبيقات ويب متكاملة.</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Python</span>
<span class="line">   ↓</span>
<span class="line">Django</span>
<span class="line">   ↓</span>
<span class="line">Backend</span>
<span class="line">   ↓</span>
<span class="line">Django Project</span>
<span class="line">   ↓</span>
<span class="line">Django Apps</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h3 id="_3-🔧-requirements" tabindex="-1"><a class="header-anchor" href="#_3-🔧-requirements"><span>3. 🔧 Requirements</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>قبل تثبيت Django، لازم يكون Python وpip موجودين، ويفضل تشغيل الـ Virtual Environment الخاصة بالمشروع.</p>
</div>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">python --version</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip --version</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><hr>
<h3 id="_4-🛠️-installation-setup" tabindex="-1"><a class="header-anchor" href="#_4-🛠️-installation-setup"><span>4. 🛠️ Installation / Setup</span></a></h3>
<h4 id="🔧-install-django" tabindex="-1"><a class="header-anchor" href="#🔧-install-django"><span>🔧 Install Django</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>لتثبيت Django داخل البيئة الافتراضية الحالية:</p>
</div>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip install django</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><hr>
<h4 id="🦄-version" tabindex="-1"><a class="header-anchor" href="#🦄-version"><span>🦄 Version</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>لمعرفة إصدار Django المثبت حاليًا:</p>
</div>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">python -m django --version</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h3 id="📦-upgrade" tabindex="-1"><a class="header-anchor" href="#📦-upgrade"><span>📦 Upgrade</span></a></h3>
<h6 id="📦-upgrade-django-if-necessary" tabindex="-1"><a class="header-anchor" href="#📦-upgrade-django-if-necessary"><span>📦 Upgrade Django ( If Necessary )</span></a></h6>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">pip install -U Django</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><hr>
<h3 id="_5-🚀-usage" tabindex="-1"><a class="header-anchor" href="#_5-🚀-usage"><span>5. 🚀 Usage</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>بعد تثبيت Django، نقدر نستخدم أدوات الـ Command Line الخاصة به لإدارة المشروع وتنفيذ الأوامر المختلفة.</p>
</div>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">django-admin</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">django-admin help</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><hr>
<h3 id="_6-📁-structure" tabindex="-1"><a class="header-anchor" href="#_6-📁-structure"><span>6. 📁 Structure</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>بعد إنشاء مشروع Django، بيكون عندنا مجموعة من الملفات والمجلدات الأساسية التي تمثل هيكل المشروع.</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">backend_django/</span>
<span class="line">│</span>
<span class="line">├── manage.py</span>
<span class="line">│</span>
<span class="line">└── backend_django/</span>
<span class="line">    ├── settings.py</span>
<span class="line">    ├── urls.py</span>
<span class="line">    ├── asgi.py</span>
<span class="line">    └── wsgi.py</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h3 id="_7-🧩-important-concepts" tabindex="-1"><a class="header-anchor" href="#_7-🧩-important-concepts"><span>7. 🧩 Important Concepts</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>من أهم المفاهيم اللي لازم نفهمها في Django: Project وApp وmanage.py وdjango-admin، لأن كل واحد منهم له دور مختلف داخل المشروع.</p>
</div>
<hr>
<h3 id="_8-💻-examples" tabindex="-1"><a class="header-anchor" href="#_8-💻-examples"><span>8. 💻 Examples</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>تثبيت Django:</p>
</div>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip install django</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>معرفة الإصدار:</p>
</div>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">python -m django --version</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><hr>
<h3 id="_9-❌-common-mistakes" tabindex="-1"><a class="header-anchor" href="#_9-❌-common-mistakes"><span>9. ❌ Common Mistakes</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>من الأخطاء الشائعة تثبيت Django خارج الـ Virtual Environment أو تحديث Django بدون التأكد من توافق الإصدار الجديد مع المشروع.</p>
</div>
<hr>
<h3 id="_10-🧠-why" tabindex="-1"><a class="header-anchor" href="#_10-🧠-why"><span>10. 🧠 Why?</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>بنستخدم Virtual Environment علشان نعزل مكتبات المشروع عن باقي مشاريع Python الموجودة على الجهاز.</p>
<p>وبنستخدم Django لأنه يوفر لنا بنية وأدوات جاهزة لبناء Backend منظم وقابل للتوسع.</p>
</div>
<hr>
<h3 id="_11-🔗-project-usage" tabindex="-1"><a class="header-anchor" href="#_11-🔗-project-usage"><span>11. 🔗 Project Usage</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>Django هو الـ Backend Framework المستخدم في مشروع So_Iam_OS، وهيكون مسؤول عن بناء الـ APIs والـ Business Logic والـ Applications الخاصة بالنظام.</p>
</div>
<hr>
<h3 id="_12-🤖-ai-reference" tabindex="-1"><a class="header-anchor" href="#_12-🤖-ai-reference"><span>12. 🤖 AI Reference</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>عند التعامل مع مشروع So_Iam_OS، اعتبر Django هو الـ Backend Framework الأساسي.</p>
<p>يجب عدم افتراض إصدار Django بدون التحقق منه.</p>
<p>يجب مراعاة الـ Virtual Environment والـ Dependencies قبل تنفيذ أوامر التثبيت أو التحديث.</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Project:</span>
<span class="line">So_Iam_OS</span>
<span class="line"></span>
<span class="line">Backend:</span>
<span class="line">Django</span>
<span class="line"></span>
<span class="line">Backend Path:</span>
<span class="line">backend_django</span>
<span class="line"></span>
<span class="line">Environment:</span>
<span class="line">Virtual Environment</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h3 id="_13-📊-current-status" tabindex="-1"><a class="header-anchor" href="#_13-📊-current-status"><span>13. 📊 Current Status</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>الحالة الحالية توضح إيه اللي تم تنفيذه وإيه اللي لسه محتاج تنفيذ داخل المشروع.</p>
</div>
<table>
<thead>
<tr>
<th>Task</th>
<th>Status</th>
</tr>
</thead>
<tbody>
<tr>
<td>Python</td>
<td>✅</td>
</tr>
<tr>
<td>Virtual Environment</td>
<td>✅</td>
</tr>
<tr>
<td>Django Installation</td>
<td>✅</td>
</tr>
<tr>
<td>Django Project</td>
<td>⬜</td>
</tr>
<tr>
<td>Django Apps</td>
<td>⬜</td>
</tr>
</tbody>
</table>
<hr>
<h3 id="_14-✅-checklist" tabindex="-1"><a class="header-anchor" href="#_14-✅-checklist"><span>14. ✅ Checklist</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>قائمة مراجعة للتأكد من تنفيذ خطوات إعداد Django بالترتيب الصحيح.</p>
</div>
<ul>
<li>[x] Python</li>
<li>[x] Virtual Environment</li>
<li>[x] Install Django</li>
<li>[x] Check Django Version</li>
<li>[ ] Create Django Project</li>
<li>[ ] Create Django Apps</li>
</ul>
<hr>
<h3 id="_15-🔗-related-documentation" tabindex="-1"><a class="header-anchor" href="#_15-🔗-related-documentation"><span>15. 🔗 Related Documentation</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>الملفات المرتبطة بموضوع Django تشمل Python وVirtual Environment وpip وDjango Apps وDatabase وAPI وAuthentication.</p>
</div>
<hr>
<h3 id="_16-📝-notes" tabindex="-1"><a class="header-anchor" href="#_16-📝-notes"><span>16. 📝 Notes</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>أي ملاحظات أو تجارب جديدة مرتبطة بـ Django يتم إضافتها هنا للحفاظ على المعرفة وتحديثها باستمرار.</p>
</div>
<h4 id="👉️-go-to-project-path-like-cd-backend-django" tabindex="-1"><a class="header-anchor" href="#👉️-go-to-project-path-like-cd-backend-django"><span>👉️ Go To Project Path Like [cd backend_django]</span></a></h4>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">cd backend_django</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">python manage.py</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div></div></template>


