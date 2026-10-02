<template><div><h1 id="debug" tabindex="-1"><a class="header-anchor" href="#debug"><span>Debug</span></a></h1>
<h2 id="why" tabindex="-1"><a class="header-anchor" href="#why"><span>Why</span></a></h2>
<div class="" dir="rtl">
<p>1️⃣ لماذا نستخدم Django Debug Toolbar؟</p>
<p>تحليل الأداء: بيوريك الوقت المستغرق لكل view و SQL queries.</p>
<p>تصحيح الأخطاء: يوضح تفاصيل request/response headers، context variables، templates المستخدمة.</p>
<p>تحسين الاستعلامات: بتشوف استعلامات الـ ORM وتقدر تقلل الـ queries الغير ضرورية.</p>
<p>مفيد أثناء التطوير فقط: لا تستخدمه في الإنتاج (security &amp; performance).</p>
</div>
<h2 id="need" tabindex="-1"><a class="header-anchor" href="#need"><span>Need</span></a></h2>
<div class="" dir="rtl">
  2️⃣ ما المطلوب لتشغيله؟
<p>مشروع Django شغال محليًا (Backend فقط).</p>
<p>Python environment مفعل.</p>
<p>Vue frontend ممكن شغال على dev server (localhost:5173 أو port آخر).</p>
<p>DEBUG = True في settings.py.</p>
<p>ملاحظة: Django Debug Toolbar يعمل فقط مع Django، فهو لا يتكامل مباشرة مع Vue لأنه لا يتحكم في واجهة Vue، لكنه يعرض كل request/response من Django REST API لو Vue تطلب البيانات منه.</p>
</div>
<h2 id="install" tabindex="-1"><a class="header-anchor" href="#install"><span>Install</span></a></h2>
<div class="" dir="rtl">
  3️⃣ خطوات تثبيت وإعداد Django Debug Toolbar
<p>A) تثبيت الحزمة</p>
</div>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip install django-debug-toolbar</span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div></div></div><h2 id="settings" tabindex="-1"><a class="header-anchor" href="#settings"><span>settings</span></a></h2>
<div class="" dir="rtl">
  B) تحديث settings.py
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># settings.py</span></span>
<span class="line"></span>
<span class="line">INSTALLED_APPS <span class="token operator">+=</span> <span class="token punctuation">[</span></span>
<span class="line">    <span class="token string">'debug_toolbar'</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">]</span></span>
<span class="line"></span>
<span class="line">MIDDLEWARE <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line">    <span class="token comment"># لازم قبل CommonMiddleware</span></span>
<span class="line">    <span class="token string">'debug_toolbar.middleware.DebugToolbarMiddleware'</span><span class="token punctuation">,</span></span>
<span class="line"></span>
<span class="line"><span class="token punctuation">]</span></span>
<span class="line"></span>
<span class="line"><span class="token comment"># Debug Toolbar settings</span></span>
<span class="line">INTERNAL_IPS <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line">    <span class="token string">'127.0.0.1'</span><span class="token punctuation">,</span>  <span class="token comment"># لو شغال محلي</span></span>
<span class="line">    <span class="token string">'localhost'</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">]</span></span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h2 id="urls" tabindex="-1"><a class="header-anchor" href="#urls"><span>urls</span></a></h2>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># 📄 [ backend_django/urls.py ] ملف</span></span>
<span class="line"></span>
<span class="line"><span class="token keyword">from</span> django<span class="token punctuation">.</span>contrib <span class="token keyword">import</span> admin</span>
<span class="line"></span>
<span class="line"><span class="token keyword">from</span> debug_toolbar<span class="token punctuation">.</span>toolbar <span class="token keyword">import</span> debug_toolbar_urls</span>
<span class="line"></span>
<span class="line"></span>
<span class="line">urlpatterns <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line">    <span class="token comment"># Admin</span></span>
<span class="line">    path<span class="token punctuation">(</span><span class="token string">'admin/'</span><span class="token punctuation">,</span> admin<span class="token punctuation">.</span>site<span class="token punctuation">.</span>urls<span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line"></span>
<span class="line"><span class="token punctuation">]</span> <span class="token operator">+</span> debug_toolbar_urls<span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div></div></template>


