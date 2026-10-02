<template><div><h1 id="django-allauth" tabindex="-1"><a class="header-anchor" href="#django-allauth"><span>django-allauth</span></a></h1>
<blockquote>
<p>إعداد متقدم لـ <code v-pre>django-allauth</code> لإدارة Email Authentication وGoogle OAuth وSessions وRedirects داخل مشروع So_Iam_OS.</p>
</blockquote>
<hr>
<h3 id="_1-🎯-purpose" tabindex="-1"><a class="header-anchor" href="#_1-🎯-purpose"><span>1. 🎯 Purpose</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>الجزء ده مسؤول عن إعداد <code v-pre>django-allauth</code> داخل مشروع Django بحيث نقدر ندير نظام الحسابات والمصادقة باستخدام:</p>
<ul>
<li>Email Authentication.</li>
<li>Google OAuth.</li>
<li>Email Verification.</li>
<li>Social Account Signup.</li>
<li>Session Management.</li>
<li>Login Redirect.</li>
<li>Logout Redirect.</li>
<li>Custom Social Account Adapter.</li>
<li>CORS Headers المطلوبة للتعامل مع الـFrontend.</li>
</ul>
<p>الهدف النهائي هو ربط نظام Authentication الموجود في Django بالـFrontend الخاص بـ <strong>So_Iam_OS</strong>.</p>
</div>
<hr>
<h3 id="_2-🧠-concept" tabindex="-1"><a class="header-anchor" href="#_2-🧠-concept"><span>2. 🧠 Concept</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>الفكرة هنا إن <code v-pre>django-allauth</code> بيكون طبقة مسؤولة عن هوية المستخدم والحسابات.</p>
<p>في البداية كان Google OAuth معمول بشكل مباشر داخل <code v-pre>settings.py</code> باستخدام:</p>
<p><code v-pre>client_id</code></p>
<p>و</p>
<p><code v-pre>secret</code></p>
<p>لكن الإعداد المتقدم بيستخدم <code v-pre>python-decouple</code> لقراءة البيانات الحساسة من Environment Variables بدل كتابتها مباشرة داخل الكود.</p>
<p>الـFlow:</p>
<p>Frontend
↓
Django / allauth
↓
Email أو Google OAuth
↓
User Identity
↓
users_accounts
↓
Authentication</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Frontend</span>
<span class="line">   │</span>
<span class="line">   ▼</span>
<span class="line">Django</span>
<span class="line">   │</span>
<span class="line">   ▼</span>
<span class="line">django-allauth</span>
<span class="line">   │</span>
<span class="line">   ├── Email</span>
<span class="line">   │</span>
<span class="line">   └── Google OAuth</span>
<span class="line">           │</span>
<span class="line">           ▼</span>
<span class="line">      User Identity</span>
<span class="line">           │</span>
<span class="line">           ▼</span>
<span class="line">     users_accounts</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h3 id="_3-🔧-requirements" tabindex="-1"><a class="header-anchor" href="#_3-🔧-requirements"><span>3. 🔧 Requirements</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>قبل تطبيق الإعدادات دي، المشروع محتاج:</p>
<ul>
<li>Django.</li>
<li><code v-pre>django-allauth</code>.</li>
<li><code v-pre>python-decouple</code>.</li>
<li>Django Sites Framework.</li>
<li>تطبيق <code v-pre>users_accounts</code>.</li>
<li>Google OAuth Application.</li>
<li>Frontend شغال.</li>
<li>Environment Variables تحتوي على Google OAuth credentials.</li>
<li>إعداد CORS مناسب للتواصل مع الـFrontend.</li>
</ul>
</div>
<hr>
<h3 id="_4-🛠️-installation-setup" tabindex="-1"><a class="header-anchor" href="#_4-🛠️-installation-setup"><span>4. 🛠️ Installation / Setup</span></a></h3>
<h4 id="📚-install-django-allauth" tabindex="-1"><a class="header-anchor" href="#📚-install-django-allauth"><span>📚 Install django-allauth</span></a></h4>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip install django-allauth</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h4 id="📚-install-python-decouple" tabindex="-1"><a class="header-anchor" href="#📚-install-python-decouple"><span>📚 Install python-decouple</span></a></h4>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip install python-decouple</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h4 id="📦-installed-apps" tabindex="-1"><a class="header-anchor" href="#📦-installed-apps"><span>📦 INSTALLED_APPS</span></a></h4>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">INSTALLED_APPS <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line">    <span class="token comment"># Libraries</span></span>
<span class="line"></span>
<span class="line">    <span class="token string">"django.contrib.sites"</span><span class="token punctuation">,</span></span>
<span class="line"></span>
<span class="line">    <span class="token string">"allauth"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"allauth.account"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"allauth.socialaccount"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"allauth.socialaccount.providers.google"</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">]</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h4 id="⚙️-accountmiddleware" tabindex="-1"><a class="header-anchor" href="#⚙️-accountmiddleware"><span>⚙️ AccountMiddleware</span></a></h4>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">MIDDLEWARE <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line">    <span class="token comment"># Add AccountMiddleware for allauth</span></span>
<span class="line"></span>
<span class="line">    <span class="token string">"allauth.account.middleware.AccountMiddleware"</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">]</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h4 id="🌐-urls" tabindex="-1"><a class="header-anchor" href="#🌐-urls"><span>🌐 URLs</span></a></h4>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># 📄 backend_django/urls.py</span></span>
<span class="line"></span>
<span class="line"><span class="token keyword">from</span> django<span class="token punctuation">.</span>contrib <span class="token keyword">import</span> admin</span>
<span class="line"><span class="token keyword">from</span> django<span class="token punctuation">.</span>urls <span class="token keyword">import</span> path<span class="token punctuation">,</span> include</span>
<span class="line"></span>
<span class="line">urlpatterns <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line">    path<span class="token punctuation">(</span><span class="token string">"accounts/"</span><span class="token punctuation">,</span> include<span class="token punctuation">(</span><span class="token string">"allauth.urls"</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">]</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h4 id="🔐-google-oauth-configuration" tabindex="-1"><a class="header-anchor" href="#🔐-google-oauth-configuration"><span>🔐 Google OAuth Configuration</span></a></h4>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">SOCIALACCOUNT_PROVIDERS <span class="token operator">=</span> <span class="token punctuation">{</span></span>
<span class="line">    <span class="token string">"google"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span></span>
<span class="line">        <span class="token string">"APP"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span></span>
<span class="line">            <span class="token string">"client_id"</span><span class="token punctuation">:</span> config<span class="token punctuation">(</span><span class="token string">"GOOGLE_OAUTH_CLIENT_ID"</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">"secret"</span><span class="token punctuation">:</span> config<span class="token punctuation">(</span><span class="token string">"GOOGLE_OAUTH_CLIENT_SECRET"</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">"key"</span><span class="token punctuation">:</span> <span class="token string">""</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">"SCOPE"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span></span>
<span class="line">            <span class="token string">"profile"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">"email"</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token punctuation">]</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">"AUTH_PARAMS"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span></span>
<span class="line">            <span class="token string">"access_type"</span><span class="token punctuation">:</span> <span class="token string">"online"</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">"OAUTH_PKCE_ENABLED"</span><span class="token punctuation">:</span> <span class="token boolean">True</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><blockquote>
<p>لا يتم تخزين <code v-pre>GOOGLE_OAUTH_CLIENT_SECRET</code> الحقيقي داخل ملف المعرفة أو Git.</p>
</blockquote>
<h4 id="📧-account-configuration" tabindex="-1"><a class="header-anchor" href="#📧-account-configuration"><span>📧 Account Configuration</span></a></h4>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">ACCOUNT_LOGOUT_ON_GET <span class="token operator">=</span> <span class="token boolean">True</span></span>
<span class="line"></span>
<span class="line">ACCOUNT_EMAIL_VERIFICATION <span class="token operator">=</span> <span class="token string">"optional"</span></span>
<span class="line"></span>
<span class="line">ACCOUNT_USER_MODEL_USERNAME_FIELD <span class="token operator">=</span> <span class="token boolean">None</span></span>
<span class="line"></span>
<span class="line">ACCOUNT_SIGNUP_FIELDS <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line">    <span class="token string">"email"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"name"</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">]</span></span>
<span class="line"></span>
<span class="line">ACCOUNT_LOGIN_METHODS <span class="token operator">=</span> <span class="token punctuation">{</span></span>
<span class="line">    <span class="token string">"email"</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line">ACCOUNT_UNIQUE_EMAIL <span class="token operator">=</span> <span class="token boolean">True</span></span>
<span class="line"></span>
<span class="line">ACCOUNT_EMAIL_REQUIRED <span class="token operator">=</span> <span class="token boolean">True</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h4 id="🔄-redirect-configuration" tabindex="-1"><a class="header-anchor" href="#🔄-redirect-configuration"><span>🔄 Redirect Configuration</span></a></h4>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">LOGIN_REDIRECT_URL <span class="token operator">=</span> <span class="token string">"http://localhost:5173/auth/callback"</span></span>
<span class="line"></span>
<span class="line">LOGOUT_REDIRECT_URL <span class="token operator">=</span> <span class="token string">"/accounts/login/"</span></span>
<span class="line"></span>
<span class="line">ACCOUNT_LOGOUT_REDIRECT_URL <span class="token operator">=</span> <span class="token punctuation">(</span></span>
<span class="line">    <span class="token string">"http://localhost:5173/login"</span></span>
<span class="line"><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">ACCOUNT_SIGNUP_REDIRECT_URL <span class="token operator">=</span> <span class="token punctuation">(</span></span>
<span class="line">    <span class="token string">"http://localhost:5173"</span></span>
<span class="line"><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">SOCIALACCOUNT_LOGIN_REDIRECT_URL <span class="token operator">=</span> <span class="token punctuation">(</span></span>
<span class="line">    <span class="token string">"http://localhost:5173/auth-callback/"</span></span>
<span class="line"><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h4 id="📧-development-email-backend" tabindex="-1"><a class="header-anchor" href="#📧-development-email-backend"><span>📧 Development Email Backend</span></a></h4>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">EMAIL_BACKEND <span class="token operator">=</span> <span class="token punctuation">(</span></span>
<span class="line">    <span class="token string">"django.core.mail.backends.console.EmailBackend"</span></span>
<span class="line"><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h4 id="🕐-session-configuration" tabindex="-1"><a class="header-anchor" href="#🕐-session-configuration"><span>🕐 Session Configuration</span></a></h4>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">SESSION_COOKIE_AGE <span class="token operator">=</span> <span class="token number">60</span> <span class="token operator">*</span> <span class="token number">60</span> <span class="token operator">*</span> <span class="token number">24</span> <span class="token operator">*</span> <span class="token number">7</span>  <span class="token comment"># 7 أيام</span></span>
<span class="line"></span>
<span class="line">SESSION_SAVE_EVERY_REQUEST <span class="token operator">=</span> <span class="token boolean">True</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h4 id="🌐-cors-headers" tabindex="-1"><a class="header-anchor" href="#🌐-cors-headers"><span>🌐 CORS Headers</span></a></h4>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">CORS_ALLOW_HEADERS <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line">    <span class="token string">"accept"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"accept-encoding"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"authorization"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"content-type"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"dnt"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"origin"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"user-agent"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"x-csrftoken"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"x-requested-with"</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">]</span></span>
<span class="line"></span>
<span class="line">CORS_EXPOSE_HEADERS <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line">    <span class="token string">"Content-Type"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"X-CSRFToken"</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">]</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h3 id="_5-🚀-usage" tabindex="-1"><a class="header-anchor" href="#_5-🚀-usage"><span>5. 🚀 Usage</span></a></h3>
<h4 id="📧-email-authentication" tabindex="-1"><a class="header-anchor" href="#📧-email-authentication"><span>📧 Email Authentication</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>النظام هنا يعتمد على Email كطريقة تسجيل الدخول بدل Username.</p>
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">ACCOUNT_USER_MODEL_USERNAME_FIELD <span class="token operator">=</span> <span class="token boolean">None</span></span>
<span class="line"></span>
<span class="line">ACCOUNT_SIGNUP_FIELDS <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line">    <span class="token string">"email"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"name"</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">]</span></span>
<span class="line"></span>
<span class="line">ACCOUNT_LOGIN_METHODS <span class="token operator">=</span> <span class="token punctuation">{</span></span>
<span class="line">    <span class="token string">"email"</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line">ACCOUNT_UNIQUE_EMAIL <span class="token operator">=</span> <span class="token boolean">True</span></span>
<span class="line"></span>
<span class="line">ACCOUNT_EMAIL_REQUIRED <span class="token operator">=</span> <span class="token boolean">True</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h4 id="✉️-email-verification" tabindex="-1"><a class="header-anchor" href="#✉️-email-verification"><span>✉️ Email Verification</span></a></h4>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">ACCOUNT_EMAIL_VERIFICATION <span class="token operator">=</span> <span class="token string">"optional"</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>القيم المذكورة في الإعدادات:</p>
<ul>
<li><code v-pre>none</code> → من غير تحقق.</li>
<li><code v-pre>optional</code> → التحقق اختياري.</li>
<li><code v-pre>mandatory</code> → لازم المستخدم يتحقق عشان الحساب يتفعل.</li>
</ul>
<p>الإعداد المستخدم حاليًا في المحتوى هو:</p>
<p><code v-pre>optional</code></p>
</div>
<h4 id="🔵-google-oauth" tabindex="-1"><a class="header-anchor" href="#🔵-google-oauth"><span>🔵 Google OAuth</span></a></h4>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">SOCIALACCOUNT_PROVIDERS <span class="token operator">=</span> <span class="token punctuation">{</span></span>
<span class="line">    <span class="token string">"google"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span></span>
<span class="line">        <span class="token string">"APP"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span></span>
<span class="line">            <span class="token string">"client_id"</span><span class="token punctuation">:</span> config<span class="token punctuation">(</span><span class="token string">"GOOGLE_OAUTH_CLIENT_ID"</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">"secret"</span><span class="token punctuation">:</span> config<span class="token punctuation">(</span><span class="token string">"GOOGLE_OAUTH_CLIENT_SECRET"</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">"key"</span><span class="token punctuation">:</span> <span class="token string">""</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">"SCOPE"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span></span>
<span class="line">            <span class="token string">"profile"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">"email"</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token punctuation">]</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">"AUTH_PARAMS"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span></span>
<span class="line">            <span class="token string">"access_type"</span><span class="token punctuation">:</span> <span class="token string">"online"</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">"OAUTH_PKCE_ENABLED"</span><span class="token punctuation">:</span> <span class="token boolean">True</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>الـGoogle Provider يستخدم:</p>
<ul>
<li><code v-pre>profile</code></li>
<li><code v-pre>email</code></li>
</ul>
<p>والـOAuth configuration مفعّل فيها PKCE.</p>
</div>
<h4 id="👤-automatic-signup" tabindex="-1"><a class="header-anchor" href="#👤-automatic-signup"><span>👤 Automatic Signup</span></a></h4>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">SOCIALACCOUNT_AUTO_SIGNUP <span class="token operator">=</span> <span class="token boolean">True</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>ده يسمح بإنشاء الحساب تلقائيًا عند استخدام Social Authentication.</p>
</div>
<h4 id="🔌-custom-adapter" tabindex="-1"><a class="header-anchor" href="#🔌-custom-adapter"><span>🔌 Custom Adapter</span></a></h4>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">SOCIALACCOUNT_ADAPTER <span class="token operator">=</span> <span class="token punctuation">(</span></span>
<span class="line">    <span class="token string">"users_accounts.adapter.MySocialAccountAdapter"</span></span>
<span class="line"><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>الـCustom Adapter موجود ضمن تطبيق <code v-pre>users_accounts</code> ويتم استخدامه لتخصيص التعامل مع Social Accounts.</p>
</div>
<hr>
<h3 id="_6-📁-structure" tabindex="-1"><a class="header-anchor" href="#_6-📁-structure"><span>6. 📁 Structure</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>الملفات المرتبطة بالإعداد:</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">So_Iam_OS/</span>
<span class="line">│</span>
<span class="line">├── backend_django/</span>
<span class="line">│   ├── settings.py</span>
<span class="line">│   └── urls.py</span>
<span class="line">│</span>
<span class="line">├── users_accounts/</span>
<span class="line">│   └── adapter.py</span>
<span class="line">│</span>
<span class="line">├── .env</span>
<span class="line">│</span>
<span class="line">└── ...</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>المسؤوليات:</p>
<p><code v-pre>settings.py</code></p>
<p>إعداد django-allauth وGoogle OAuth والـSession والـRedirects.</p>
<p><code v-pre>urls.py</code></p>
<p>ربط URLs الخاصة بـallauth.</p>
<p><code v-pre>users_accounts/adapter.py</code></p>
<p>الـCustom Social Account Adapter.</p>
<p><code v-pre>.env</code></p>
<p>تخزين Environment Variables الحساسة.</p>
</div>
<hr>
<h3 id="_7-🧩-important-concepts" tabindex="-1"><a class="header-anchor" href="#_7-🧩-important-concepts"><span>7. 🧩 Important Concepts</span></a></h3>
<h4 id="🔐-environment-variables" tabindex="-1"><a class="header-anchor" href="#🔐-environment-variables"><span>🔐 Environment Variables</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>بدل ما نحط Google credentials مباشرة داخل <code v-pre>settings.py</code>، بنقرأها باستخدام <code v-pre>config()</code>.</p>
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">client_id <span class="token operator">=</span> config<span class="token punctuation">(</span><span class="token string">"GOOGLE_OAUTH_CLIENT_ID"</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">secret <span class="token operator">=</span> config<span class="token punctuation">(</span><span class="token string">"GOOGLE_OAUTH_CLIENT_SECRET"</span><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h4 id="🔑-oauth-pkce" tabindex="-1"><a class="header-anchor" href="#🔑-oauth-pkce"><span>🔑 OAuth PKCE</span></a></h4>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token string">"OAUTH_PKCE_ENABLED"</span><span class="token punctuation">:</span> <span class="token boolean">True</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>الإعداد ده بيفعّل PKCE ضمن OAuth flow المستخدم مع Google.</p>
</div>
<h4 id="🌐-redirect-urls" tabindex="-1"><a class="header-anchor" href="#🌐-redirect-urls"><span>🌐 Redirect URLs</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>بعد نجاح Login أو Logout، المستخدم يتم توجيهه إلى Frontend routes محددة.</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Login</span>
<span class="line">  ↓</span>
<span class="line">http://localhost:5173/auth/callback</span>
<span class="line"></span>
<span class="line">Logout</span>
<span class="line">  ↓</span>
<span class="line">http://localhost:5173/login</span>
<span class="line"></span>
<span class="line">Signup</span>
<span class="line">  ↓</span>
<span class="line">http://localhost:5173</span>
<span class="line"></span>
<span class="line">Social Login</span>
<span class="line">  ↓</span>
<span class="line">http://localhost:5173/auth-callback/</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h4 id="🕐-sessions" tabindex="-1"><a class="header-anchor" href="#🕐-sessions"><span>🕐 Sessions</span></a></h4>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">SESSION_COOKIE_AGE <span class="token operator">=</span> <span class="token number">60</span> <span class="token operator">*</span> <span class="token number">60</span> <span class="token operator">*</span> <span class="token number">24</span> <span class="token operator">*</span> <span class="token number">7</span></span>
<span class="line"></span>
<span class="line">SESSION_SAVE_EVERY_REQUEST <span class="token operator">=</span> <span class="token boolean">True</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>الإعدادات دي مرتبطة بإدارة Django Session.</p>
</div>
<h4 id="🌍-cors" tabindex="-1"><a class="header-anchor" href="#🌍-cors"><span>🌍 CORS</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>CORS يسمح للـFrontend والـBackend بالتعامل مع بعض عبر HTTP عندما تكون origins مختلفة.</p>
</div>
<hr>
<h3 id="_8-💻-examples" tabindex="-1"><a class="header-anchor" href="#_8-💻-examples"><span>8. 💻 Examples</span></a></h3>
<h4 id="🔐-environment-configuration" tabindex="-1"><a class="header-anchor" href="#🔐-environment-configuration"><span>🔐 Environment Configuration</span></a></h4>
<div class="language-env line-numbers-mode" data-highlighter="prismjs" data-ext="env"><pre v-pre><code><span class="line">GOOGLE_OAUTH_CLIENT_ID=YOUR_GOOGLE_CLIENT_ID</span>
<span class="line">GOOGLE_OAUTH_CLIENT_SECRET=YOUR_GOOGLE_CLIENT_SECRET</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div></div></div><h4 id="🐍-django-settings" tabindex="-1"><a class="header-anchor" href="#🐍-django-settings"><span>🐍 Django Settings</span></a></h4>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">from</span> decouple <span class="token keyword">import</span> config</span>
<span class="line"></span>
<span class="line">SOCIALACCOUNT_PROVIDERS <span class="token operator">=</span> <span class="token punctuation">{</span></span>
<span class="line">    <span class="token string">"google"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span></span>
<span class="line">        <span class="token string">"APP"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span></span>
<span class="line">            <span class="token string">"client_id"</span><span class="token punctuation">:</span> config<span class="token punctuation">(</span><span class="token string">"GOOGLE_OAUTH_CLIENT_ID"</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">"secret"</span><span class="token punctuation">:</span> config<span class="token punctuation">(</span><span class="token string">"GOOGLE_OAUTH_CLIENT_SECRET"</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">"key"</span><span class="token punctuation">:</span> <span class="token string">""</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">"SCOPE"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span></span>
<span class="line">            <span class="token string">"profile"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">"email"</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token punctuation">]</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">"AUTH_PARAMS"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span></span>
<span class="line">            <span class="token string">"access_type"</span><span class="token punctuation">:</span> <span class="token string">"online"</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">"OAUTH_PKCE_ENABLED"</span><span class="token punctuation">:</span> <span class="token boolean">True</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h4 id="🔄-redirects" tabindex="-1"><a class="header-anchor" href="#🔄-redirects"><span>🔄 Redirects</span></a></h4>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">LOGIN_REDIRECT_URL <span class="token operator">=</span> <span class="token punctuation">(</span></span>
<span class="line">    <span class="token string">"http://localhost:5173/auth/callback"</span></span>
<span class="line"><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">ACCOUNT_LOGOUT_REDIRECT_URL <span class="token operator">=</span> <span class="token punctuation">(</span></span>
<span class="line">    <span class="token string">"http://localhost:5173/login"</span></span>
<span class="line"><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">ACCOUNT_SIGNUP_REDIRECT_URL <span class="token operator">=</span> <span class="token punctuation">(</span></span>
<span class="line">    <span class="token string">"http://localhost:5173"</span></span>
<span class="line"><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">SOCIALACCOUNT_LOGIN_REDIRECT_URL <span class="token operator">=</span> <span class="token punctuation">(</span></span>
<span class="line">    <span class="token string">"http://localhost:5173/auth-callback/"</span></span>
<span class="line"><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h4 id="🧪-development-debugging" tabindex="-1"><a class="header-anchor" href="#🧪-development-debugging"><span>🧪 Development Debugging</span></a></h4>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string">"✅ Settings loaded Django"</span><span class="token punctuation">)</span></span>
<span class="line"><span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string-interpolation"><span class="token string">f"✅ AUTH_USER_MODEL: </span><span class="token interpolation"><span class="token punctuation">{</span>AUTH_USER_MODEL<span class="token punctuation">}</span></span><span class="token string">"</span></span><span class="token punctuation">)</span></span>
<span class="line"><span class="token keyword">print</span><span class="token punctuation">(</span></span>
<span class="line">    <span class="token string-interpolation"><span class="token string">f"✅ SOCIALACCOUNT_ADAPTER: "</span></span></span>
<span class="line">    <span class="token string-interpolation"><span class="token string">f"</span><span class="token interpolation"><span class="token punctuation">{</span>SOCIALACCOUNT_ADAPTER<span class="token punctuation">}</span></span><span class="token string">"</span></span></span>
<span class="line"><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>الـprint statements دي مفيدة أثناء Development للتأكد إن <code v-pre>settings.py</code> اتحمل وإن الإعدادات الأساسية موجودة.</p>
</div>
<hr>
<h3 id="_9-❌-common-mistakes" tabindex="-1"><a class="header-anchor" href="#_9-❌-common-mistakes"><span>9. ❌ Common Mistakes</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>أهم الأخطاء:</p>
<ol>
<li>وضع Google Client Secret مباشرة داخل <code v-pre>settings.py</code>.</li>
<li>رفع <code v-pre>.env</code> إلى Git.</li>
<li>نسيان <code v-pre>allauth.socialaccount.providers.google</code>.</li>
<li>نسيان <code v-pre>django.contrib.sites</code>.</li>
<li>نسيان <code v-pre>SITE_ID</code>.</li>
<li>نسيان <code v-pre>AccountMiddleware</code>.</li>
<li>نسيان ربط <code v-pre>allauth.urls</code>.</li>
<li>استخدام Redirect URL مختلف عن المسجل في Google OAuth.</li>
<li>استخدام <code v-pre>localhost</code> URLs في Production بدون تعديلها.</li>
<li>عدم ضبط CORS عند وجود Frontend منفصل.</li>
<li>عدم وجود <code v-pre>users_accounts.adapter.MySocialAccountAdapter</code> مع تفعيل هذا المسار.</li>
<li>الاعتماد على Console Email Backend في Production.</li>
</ol>
</div>
<hr>
<h3 id="_10-🧠-why" tabindex="-1"><a class="header-anchor" href="#_10-🧠-why"><span>10. 🧠 Why?</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>ليه بنستخدم <code v-pre>config()</code>؟</p>
<p>عشان نفصل الـSecrets عن Source Code.</p>
<p>بدل:</p>
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token string">"secret"</span><span class="token punctuation">:</span> <span class="token string">"REAL_SECRET"</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>نستخدم:</p>
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token string">"secret"</span><span class="token punctuation">:</span> config<span class="token punctuation">(</span><span class="token string">"GOOGLE_OAUTH_CLIENT_SECRET"</span><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>وبالتالي الـSecret يكون خارج الكود.</p>
<p>وليه بنستخدم Redirect URLs؟</p>
<p>لأن Authentication Flow محتاج يعرف المستخدم يرجع لفين بعد انتهاء العملية.</p>
<p>وليه بنستخدم Custom Adapter؟</p>
<p>لأن المشروع ممكن يحتاج Logic خاص أثناء إنشاء أو ربط Social Account، بدل الاعتماد على السلوك الافتراضي فقط.</p>
</div>
<hr>
<h3 id="_11-🔗-project-usage" tabindex="-1"><a class="header-anchor" href="#_11-🔗-project-usage"><span>11. 🔗 Project Usage</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>داخل <strong>So_Iam_OS</strong>، الإعدادات دي بتربط Backend Django بالـFrontend Vue عن طريق Authentication Flow.</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Vue Frontend</span>
<span class="line">     │</span>
<span class="line">     ▼</span>
<span class="line">Django Backend</span>
<span class="line">     │</span>
<span class="line">     ▼</span>
<span class="line">django-allauth</span>
<span class="line">     │</span>
<span class="line">     ├──────────────┐</span>
<span class="line">     ▼              ▼</span>
<span class="line">   Email         Google</span>
<span class="line">     │              │</span>
<span class="line">     └──────┬───────┘</span>
<span class="line">            ▼</span>
<span class="line">       User Identity</span>
<span class="line">            │</span>
<span class="line">            ▼</span>
<span class="line">     users_accounts</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>الـFrontend المستخدم في الإعدادات الحالية يعمل على:</p>
<p><code v-pre>http://localhost:5173</code></p>
</div>
<hr>
<h3 id="_12-🤖-ai-reference" tabindex="-1"><a class="header-anchor" href="#_12-🤖-ai-reference"><span>12. 🤖 AI Reference</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>عند تعامل الـAI مع إعدادات <code v-pre>django-allauth</code> داخل المشروع، لازم يعرف الآتي:</p>
<ul>
<li><code v-pre>django-allauth</code> مسؤول عن Account + Social Authentication.</li>
<li>Login Method هو Email.</li>
<li>Google هو Social Provider.</li>
<li>Google credentials يتم قراءتها من Environment Variables.</li>
<li><code v-pre>python-decouple</code> مستخدم لقراءة الـEnvironment Variables.</li>
<li>PKCE مفعّل في Google OAuth.</li>
<li><code v-pre>SOCIALACCOUNT_AUTO_SIGNUP = True</code>.</li>
<li>يوجد Custom Adapter.</li>
<li>الـCustom Adapter مساره <code v-pre>users_accounts.adapter.MySocialAccountAdapter</code>.</li>
<li>Frontend Development URL هو <code v-pre>http://localhost:5173</code>.</li>
<li>Email Backend الحالي هو Console Email Backend.</li>
<li>Session Age مضبوطة على 7 أيام.</li>
<li>CORS Headers محددة في settings.</li>
<li><code v-pre>settings.py</code> هو مركز إعدادات allauth.</li>
<li><code v-pre>urls.py</code> يربط <code v-pre>allauth.urls</code> تحت <code v-pre>/accounts/</code>.</li>
</ul>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Project:</span>
<span class="line">So_Iam_OS</span>
<span class="line"></span>
<span class="line">Technology:</span>
<span class="line">django-allauth</span>
<span class="line"></span>
<span class="line">Dependency:</span>
<span class="line">python-decouple</span>
<span class="line"></span>
<span class="line">Authentication:</span>
<span class="line">- Email</span>
<span class="line">- Google OAuth</span>
<span class="line"></span>
<span class="line">Google Credentials:</span>
<span class="line">- Environment Variables</span>
<span class="line"></span>
<span class="line">Google Scope:</span>
<span class="line">- profile</span>
<span class="line">- email</span>
<span class="line"></span>
<span class="line">OAuth:</span>
<span class="line">- PKCE Enabled</span>
<span class="line">- access_type = online</span>
<span class="line"></span>
<span class="line">Frontend:</span>
<span class="line">http://localhost:5173</span>
<span class="line"></span>
<span class="line">Custom Adapter:</span>
<span class="line">users_accounts.adapter.MySocialAccountAdapter</span>
<span class="line"></span>
<span class="line">Email Backend:</span>
<span class="line">django.core.mail.backends.console.EmailBackend</span>
<span class="line"></span>
<span class="line">Session:</span>
<span class="line">- 7 Days</span>
<span class="line">- SAVE_EVERY_REQUEST = True</span>
<span class="line"></span>
<span class="line">URL Prefix:</span>
<span class="line"> /accounts/</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h3 id="_13-📊-current-status" tabindex="-1"><a class="header-anchor" href="#_13-📊-current-status"><span>13. 📊 Current Status</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>الحالة هنا تمثل التنفيذ الفعلي داخل المشروع، وليس مجرد وجود الكود داخل ملف المعرفة.</p>
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
<td>Install <code v-pre>django-allauth</code></td>
<td>⬜</td>
</tr>
<tr>
<td>Install <code v-pre>python-decouple</code></td>
<td>⬜</td>
</tr>
<tr>
<td>Configure <code v-pre>INSTALLED_APPS</code></td>
<td>⬜</td>
</tr>
<tr>
<td>Add <code v-pre>AccountMiddleware</code></td>
<td>⬜</td>
</tr>
<tr>
<td>Configure Email Authentication</td>
<td>⬜</td>
</tr>
<tr>
<td>Configure Email Verification</td>
<td>⬜</td>
</tr>
<tr>
<td>Configure Google OAuth</td>
<td>⬜</td>
</tr>
<tr>
<td>Configure Google Environment Variables</td>
<td>⬜</td>
</tr>
<tr>
<td>Enable OAuth PKCE</td>
<td>⬜</td>
</tr>
<tr>
<td>Configure <code v-pre>SITE_ID</code></td>
<td>⬜</td>
</tr>
<tr>
<td>Configure Social Auto Signup</td>
<td>⬜</td>
</tr>
<tr>
<td>Configure Custom Adapter</td>
<td>⬜</td>
</tr>
<tr>
<td>Configure Redirect URLs</td>
<td>⬜</td>
</tr>
<tr>
<td>Configure Session</td>
<td>⬜</td>
</tr>
<tr>
<td>Configure CORS Headers</td>
<td>⬜</td>
</tr>
<tr>
<td>Configure Email Backend</td>
<td>⬜</td>
</tr>
<tr>
<td>Connect <code v-pre>allauth.urls</code></td>
<td>⬜</td>
</tr>
<tr>
<td>Test Email Authentication</td>
<td>⬜</td>
</tr>
<tr>
<td>Test Google Authentication</td>
<td>⬜</td>
</tr>
<tr>
<td>Test Frontend Callback</td>
<td>⬜</td>
</tr>
<tr>
<td>Production Configuration</td>
<td>⬜</td>
</tr>
</tbody>
</table>
<hr>
<h3 id="_14-✅-checklist" tabindex="-1"><a class="header-anchor" href="#_14-✅-checklist"><span>14. ✅ Checklist</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>قائمة تنفيذ ومراجعة <code v-pre>django-allauth</code>:</p>
</div>
<ul>
<li>[ ] Install <code v-pre>django-allauth</code></li>
<li>[ ] Install <code v-pre>python-decouple</code></li>
<li>[ ] Add <code v-pre>django.contrib.sites</code></li>
<li>[ ] Add <code v-pre>allauth</code></li>
<li>[ ] Add <code v-pre>allauth.account</code></li>
<li>[ ] Add <code v-pre>allauth.socialaccount</code></li>
<li>[ ] Add Google Provider</li>
<li>[ ] Add <code v-pre>AccountMiddleware</code></li>
<li>[ ] Configure Email Authentication</li>
<li>[ ] Configure Email Verification</li>
<li>[ ] Configure Google OAuth</li>
<li>[ ] Add Google credentials to Environment Variables</li>
<li>[ ] Enable PKCE</li>
<li>[ ] Configure <code v-pre>SITE_ID</code></li>
<li>[ ] Enable Social Auto Signup</li>
<li>[ ] Configure Custom Adapter</li>
<li>[ ] Configure Login Redirect</li>
<li>[ ] Configure Logout Redirect</li>
<li>[ ] Configure Signup Redirect</li>
<li>[ ] Configure Social Login Redirect</li>
<li>[ ] Configure Session</li>
<li>[ ] Configure CORS</li>
<li>[ ] Configure Development Email Backend</li>
<li>[ ] Connect <code v-pre>allauth.urls</code></li>
<li>[ ] Run migrations</li>
<li>[ ] Test Email Authentication</li>
<li>[ ] Test Google OAuth</li>
<li>[ ] Test Frontend Callback</li>
<li>[ ] Review Production Security</li>
</ul>
<hr>
<h3 id="_15-🔗-related-documentation" tabindex="-1"><a class="header-anchor" href="#_15-🔗-related-documentation"><span>15. 🔗 Related Documentation</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>الملفات والمواضيع المرتبطة:</p>
</div>
<ul>
<li><code v-pre>backend_django/settings.py</code></li>
<li><code v-pre>backend_django/urls.py</code></li>
<li><code v-pre>users_accounts/</code></li>
<li><code v-pre>users_accounts/adapter.py</code></li>
<li>Django Authentication</li>
<li>Django Sites Framework</li>
<li>Google OAuth</li>
<li>OAuth PKCE</li>
<li><code v-pre>python-decouple</code></li>
<li>Environment Variables</li>
<li>CORS</li>
<li>Django Sessions</li>
<li>Django REST Framework</li>
<li>SimpleJWT</li>
</ul>
<hr>
<h3 id="_16-📝-notes" tabindex="-1"><a class="header-anchor" href="#_16-📝-notes"><span>16. 📝 Notes</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>الإعداد الحالي يمثل Development Configuration لأن الـFrontend يستخدم:</p>
<p><code v-pre>http://localhost:5173</code></p>
<p>وكمان Email Backend الحالي هو Console Backend.</p>
<p>لذلك لا يتم اعتبار الإعداد الحالي Production Configuration.</p>
<p>كمان الـGoogle Client ID والـClient Secret الموجودين في النص الأصلي تم استبدالهم في ملف المعرفة بـPlaceholders.</p>
<p>لو كانت القيم الأصلية حقيقية وتم نشرها أو مشاركتها، الأفضل اعتبار الـSecret مكشوفًا وعمل Rotation / Regeneration له.</p>
<p>المعماريًا، <code v-pre>django-allauth</code> مسؤول عن:</p>
<p><strong>Account + Social Authentication</strong></p>
<p>بينما Authentication الخاصة بالـREST API يمكن فصلها في طبقة أخرى مثل:</p>
<p><strong>SimpleJWT</strong></p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">So_Iam_OS</span>
<span class="line">    │</span>
<span class="line">    ├── Frontend</span>
<span class="line">    │      └── Vue</span>
<span class="line">    │</span>
<span class="line">    └── Backend</span>
<span class="line">           │</span>
<span class="line">           └── Django</span>
<span class="line">                 │</span>
<span class="line">                 └── django-allauth</span>
<span class="line">                       │</span>
<span class="line">                       ├── Email</span>
<span class="line">                       │</span>
<span class="line">                       └── Google OAuth</span>
<span class="line">                              │</span>
<span class="line">                              ▼</span>
<span class="line">                         User Identity</span>
<span class="line">                              │</span>
<span class="line">                              ▼</span>
<span class="line">                       users_accounts</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div></div></template>


