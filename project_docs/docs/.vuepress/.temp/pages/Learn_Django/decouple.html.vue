<template><div><h1 id="🔐-django-environment-configuration-—-decouple-dotenv" tabindex="-1"><a class="header-anchor" href="#🔐-django-environment-configuration-—-decouple-dotenv"><span>🔐 Django Environment Configuration — Decouple + Dotenv</span></a></h1>
<blockquote>
<p>دمج <code v-pre>python-decouple</code> و<code v-pre>python-dotenv</code> لإدارة إعدادات وSecrets مشروع So_Iam_OS حسب بيئة التشغيل.</p>
</blockquote>
<hr>
<h3 id="_1-🎯-purpose" tabindex="-1"><a class="header-anchor" href="#_1-🎯-purpose"><span>1. 🎯 Purpose</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>الهدف من النظام ده هو فصل إعدادات مشروع <strong>So_Iam_OS</strong> عن كود Django نفسه.</p>
<p>بدل ما نحط البيانات الحساسة مباشرة داخل <code v-pre>settings.py</code> مثل:</p>
<ul>
<li><code v-pre>SECRET_KEY</code></li>
<li><code v-pre>Database Password</code></li>
<li>Google OAuth Client ID</li>
<li>Google OAuth Client Secret</li>
<li>API Keys</li>
<li>إعدادات البيئة</li>
</ul>
<p>هنحطها داخل ملفات Environment، وبعد كده Django يقرأها وقت التشغيل.</p>
<p>في المشروع هنستخدم مكتبتين مع بعض:</p>
<p><strong>python-dotenv</strong></p>
<p>مسؤولة عن تحميل ملف <code v-pre>.env</code> المناسب إلى Environment Variables.</p>
<p><strong>python-decouple</strong></p>
<p>مسؤولة عن قراءة القيم داخل <code v-pre>settings.py</code> باستخدام <code v-pre>config()</code>، مع إمكانية تحديد Default Values وتحويل أنواع البيانات.</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Environment File</span>
<span class="line">       ↓</span>
<span class="line">python-dotenv</span>
<span class="line">       ↓</span>
<span class="line">Environment Variables</span>
<span class="line">       ↓</span>
<span class="line">python-decouple</span>
<span class="line">       ↓</span>
<span class="line">config()</span>
<span class="line">       ↓</span>
<span class="line">settings.py</span>
<span class="line">       ↓</span>
<span class="line">Django</span>
<span class="line">       ↓</span>
<span class="line">So_Iam_OS</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h3 id="_2-🧠-concept" tabindex="-1"><a class="header-anchor" href="#_2-🧠-concept"><span>2. 🧠 Concept</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>الفكرة الأساسية إن <code v-pre>settings.py</code> مايبقاش فيه Secrets حقيقية.</p>
<p>بدل:</p>
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">SECRET_KEY <span class="token operator">=</span> <span class="token string">"REAL_SECRET_KEY"</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>نستخدم:</p>
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">SECRET_KEY <span class="token operator">=</span> config<span class="token punctuation">(</span><span class="token string">"SECRET_KEY"</span><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>لكن عندنا مشكلة إضافية في So_Iam_OS:</p>
<p>إحنا مش عايزين ملف Environment واحد فقط.</p>
<p>إحنا محتاجين نميز بين:</p>
<p><strong>Local Development</strong></p>
<p>و</p>
<p><strong>Production</strong></p>
<p>لذلك نستخدم:</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">DJANGO_ENV</span>
<span class="line">    │</span>
<span class="line">    ├── local</span>
<span class="line">    │      ↓</span>
<span class="line">    │   .env.local</span>
<span class="line">    │</span>
<span class="line">    └── production</span>
<span class="line">           ↓</span>
<span class="line">      .env.production</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>بعد تحديد البيئة، <code v-pre>python-dotenv</code> يقوم بتحميل الملف المناسب.</p>
<p>وبعد تحميله، <code v-pre>python-decouple</code> يقرأ القيم باستخدام <code v-pre>config()</code>.</p>
</div>
<hr>
<h3 id="_3-🔧-requirements" tabindex="-1"><a class="header-anchor" href="#_3-🔧-requirements"><span>3. 🔧 Requirements</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>قبل استخدام النظام ده، المشروع يحتاج:</p>
<ul>
<li>Python.</li>
<li>Django.</li>
<li>Virtual Environment.</li>
<li><code v-pre>python-decouple</code>.</li>
<li><code v-pre>python-dotenv</code>.</li>
<li>ملف <code v-pre>settings.py</code>.</li>
<li>ملف <code v-pre>manage.py</code>.</li>
<li>Environment File لكل بيئة تشغيل.</li>
</ul>
<p>ويجب تثبيت المكتبات داخل الـVirtual Environment الخاصة بمشروع So_Iam_OS.</p>
</div>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">venv\Scripts\activate</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><hr>
<h3 id="_4-🛠️-installation-setup" tabindex="-1"><a class="header-anchor" href="#_4-🛠️-installation-setup"><span>4. 🛠️ Installation / Setup</span></a></h3>
<h4 id="📦-install-python-decouple" tabindex="-1"><a class="header-anchor" href="#📦-install-python-decouple"><span>📦 Install python-decouple</span></a></h4>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip install python-decouple</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h4 id="📦-install-python-dotenv" tabindex="-1"><a class="header-anchor" href="#📦-install-python-dotenv"><span>📦 Install python-dotenv</span></a></h4>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip install python-dotenv</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h4 id="📁-environment-files" tabindex="-1"><a class="header-anchor" href="#📁-environment-files"><span>📁 Environment Files</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>في So_Iam_OS هنستخدم ملفات منفصلة للبيئات.</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">So_Iam_OS/</span>
<span class="line">│</span>
<span class="line">├── .env.local</span>
<span class="line">├── .env.production</span>
<span class="line">├── .gitignore</span>
<span class="line">│</span>
<span class="line">├── manage.py</span>
<span class="line">│</span>
<span class="line">└── backend_django/</span>
<span class="line">    ├── settings.py</span>
<span class="line">    ├── urls.py</span>
<span class="line">    ├── asgi.py</span>
<span class="line">    └── wsgi.py</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h4 id="🏠-env-local" tabindex="-1"><a class="header-anchor" href="#🏠-env-local"><span>🏠 <code v-pre>.env.local</code></span></a></h4>
<div class="language-env line-numbers-mode" data-highlighter="prismjs" data-ext="env"><pre v-pre><code><span class="line">DJANGO_ENV=local</span>
<span class="line"></span>
<span class="line">SECRET_KEY=YOUR_LOCAL_SECRET_KEY</span>
<span class="line"></span>
<span class="line">DEBUG=True</span>
<span class="line"></span>
<span class="line">DB_NAME=YOUR_LOCAL_DATABASE_NAME</span>
<span class="line">DB_USER=YOUR_LOCAL_DATABASE_USER</span>
<span class="line">DB_PASSWORD=YOUR_LOCAL_DATABASE_PASSWORD</span>
<span class="line">DB_HOST=localhost</span>
<span class="line">DB_PORT=5432</span>
<span class="line"></span>
<span class="line">GOOGLE_OAUTH_CLIENT_ID=YOUR_LOCAL_GOOGLE_CLIENT_ID</span>
<span class="line">GOOGLE_OAUTH_CLIENT_SECRET=YOUR_LOCAL_GOOGLE_CLIENT_SECRET</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h4 id="🚀-env-production" tabindex="-1"><a class="header-anchor" href="#🚀-env-production"><span>🚀 <code v-pre>.env.production</code></span></a></h4>
<div class="language-env line-numbers-mode" data-highlighter="prismjs" data-ext="env"><pre v-pre><code><span class="line">DJANGO_ENV=production</span>
<span class="line"></span>
<span class="line">SECRET_KEY=YOUR_PRODUCTION_SECRET_KEY</span>
<span class="line"></span>
<span class="line">DEBUG=False</span>
<span class="line"></span>
<span class="line">DB_NAME=YOUR_PRODUCTION_DATABASE_NAME</span>
<span class="line">DB_USER=YOUR_PRODUCTION_DATABASE_USER</span>
<span class="line">DB_PASSWORD=YOUR_PRODUCTION_DATABASE_PASSWORD</span>
<span class="line">DB_HOST=YOUR_PRODUCTION_DATABASE_HOST</span>
<span class="line">DB_PORT=5432</span>
<span class="line"></span>
<span class="line">GOOGLE_OAUTH_CLIENT_ID=YOUR_PRODUCTION_GOOGLE_CLIENT_ID</span>
<span class="line">GOOGLE_OAUTH_CLIENT_SECRET=YOUR_PRODUCTION_GOOGLE_CLIENT_SECRET</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h4 id="⚙️-settings-py" tabindex="-1"><a class="header-anchor" href="#⚙️-settings-py"><span>⚙️ settings.py</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>الكود الأساسي المستخدم في المشروع لدمج المكتبتين:</p>
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">import</span> os</span>
<span class="line"></span>
<span class="line"><span class="token keyword">from</span> pathlib <span class="token keyword">import</span> Path</span>
<span class="line"></span>
<span class="line"><span class="token comment"># 1️⃣ Library Decouple &amp; Dotenv</span></span>
<span class="line"><span class="token keyword">from</span> decouple <span class="token keyword">import</span> config</span>
<span class="line"><span class="token keyword">from</span> dotenv <span class="token keyword">import</span> load_dotenv</span>
<span class="line"></span>
<span class="line"><span class="token comment"># 2️⃣ Library SimpleJWT</span></span>
<span class="line"><span class="token keyword">from</span> datetime <span class="token keyword">import</span> timedelta</span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token comment"># ====================================================</span></span>
<span class="line"><span class="token comment"># BASE DIRECTORY</span></span>
<span class="line"><span class="token comment"># ====================================================</span></span>
<span class="line"></span>
<span class="line">BASE_DIR <span class="token operator">=</span> Path<span class="token punctuation">(</span>__file__<span class="token punctuation">)</span><span class="token punctuation">.</span>resolve<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span>parent<span class="token punctuation">.</span>parent</span>
<span class="line">PROJECT_ROOT <span class="token operator">=</span> BASE_DIR<span class="token punctuation">.</span>parent</span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token comment"># ====================================================</span></span>
<span class="line"><span class="token comment"># ENVIRONMENT</span></span>
<span class="line"><span class="token comment"># ====================================================</span></span>
<span class="line"></span>
<span class="line">ENVIRONMENT <span class="token operator">=</span> os<span class="token punctuation">.</span>getenv<span class="token punctuation">(</span></span>
<span class="line">    <span class="token string">"DJANGO_ENV"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"local"</span></span>
<span class="line"><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token comment"># ====================================================</span></span>
<span class="line"><span class="token comment"># ENVIRONMENT FILE</span></span>
<span class="line"><span class="token comment"># ====================================================</span></span>
<span class="line"></span>
<span class="line"><span class="token keyword">if</span> ENVIRONMENT <span class="token operator">==</span> <span class="token string">"production"</span><span class="token punctuation">:</span></span>
<span class="line">    ENV_FILE <span class="token operator">=</span> PROJECT_ROOT <span class="token operator">/</span> <span class="token string">".env.production"</span></span>
<span class="line"><span class="token keyword">else</span><span class="token punctuation">:</span></span>
<span class="line">    ENV_FILE <span class="token operator">=</span> PROJECT_ROOT <span class="token operator">/</span> <span class="token string">".env.local"</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token comment"># ====================================================</span></span>
<span class="line"><span class="token comment"># LOAD ENVIRONMENT</span></span>
<span class="line"><span class="token comment"># ====================================================</span></span>
<span class="line"></span>
<span class="line">load_dotenv<span class="token punctuation">(</span>ENV_FILE<span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token comment"># ====================================================</span></span>
<span class="line"><span class="token comment"># DJANGO SETTINGS</span></span>
<span class="line"><span class="token comment"># ====================================================</span></span>
<span class="line"></span>
<span class="line">SECRET_KEY <span class="token operator">=</span> config<span class="token punctuation">(</span><span class="token string">"SECRET_KEY"</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">DEBUG <span class="token operator">=</span> config<span class="token punctuation">(</span></span>
<span class="line">    <span class="token string">"DEBUG"</span><span class="token punctuation">,</span></span>
<span class="line">    default<span class="token operator">=</span><span class="token boolean">False</span><span class="token punctuation">,</span></span>
<span class="line">    cast<span class="token operator">=</span><span class="token builtin">bool</span></span>
<span class="line"><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h4 id="🔐-important-environment-rule" tabindex="-1"><a class="header-anchor" href="#🔐-important-environment-rule"><span>🔐 Important Environment Rule</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>في الكود الحالي، <code v-pre>DJANGO_ENV</code> يتم قراءته <strong>قبل</strong> تشغيل <code v-pre>load_dotenv()</code>.</p>
<p>وده معناه إن <code v-pre>DJANGO_ENV</code> لازم يكون متوفر بالفعل في Environment الخاصة بالعملية لو عايزين نستخدمه لاختيار الملف.</p>
<p>يعني:</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">DJANGO_ENV</span>
<span class="line">    ↓</span>
<span class="line">Choose Environment File</span>
<span class="line">    ↓</span>
<span class="line">load_dotenv()</span>
<span class="line">    ↓</span>
<span class="line">config()</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>لذلك لا نعتمد على وجود <code v-pre>DJANGO_ENV</code> داخل <code v-pre>.env.production</code> أو <code v-pre>.env.local</code> لاختيار الملف نفسه في هذا التصميم.</p>
</div>
<h4 id="🚫-gitignore" tabindex="-1"><a class="header-anchor" href="#🚫-gitignore"><span>🚫 .gitignore</span></a></h4>
<div class="language-gitignore line-numbers-mode" data-highlighter="prismjs" data-ext="gitignore"><pre v-pre><code><span class="line"><span class="token entry string">.env</span></span>
<span class="line"><span class="token entry string"><span class="token operator">*</span>.env</span></span>
<span class="line"><span class="token entry string">.env.local</span></span>
<span class="line"><span class="token entry string">.env.production</span></span>
<span class="line"></span>
<span class="line"><span class="token entry string">__pycache__<span class="token punctuation">/</span></span></span>
<span class="line"><span class="token entry string"><span class="token operator">*</span>.py<span class="token regex">[cod]</span></span></span>
<span class="line"></span>
<span class="line"><span class="token entry string">venv<span class="token punctuation">/</span></span></span>
<span class="line"><span class="token entry string">.venv<span class="token punctuation">/</span></span></span>
<span class="line"></span>
<span class="line"><span class="token entry string">db.sqlite3</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h3 id="_5-🚀-usage" tabindex="-1"><a class="header-anchor" href="#_5-🚀-usage"><span>5. 🚀 Usage</span></a></h3>
<h4 id="🔐-secret-key" tabindex="-1"><a class="header-anchor" href="#🔐-secret-key"><span>🔐 SECRET_KEY</span></a></h4>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">SECRET_KEY <span class="token operator">=</span> config<span class="token punctuation">(</span><span class="token string">"SECRET_KEY"</span><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>Django يقرأ <code v-pre>SECRET_KEY</code> من Environment بدل كتابتها داخل Source Code.</p>
</div>
<h4 id="🐛-debug" tabindex="-1"><a class="header-anchor" href="#🐛-debug"><span>🐛 DEBUG</span></a></h4>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">DEBUG <span class="token operator">=</span> config<span class="token punctuation">(</span></span>
<span class="line">    <span class="token string">"DEBUG"</span><span class="token punctuation">,</span></span>
<span class="line">    default<span class="token operator">=</span><span class="token boolean">False</span><span class="token punctuation">,</span></span>
<span class="line">    cast<span class="token operator">=</span><span class="token builtin">bool</span></span>
<span class="line"><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>استخدام <code v-pre>cast=bool</code> مهم لأن Environment Variables يتم التعامل معها كنصوص، وإحنا محتاجين قيمة Boolean.</p>
</div>
<h4 id="🗄️-database" tabindex="-1"><a class="header-anchor" href="#🗄️-database"><span>🗄️ Database</span></a></h4>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">DATABASES <span class="token operator">=</span> <span class="token punctuation">{</span></span>
<span class="line">    <span class="token string">"default"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span></span>
<span class="line">        <span class="token string">"ENGINE"</span><span class="token punctuation">:</span> <span class="token string">"django.db.backends.postgresql"</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">"NAME"</span><span class="token punctuation">:</span> config<span class="token punctuation">(</span><span class="token string">"DB_NAME"</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">"USER"</span><span class="token punctuation">:</span> config<span class="token punctuation">(</span><span class="token string">"DB_USER"</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">"PASSWORD"</span><span class="token punctuation">:</span> config<span class="token punctuation">(</span><span class="token string">"DB_PASSWORD"</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">"HOST"</span><span class="token punctuation">:</span> config<span class="token punctuation">(</span></span>
<span class="line">            <span class="token string">"DB_HOST"</span><span class="token punctuation">,</span></span>
<span class="line">            default<span class="token operator">=</span><span class="token string">"localhost"</span></span>
<span class="line">        <span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">"PORT"</span><span class="token punctuation">:</span> config<span class="token punctuation">(</span></span>
<span class="line">            <span class="token string">"DB_PORT"</span><span class="token punctuation">,</span></span>
<span class="line">            default<span class="token operator">=</span><span class="token string">"5432"</span></span>
<span class="line">        <span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">}</span></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h4 id="🔵-google-oauth" tabindex="-1"><a class="header-anchor" href="#🔵-google-oauth"><span>🔵 Google OAuth</span></a></h4>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">SOCIALACCOUNT_PROVIDERS <span class="token operator">=</span> <span class="token punctuation">{</span></span>
<span class="line">    <span class="token string">"google"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span></span>
<span class="line">        <span class="token string">"APP"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span></span>
<span class="line">            <span class="token string">"client_id"</span><span class="token punctuation">:</span> config<span class="token punctuation">(</span></span>
<span class="line">                <span class="token string">"GOOGLE_OAUTH_CLIENT_ID"</span></span>
<span class="line">            <span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">"secret"</span><span class="token punctuation">:</span> config<span class="token punctuation">(</span></span>
<span class="line">                <span class="token string">"GOOGLE_OAUTH_CLIENT_SECRET"</span></span>
<span class="line">            <span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">"key"</span><span class="token punctuation">:</span> <span class="token string">""</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">"SCOPE"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span></span>
<span class="line">            <span class="token string">"profile"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">"email"</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token punctuation">]</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">"AUTH_PARAMS"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span></span>
<span class="line">            <span class="token string">"access_type"</span><span class="token punctuation">:</span> <span class="token string">"online"</span></span>
<span class="line">        <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">"OAUTH_PKCE_ENABLED"</span><span class="token punctuation">:</span> <span class="token boolean">True</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>وبالتالي إعدادات Google OAuth نفسها لا تحتوي على الـSecrets الحقيقية.</p>
</div>
<hr>
<h3 id="_6-📁-structure" tabindex="-1"><a class="header-anchor" href="#_6-📁-structure"><span>6. 📁 Structure</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>الهيكل المستخدم في So_Iam_OS:</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">So_Iam_OS/</span>
<span class="line">│</span>
<span class="line">├── .env.local</span>
<span class="line">├── .env.production</span>
<span class="line">├── .gitignore</span>
<span class="line">│</span>
<span class="line">├── manage.py</span>
<span class="line">│</span>
<span class="line">└── backend_django/</span>
<span class="line">    │</span>
<span class="line">    ├── __init__.py</span>
<span class="line">    ├── settings.py</span>
<span class="line">    ├── urls.py</span>
<span class="line">    ├── asgi.py</span>
<span class="line">    └── wsgi.py</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>المسؤوليات:</p>
<p><code v-pre>.env.local</code></p>
<p>إعدادات بيئة التطوير المحلية.</p>
<p><code v-pre>.env.production</code></p>
<p>إعدادات بيئة Production.</p>
<p><code v-pre>settings.py</code></p>
<p>يحدد البيئة، يحمل ملف Environment، وبعدها يقرأ القيم.</p>
<p><code v-pre>python-dotenv</code></p>
<p>يحمل Environment File.</p>
<p><code v-pre>python-decouple</code></p>
<p>يقرأ القيم من خلال <code v-pre>config()</code>.</p>
<p><code v-pre>.gitignore</code></p>
<p>يمنع ملفات Environment من الصعود إلى Git.</p>
</div>
<hr>
<h3 id="_7-🧩-important-concepts" tabindex="-1"><a class="header-anchor" href="#_7-🧩-important-concepts"><span>7. 🧩 Important Concepts</span></a></h3>
<h4 id="🔹-python-dotenv" tabindex="-1"><a class="header-anchor" href="#🔹-python-dotenv"><span>🔹 python-dotenv</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>مسؤولة في التصميم الحالي عن تحميل ملف <code v-pre>.env.local</code> أو <code v-pre>.env.production</code> إلى Environment Variables.</p>
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">from</span> dotenv <span class="token keyword">import</span> load_dotenv</span>
<span class="line"></span>
<span class="line">load_dotenv<span class="token punctuation">(</span>ENV_FILE<span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h4 id="🔹-python-decouple" tabindex="-1"><a class="header-anchor" href="#🔹-python-decouple"><span>🔹 python-decouple</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>مسؤولة عن قراءة القيم من خلال <code v-pre>config()</code>.</p>
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">from</span> decouple <span class="token keyword">import</span> config</span>
<span class="line"></span>
<span class="line">SECRET_KEY <span class="token operator">=</span> config<span class="token punctuation">(</span><span class="token string">"SECRET_KEY"</span><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h4 id="🔹-environment-selection" tabindex="-1"><a class="header-anchor" href="#🔹-environment-selection"><span>🔹 Environment Selection</span></a></h4>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">ENVIRONMENT <span class="token operator">=</span> os<span class="token punctuation">.</span>getenv<span class="token punctuation">(</span></span>
<span class="line">    <span class="token string">"DJANGO_ENV"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"local"</span></span>
<span class="line"><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>السطر ده يحدد البيئة الحالية.</p>
<p>لو مفيش <code v-pre>DJANGO_ENV</code>، القيمة الافتراضية هي:</p>
<p><code v-pre>local</code></p>
</div>
<h4 id="🔹-environment-file-selection" tabindex="-1"><a class="header-anchor" href="#🔹-environment-file-selection"><span>🔹 Environment File Selection</span></a></h4>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">if</span> ENVIRONMENT <span class="token operator">==</span> <span class="token string">"production"</span><span class="token punctuation">:</span></span>
<span class="line">    ENV_FILE <span class="token operator">=</span> PROJECT_ROOT <span class="token operator">/</span> <span class="token string">".env.production"</span></span>
<span class="line"><span class="token keyword">else</span><span class="token punctuation">:</span></span>
<span class="line">    ENV_FILE <span class="token operator">=</span> PROJECT_ROOT <span class="token operator">/</span> <span class="token string">".env.local"</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>لو البيئة <code v-pre>production</code> يتم استخدام <code v-pre>.env.production</code>.</p>
<p>وأي قيمة أخرى تؤدي إلى استخدام <code v-pre>.env.local</code> حسب الكود الحالي.</p>
</div>
<h4 id="🔹-base-dir" tabindex="-1"><a class="header-anchor" href="#🔹-base-dir"><span>🔹 BASE_DIR</span></a></h4>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">BASE_DIR <span class="token operator">=</span> Path<span class="token punctuation">(</span>__file__<span class="token punctuation">)</span><span class="token punctuation">.</span>resolve<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span>parent<span class="token punctuation">.</span>parent</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>يمثل المسار الأساسي لمشروع Django.</p>
</div>
<h4 id="🔹-project-root" tabindex="-1"><a class="header-anchor" href="#🔹-project-root"><span>🔹 PROJECT_ROOT</span></a></h4>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">PROJECT_ROOT <span class="token operator">=</span> BASE_DIR<span class="token punctuation">.</span>parent</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>يستخدم الكود ده للوصول إلى جذر المشروع الذي توجد فيه ملفات <code v-pre>.env.local</code> و<code v-pre>.env.production</code>.</p>
</div>
<hr>
<h3 id="_8-💻-examples" tabindex="-1"><a class="header-anchor" href="#_8-💻-examples"><span>8. 💻 Examples</span></a></h3>
<h4 id="🏠-local-environment" tabindex="-1"><a class="header-anchor" href="#🏠-local-environment"><span>🏠 Local Environment</span></a></h4>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">DJANGO_ENV=local</span>
<span class="line">        ↓</span>
<span class="line">.env.local</span>
<span class="line">        ↓</span>
<span class="line">load_dotenv()</span>
<span class="line">        ↓</span>
<span class="line">config()</span>
<span class="line">        ↓</span>
<span class="line">settings.py</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h4 id="🚀-production-environment" tabindex="-1"><a class="header-anchor" href="#🚀-production-environment"><span>🚀 Production Environment</span></a></h4>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">DJANGO_ENV=production</span>
<span class="line">        ↓</span>
<span class="line">.env.production</span>
<span class="line">        ↓</span>
<span class="line">load_dotenv()</span>
<span class="line">        ↓</span>
<span class="line">config()</span>
<span class="line">        ↓</span>
<span class="line">settings.py</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h4 id="🔐-complete-configuration-example" tabindex="-1"><a class="header-anchor" href="#🔐-complete-configuration-example"><span>🔐 Complete Configuration Example</span></a></h4>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">import</span> os</span>
<span class="line"></span>
<span class="line"><span class="token keyword">from</span> pathlib <span class="token keyword">import</span> Path</span>
<span class="line"></span>
<span class="line"><span class="token keyword">from</span> decouple <span class="token keyword">import</span> config</span>
<span class="line"><span class="token keyword">from</span> dotenv <span class="token keyword">import</span> load_dotenv</span>
<span class="line"></span>
<span class="line"><span class="token keyword">from</span> datetime <span class="token keyword">import</span> timedelta</span>
<span class="line"></span>
<span class="line"></span>
<span class="line">BASE_DIR <span class="token operator">=</span> Path<span class="token punctuation">(</span>__file__<span class="token punctuation">)</span><span class="token punctuation">.</span>resolve<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span>parent<span class="token punctuation">.</span>parent</span>
<span class="line"></span>
<span class="line">PROJECT_ROOT <span class="token operator">=</span> BASE_DIR<span class="token punctuation">.</span>parent</span>
<span class="line"></span>
<span class="line"></span>
<span class="line">ENVIRONMENT <span class="token operator">=</span> os<span class="token punctuation">.</span>getenv<span class="token punctuation">(</span></span>
<span class="line">    <span class="token string">"DJANGO_ENV"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"local"</span></span>
<span class="line"><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token keyword">if</span> ENVIRONMENT <span class="token operator">==</span> <span class="token string">"production"</span><span class="token punctuation">:</span></span>
<span class="line">    ENV_FILE <span class="token operator">=</span> PROJECT_ROOT <span class="token operator">/</span> <span class="token string">".env.production"</span></span>
<span class="line"><span class="token keyword">else</span><span class="token punctuation">:</span></span>
<span class="line">    ENV_FILE <span class="token operator">=</span> PROJECT_ROOT <span class="token operator">/</span> <span class="token string">".env.local"</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line">load_dotenv<span class="token punctuation">(</span>ENV_FILE<span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line">SECRET_KEY <span class="token operator">=</span> config<span class="token punctuation">(</span><span class="token string">"SECRET_KEY"</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line">DEBUG <span class="token operator">=</span> config<span class="token punctuation">(</span></span>
<span class="line">    <span class="token string">"DEBUG"</span><span class="token punctuation">,</span></span>
<span class="line">    default<span class="token operator">=</span><span class="token boolean">False</span><span class="token punctuation">,</span></span>
<span class="line">    cast<span class="token operator">=</span><span class="token builtin">bool</span></span>
<span class="line"><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h4 id="🗄️-database-example" tabindex="-1"><a class="header-anchor" href="#🗄️-database-example"><span>🗄️ Database Example</span></a></h4>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">DATABASES <span class="token operator">=</span> <span class="token punctuation">{</span></span>
<span class="line">    <span class="token string">"default"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span></span>
<span class="line">        <span class="token string">"ENGINE"</span><span class="token punctuation">:</span> <span class="token string">"django.db.backends.postgresql"</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">"NAME"</span><span class="token punctuation">:</span> config<span class="token punctuation">(</span><span class="token string">"DB_NAME"</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">"USER"</span><span class="token punctuation">:</span> config<span class="token punctuation">(</span><span class="token string">"DB_USER"</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">"PASSWORD"</span><span class="token punctuation">:</span> config<span class="token punctuation">(</span><span class="token string">"DB_PASSWORD"</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">"HOST"</span><span class="token punctuation">:</span> config<span class="token punctuation">(</span></span>
<span class="line">            <span class="token string">"DB_HOST"</span><span class="token punctuation">,</span></span>
<span class="line">            default<span class="token operator">=</span><span class="token string">"localhost"</span></span>
<span class="line">        <span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">"PORT"</span><span class="token punctuation">:</span> config<span class="token punctuation">(</span></span>
<span class="line">            <span class="token string">"DB_PORT"</span><span class="token punctuation">,</span></span>
<span class="line">            default<span class="token operator">=</span><span class="token string">"5432"</span></span>
<span class="line">        <span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">}</span></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h4 id="🔵-google-oauth-example" tabindex="-1"><a class="header-anchor" href="#🔵-google-oauth-example"><span>🔵 Google OAuth Example</span></a></h4>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">SOCIALACCOUNT_PROVIDERS <span class="token operator">=</span> <span class="token punctuation">{</span></span>
<span class="line">    <span class="token string">"google"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span></span>
<span class="line">        <span class="token string">"APP"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span></span>
<span class="line">            <span class="token string">"client_id"</span><span class="token punctuation">:</span> config<span class="token punctuation">(</span></span>
<span class="line">                <span class="token string">"GOOGLE_OAUTH_CLIENT_ID"</span></span>
<span class="line">            <span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">"secret"</span><span class="token punctuation">:</span> config<span class="token punctuation">(</span></span>
<span class="line">                <span class="token string">"GOOGLE_OAUTH_CLIENT_SECRET"</span></span>
<span class="line">            <span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">"key"</span><span class="token punctuation">:</span> <span class="token string">""</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">"SCOPE"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span></span>
<span class="line">            <span class="token string">"profile"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">"email"</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token punctuation">]</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">"AUTH_PARAMS"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span></span>
<span class="line">            <span class="token string">"access_type"</span><span class="token punctuation">:</span> <span class="token string">"online"</span></span>
<span class="line">        <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">"OAUTH_PKCE_ENABLED"</span><span class="token punctuation">:</span> <span class="token boolean">True</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h3 id="_9-❌-common-mistakes" tabindex="-1"><a class="header-anchor" href="#_9-❌-common-mistakes"><span>9. ❌ Common Mistakes</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<h4 id="❌-وضع-secrets-داخل-settings-py" tabindex="-1"><a class="header-anchor" href="#❌-وضع-secrets-داخل-settings-py"><span>❌ وضع Secrets داخل <code v-pre>settings.py</code></span></a></h4>
<p>لا نكتب:</p>
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">SECRET_KEY <span class="token operator">=</span> <span class="token string">"REAL_SECRET"</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>نستخدم:</p>
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">SECRET_KEY <span class="token operator">=</span> config<span class="token punctuation">(</span><span class="token string">"SECRET_KEY"</span><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<h4 id="❌-رفع-env-إلى-git" tabindex="-1"><a class="header-anchor" href="#❌-رفع-env-إلى-git"><span>❌ رفع <code v-pre>.env</code> إلى Git</span></a></h4>
<p>لازم ملفات Environment تكون موجودة في <code v-pre>.gitignore</code>.</p>
<h4 id="❌-وضع-secrets-حقيقية-في-knowledge-documentation" tabindex="-1"><a class="header-anchor" href="#❌-وضع-secrets-حقيقية-في-knowledge-documentation"><span>❌ وضع Secrets حقيقية في Knowledge Documentation</span></a></h4>
<p>ملفات المعرفة تستخدم Placeholders فقط.</p>
<h4 id="❌-نسيان-cast-bool" tabindex="-1"><a class="header-anchor" href="#❌-نسيان-cast-bool"><span>❌ نسيان <code v-pre>cast=bool</code></span></a></h4>
<p>لازم نستخدم:</p>
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">DEBUG <span class="token operator">=</span> config<span class="token punctuation">(</span></span>
<span class="line">    <span class="token string">"DEBUG"</span><span class="token punctuation">,</span></span>
<span class="line">    default<span class="token operator">=</span><span class="token boolean">False</span><span class="token punctuation">,</span></span>
<span class="line">    cast<span class="token operator">=</span><span class="token builtin">bool</span></span>
<span class="line"><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<h4 id="❌-الخلط-بين-دور-المكتبتين" tabindex="-1"><a class="header-anchor" href="#❌-الخلط-بين-دور-المكتبتين"><span>❌ الخلط بين دور المكتبتين</span></a></h4>
<p>لازم نفهم إن التصميم الحالي بيفصل الأدوار:</p>
<p><code v-pre>dotenv</code></p>
<p>تحميل ملف Environment.</p>
<p><code v-pre>decouple</code></p>
<p>قراءة القيم باستخدام <code v-pre>config()</code>.</p>
<h4 id="❌-محاولة-استخدام-django-env-من-ملف-لم-يتم-تحميله-بعد" tabindex="-1"><a class="header-anchor" href="#❌-محاولة-استخدام-django-env-من-ملف-لم-يتم-تحميله-بعد"><span>❌ محاولة استخدام <code v-pre>DJANGO_ENV</code> من ملف لم يتم تحميله بعد</span></a></h4>
<p>في الكود الحالي، اختيار <code v-pre>.env</code> يحدث قبل <code v-pre>load_dotenv()</code>.</p>
<p>لذلك <code v-pre>DJANGO_ENV</code> المستخدم لاختيار الملف يجب أن يكون متوفرًا قبل عملية تحميل الملف.</p>
</div>
<hr>
<h3 id="_10-🧠-why" tabindex="-1"><a class="header-anchor" href="#_10-🧠-why"><span>10. 🧠 Why?</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>ليه So_Iam_OS محتاج النظام ده؟</p>
<p>لأن المشروع عنده أكثر من بيئة تشغيل.</p>
<p>في Development عندنا إعدادات مختلفة عن Production.</p>
<p>مثلًا:</p>
<ul>
<li>Database مختلفة.</li>
<li><code v-pre>DEBUG</code> مختلف.</li>
<li>Google OAuth credentials مختلفة.</li>
<li><code v-pre>SECRET_KEY</code> مختلفة.</li>
<li>إعدادات مستقبلية مختلفة.</li>
</ul>
<p>بدل تغيير <code v-pre>settings.py</code> كل مرة، بنغير Environment فقط.</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">                    So_Iam_OS</span>
<span class="line">                        │</span>
<span class="line">              ┌─────────┴─────────┐</span>
<span class="line">              │                   │</span>
<span class="line">           Local              Production</span>
<span class="line">              │                   │</span>
<span class="line">       .env.local        .env.production</span>
<span class="line">              │                   │</span>
<span class="line">              └─────────┬─────────┘</span>
<span class="line">                        ↓</span>
<span class="line">                 python-dotenv</span>
<span class="line">                        ↓</span>
<span class="line">                Environment Vars</span>
<span class="line">                        ↓</span>
<span class="line">                python-decouple</span>
<span class="line">                        ↓</span>
<span class="line">                    settings.py</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h3 id="_11-🔗-project-usage" tabindex="-1"><a class="header-anchor" href="#_11-🔗-project-usage"><span>11. 🔗 Project Usage</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>داخل مشروع <strong>So_Iam_OS</strong>، النظام ده جزء أساسي من Backend Configuration.</p>
<p>يتم استخدامه مع:</p>
<ul>
<li>Django.</li>
<li>PostgreSQL.</li>
<li>Google OAuth.</li>
<li>django-allauth.</li>
<li>SimpleJWT.</li>
<li>أي API Keys مستقبلية.</li>
<li>أي Secrets مستقبلية.</li>
</ul>
<p>وبالتالي <code v-pre>settings.py</code> لا يكون مكان تخزين الأسرار، وإنما مكان استخدام الإعدادات.</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">So_Iam_OS</span>
<span class="line">│</span>
<span class="line">├── Frontend</span>
<span class="line">│</span>
<span class="line">└── Backend</span>
<span class="line">    │</span>
<span class="line">    └── Django</span>
<span class="line">        │</span>
<span class="line">        └── settings.py</span>
<span class="line">            │</span>
<span class="line">            ├── Environment Selection</span>
<span class="line">            │</span>
<span class="line">            ├── python-dotenv</span>
<span class="line">            │</span>
<span class="line">            ├── python-decouple</span>
<span class="line">            │</span>
<span class="line">            ├── SECRET_KEY</span>
<span class="line">            │</span>
<span class="line">            ├── DEBUG</span>
<span class="line">            │</span>
<span class="line">            ├── PostgreSQL</span>
<span class="line">            │</span>
<span class="line">            ├── Google OAuth</span>
<span class="line">            │</span>
<span class="line">            ├── django-allauth</span>
<span class="line">            │</span>
<span class="line">            └── SimpleJWT</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h3 id="_12-🤖-ai-reference" tabindex="-1"><a class="header-anchor" href="#_12-🤖-ai-reference"><span>12. 🤖 AI Reference</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>عند تعامل الـAI مع إعدادات Environment في So_Iam_OS، يجب الالتزام بالتصميم الموجود.</p>
<p>الـAI لا يقوم بتغيير النظام إلى طريقة أخرى بدون طلب.</p>
<p>الـArchitecture الحالية تعتمد على دمج:</p>
<p><code v-pre>python-dotenv</code></p>
<p>مع:</p>
<p><code v-pre>python-decouple</code></p>
<p><code v-pre>python-dotenv</code> مسؤول عن تحميل ملف Environment.</p>
<p><code v-pre>python-decouple</code> مسؤول عن قراءة القيم باستخدام <code v-pre>config()</code>.</p>
<p>البيئة يتم تحديدها باستخدام:</p>
<p><code v-pre>DJANGO_ENV</code></p>
<p>القيمة الافتراضية هي:</p>
<p><code v-pre>local</code></p>
<p>إذا كانت البيئة:</p>
<p><code v-pre>production</code></p>
<p>يتم اختيار:</p>
<p><code v-pre>.env.production</code></p>
<p>وفي غير ذلك يتم اختيار:</p>
<p><code v-pre>.env.local</code></p>
<p>ملفات Environment تحتوي على Secrets ولا يجب رفعها إلى Git.</p>
<p>لا يتم وضع Secrets حقيقية داخل Documentation.</p>
<p>عند إضافة إعداد حساس جديد للمشروع، يجب استخدام Environment Variable بدل وضع القيمة السرية مباشرة داخل Source Code.</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Project:</span>
<span class="line">So_Iam_OS</span>
<span class="line"></span>
<span class="line">Backend:</span>
<span class="line">Django</span>
<span class="line"></span>
<span class="line">Environment Management:</span>
<span class="line">python-dotenv + python-decouple</span>
<span class="line"></span>
<span class="line">Environment Variable:</span>
<span class="line">DJANGO_ENV</span>
<span class="line"></span>
<span class="line">Default Environment:</span>
<span class="line">local</span>
<span class="line"></span>
<span class="line">Local File:</span>
<span class="line">.env.local</span>
<span class="line"></span>
<span class="line">Production File:</span>
<span class="line">.env.production</span>
<span class="line"></span>
<span class="line">Loader:</span>
<span class="line">python-dotenv</span>
<span class="line"></span>
<span class="line">Reader:</span>
<span class="line">python-decouple</span>
<span class="line"></span>
<span class="line">Reader Function:</span>
<span class="line">config()</span>
<span class="line"></span>
<span class="line">Main Configuration:</span>
<span class="line">settings.py</span>
<span class="line"></span>
<span class="line">Sensitive Configuration:</span>
<span class="line">- SECRET_KEY</span>
<span class="line">- Database Credentials</span>
<span class="line">- Google OAuth Credentials</span>
<span class="line">- API Keys</span>
<span class="line">- Future Secrets</span>
<span class="line"></span>
<span class="line">Git Rule:</span>
<span class="line">Environment files must not be committed.</span>
<span class="line"></span>
<span class="line">Security Rule:</span>
<span class="line">Never expose real Secrets in documentation.</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h3 id="_13-📊-current-status" tabindex="-1"><a class="header-anchor" href="#_13-📊-current-status"><span>13. 📊 Current Status</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>الحالة هنا يجب أن تعكس ما تم تنفيذه فعليًا داخل المشروع، وليس مجرد وجود الكود في ملف المعرفة.</p>
<p>حسب حالة المشروع الحالية، <code v-pre>settings.py</code> و<code v-pre>urls.py</code> هما الملفات التي تم تنفيذها بالفعل، أما دمج كل إعدادات Environment الإضافية فيجب اعتباره منفذًا فقط بعد التأكد من تشغيله واختباره داخل المشروع.</p>
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
<td><code v-pre>settings.py</code> موجود</td>
<td>✅</td>
</tr>
<tr>
<td><code v-pre>urls.py</code> موجود</td>
<td>✅</td>
</tr>
<tr>
<td>Install <code v-pre>python-decouple</code></td>
<td>⬜</td>
</tr>
<tr>
<td>Install <code v-pre>python-dotenv</code></td>
<td>⬜</td>
</tr>
<tr>
<td>Create <code v-pre>.env.local</code></td>
<td>⬜</td>
</tr>
<tr>
<td>Create <code v-pre>.env.production</code></td>
<td>⬜</td>
</tr>
<tr>
<td>Configure <code v-pre>DJANGO_ENV</code></td>
<td>⬜</td>
</tr>
<tr>
<td>Configure Environment Selection</td>
<td>⬜</td>
</tr>
<tr>
<td>Configure <code v-pre>load_dotenv()</code></td>
<td>⬜</td>
</tr>
<tr>
<td>Configure <code v-pre>config()</code></td>
<td>⬜</td>
</tr>
<tr>
<td>Move <code v-pre>SECRET_KEY</code> to Environment</td>
<td>⬜</td>
</tr>
<tr>
<td>Move <code v-pre>DEBUG</code> to Environment</td>
<td>⬜</td>
</tr>
<tr>
<td>Move Database Configuration</td>
<td>⬜</td>
</tr>
<tr>
<td>Move Google OAuth Configuration</td>
<td>⬜</td>
</tr>
<tr>
<td>Add Environment files to <code v-pre>.gitignore</code></td>
<td>⬜</td>
</tr>
<tr>
<td>Test Local Environment</td>
<td>⬜</td>
</tr>
<tr>
<td>Test Production Environment</td>
<td>⬜</td>
</tr>
<tr>
<td>Verify Django Settings</td>
<td>⬜</td>
</tr>
</tbody>
</table>
<hr>
<h3 id="_14-✅-checklist" tabindex="-1"><a class="header-anchor" href="#_14-✅-checklist"><span>14. ✅ Checklist</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>قائمة مراجعة تنفيذ نظام Environment Configuration في So_Iam_OS:</p>
</div>
<ul>
<li>[x] <code v-pre>settings.py</code> موجود</li>
<li>[x] <code v-pre>urls.py</code> موجود</li>
<li>[ ] Install <code v-pre>python-decouple</code></li>
<li>[ ] Install <code v-pre>python-dotenv</code></li>
<li>[ ] Create <code v-pre>.env.local</code></li>
<li>[ ] Create <code v-pre>.env.production</code></li>
<li>[ ] Configure <code v-pre>DJANGO_ENV</code></li>
<li>[ ] Configure <code v-pre>BASE_DIR</code></li>
<li>[ ] Configure <code v-pre>PROJECT_ROOT</code></li>
<li>[ ] Configure Environment Selection</li>
<li>[ ] Configure <code v-pre>load_dotenv()</code></li>
<li>[ ] Import <code v-pre>config</code></li>
<li>[ ] Configure <code v-pre>SECRET_KEY</code></li>
<li>[ ] Configure <code v-pre>DEBUG</code></li>
<li>[ ] Configure PostgreSQL</li>
<li>[ ] Configure Google OAuth</li>
<li>[ ] Add <code v-pre>.env</code> files to <code v-pre>.gitignore</code></li>
<li>[ ] Test Local Environment</li>
<li>[ ] Test Database Configuration</li>
<li>[ ] Test Google OAuth Configuration</li>
<li>[ ] Test Production Environment</li>
<li>[ ] Verify Secrets are not committed</li>
</ul>
<hr>
<h3 id="_15-🔗-related-documentation" tabindex="-1"><a class="header-anchor" href="#_15-🔗-related-documentation"><span>15. 🔗 Related Documentation</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>المواضيع والملفات المرتبطة بالنظام ده داخل So_Iam_OS:</p>
</div>
<ul>
<li><code v-pre>backend_django/settings.py</code></li>
<li><code v-pre>backend_django/urls.py</code></li>
<li><code v-pre>.env.local</code></li>
<li><code v-pre>.env.production</code></li>
<li><code v-pre>.gitignore</code></li>
<li>Python Virtual Environment</li>
<li>Django Settings</li>
<li>PostgreSQL</li>
<li><code v-pre>python-decouple</code></li>
<li><code v-pre>python-dotenv</code></li>
<li>django-allauth</li>
<li>Google OAuth</li>
<li>SimpleJWT</li>
<li>CORS</li>
<li>Environment Variables</li>
<li>Secrets Management</li>
</ul>
<hr>
<h3 id="_16-📝-notes" tabindex="-1"><a class="header-anchor" href="#_16-📝-notes"><span>16. 📝 Notes</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>النظام الحالي مصمم على أساس وجود بيئتين رئيسيتين:</p>
<p><strong>Local</strong></p>
<p>و</p>
<p><strong>Production</strong></p>
<p>والفكرة الأساسية هي:</p>
<p><strong>نفس Source Code</strong></p>
<p>لكن:</p>
<p><strong>Environment مختلفة</strong></p>
<p>وبالتالي لا نحتاج إلى تعديل الكود في كل مرة ننتقل فيها من Development إلى Production.</p>
<p>النقطة المهمة في التصميم الحالي هي ترتيب التنفيذ:</p>
<p>أولًا يتم تحديد <code v-pre>DJANGO_ENV</code>.</p>
<p>بعدها يتم اختيار <code v-pre>.env.local</code> أو <code v-pre>.env.production</code>.</p>
<p>بعدها يتم تشغيل <code v-pre>load_dotenv()</code>.</p>
<p>بعدها يتم استخدام <code v-pre>config()</code> لقراءة القيم.</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">DJANGO_ENV</span>
<span class="line">    ↓</span>
<span class="line">Environment Selection</span>
<span class="line">    ↓</span>
<span class="line">.env.local / .env.production</span>
<span class="line">    ↓</span>
<span class="line">load_dotenv()</span>
<span class="line">    ↓</span>
<span class="line">Environment Variables</span>
<span class="line">    ↓</span>
<span class="line">config()</span>
<span class="line">    ↓</span>
<span class="line">settings.py</span>
<span class="line">    ↓</span>
<span class="line">Django</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>كمان مهم إننا ملتزمين في So_Iam_OS بالفصل بين:</p>
<p><strong>Configuration</strong></p>
<p>و</p>
<p><strong>Secrets</strong></p>
<p><code v-pre>settings.py</code> يحتوي على طريقة استخدام الإعدادات.</p>
<p>أما القيم الحساسة نفسها فتأتي من Environment.</p>
<p>ولا يتم وضع Google Client Secret أو Database Password أو Django Secret Key الحقيقية داخل Knowledge Documentation.</p>
</div>
<h4 id="⚡-quick-reference" tabindex="-1"><a class="header-anchor" href="#⚡-quick-reference"><span>⚡ Quick Reference</span></a></h4>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip install python-decouple</span>
<span class="line">pip install python-dotenv</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div></div></div><div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">import</span> os</span>
<span class="line"></span>
<span class="line"><span class="token keyword">from</span> pathlib <span class="token keyword">import</span> Path</span>
<span class="line"></span>
<span class="line"><span class="token keyword">from</span> decouple <span class="token keyword">import</span> config</span>
<span class="line"><span class="token keyword">from</span> dotenv <span class="token keyword">import</span> load_dotenv</span>
<span class="line"></span>
<span class="line"></span>
<span class="line">BASE_DIR <span class="token operator">=</span> Path<span class="token punctuation">(</span>__file__<span class="token punctuation">)</span><span class="token punctuation">.</span>resolve<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span>parent<span class="token punctuation">.</span>parent</span>
<span class="line"></span>
<span class="line">PROJECT_ROOT <span class="token operator">=</span> BASE_DIR<span class="token punctuation">.</span>parent</span>
<span class="line"></span>
<span class="line"></span>
<span class="line">ENVIRONMENT <span class="token operator">=</span> os<span class="token punctuation">.</span>getenv<span class="token punctuation">(</span></span>
<span class="line">    <span class="token string">"DJANGO_ENV"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"local"</span></span>
<span class="line"><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token keyword">if</span> ENVIRONMENT <span class="token operator">==</span> <span class="token string">"production"</span><span class="token punctuation">:</span></span>
<span class="line">    ENV_FILE <span class="token operator">=</span> PROJECT_ROOT <span class="token operator">/</span> <span class="token string">".env.production"</span></span>
<span class="line"><span class="token keyword">else</span><span class="token punctuation">:</span></span>
<span class="line">    ENV_FILE <span class="token operator">=</span> PROJECT_ROOT <span class="token operator">/</span> <span class="token string">".env.local"</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line">load_dotenv<span class="token punctuation">(</span>ENV_FILE<span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line">SECRET_KEY <span class="token operator">=</span> config<span class="token punctuation">(</span><span class="token string">"SECRET_KEY"</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">DEBUG <span class="token operator">=</span> config<span class="token punctuation">(</span></span>
<span class="line">    <span class="token string">"DEBUG"</span><span class="token punctuation">,</span></span>
<span class="line">    default<span class="token operator">=</span><span class="token boolean">False</span><span class="token punctuation">,</span></span>
<span class="line">    cast<span class="token operator">=</span><span class="token builtin">bool</span></span>
<span class="line"><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div class="language-gitignore line-numbers-mode" data-highlighter="prismjs" data-ext="gitignore"><pre v-pre><code><span class="line"><span class="token entry string">.env</span></span>
<span class="line"><span class="token entry string"><span class="token operator">*</span>.env</span></span>
<span class="line"><span class="token entry string">.env.local</span></span>
<span class="line"><span class="token entry string">.env.production</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h4 id="🧠-architecture-rule" tabindex="-1"><a class="header-anchor" href="#🧠-architecture-rule"><span>🧠 Architecture Rule</span></a></h4>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">python-dotenv</span>
<span class="line">      │</span>
<span class="line">      │ Load</span>
<span class="line">      ▼</span>
<span class="line">Environment Variables</span>
<span class="line">      │</span>
<span class="line">      │ Read</span>
<span class="line">      ▼</span>
<span class="line">python-decouple</span>
<span class="line">      │</span>
<span class="line">      │ config()</span>
<span class="line">      ▼</span>
<span class="line">settings.py</span>
<span class="line">      │</span>
<span class="line">      ▼</span>
<span class="line">Django</span>
<span class="line">      │</span>
<span class="line">      ▼</span>
<span class="line">So_Iam_OS</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div></div></template>


