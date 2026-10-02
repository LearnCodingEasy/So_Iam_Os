<template><div><h2 id="django" tabindex="-1"><a class="header-anchor" href="#django"><span>Django</span></a></h2>
<h3 id="_1️⃣-install" tabindex="-1"><a class="header-anchor" href="#_1️⃣-install"><span>1️⃣ Install</span></a></h3>
<div dir="rtl" style="font-size:2vw">
<p>هي المسؤولة عن التحكم في الـ CORS (Cross-Origin Resource Sharing) — السماح أو منع الطلبات اللي جاية من دومينات مختلفة.</p>
</div>
<h4 id="_1️⃣-install-📚" tabindex="-1"><a class="header-anchor" href="#_1️⃣-install-📚"><span>1️⃣ Install 📚</span></a></h4>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip install django-cors-headers</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h3 id="_2️⃣-setup-🛠️" tabindex="-1"><a class="header-anchor" href="#_2️⃣-setup-🛠️"><span>2️⃣ Setup 🛠️</span></a></h3>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># corsheaders إعدادات</span></span>
<span class="line"><span class="token comment"># Allow CORS requests from specific addresses</span></span>
<span class="line"><span class="token comment"># Allow requests from this origin</span></span>
<span class="line">CORS_ALLOWED_ORIGINS <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line">    <span class="token string">"http://localhost:5173"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"http://localhost:5174"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"http://192.168.1.5:5173"</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">]</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">INSTALLED_APPS <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line">  <span class="token comment"># Libraries</span></span>
<span class="line">  <span class="token string">"corsheaders"</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">]</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">MIDDLEWARE <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line"><span class="token comment"># Libraries [ Django Cors Headers ]</span></span>
<span class="line"><span class="token string">"corsheaders.middleware.CorsMiddleware"</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">]</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div></div></template>


