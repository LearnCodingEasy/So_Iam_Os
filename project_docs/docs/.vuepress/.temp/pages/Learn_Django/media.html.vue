<template><div><h1 id="media" tabindex="-1"><a class="header-anchor" href="#media"><span>Media</span></a></h1>
<h2 id="settings-py" tabindex="-1"><a class="header-anchor" href="#settings-py"><span>settings.py</span></a></h2>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># Access path for media files (such as images and files uploaded by users)</span></span>
<span class="line">MEDIA_URL <span class="token operator">=</span> <span class="token string">"media/"</span></span>
<span class="line"><span class="token comment"># Specify a "media" folder in the project to store uploaded media files</span></span>
<span class="line">MEDIA_ROOT <span class="token operator">=</span> BASE_DIR <span class="token operator">/</span> <span class="token string">"media"</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h2 id="urls-py" tabindex="-1"><a class="header-anchor" href="#urls-py"><span>urls.py</span></a></h2>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">from</span> django<span class="token punctuation">.</span>conf <span class="token keyword">import</span> settings</span>
<span class="line"><span class="token keyword">from</span> django<span class="token punctuation">.</span>conf<span class="token punctuation">.</span>urls<span class="token punctuation">.</span>static <span class="token keyword">import</span> static</span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token punctuation">]</span> <span class="token operator">+</span> static<span class="token punctuation">(</span>settings<span class="token punctuation">.</span>MEDIA_URL<span class="token punctuation">,</span> document_root<span class="token operator">=</span>settings<span class="token punctuation">.</span>MEDIA_ROOT<span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div></div></template>


