<template><div><h2 id="urls" tabindex="-1"><a class="header-anchor" href="#urls"><span>Urls</span></a></h2>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">from</span> django<span class="token punctuation">.</span>urls <span class="token keyword">import</span> path</span>
<span class="line"></span>
<span class="line"><span class="token keyword">from</span> <span class="token punctuation">.</span> <span class="token keyword">import</span> views</span>
<span class="line"></span>
<span class="line">urlpatterns <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line">    path<span class="token punctuation">(</span><span class="token string">"product_list/"</span><span class="token punctuation">,</span> views<span class="token punctuation">.</span>product_list<span class="token punctuation">,</span> name<span class="token operator">=</span><span class="token string">"product_list"</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">]</span></span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># urls.py</span></span>
<span class="line"></span>
<span class="line"><span class="token keyword">from</span> django<span class="token punctuation">.</span>urls <span class="token keyword">import</span> path<span class="token punctuation">,</span> include</span>
<span class="line"><span class="token keyword">from</span> rest_framework<span class="token punctuation">.</span>routers <span class="token keyword">import</span> DefaultRouter</span>
<span class="line"><span class="token keyword">from</span> <span class="token punctuation">.</span> <span class="token keyword">import</span> views</span>
<span class="line"></span>
<span class="line">router <span class="token operator">=</span> DefaultRouter<span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line"><span class="token comment"># product_list</span></span>
<span class="line">router<span class="token punctuation">.</span>register<span class="token punctuation">(</span><span class="token string">r'product_list'</span><span class="token punctuation">,</span> views<span class="token punctuation">.</span>product_list<span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">urlpatterns <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line">    path<span class="token punctuation">(</span><span class="token string">''</span><span class="token punctuation">,</span> include<span class="token punctuation">(</span>router<span class="token punctuation">.</span>urls<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">]</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div></div></template>


