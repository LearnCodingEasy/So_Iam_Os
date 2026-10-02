<template><div><h1 id="rich" tabindex="-1"><a class="header-anchor" href="#rich"><span>Rich</span></a></h1>
<h2 id="install" tabindex="-1"><a class="header-anchor" href="#install"><span>Install</span></a></h2>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip install rich</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h2 id="used" tabindex="-1"><a class="header-anchor" href="#used"><span>Used</span></a></h2>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">from</span> rich<span class="token punctuation">.</span>console <span class="token keyword">import</span> Console</span>
<span class="line"><span class="token keyword">from</span> rich<span class="token punctuation">.</span>table <span class="token keyword">import</span> Table</span>
<span class="line"><span class="token comment"># Rich Console إعداد الـ</span></span>
<span class="line">console <span class="token operator">=</span> Console<span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">name   <span class="token operator">=</span> <span class="token string">'Hossam Rashad'</span></span>
<span class="line">errors   <span class="token operator">=</span> <span class="token boolean">False</span></span>
<span class="line"></span>
<span class="line">console<span class="token punctuation">.</span><span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string-interpolation"><span class="token string">f"[bold green]Successfully: </span><span class="token interpolation"><span class="token punctuation">{</span>name<span class="token punctuation">}</span></span><span class="token string">[/bold green]"</span></span><span class="token punctuation">)</span></span>
<span class="line">console<span class="token punctuation">.</span><span class="token keyword">print</span><span class="token punctuation">(</span><span class="token string-interpolation"><span class="token string">f"[bold red]Failed Errors: </span><span class="token interpolation"><span class="token punctuation">{</span>errors<span class="token punctuation">}</span></span><span class="token string">[/bold red]"</span></span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">console<span class="token punctuation">.</span><span class="token keyword">print</span><span class="token punctuation">(</span>table<span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div></div></template>


