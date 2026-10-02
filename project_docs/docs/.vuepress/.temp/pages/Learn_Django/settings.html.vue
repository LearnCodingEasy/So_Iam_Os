<template><div><h1 id="setting" tabindex="-1"><a class="header-anchor" href="#setting"><span>Setting</span></a></h1>
<h2 id="path" tabindex="-1"><a class="header-anchor" href="#path"><span>Path</span></a></h2>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">from</span> pathlib <span class="token keyword">import</span> Path</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h2 id="base-dir" tabindex="-1"><a class="header-anchor" href="#base-dir"><span>BASE_DIR</span></a></h2>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">BASE_DIR <span class="token operator">=</span> Path<span class="token punctuation">(</span>__file__<span class="token punctuation">)</span><span class="token punctuation">.</span>resolve<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span>parent<span class="token punctuation">.</span>parent</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h2 id="secret-key" tabindex="-1"><a class="header-anchor" href="#secret-key"><span>SECRET_KEY</span></a></h2>
<div class="" dir="rtl"></div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># Default</span></span>
<span class="line">SECRET_KEY <span class="token operator">=</span> <span class="token string">'************'</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div></div></div><div class="" dir="rtl">
المكتبة دي مفيدة جدًا عشان تفصل المعلومات الحساسة (زي الـ SECRET_KEY، بيانات قواعد البيانات، API keys، …) عن كود المشروع نفسه.
</div>
<p><RouteLink to="/Learn_Django/decouple.html">Decouple</RouteLink></p>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">from</span> decouple <span class="token keyword">import</span> config</span>
<span class="line"></span>
<span class="line">SECRET_KEY <span class="token operator">=</span> config<span class="token punctuation">(</span><span class="token string">'SECRET_KEY'</span><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h2 id="debug" tabindex="-1"><a class="header-anchor" href="#debug"><span>DEBUG</span></a></h2>
<div class="" dir="rtl">
تحذير أمني: لا تعمل مع تشغيل تصحيح الأخطاء في الإنتاج!
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># Default</span></span>
<span class="line">DEBUG <span class="token operator">=</span> <span class="token boolean">True</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div></div></div><div class="" dir="rtl">
المكتبة دي مفيدة جدًا عشان تفصل المعلومات الحساسة (زي الـ SECRET_KEY، بيانات قواعد البيانات، API keys، …) عن كود المشروع نفسه.
</div>
<p><RouteLink to="/Learn_Django/decouple.html">Decouple</RouteLink></p>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">from</span> decouple <span class="token keyword">import</span> config</span>
<span class="line">DEBUG <span class="token operator">=</span> config<span class="token punctuation">(</span><span class="token string">'DEBUG'</span><span class="token punctuation">,</span> default<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">,</span> cast<span class="token operator">=</span><span class="token builtin">bool</span><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div></div></div><h2 id="allowed-hosts" tabindex="-1"><a class="header-anchor" href="#allowed-hosts"><span>ALLOWED_HOSTS</span></a></h2>
<div class="" dir="rtl">
<p>ALLOWED_HOSTS ده المتغير اللي بنحدد فيه الدومينات أو الآيبيهات اللي مسموح لها تشغل المشروع</p>
<p>للسماح بكل الطلبات أثناء التطوير</p>
<p>استبدل 192.168.1.5 بعنوان IP لجهاز الكمبيوتر.</p>
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># Default</span></span>
<span class="line">ALLOWED_HOSTS <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token punctuation">]</span></span>
<span class="line"><span class="token comment"># ______________ 📺 __________________</span></span>
<span class="line"><span class="token comment"># My Code</span></span>
<span class="line"><span class="token comment"># ALLOWED_HOSTS = ['*']</span></span>
<span class="line"><span class="token comment"># ALLOWED_HOSTS = ['127.0.0.1']</span></span>
<span class="line"><span class="token comment"># ALLOWED_HOSTS = [</span></span>
<span class="line"><span class="token comment">#     "localhost",</span></span>
<span class="line"><span class="token comment">#     "127.0.0.1",</span></span>
<span class="line"><span class="token comment">#     "192.168.1.5",</span></span>
<span class="line"><span class="token comment">#     '0.0.0.0'</span></span>
<span class="line"><span class="token comment">## Firebase يسمح بجميع نطاقات</span></span>
<span class="line"><span class="token comment">#     ".firebaseapp.com",</span></span>
<span class="line"><span class="token comment">## Firebase Hosting يسمح باستضافة</span></span>
<span class="line"><span class="token comment">#     ".web.app",</span></span>
<span class="line"><span class="token comment"># ]</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h2 id="installed-apps" tabindex="-1"><a class="header-anchor" href="#installed-apps"><span>INSTALLED_APPS</span></a></h2>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">INSTALLED_APPS <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line">  <span class="token comment"># Default</span></span>
<span class="line">  <span class="token string">'django.contrib.admin'</span><span class="token punctuation">,</span></span>
<span class="line">  <span class="token string">'django.contrib.auth'</span><span class="token punctuation">,</span></span>
<span class="line">  <span class="token string">'django.contrib.contenttypes'</span><span class="token punctuation">,</span></span>
<span class="line">  <span class="token string">'django.contrib.sessions'</span><span class="token punctuation">,</span></span>
<span class="line">  <span class="token string">'django.contrib.messages'</span><span class="token punctuation">,</span></span>
<span class="line">  <span class="token string">'django.contrib.staticfiles'</span><span class="token punctuation">,</span></span>
<span class="line"></span>
<span class="line">    <span class="token comment"># ...</span></span>
<span class="line">    <span class="token comment"># My Apps</span></span>
<span class="line">    <span class="token string">'users_accounts'</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token comment"># ...</span></span>
<span class="line">    <span class="token comment"># Libraries</span></span>
<span class="line">    <span class="token string">'rest_framework'</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">'corsheaders'</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token comment"># ...</span></span>
<span class="line"><span class="token punctuation">]</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h2 id="middleware" tabindex="-1"><a class="header-anchor" href="#middleware"><span>MIDDLEWARE</span></a></h2>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">MIDDLEWARE <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line">    <span class="token comment"># Default</span></span>
<span class="line">    <span class="token string">'django.middleware.security.SecurityMiddleware'</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">'django.contrib.sessions.middleware.SessionMiddleware'</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">'django.middleware.common.CommonMiddleware'</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">'django.middleware.csrf.CsrfViewMiddleware'</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">'django.contrib.auth.middleware.AuthenticationMiddleware'</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">'django.contrib.messages.middleware.MessageMiddleware'</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">'django.middleware.clickjacking.XFrameOptionsMiddleware'</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">]</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h2 id="root-urlconf" tabindex="-1"><a class="header-anchor" href="#root-urlconf"><span>ROOT_URLCONF</span></a></h2>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">ROOT_URLCONF <span class="token operator">=</span> <span class="token string">'backend_django.urls'</span></span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div></div></div><h2 id="templates" tabindex="-1"><a class="header-anchor" href="#templates"><span>TEMPLATES</span></a></h2>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">TEMPLATES <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line">    <span class="token punctuation">{</span></span>
<span class="line">        <span class="token string">'BACKEND'</span><span class="token punctuation">:</span> <span class="token string">'django.template.backends.django.DjangoTemplates'</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token comment"># Default</span></span>
<span class="line">        <span class="token string">'DIRS'</span><span class="token punctuation">:</span> <span class="token punctuation">[</span><span class="token punctuation">]</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">'APP_DIRS'</span><span class="token punctuation">:</span> <span class="token boolean">True</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">'OPTIONS'</span><span class="token punctuation">:</span> <span class="token punctuation">{</span></span>
<span class="line">            <span class="token string">'context_processors'</span><span class="token punctuation">:</span> <span class="token punctuation">[</span></span>
<span class="line">                <span class="token string">'django.template.context_processors.debug'</span><span class="token punctuation">,</span></span>
<span class="line">                <span class="token string">'django.template.context_processors.request'</span><span class="token punctuation">,</span></span>
<span class="line">                <span class="token string">'django.contrib.auth.context_processors.auth'</span><span class="token punctuation">,</span></span>
<span class="line">                <span class="token string">'django.contrib.messages.context_processors.messages'</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token punctuation">]</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">]</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h2 id="wsgi-application" tabindex="-1"><a class="header-anchor" href="#wsgi-application"><span>WSGI_APPLICATION</span></a></h2>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">WSGI_APPLICATION <span class="token operator">=</span> <span class="token string">'backend.wsgi.application'</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h2 id="databases" tabindex="-1"><a class="header-anchor" href="#databases"><span>DATABASES</span></a></h2>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">DATABASES <span class="token operator">=</span> <span class="token punctuation">{</span></span>
<span class="line">    <span class="token comment"># Default</span></span>
<span class="line">    <span class="token string">'default'</span><span class="token punctuation">:</span> <span class="token punctuation">{</span></span>
<span class="line">        <span class="token string">'ENGINE'</span><span class="token punctuation">:</span> <span class="token string">'django.db.backends.sqlite3'</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">'NAME'</span><span class="token punctuation">:</span> BASE_DIR <span class="token operator">/</span> <span class="token string">'db.sqlite3'</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">}</span></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h2 id="auth-password-validators" tabindex="-1"><a class="header-anchor" href="#auth-password-validators"><span>AUTH_PASSWORD_VALIDATORS</span></a></h2>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">AUTH_PASSWORD_VALIDATORS <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line">    <span class="token punctuation">{</span></span>
<span class="line">        <span class="token string">'NAME'</span><span class="token punctuation">:</span> <span class="token string">'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">{</span></span>
<span class="line">        <span class="token string">'NAME'</span><span class="token punctuation">:</span> <span class="token string">'django.contrib.auth.password_validation.MinimumLengthValidator'</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">{</span></span>
<span class="line">        <span class="token string">'NAME'</span><span class="token punctuation">:</span> <span class="token string">'django.contrib.auth.password_validation.CommonPasswordValidator'</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">{</span></span>
<span class="line">        <span class="token string">'NAME'</span><span class="token punctuation">:</span> <span class="token string">'django.contrib.auth.password_validation.NumericPasswordValidator'</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">]</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h2 id="internationalization" tabindex="-1"><a class="header-anchor" href="#internationalization"><span>Internationalization</span></a></h2>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">LANGUAGE_CODE <span class="token operator">=</span> <span class="token string">'en-us'</span></span>
<span class="line">TIME_ZONE <span class="token operator">=</span> <span class="token string">'UTC'</span></span>
<span class="line">USE_I18N <span class="token operator">=</span> <span class="token boolean">True</span></span>
<span class="line">USE_TZ <span class="token operator">=</span> <span class="token boolean">True</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h2 id="static-url" tabindex="-1"><a class="header-anchor" href="#static-url"><span>STATIC_URL</span></a></h2>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">STATIC_URL <span class="token operator">=</span> <span class="token string">'static/'</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h2 id="default-auto-field" tabindex="-1"><a class="header-anchor" href="#default-auto-field"><span>DEFAULT_AUTO_FIELD</span></a></h2>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">DEFAULT_AUTO_FIELD <span class="token operator">=</span> <span class="token string">'django.db.models.BigAutoField'</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div></div></template>


