<template><div><h2 id="serializers" tabindex="-1"><a class="header-anchor" href="#serializers"><span>Serializers</span></a></h2>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># Serializers.py</span></span>
<span class="line"></span>
<span class="line"><span class="token keyword">from</span> rest_framework <span class="token keyword">import</span> serializers</span>
<span class="line"><span class="token keyword">from</span> <span class="token punctuation">.</span>models <span class="token keyword">import</span> Product</span>
<span class="line"></span>
<span class="line"><span class="token comment"># ----------------------------</span></span>
<span class="line"><span class="token comment"># 🔘 Product Serializer</span></span>
<span class="line"><span class="token comment"># ----------------------------</span></span>
<span class="line"></span>
<span class="line"><span class="token keyword">class</span> <span class="token class-name">ProductSerializer</span><span class="token punctuation">(</span>serializers<span class="token punctuation">.</span>ModelSerializer<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">    <span class="token keyword">class</span> <span class="token class-name">Meta</span><span class="token punctuation">:</span></span>
<span class="line">        model <span class="token operator">=</span> Product</span>
<span class="line">        fields <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line">            <span class="token string">'id'</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">'created_at'</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">'created_at_formatted'</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">'updated_at'</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">'updated_at_formatted'</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token comment"># 'created_by',</span></span>
<span class="line"></span>
<span class="line">            <span class="token string">'name'</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">'description'</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">'price'</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">'is_available'</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token punctuation">]</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div></div></template>


