<template><div><h3 id="📚-install-setup-vue-libraries-tailwind" tabindex="-1"><a class="header-anchor" href="#📚-install-setup-vue-libraries-tailwind"><span>📚 Install &amp; Setup Vue Libraries [ Tailwind ]</span></a></h3>
<h3 id="_1️⃣-install-📚" tabindex="-1"><a class="header-anchor" href="#_1️⃣-install-📚"><span>1️⃣ Install 📚</span></a></h3>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">npm install -D tailwindcss@3 postcss autoprefixer</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">npx tailwindcss init -p</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h3 id="_2️⃣-setup-🛠️" tabindex="-1"><a class="header-anchor" href="#_2️⃣-setup-🛠️"><span>2️⃣ Setup 🛠️</span></a></h3>
<ul>
<li>📝 File [ tailwind.config.js ]</li>
</ul>
<div class="language-javascript line-numbers-mode" data-highlighter="prismjs" data-ext="js"><pre v-pre><code><span class="line"><span class="token comment">// ...</span></span>
<span class="line"><span class="token literal-property property">content</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token string">"./index.html"</span><span class="token punctuation">,</span> <span class="token string">"./src/**/*.{vue,js,ts,jsx,tsx}"</span><span class="token punctuation">]</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token comment">// ...</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h3 id="_3️⃣-create-folder-and-file" tabindex="-1"><a class="header-anchor" href="#_3️⃣-create-folder-and-file"><span>3️⃣ Create Folder And File</span></a></h3>
<ul>
<li>📝 Create File [ tailwind.css ] Inside [ src\assets\Tailwind\tailwind.css ]</li>
</ul>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Tailwind\tailwind.css</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div class="language-css line-numbers-mode" data-highlighter="prismjs" data-ext="css"><pre v-pre><code><span class="line"><span class="token atrule"><span class="token rule">@tailwind</span> base<span class="token punctuation">;</span></span></span>
<span class="line"><span class="token atrule"><span class="token rule">@tailwind</span> components<span class="token punctuation">;</span></span></span>
<span class="line"><span class="token atrule"><span class="token rule">@tailwind</span> utilities<span class="token punctuation">;</span></span></span>
<span class="line"><span class="token atrule"><span class="token rule">@import</span> <span class="token string">"tailwindcss/base"</span><span class="token punctuation">;</span></span></span>
<span class="line"><span class="token atrule"><span class="token rule">@import</span> <span class="token string">"tailwindcss/components"</span><span class="token punctuation">;</span></span></span>
<span class="line"><span class="token atrule"><span class="token rule">@import</span> <span class="token string">"tailwindcss/utilities"</span><span class="token punctuation">;</span></span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h3 id="_4️⃣-import" tabindex="-1"><a class="header-anchor" href="#_4️⃣-import"><span>4️⃣ Import</span></a></h3>
<ul>
<li>Import File Inside [main.js]</li>
</ul>
<div class="language-javascript line-numbers-mode" data-highlighter="prismjs" data-ext="js"><pre v-pre><code><span class="line"><span class="token comment">// Tailwind</span></span>
<span class="line"><span class="token keyword">import</span> <span class="token string">"./assets/Tailwind/tailwind.css"</span><span class="token punctuation">;</span></span>
<span class="line"><span class="token keyword">import</span> <span class="token string">"tailwindcss/tailwind.css"</span><span class="token punctuation">;</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div></div></template>


