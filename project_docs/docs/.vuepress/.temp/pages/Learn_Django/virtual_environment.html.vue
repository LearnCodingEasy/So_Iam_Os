<template><div><h1 id="🐍-django-—-virtual-environment" tabindex="-1"><a class="header-anchor" href="#🐍-django-—-virtual-environment"><span>🐍 Django — Virtual Environment</span></a></h1>
<blockquote>
<p>بيئة Python معزولة خاصة بالمشروع، تُستخدم لفصل مكتبات وإصدارات المشروع عن باقي مشاريع Python الموجودة على الجهاز.</p>
</blockquote>
<hr>
<h3 id="_1-🎯-purpose" tabindex="-1"><a class="header-anchor" href="#_1-🎯-purpose"><span>1. 🎯 Purpose</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>الـVirtual Environment بتعمل بيئة مستقلة للمشروع، بحيث مكتبات وإصدارات المشروع ما تتعارضش مع مشاريع Python تانية على الجهاز.</p>
<p>مثال:</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Project A</span>
<span class="line">├── Django 4.x</span>
<span class="line">│</span>
<span class="line">Project B</span>
<span class="line">└── Django 5.x</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>كل مشروع يقدر يشتغل بإصداراته الخاصة بدون تعارض.</p>
</div>
<hr>
<h3 id="_2-🧠-concept" tabindex="-1"><a class="header-anchor" href="#_2-🧠-concept"><span>2. 🧠 Concept</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>بدل ما كل مشاريع Python تستخدم نفس المكتبات الموجودة بشكل Global على الجهاز، بننشئ بيئة خاصة بكل مشروع.</p>
<p>بدون Virtual Environment:</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Computer</span>
<span class="line">│</span>
<span class="line">├── Python</span>
<span class="line">├── Django</span>
<span class="line">├── Requests</span>
<span class="line">└── Other Libraries</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>مع Virtual Environment:</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Project</span>
<span class="line">│</span>
<span class="line">├── venv</span>
<span class="line">│   ├── Scripts</span>
<span class="line">│   ├── Lib</span>
<span class="line">│   └── ...</span>
<span class="line">│</span>
<span class="line">├── manage.py</span>
<span class="line">└── ...</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>الفكرة الأساسية:</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Project</span>
<span class="line">   ↓</span>
<span class="line">Virtual Environment</span>
<span class="line">   ↓</span>
<span class="line">Project Dependencies</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>وبالتالي كل مشروع بيكون عنده مساحة مستقلة للمكتبات والإصدارات الخاصة بيه.</p>
</div>
<hr>
<h3 id="_3-🔧-requirements" tabindex="-1"><a class="header-anchor" href="#_3-🔧-requirements"><span>3. 🔧 Requirements</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>قبل إنشاء البيئة الافتراضية، لازم نتأكد إن Python وpip موجودين على الجهاز.</p>
</div>
<h4 id="🐍-python-version" tabindex="-1"><a class="header-anchor" href="#🐍-python-version"><span>🐍 Python Version</span></a></h4>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">python --version</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><p>أو:</p>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">py --version</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h4 id="📦-pip-version" tabindex="-1"><a class="header-anchor" href="#📦-pip-version"><span>📦 Pip Version</span></a></h4>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip --version</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>كمان يُفضل تنفيذ الخطوات من داخل مجلد المشروع.</p>
</div>
<hr>
<h3 id="_4-🛠️-installation-setup" tabindex="-1"><a class="header-anchor" href="#_4-🛠️-installation-setup"><span>4. 🛠️ Installation / Setup</span></a></h3>
<h4 id="⬆️-upgrade-pip" tabindex="-1"><a class="header-anchor" href="#⬆️-upgrade-pip"><span>⬆️ Upgrade Pip</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>لو محتاج تحدث pip، استخدم:</p>
</div>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">py -m pip install --upgrade pip</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>مش محتاج تثبت virtualenv بشكل منفصل لو هتستخدم الأداة المدمجة في Python وهي venv.</p>
</div>
<h4 id="📦-create-virtual-environment" tabindex="-1"><a class="header-anchor" href="#📦-create-virtual-environment"><span>📦 Create Virtual Environment</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>داخل مجلد المشروع:</p>
</div>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">python -m venv venv</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><p>أو:</p>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">py -m venv venv</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h4 id="🚀-activate-on-windows" tabindex="-1"><a class="header-anchor" href="#🚀-activate-on-windows"><span>🚀 Activate on Windows</span></a></h4>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">venv\Scripts\activate</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>بعد التفعيل، أوامر Python وpip هتتعامل مع البيئة الخاصة بالمشروع بدل البيئة الـGlobal.</p>
</div>
<hr>
<h3 id="_5-🚀-usage" tabindex="-1"><a class="header-anchor" href="#_5-🚀-usage"><span>5. 🚀 Usage</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>بعد إنشاء وتفعيل البيئة الافتراضية، بنستخدمها لتثبيت مكتبات المشروع وتشغيل أوامر Python الخاصة بالمشروع.</p>
</div>
<h4 id="📚-show-installed-libraries" tabindex="-1"><a class="header-anchor" href="#📚-show-installed-libraries"><span>📚 Show Installed Libraries</span></a></h4>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip list</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h4 id="📋-export-dependencies" tabindex="-1"><a class="header-anchor" href="#📋-export-dependencies"><span>📋 Export Dependencies</span></a></h4>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip freeze</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>ويُفضل تسجيل dependencies داخل ملف requirements.txt:</p>
</div>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip freeze &gt; requirements.txt</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h4 id="⛔-deactivate" tabindex="-1"><a class="header-anchor" href="#⛔-deactivate"><span>⛔ Deactivate</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>لإغلاق البيئة الافتراضية:</p>
</div>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">deactivate</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><hr>
<h3 id="_6-📁-structure" tabindex="-1"><a class="header-anchor" href="#_6-📁-structure"><span>6. 📁 Structure</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>بعد إنشاء البيئة الافتراضية، شكل المشروع ممكن يكون كالتالي:</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Project/</span>
<span class="line">│</span>
<span class="line">├── .git/</span>
<span class="line">│</span>
<span class="line">├── venv/</span>
<span class="line">│   ├── Include/</span>
<span class="line">│   ├── Lib/</span>
<span class="line">│   ├── Scripts/</span>
<span class="line">│   │   ├── activate</span>
<span class="line">│   │   └── ...</span>
<span class="line">│   │</span>
<span class="line">│   └── pyvenv.cfg</span>
<span class="line">│</span>
<span class="line">├── .gitignore</span>
<span class="line">├── LICENSE</span>
<span class="line">└── README.md</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>مجلد venv بيحتوي على ملفات البيئة والمكتبات الخاصة بالمشروع، ولذلك لا يتم رفعه إلى Git.</p>
</div>
<hr>
<h3 id="_7-🧩-important-concepts" tabindex="-1"><a class="header-anchor" href="#_7-🧩-important-concepts"><span>7. 🧩 Important Concepts</span></a></h3>
<h4 id="🔹-virtual-environment" tabindex="-1"><a class="header-anchor" href="#🔹-virtual-environment"><span>🔹 Virtual Environment</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>بيئة Python مستقلة عن باقي مشاريع Python.</p>
</div>
<h4 id="🔹-dependency-isolation" tabindex="-1"><a class="header-anchor" href="#🔹-dependency-isolation"><span>🔹 Dependency Isolation</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>عزل مكتبات المشروع وإصداراتها عن المشاريع الأخرى.</p>
</div>
<h4 id="🔹-pip" tabindex="-1"><a class="header-anchor" href="#🔹-pip"><span>🔹 pip</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>أداة Python الأساسية لإدارة وتثبيت packages.</p>
</div>
<h4 id="🔹-requirements-txt" tabindex="-1"><a class="header-anchor" href="#🔹-requirements-txt"><span>🔹 requirements.txt</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>ملف بيتم فيه تسجيل dependencies المطلوبة للمشروع، بحيث يمكن إعادة تجهيز البيئة على جهاز آخر.</p>
</div>
<h4 id="🔹-gitignore" tabindex="-1"><a class="header-anchor" href="#🔹-gitignore"><span>🔹 .gitignore</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>ملف بيحدد الملفات والمجلدات التي لا يجب رفعها إلى Git، ومنها Virtual Environment.</p>
</div>
<hr>
<h3 id="_8-💻-examples" tabindex="-1"><a class="header-anchor" href="#_8-💻-examples"><span>8. 💻 Examples</span></a></h3>
<h4 id="example-1-—-create-environment" tabindex="-1"><a class="header-anchor" href="#example-1-—-create-environment"><span>Example 1 — Create Environment</span></a></h4>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">python -m venv venv</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h4 id="example-2-—-activate" tabindex="-1"><a class="header-anchor" href="#example-2-—-activate"><span>Example 2 — Activate</span></a></h4>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">venv\Scripts\activate</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h4 id="example-3-—-install-django-after-activation" tabindex="-1"><a class="header-anchor" href="#example-3-—-install-django-after-activation"><span>Example 3 — Install Django After Activation</span></a></h4>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">venv\Scripts\activate</span>
<span class="line"></span>
<span class="line">pip install django</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>المهم إن تثبيت المكتبات يتم بعد التأكد إن البيئة الصحيحة مفعلة.</p>
</div>
<h4 id="example-4-—-save-dependencies" tabindex="-1"><a class="header-anchor" href="#example-4-—-save-dependencies"><span>Example 4 — Save Dependencies</span></a></h4>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip freeze &gt; requirements.txt</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h4 id="example-5-—-recreate-dependencies" tabindex="-1"><a class="header-anchor" href="#example-5-—-recreate-dependencies"><span>Example 5 — Recreate Dependencies</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>عند تجهيز بيئة جديدة للمشروع، يمكن تثبيت dependencies المسجلة في requirements.txt:</p>
</div>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip install -r requirements.txt</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><hr>
<h3 id="_9-❌-common-mistakes" tabindex="-1"><a class="header-anchor" href="#_9-❌-common-mistakes"><span>9. ❌ Common Mistakes</span></a></h3>
<h4 id="_1-تثبيت-المكتبات-قبل-تفعيل-البيئة" tabindex="-1"><a class="header-anchor" href="#_1-تثبيت-المكتبات-قبل-تفعيل-البيئة"><span>1. تثبيت المكتبات قبل تفعيل البيئة</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>من الأخطاء الشائعة تثبيت مكتبات المشروع بدون التأكد إن Virtual Environment مفعلة.</p>
</div>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip install django</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>الأفضل:</p>
</div>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">venv\Scripts\activate</span>
<span class="line"></span>
<span class="line">pip install django</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h4 id="_2-رفع-venv-إلى-git" tabindex="-1"><a class="header-anchor" href="#_2-رفع-venv-إلى-git"><span>2. رفع venv إلى Git</span></a></h4>
<p>لا يتم رفع:</p>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">venv/</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><p>ويجب إضافتها إلى:</p>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">.gitignore</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><p>مثال:</p>
<div class="language-gitignore line-numbers-mode" data-highlighter="prismjs" data-ext="gitignore"><pre v-pre><code><span class="line"><span class="token entry string">venv<span class="token punctuation">/</span></span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h4 id="_3-عدم-تسجيل-dependencies" tabindex="-1"><a class="header-anchor" href="#_3-عدم-تسجيل-dependencies"><span>3. عدم تسجيل Dependencies</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>وجود المكتبات داخل جهازك مش كفاية.</p>
<p>لازم dependencies تكون مسجلة عشان تقدر تعيد بناء البيئة بسهولة.</p>
</div>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip freeze &gt; requirements.txt</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h4 id="_4-اعتبار-venv-جزءًا-من-source-code" tabindex="-1"><a class="header-anchor" href="#_4-اعتبار-venv-جزءًا-من-source-code"><span>4. اعتبار venv جزءًا من Source Code</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>الـvenv نفسها مش المفروض تكون جزء من الكود الذي يتم مشاركته في Git.</p>
<p>الذي يتم مشاركته هو تعريف dependencies، وليس ملفات البيئة نفسها.</p>
</div>
<hr>
<h3 id="_10-🧠-why" tabindex="-1"><a class="header-anchor" href="#_10-🧠-why"><span>10. 🧠 Why?</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>نستخدم Virtual Environment لأن كل مشروع ممكن يعتمد على إصدارات معينة من المكتبات.</p>
<p>بدون العزل ممكن يحصل Version Conflict:</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Project A</span>
<span class="line">    ↓</span>
<span class="line">Global Python</span>
<span class="line">    ↑</span>
<span class="line">Project B</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>أما مع العزل:</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Project A</span>
<span class="line">    ↓</span>
<span class="line">  venv A</span>
<span class="line"></span>
<span class="line"></span>
<span class="line">Project B</span>
<span class="line">    ↓</span>
<span class="line">  venv B</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>وبالتالي كل مشروع يقدر يحتفظ بالـdependencies الخاصة بيه بدون التأثير على المشاريع الأخرى.</p>
</div>
<hr>
<h3 id="_11-🔗-project-usage" tabindex="-1"><a class="header-anchor" href="#_11-🔗-project-usage"><span>11. 🔗 Project Usage</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>داخل مشروع So_Iam_OS، الـVirtual Environment تعتبر جزء أساسي من إعداد الـBackend.</p>
<p>التسلسل الأساسي:</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Python</span>
<span class="line">   ↓</span>
<span class="line">Virtual Environment</span>
<span class="line">   ↓</span>
<span class="line">Activate</span>
<span class="line">   ↓</span>
<span class="line">Upgrade pip</span>
<span class="line">   ↓</span>
<span class="line">Install Dependencies</span>
<span class="line">   ↓</span>
<span class="line">Django</span>
<span class="line">   ↓</span>
<span class="line">Project Setup</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>يعني قبل تثبيت Django وباقي مكتبات الـBackend، لازم تكون البيئة الافتراضية جاهزة ومفعلة.</p>
</div>
<hr>
<h3 id="_12-🤖-ai-reference" tabindex="-1"><a class="header-anchor" href="#_12-🤖-ai-reference"><span>12. 🤖 AI Reference</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>المعلومات التالية تعتبر قواعد مرجعية للـAI عند التعامل مع إعداد Backend المشروع.</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Project:</span>
<span class="line">So_Iam_OS</span>
<span class="line"></span>
<span class="line">Technology:</span>
<span class="line">Python / Django</span>
<span class="line"></span>
<span class="line">Domain:</span>
<span class="line">Backend</span>
<span class="line"></span>
<span class="line">Topic:</span>
<span class="line">Virtual Environment</span>
<span class="line"></span>
<span class="line">Purpose:</span>
<span class="line">Dependency Isolation</span>
<span class="line"></span>
<span class="line">Environment:</span>
<span class="line">venv</span>
<span class="line"></span>
<span class="line">Activation:</span>
<span class="line">venv\Scripts\activate</span>
<span class="line"></span>
<span class="line">Dependency File:</span>
<span class="line">requirements.txt</span>
<span class="line"></span>
<span class="line">Version Control:</span>
<span class="line">Git</span>
<span class="line"></span>
<span class="line">Ignored Directory:</span>
<span class="line">venv/</span>
<span class="line"></span>
<span class="line">Rules:</span>
<span class="line">- يجب تشغيل Virtual Environment قبل تثبيت مكتبات المشروع.</span>
<span class="line">- لا يتم تثبيت Dependencies الخاصة بالمشروع Global بدون سبب.</span>
<span class="line">- venv لا يتم رفعها إلى Git.</span>
<span class="line">- Dependencies يجب تسجيلها.</span>
<span class="line">- requirements.txt هو ملف تعريف Dependencies للمشروع.</span>
<span class="line">- Virtual Environment جزء من Backend Setup.</span>
<span class="line">- حذف venv لا يعني حذف Source Code للمشروع.</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h3 id="_13-📊-current-status" tabindex="-1"><a class="header-anchor" href="#_13-📊-current-status"><span>13. 📊 Current Status</span></a></h3>
<table>
<thead>
<tr>
<th>Task</th>
<th>Status</th>
</tr>
</thead>
<tbody>
<tr>
<td>Python Installed</td>
<td>✅</td>
</tr>
<tr>
<td>Pip Available</td>
<td>✅</td>
</tr>
<tr>
<td>Virtual Environment Created</td>
<td>✅</td>
</tr>
<tr>
<td>Virtual Environment Activated</td>
<td>✅</td>
</tr>
<tr>
<td>Dependencies Setup</td>
<td>⬜</td>
</tr>
<tr>
<td>Django Installation</td>
<td>⬜</td>
</tr>
<tr>
<td>requirements.txt</td>
<td>⬜</td>
</tr>
<tr>
<td>venv added to .gitignore</td>
<td>⬜</td>
</tr>
</tbody>
</table>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>الحالة هنا خاصة بمرحلة Virtual Environment. بعد تنفيذ الخطوات فعليًا داخل المشروع، يتم تحديث الـStatus حسب الواقع.</p>
</div>
<hr>
<h3 id="_14-✅-checklist" tabindex="-1"><a class="header-anchor" href="#_14-✅-checklist"><span>14. ✅ Checklist</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>استخدم القائمة دي للتأكد إن مرحلة Virtual Environment خلصت بشكل صحيح.</p>
</div>
<ul>
<li>[x] التأكد من Python</li>
<li>[x] التأكد من pip</li>
<li>[x] إنشاء Virtual Environment</li>
<li>[x] تفعيل البيئة</li>
<li>[x] إضافة venv إلى <code v-pre>.gitignore</code></li>
<li>[ ] تثبيت Django</li>
<li>[ ] تثبيت باقي dependencies</li>
<li>[ ] إنشاء <code v-pre>requirements.txt</code></li>
</ul>
<hr>
<h3 id="_15-🔗-related-documentation" tabindex="-1"><a class="header-anchor" href="#_15-🔗-related-documentation"><span>15. 🔗 Related Documentation</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>الملفات والتقنيات المرتبطة بالموضوع:</p>
</div>
<ul>
<li>Python</li>
<li>pip</li>
<li>Django</li>
<li><code v-pre>requirements.txt</code></li>
<li>Git</li>
<li><code v-pre>.gitignore</code></li>
<li>Backend Setup</li>
</ul>
<hr>
<h3 id="_16-📝-notes" tabindex="-1"><a class="header-anchor" href="#_16-📝-notes"><span>16. 📝 Notes</span></a></h3>
<h4 id="🔹-اسم-البيئة" tabindex="-1"><a class="header-anchor" href="#🔹-اسم-البيئة"><span>🔹 اسم البيئة</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p><code v-pre>venv</code> هو اسم شائع للـVirtual Environment، لكن ممكن تسمي البيئة بأي اسم مناسب.</p>
</div>
<p>مثال:</p>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">python -m venv .venv</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>في الحالة دي هيكون مسار البيئة:</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">.venv/</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>ولازم يتم تحديث <code v-pre>.gitignore</code> وفقًا للاسم المستخدم.</p>
</div>
<div class="language-gitignore line-numbers-mode" data-highlighter="prismjs" data-ext="gitignore"><pre v-pre><code><span class="line"><span class="token entry string">.venv<span class="token punctuation">/</span></span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h4 id="🔹-حذف-virtual-environment" tabindex="-1"><a class="header-anchor" href="#🔹-حذف-virtual-environment"><span>🔹 حذف Virtual Environment</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>لحذف البيئة على Windows:</p>
</div>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">rmdir /S /Q venv</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>حذف <code v-pre>venv</code> لا يحذف ملفات المشروع الأساسية، لكنه يحذف البيئة والمكتبات المثبتة بداخلها.</p>
<p>بعد حذفها يمكن إنشاء بيئة جديدة وتثبيت dependencies مرة أخرى.</p>
</div>
<hr>
<h2 id="📌-quick-reference" tabindex="-1"><a class="header-anchor" href="#📌-quick-reference"><span>📌 Quick Reference</span></a></h2>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">python --version</span>
<span class="line"></span>
<span class="line">py --version</span>
<span class="line"></span>
<span class="line">pip --version</span>
<span class="line"></span>
<span class="line">py -m pip install --upgrade pip</span>
<span class="line"></span>
<span class="line">python -m venv venv</span>
<span class="line"></span>
<span class="line">venv\Scripts\activate</span>
<span class="line"></span>
<span class="line">pip list</span>
<span class="line"></span>
<span class="line">pip freeze</span>
<span class="line"></span>
<span class="line">pip freeze &gt; requirements.txt</span>
<span class="line"></span>
<span class="line">pip install -r requirements.txt</span>
<span class="line"></span>
<span class="line">deactivate</span>
<span class="line"></span>
<span class="line">rmdir /S /Q venv</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h2 id="🧠-ai-rules" tabindex="-1"><a class="header-anchor" href="#🧠-ai-rules"><span>🧠 AI Rules</span></a></h2>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<ul>
<li>Virtual Environment هي أول مرحلة في Backend Setup.</li>
<li>يجب تفعيل البيئة قبل تثبيت Dependencies.</li>
<li>لا يتم رفع <code v-pre>venv/</code> إلى Git.</li>
<li>يتم مشاركة <code v-pre>requirements.txt</code> بدلًا من مشاركة ملفات <code v-pre>venv</code>.</li>
<li>عند إعادة بناء المشروع على جهاز جديد، يتم إنشاء Virtual Environment جديدة.</li>
<li>يتم تثبيت Dependencies من <code v-pre>requirements.txt</code>.</li>
<li>لا يتم افتراض أن حذف <code v-pre>venv</code> يؤدي إلى حذف المشروع.</li>
<li>إذا تغير اسم البيئة من <code v-pre>venv</code> إلى <code v-pre>.venv</code>، يجب تحديث أوامر التفعيل و<code v-pre>.gitignore</code>.</li>
<li>حالة المشروع يجب أن تعكس ما تم تنفيذه فعليًا، وليس ما هو مخطط له فقط.</li>
</ul>
</div>
</div></template>


