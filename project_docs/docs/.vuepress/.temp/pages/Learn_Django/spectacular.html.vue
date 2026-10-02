<template><div><h1 id="document" tabindex="-1"><a class="header-anchor" href="#document"><span>Document</span></a></h1>
<h2 id="spectacular" tabindex="-1"><a class="header-anchor" href="#spectacular"><span>spectacular</span></a></h2>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip install drf-spectacular</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># 3️⃣ rest_framework</span></span>
<span class="line">REST_FRAMEWORK <span class="token operator">=</span> <span class="token punctuation">{</span></span>
<span class="line">    <span class="token string">'DEFAULT_SCHEMA_CLASS'</span><span class="token punctuation">:</span> <span class="token string">'drf_spectacular.openapi.AutoSchema'</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"><span class="token comment"># 0️⃣1️⃣ Document</span></span>
<span class="line">SPECTACULAR_SETTINGS <span class="token operator">=</span> <span class="token punctuation">{</span></span>
<span class="line">    <span class="token string">'TITLE'</span><span class="token punctuation">:</span> <span class="token string">'Your Project API'</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">'DESCRIPTION'</span><span class="token punctuation">:</span> <span class="token string">'Your project description'</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">'VERSION'</span><span class="token punctuation">:</span> <span class="token string">'1.0.0'</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">'SERVE_INCLUDE_SCHEMA'</span><span class="token punctuation">:</span> <span class="token boolean">False</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">    <span class="token string">'drf_spectacular'</span><span class="token punctuation">,</span></span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div></div></div><div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">SpectacularRedocView</span>
<span class="line">urlpatterns <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line"><span class="token comment"># 0️⃣1️⃣ Document</span></span>
<span class="line">    path<span class="token punctuation">(</span><span class="token string">'api/schema/'</span><span class="token punctuation">,</span> SpectacularAPIView<span class="token punctuation">.</span>as_view<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span> name<span class="token operator">=</span><span class="token string">'schema'</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">    path<span class="token punctuation">(</span><span class="token string">'api/schema/swagger-ui/'</span><span class="token punctuation">,</span></span>
<span class="line">         SpectacularSwaggerView<span class="token punctuation">.</span>as_view<span class="token punctuation">(</span>url_name<span class="token operator">=</span><span class="token string">'schema'</span><span class="token punctuation">)</span><span class="token punctuation">,</span> name<span class="token operator">=</span><span class="token string">'swagger-ui'</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">    path<span class="token punctuation">(</span><span class="token string">'api/schema/redoc/'</span><span class="token punctuation">,</span></span>
<span class="line">         SpectacularRedocView<span class="token punctuation">.</span>as_view<span class="token punctuation">(</span>url_name<span class="token operator">=</span><span class="token string">'schema'</span><span class="token punctuation">)</span><span class="token punctuation">,</span> name<span class="token operator">=</span><span class="token string">'redoc'</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line"></span>
<span class="line"><span class="token punctuation">]</span> <span class="token operator">+</span> static<span class="token punctuation">(</span>settings<span class="token punctuation">.</span>MEDIA_URL<span class="token punctuation">,</span> document_root<span class="token operator">=</span>settings<span class="token punctuation">.</span>MEDIA_ROOT<span class="token punctuation">)</span> <span class="token operator">+</span> debug_toolbar_urls<span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><ul>
<li>swagger</li>
</ul>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">http://localhost:8000/api/schema/swagger-ui</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><ul>
<li>redec</li>
</ul>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">http://localhost:8000/api/schema/redoc/</span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div></div></div></div></template>


