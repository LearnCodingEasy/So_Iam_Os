<template><div><h2 id="django" tabindex="-1"><a class="header-anchor" href="#django"><span>Django</span></a></h2>
<div dir="rtl" style="font-size:2vw">
<ol>
<li>الاعدادات الخاصة بمشروع Django الأساسي</li>
</ol>
</div>
<div dir="rtl" style="font-size:1.5vw">
<ul>
<li>
<p>قائمة النطاقات أو العناوين المسموح للسيرفر يستقبل طلبات منها (لحماية الأمان).</p>
</li>
<li>
<p>Backends - إعدادات المصادقة</p>
<ul>
<li>
<p>هذه قائمة طرق المصادقة التي يقبلها النظام.</p>
</li>
<li>
<p>ModelBackend يدير تسجيل الدخول التقليدي بالبريد أو اسم المستخدم.</p>
</li>
<li>
<p>AuthenticationBackend من allauth يدير تسجيل الدخول الاجتماعي (Google، Facebook...).</p>
</li>
</ul>
</li>
<li>
<p>CSRF_TRUSTED_ORIGINS : عناوين يُسمح لها بتجاوز حماية CSRF (مهمة لتجربة الAPI من المتصفح).</p>
</li>
<li>
<p>CORS_ALLOW_ALL_ORIGINS = True : تسمح لجميع المواقع بطلبات CORS (غير آمن للإنتاج).</p>
</li>
<li>
<p>CSRF_COOKIE_SECURE و SESSION_COOKIE_SECURE: تعطيل خاصية التشفير على الكوكيز (مناسب للتطوير فقط).</p>
</li>
</ul>
</div>
<h3 id="_2️⃣-setup-🛠️" tabindex="-1"><a class="header-anchor" href="#_2️⃣-setup-🛠️"><span>2️⃣ Setup 🛠️</span></a></h3>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># ______________ 📺 __________________</span></span>
<span class="line"><span class="token comment"># أثناء التطوير</span></span>
<span class="line"><span class="token comment"># للسماح بكل الطلبات أثناء التطوير</span></span>
<span class="line"><span class="token comment"># لجهاز الكمبيوتر. IP استبدل 192.168.1.5 بعنوان</span></span>
<span class="line"></span>
<span class="line">ALLOWED_HOSTS <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token string">"localhost"</span><span class="token punctuation">,</span> <span class="token string">"127.0.0.1"</span><span class="token punctuation">,</span> <span class="token string">"192.168.1.5"</span><span class="token punctuation">]</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># (AUTHENTICATION_BACKENDS) إعداد المصادقة</span></span>
<span class="line"></span>
<span class="line">AUTHENTICATION_BACKENDS <span class="token operator">=</span> <span class="token punctuation">(</span></span>
<span class="line">    <span class="token comment"># تسجيل الدخول التقليدي</span></span>
<span class="line">    <span class="token string">"django.contrib.auth.backends.ModelBackend"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token comment"># تسجيل الدخول عبر مواقع التواصل</span></span>
<span class="line">    <span class="token string">"allauth.account.auth_backends.AuthenticationBackend"</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># Allow CSRF requests from specific addresses</span></span>
<span class="line"></span>
<span class="line">CSRF_TRUSTED_ORIGINS <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line">    <span class="token string">"http://localhost:5173"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"http://localhost:5174"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"http://192.168.1.5:5173"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"http://192.168.1.5:5174"</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">]</span></span>
<span class="line"></span>
<span class="line">CORS_ALLOW_ALL_ORIGINS <span class="token operator">=</span> <span class="token boolean">True</span></span>
<span class="line"></span>
<span class="line">CSRF_COOKIE_SECURE <span class="token operator">=</span> <span class="token boolean">False</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line">SESSION_COOKIE_SECURE <span class="token operator">=</span> <span class="token boolean">False</span></span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div></div></template>


