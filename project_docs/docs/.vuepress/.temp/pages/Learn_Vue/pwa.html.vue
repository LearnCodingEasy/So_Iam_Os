<template><div><h5 id="📚-install-setup-vue-libraries" tabindex="-1"><a class="header-anchor" href="#📚-install-setup-vue-libraries"><span>📚 Install &amp; Setup Vue Libraries</span></a></h5>
<h4 id="_6️⃣-pwa" tabindex="-1"><a class="header-anchor" href="#_6️⃣-pwa"><span>6️⃣ Pwa</span></a></h4>
<h3 id="_1️⃣-install-📚" tabindex="-1"><a class="header-anchor" href="#_1️⃣-install-📚"><span>1️⃣ Install 📚</span></a></h3>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">npm install -D vite-plugin-pwa</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h3 id="_2️⃣-setup-🛠️" tabindex="-1"><a class="header-anchor" href="#_2️⃣-setup-🛠️"><span>2️⃣ Setup 🛠️</span></a></h3>
<h4 id="📝-edit-page-vite-config-js" tabindex="-1"><a class="header-anchor" href="#📝-edit-page-vite-config-js"><span>📝 Edit Page [ vite.config.js ]</span></a></h4>
<div class="language-javascript line-numbers-mode" data-highlighter="prismjs" data-ext="js"><pre v-pre><code><span class="line"><span class="token keyword">import</span> <span class="token punctuation">{</span> fileURLToPath<span class="token punctuation">,</span> <span class="token constant">URL</span> <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">"node:url"</span><span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line"><span class="token keyword">import</span> <span class="token punctuation">{</span> defineConfig <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">"vite"</span><span class="token punctuation">;</span></span>
<span class="line"><span class="token keyword">import</span> vue <span class="token keyword">from</span> <span class="token string">"@vitejs/plugin-vue"</span><span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line"><span class="token comment">// For Pwa</span></span>
<span class="line"><span class="token comment">// https://vite-pwa-org.netlify.app/guide/</span></span>
<span class="line"><span class="token keyword">import</span> <span class="token punctuation">{</span> VitePWA <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">"vite-plugin-pwa"</span><span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line"><span class="token comment">// https://vite.dev/config/</span></span>
<span class="line"><span class="token keyword">export</span> <span class="token keyword">default</span> <span class="token function">defineConfig</span><span class="token punctuation">(</span><span class="token punctuation">{</span></span>
<span class="line">  <span class="token literal-property property">plugins</span><span class="token operator">:</span> <span class="token punctuation">[</span></span>
<span class="line">    <span class="token function">vue</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token comment">// For Pwa</span></span>
<span class="line">    <span class="token function">VitePWA</span><span class="token punctuation">(</span><span class="token punctuation">{</span></span>
<span class="line">      <span class="token literal-property property">registerType</span><span class="token operator">:</span> <span class="token string">"autoUpdate"</span><span class="token punctuation">,</span></span>
<span class="line">      <span class="token literal-property property">workbox</span><span class="token operator">:</span> <span class="token punctuation">{</span></span>
<span class="line">        <span class="token literal-property property">globPatterns</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token string">"**/*.{js,css,html,ico,png,svg}"</span><span class="token punctuation">]</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token literal-property property">clientsClaim</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token literal-property property">skipWaiting</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token literal-property property">cleanupOutdatedCaches</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token literal-property property">offlineGoogleAnalytics</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token literal-property property">sourcemap</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token literal-property property">runtimeCaching</span><span class="token operator">:</span> <span class="token punctuation">[</span></span>
<span class="line">          <span class="token punctuation">{</span></span>
<span class="line">            <span class="token function-variable function">urlPattern</span><span class="token operator">:</span> <span class="token punctuation">(</span><span class="token parameter"><span class="token punctuation">{</span> request <span class="token punctuation">}</span></span><span class="token punctuation">)</span> <span class="token operator">=></span></span>
<span class="line">              request<span class="token punctuation">.</span>destination <span class="token operator">===</span> <span class="token string">"document"</span> <span class="token operator">||</span></span>
<span class="line">              request<span class="token punctuation">.</span>destination <span class="token operator">===</span> <span class="token string">"script"</span> <span class="token operator">||</span></span>
<span class="line">              request<span class="token punctuation">.</span>destination <span class="token operator">===</span> <span class="token string">"style"</span> <span class="token operator">||</span></span>
<span class="line">              request<span class="token punctuation">.</span>destination <span class="token operator">===</span> <span class="token string">"image"</span> <span class="token operator">||</span></span>
<span class="line">              request<span class="token punctuation">.</span>destination <span class="token operator">===</span> <span class="token string">"font"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token literal-property property">handler</span><span class="token operator">:</span> <span class="token string">"StaleWhileRevalidate"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token literal-property property">options</span><span class="token operator">:</span> <span class="token punctuation">{</span></span>
<span class="line">              <span class="token literal-property property">cacheName</span><span class="token operator">:</span> <span class="token string">"assets-cache"</span><span class="token punctuation">,</span></span>
<span class="line">              <span class="token literal-property property">expiration</span><span class="token operator">:</span> <span class="token punctuation">{</span></span>
<span class="line">                <span class="token literal-property property">maxEntries</span><span class="token operator">:</span> <span class="token number">100</span><span class="token punctuation">,</span></span>
<span class="line">                <span class="token literal-property property">maxAgeSeconds</span><span class="token operator">:</span> <span class="token number">60</span> <span class="token operator">*</span> <span class="token number">60</span> <span class="token operator">*</span> <span class="token number">24</span> <span class="token operator">*</span> <span class="token number">30</span><span class="token punctuation">,</span></span>
<span class="line">              <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">          <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token punctuation">]</span><span class="token punctuation">,</span></span>
<span class="line">      <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">      <span class="token literal-property property">devOptions</span><span class="token operator">:</span> <span class="token punctuation">{</span></span>
<span class="line">        <span class="token literal-property property">enabled</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span></span>
<span class="line">      <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">      <span class="token literal-property property">injectRegister</span><span class="token operator">:</span> <span class="token string">"auto"</span><span class="token punctuation">,</span></span>
<span class="line">      <span class="token literal-property property">includeAssets</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token string">"**/*"</span><span class="token punctuation">]</span><span class="token punctuation">,</span></span>
<span class="line">      <span class="token literal-property property">manifest</span><span class="token operator">:</span> <span class="token punctuation">{</span></span>
<span class="line">        <span class="token literal-property property">name</span><span class="token operator">:</span> <span class="token string">"Script Youtube"</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token literal-property property">short_name</span><span class="token operator">:</span> <span class="token string">"Script Youtube"</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token literal-property property">description</span><span class="token operator">:</span> <span class="token string">"My Awesome App Script Youtube"</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token literal-property property">theme_color</span><span class="token operator">:</span> <span class="token string">"#ffffff"</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token literal-property property">icons</span><span class="token operator">:</span> <span class="token punctuation">[</span></span>
<span class="line">          <span class="token punctuation">{</span></span>
<span class="line">            <span class="token literal-property property">src</span><span class="token operator">:</span> <span class="token string">"./images/icons/icon_72x72.png"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token literal-property property">type</span><span class="token operator">:</span> <span class="token string">"image/png"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token literal-property property">sizes</span><span class="token operator">:</span> <span class="token string">"72x72"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token literal-property property">purpose</span><span class="token operator">:</span> <span class="token string">"any maskable"</span><span class="token punctuation">,</span></span>
<span class="line">          <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">          <span class="token punctuation">{</span></span>
<span class="line">            <span class="token literal-property property">src</span><span class="token operator">:</span> <span class="token string">"./images/icons/icon_96x96.png"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token literal-property property">type</span><span class="token operator">:</span> <span class="token string">"image/png"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token literal-property property">sizes</span><span class="token operator">:</span> <span class="token string">"96x96"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token literal-property property">purpose</span><span class="token operator">:</span> <span class="token string">"any maskable"</span><span class="token punctuation">,</span></span>
<span class="line">          <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">          <span class="token punctuation">{</span></span>
<span class="line">            <span class="token literal-property property">src</span><span class="token operator">:</span> <span class="token string">"./images/icons/icon_128x128.png"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token literal-property property">type</span><span class="token operator">:</span> <span class="token string">"image/png"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token literal-property property">sizes</span><span class="token operator">:</span> <span class="token string">"128x128"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token literal-property property">purpose</span><span class="token operator">:</span> <span class="token string">"any maskable"</span><span class="token punctuation">,</span></span>
<span class="line">          <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">          <span class="token punctuation">{</span></span>
<span class="line">            <span class="token literal-property property">src</span><span class="token operator">:</span> <span class="token string">"./images/icons/icon_144x144.png"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token literal-property property">type</span><span class="token operator">:</span> <span class="token string">"image/png"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token literal-property property">sizes</span><span class="token operator">:</span> <span class="token string">"144x144"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token literal-property property">purpose</span><span class="token operator">:</span> <span class="token string">"any maskable"</span><span class="token punctuation">,</span></span>
<span class="line">          <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">          <span class="token punctuation">{</span></span>
<span class="line">            <span class="token literal-property property">src</span><span class="token operator">:</span> <span class="token string">"./images/icons/icon_152x152.png"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token literal-property property">type</span><span class="token operator">:</span> <span class="token string">"image/png"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token literal-property property">sizes</span><span class="token operator">:</span> <span class="token string">"152x152"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token literal-property property">purpose</span><span class="token operator">:</span> <span class="token string">"any maskable"</span><span class="token punctuation">,</span></span>
<span class="line">          <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">          <span class="token punctuation">{</span></span>
<span class="line">            <span class="token literal-property property">src</span><span class="token operator">:</span> <span class="token string">"./images/icons/icon_192x192.png"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token literal-property property">type</span><span class="token operator">:</span> <span class="token string">"image/png"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token literal-property property">sizes</span><span class="token operator">:</span> <span class="token string">"192x192"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token literal-property property">purpose</span><span class="token operator">:</span> <span class="token string">"any maskable"</span><span class="token punctuation">,</span></span>
<span class="line">          <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">          <span class="token punctuation">{</span></span>
<span class="line">            <span class="token literal-property property">src</span><span class="token operator">:</span> <span class="token string">"./images/icons/icon_384x384.png"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token literal-property property">type</span><span class="token operator">:</span> <span class="token string">"image/png"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token literal-property property">sizes</span><span class="token operator">:</span> <span class="token string">"384x384"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token literal-property property">purpose</span><span class="token operator">:</span> <span class="token string">"any maskable"</span><span class="token punctuation">,</span></span>
<span class="line">          <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">          <span class="token punctuation">{</span></span>
<span class="line">            <span class="token literal-property property">src</span><span class="token operator">:</span> <span class="token string">"./images/icons/icon_512x512.png"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token literal-property property">type</span><span class="token operator">:</span> <span class="token string">"image/png"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token literal-property property">sizes</span><span class="token operator">:</span> <span class="token string">"512x512"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token literal-property property">purpose</span><span class="token operator">:</span> <span class="token string">"any maskable"</span><span class="token punctuation">,</span></span>
<span class="line">          <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token punctuation">]</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token literal-property property">screenshots</span><span class="token operator">:</span> <span class="token punctuation">[</span></span>
<span class="line">          <span class="token punctuation">{</span></span>
<span class="line">            <span class="token literal-property property">src</span><span class="token operator">:</span> <span class="token string">"./images/screenshots/screenshots.png"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token literal-property property">sizes</span><span class="token operator">:</span> <span class="token string">"640x480"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token literal-property property">type</span><span class="token operator">:</span> <span class="token string">"image/png"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token literal-property property">form_factor</span><span class="token operator">:</span> <span class="token string">"wide"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token comment">// "form_factor": "narrow"</span></span>
<span class="line">          <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token punctuation">]</span><span class="token punctuation">,</span></span>
<span class="line">      <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">  <span class="token punctuation">]</span><span class="token punctuation">,</span></span>
<span class="line">  <span class="token literal-property property">content</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token string">"./index.html"</span><span class="token punctuation">,</span> <span class="token string">"./src/**/*.{vue,js,ts,jsx,tsx}"</span><span class="token punctuation">]</span><span class="token punctuation">,</span></span>
<span class="line">  <span class="token literal-property property">resolve</span><span class="token operator">:</span> <span class="token punctuation">{</span></span>
<span class="line">    <span class="token literal-property property">alias</span><span class="token operator">:</span> <span class="token punctuation">{</span></span>
<span class="line">      <span class="token string-property property">"@"</span><span class="token operator">:</span> <span class="token function">fileURLToPath</span><span class="token punctuation">(</span><span class="token keyword">new</span> <span class="token class-name">URL</span><span class="token punctuation">(</span><span class="token string">"./src"</span><span class="token punctuation">,</span> <span class="token keyword">import</span><span class="token punctuation">.</span>meta<span class="token punctuation">.</span>url<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">  <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><ul>
<li>🖼️ Add Image Inside Public</li>
</ul>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">images</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">icons</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">screenshots</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line"></span>
<span class="line">├── public/</span>
<span class="line">│ ├── images/</span>
<span class="line">│ | ├── icons/</span>
<span class="line">│ │ | ├── 🖼️ icon_72x72.png</span>
<span class="line">│ │ | ├── 🖼️ icon_96x96.png</span>
<span class="line">│ │ | ├── 🖼️ icon_128x128.png</span>
<span class="line">│ │ | ├── 🖼️ icon_144x144.png</span>
<span class="line">│ │ | ├── 🖼️ icon_152x152.png</span>
<span class="line">│ │ | ├── 🖼️ icon_192x192.png</span>
<span class="line">│ │ | ├── 🖼️ icon_256x256.png</span>
<span class="line">│ │ | ├── 🖼️ icon_384x384.png</span>
<span class="line">│ │ | ├── 🖼️ icon_512x512.png</span>
<span class="line">│ | ├── screenshots/</span>
<span class="line">│ │ | ├── 🖼️ screenshots.png</span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">icon_72x72</span>
<span class="line">icon_96x96</span>
<span class="line">icon_128x128</span>
<span class="line">icon_144x144</span>
<span class="line">icon_152x152</span>
<span class="line">icon_192x192</span>
<span class="line">icon_256x256</span>
<span class="line">icon_384x384</span>
<span class="line">icon_512x512</span>
<span class="line">screenshots_640x480</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h3 id="_3️⃣-resize-image-📸" tabindex="-1"><a class="header-anchor" href="#_3️⃣-resize-image-📸"><span>3️⃣ Resize Image 📸</span></a></h3>
<h6 id="👉️-go-to-website-to-resize-image" tabindex="-1"><a class="header-anchor" href="#👉️-go-to-website-to-resize-image"><span>👉️ Go To Website To Resize Image</span></a></h6>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">https://www.iloveimg.com/resize-image</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div></div></template>


