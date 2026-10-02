<template><div><h1 id="vite-press" tabindex="-1"><a class="header-anchor" href="#vite-press"><span>Vite Press</span></a></h1>
<h2 id="_0️⃣1️⃣-create-vuepress" tabindex="-1"><a class="header-anchor" href="#_0️⃣1️⃣-create-vuepress"><span>0️⃣1️⃣ Create Vuepress</span></a></h2>
<h6 id="🖥️-create-vuepress" tabindex="-1"><a class="header-anchor" href="#🖥️-create-vuepress"><span>🖥️ Create Vuepress</span></a></h6>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">npm init vuepress project_docs</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h6 id="📁-project-readmap" tabindex="-1"><a class="header-anchor" href="#📁-project-readmap"><span>📁 Project Readmap</span></a></h6>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">📁Project</span>
<span class="line">┣ 📁 project_docs</span>
<span class="line"></span>
<span class="line">┣ 📜 .gitignore</span>
<span class="line">┣ 📜 LICENSE</span>
<span class="line">┣ 📜 README.md</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h2 id="_0️⃣2️⃣-go-to-vuepress" tabindex="-1"><a class="header-anchor" href="#_0️⃣2️⃣-go-to-vuepress"><span>0️⃣2️⃣ Go To Vuepress</span></a></h2>
<h6 id="🖥️-command-path" tabindex="-1"><a class="header-anchor" href="#🖥️-command-path"><span>🖥️ Command Path</span></a></h6>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">cd project_docs</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h2 id="_0️⃣3️⃣-install-sass" tabindex="-1"><a class="header-anchor" href="#_0️⃣3️⃣-install-sass"><span>0️⃣3️⃣ Install Sass</span></a></h2>
<h6 id="🖥️-install-sass" tabindex="-1"><a class="header-anchor" href="#🖥️-install-sass"><span>🖥️ Install Sass</span></a></h6>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">npm install -D sass-embedded</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h2 id="_0️⃣4️⃣-create-file" tabindex="-1"><a class="header-anchor" href="#_0️⃣4️⃣-create-file"><span>0️⃣4️⃣ Create File</span></a></h2>
<h6 id="📝-create-file-index-md-inside-docs" tabindex="-1"><a class="header-anchor" href="#📝-create-file-index-md-inside-docs"><span>📝 Create File [ index.md ] Inside Docs</span></a></h6>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">index.md</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">touch index.md</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h6 id="📁-project-readmap-1" tabindex="-1"><a class="header-anchor" href="#📁-project-readmap-1"><span>📁 Project Readmap</span></a></h6>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">📁Project</span>
<span class="line">┣ 📁 project_docs</span>
<span class="line">┃ ┣ 📂 .github</span>
<span class="line">┃ ┣ 📂 Scripts</span>
<span class="line">┃ ┃ ┣ 📂 docs</span>
<span class="line">┃ ┃ ┃ ┣ 📂 .vuepress</span>
<span class="line">┃ ┃ ┃ ┣ 📜 get-started.md</span>
<span class="line">┃ ┃ ┃ ┣ 📜 index.md</span>
<span class="line">┃ ┃ ┃ ┣ 📜 README.md</span>
<span class="line">┃ ┣ 📂 node_modules</span>
<span class="line">┃ ┣ 📜 package-lock.json</span>
<span class="line">┃ ┣ 📜 package.json</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h2 id="_0️⃣5️⃣-edit-file" tabindex="-1"><a class="header-anchor" href="#_0️⃣5️⃣-edit-file"><span>0️⃣5️⃣ Edit File</span></a></h2>
<h6 id="📝-edit-file-index-md-inside-docs-vuepress-config-js" tabindex="-1"><a class="header-anchor" href="#📝-edit-file-index-md-inside-docs-vuepress-config-js"><span>📝 Edit File [ index.md ] Inside Docs &gt; .vuepress &gt; config.js</span></a></h6>
<div class="language-javascript line-numbers-mode" data-highlighter="prismjs" data-ext="js"><pre v-pre><code><span class="line"><span class="token comment">// 📂 Project Name</span></span>
<span class="line"></span>
<span class="line"><span class="token comment">// 🖌️ VuePress استيراد الثيم الافتراضي من</span></span>
<span class="line"><span class="token keyword">import</span> <span class="token punctuation">{</span> defaultTheme <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">"@vuepress/theme-default"</span><span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line"><span class="token comment">// 🛠️ VuePress استيراد دالة تعريف إعدادات المستخدم في</span></span>
<span class="line"><span class="token keyword">import</span> <span class="token punctuation">{</span> defineUserConfig <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">"vuepress"</span><span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line"><span class="token comment">// ⚡ VuePress لاستخدامه مع Vite استيراد</span></span>
<span class="line"><span class="token keyword">import</span> <span class="token punctuation">{</span> viteBundler <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">"@vuepress/bundler-vite"</span><span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line"><span class="token comment">// 📄 تصدير إعدادات المستخدم الرئيسية</span></span>
<span class="line"><span class="token keyword">export</span> <span class="token keyword">default</span> <span class="token function">defineUserConfig</span><span class="token punctuation">(</span><span class="token punctuation">{</span></span>
<span class="line">  <span class="token comment">// 🌐 لغة الموقع</span></span>
<span class="line">  <span class="token literal-property property">lang</span><span class="token operator">:</span> <span class="token string">"en-US"</span><span class="token punctuation">,</span></span>
<span class="line"></span>
<span class="line">  <span class="token comment">// 📍 عنوان الموقع الرئيسي</span></span>
<span class="line"></span>
<span class="line">  <span class="token literal-property property">title</span><span class="token operator">:</span> <span class="token string">"Project Title"</span><span class="token punctuation">,</span></span>
<span class="line">  <span class="token comment">// 💬 وصف الموقع</span></span>
<span class="line">  <span class="token literal-property property">description</span><span class="token operator">:</span> <span class="token string">"Project Description"</span><span class="token punctuation">,</span></span>
<span class="line"></span>
<span class="line">  <span class="token comment">// 🛠️ إعدادات الثيم الافتراضي مع تخصيص بعض الخصائص</span></span>
<span class="line"></span>
<span class="line">  <span class="token literal-property property">theme</span><span class="token operator">:</span> <span class="token function">defaultTheme</span><span class="token punctuation">(</span><span class="token punctuation">{</span></span>
<span class="line">    <span class="token comment">// 📸 Project Logo</span></span>
<span class="line">    <span class="token comment">// Default</span></span>
<span class="line">    <span class="token comment">// logo: "https://vuejs.press/images/hero.png",</span></span>
<span class="line">    <span class="token literal-property property">logo</span><span class="token operator">:</span> <span class="token string">"../Images/Logo.png"</span><span class="token punctuation">,</span></span>
<span class="line"></span>
<span class="line">    <span class="token comment">// 🖱️ شريط التنقل في الموقع</span></span>
<span class="line">    <span class="token literal-property property">navbar</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token string">"/"</span><span class="token punctuation">,</span> <span class="token string">"/Learn_Django/index"</span><span class="token punctuation">,</span> <span class="token string">"/Learn_Vue/index"</span><span class="token punctuation">,</span> <span class="token string">"/get-started"</span><span class="token punctuation">]</span><span class="token punctuation">,</span></span>
<span class="line">  <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line"></span>
<span class="line">  <span class="token comment">// ⚡ لبناء المشروع Vite استخدام الباني</span></span>
<span class="line">  <span class="token literal-property property">bundler</span><span class="token operator">:</span> <span class="token function">viteBundler</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h6 id="📁-project-readmap-2" tabindex="-1"><a class="header-anchor" href="#📁-project-readmap-2"><span>📁 Project Readmap</span></a></h6>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">📁Project</span>
<span class="line">┣ 📁 project_docs</span>
<span class="line">┃ ┣ 📂 .github</span>
<span class="line">┃ ┣ 📂 Scripts</span>
<span class="line">┃ ┃ ┣ 📂 docs</span>
<span class="line">┃ ┃ ┃ ┣ 📂 .vuepress</span>
<span class="line">┃ ┃ ┃ ┃ ┣ 📂 .cache</span>
<span class="line">┃ ┃ ┃ ┃ ┣ 📂 .temp</span>
<span class="line">┃ ┃ ┃ ┃ ┣ 📜 config.js</span>
<span class="line">┃ ┃ ┃ ┣ 📜 get-started.md</span>
<span class="line">┃ ┃ ┃ ┣ 📜 index.md</span>
<span class="line">┃ ┃ ┃ ┣ 📜 README.md</span>
<span class="line">┃ ┣ 📂 node_modules</span>
<span class="line">┃ ┣ 📜 package-lock.json</span>
<span class="line">┃ ┣ 📜 package.json</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h2 id="_0️⃣6️⃣-extra-style" tabindex="-1"><a class="header-anchor" href="#_0️⃣6️⃣-extra-style"><span>0️⃣6️⃣ Extra Style</span></a></h2>
<h6 id="🖌️-add-your-extra-style" tabindex="-1"><a class="header-anchor" href="#🖌️-add-your-extra-style"><span>🖌️ Add Your Extra Style</span></a></h6>
<ul>
<li>Create File In [.vuepress/styles/index.scss]</li>
</ul>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">styles/index.scss</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">touch styles/index.scss</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div class="language-scss line-numbers-mode" data-highlighter="prismjs" data-ext="scss"><pre v-pre><code><span class="line"><span class="token selector">body </span><span class="token punctuation">{</span></span>
<span class="line">  <span class="token selector">#app </span><span class="token punctuation">{</span></span>
<span class="line">    <span class="token selector">.vp-theme-container </span><span class="token punctuation">{</span></span>
<span class="line">      <span class="token selector">header </span><span class="token punctuation">{</span></span>
<span class="line">        <span class="token property">overflow</span><span class="token punctuation">:</span> hidden<span class="token punctuation">;</span></span>
<span class="line">        <span class="token property">transition</span><span class="token punctuation">:</span> all 0.5s linear<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line">        <span class="token selector">> span </span><span class="token punctuation">{</span></span>
<span class="line">          <span class="token property">display</span><span class="token punctuation">:</span> inline-block<span class="token punctuation">;</span></span>
<span class="line">          <span class="token property">padding</span><span class="token punctuation">:</span> 0.3rem 0.5rem<span class="token punctuation">;</span></span>
<span class="line">          <span class="token property">border-radius</span><span class="token punctuation">:</span> 5px<span class="token punctuation">;</span></span>
<span class="line">          <span class="token property">margin-top</span><span class="token punctuation">:</span> -0.2rem<span class="token punctuation">;</span></span>
<span class="line">          <span class="token property">transition</span><span class="token punctuation">:</span> all 0.5s linear<span class="token punctuation">;</span></span>
<span class="line">          <span class="token property">box-shadow</span><span class="token punctuation">:</span> 0px 0px 3px 1px #29976479<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line">          <span class="token selector">> .route-link </span><span class="token punctuation">{</span></span>
<span class="line">            <span class="token property">display</span><span class="token punctuation">:</span> flex<span class="token punctuation">;</span></span>
<span class="line">            <span class="token property">align-items</span><span class="token punctuation">:</span> center<span class="token punctuation">;</span></span>
<span class="line">            <span class="token selector">.vp-site-logo </span><span class="token punctuation">{</span></span>
<span class="line">              <span class="token property">width</span><span class="token punctuation">:</span> 50px<span class="token punctuation">;</span></span>
<span class="line">              <span class="token property">height</span><span class="token punctuation">:</span> 35px<span class="token punctuation">;</span></span>
<span class="line">              <span class="token property">border-radius</span><span class="token punctuation">:</span> 5px<span class="token punctuation">;</span></span>
<span class="line">            <span class="token punctuation">}</span></span>
<span class="line">            <span class="token selector">.vp-site-name </span><span class="token punctuation">{</span></span>
<span class="line">              <span class="token property">text-transform</span><span class="token punctuation">:</span> capitalize<span class="token punctuation">;</span></span>
<span class="line">            <span class="token punctuation">}</span></span>
<span class="line">          <span class="token punctuation">}</span></span>
<span class="line">        <span class="token punctuation">}</span></span>
<span class="line">        <span class="token selector">> .vp-navbar-items-wrapper </span><span class="token punctuation">{</span></span>
<span class="line">          <span class="token selector">nav </span><span class="token punctuation">{</span></span>
<span class="line">            <span class="token selector">.vp-navbar-item </span><span class="token punctuation">{</span></span>
<span class="line">              <span class="token selector">a </span><span class="token punctuation">{</span></span>
<span class="line">                <span class="token property">padding</span><span class="token punctuation">:</span> 0.1rem 0.5rem<span class="token punctuation">;</span></span>
<span class="line">                <span class="token selector"><span class="token parent important">&amp;</span>.route-link-active </span><span class="token punctuation">{</span></span>
<span class="line">                  <span class="token property">border-bottom</span><span class="token punctuation">:</span> 0.1rem solid #299764<span class="token punctuation">;</span></span>
<span class="line">                  <span class="token property">box-shadow</span><span class="token punctuation">:</span> 0px 0px 3px 1px #2997649c<span class="token punctuation">;</span></span>
<span class="line">                  <span class="token property">border-radius</span><span class="token punctuation">:</span> 5px<span class="token punctuation">;</span></span>
<span class="line">                <span class="token punctuation">}</span></span>
<span class="line">              <span class="token punctuation">}</span></span>
<span class="line">            <span class="token punctuation">}</span></span>
<span class="line">          <span class="token punctuation">}</span></span>
<span class="line">          <span class="token selector">button </span><span class="token punctuation">{</span></span>
<span class="line">            <span class="token comment">// border: 0.1rem solid #c0bfbf52;</span></span>
<span class="line">            <span class="token property">box-shadow</span><span class="token punctuation">:</span> 0px 0px 3px 1px #299764a6<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line">            <span class="token property">padding</span><span class="token punctuation">:</span> 5px<span class="token punctuation">;</span></span>
<span class="line">            <span class="token property">border-radius</span><span class="token punctuation">:</span> 5px<span class="token punctuation">;</span></span>
<span class="line">          <span class="token punctuation">}</span></span>
<span class="line">        <span class="token punctuation">}</span></span>
<span class="line">      <span class="token punctuation">}</span></span>
<span class="line">      <span class="token selector">aside </span><span class="token punctuation">{</span></span>
<span class="line">        <span class="token selector">.vp-sidebar-items </span><span class="token punctuation">{</span></span>
<span class="line">          <span class="token selector">> li </span><span class="token punctuation">{</span></span>
<span class="line">            <span class="token selector">p </span><span class="token punctuation">{</span></span>
<span class="line">              <span class="token property">text-transform</span><span class="token punctuation">:</span> capitalize<span class="token punctuation">;</span></span>
<span class="line">            <span class="token punctuation">}</span></span>
<span class="line">            <span class="token selector">> ul </span><span class="token punctuation">{</span></span>
<span class="line">              <span class="token selector">> li </span><span class="token punctuation">{</span></span>
<span class="line">                <span class="token selector">> a.active </span><span class="token punctuation">{</span></span>
<span class="line">                  <span class="token property">border-right</span><span class="token punctuation">:</span> 0.4rem solid #299764<span class="token punctuation">;</span></span>
<span class="line">                <span class="token punctuation">}</span></span>
<span class="line">                <span class="token selector">> ul </span><span class="token punctuation">{</span></span>
<span class="line">                  <span class="token selector">> li </span><span class="token punctuation">{</span></span>
<span class="line">                    <span class="token selector">> a.active </span><span class="token punctuation">{</span></span>
<span class="line">                      <span class="token property">border-bottom</span><span class="token punctuation">:</span> 0.4rem solid #299764<span class="token punctuation">;</span></span>
<span class="line">                    <span class="token punctuation">}</span></span>
<span class="line">                  <span class="token punctuation">}</span></span>
<span class="line">                <span class="token punctuation">}</span></span>
<span class="line">              <span class="token punctuation">}</span></span>
<span class="line">            <span class="token punctuation">}</span></span>
<span class="line">          <span class="token punctuation">}</span></span>
<span class="line">        <span class="token punctuation">}</span></span>
<span class="line">      <span class="token punctuation">}</span></span>
<span class="line">      <span class="token selector">main.vp-page </span><span class="token punctuation">{</span></span>
<span class="line">        <span class="token selector">> div </span><span class="token punctuation">{</span></span>
<span class="line">          <span class="token selector">> div </span><span class="token punctuation">{</span></span>
<span class="line">            <span class="token selector">h1 </span><span class="token punctuation">{</span></span>
<span class="line">              <span class="token property">text-align</span><span class="token punctuation">:</span> center<span class="token punctuation">;</span></span>
<span class="line">              <span class="token property">font-size</span><span class="token punctuation">:</span> 3vw<span class="token punctuation">;</span></span>
<span class="line">              <span class="token property">font-weight</span><span class="token punctuation">:</span> bold<span class="token punctuation">;</span></span>
<span class="line">              <span class="token property">text-transform</span><span class="token punctuation">:</span> capitalize<span class="token punctuation">;</span></span>
<span class="line">            <span class="token punctuation">}</span></span>
<span class="line">            <span class="token selector">h2 </span><span class="token punctuation">{</span></span>
<span class="line">              <span class="token property">font-size</span><span class="token punctuation">:</span> 2vw<span class="token punctuation">;</span></span>
<span class="line">              <span class="token property">font-weight</span><span class="token punctuation">:</span> bold<span class="token punctuation">;</span></span>
<span class="line">              <span class="token property">text-transform</span><span class="token punctuation">:</span> capitalize<span class="token punctuation">;</span></span>
<span class="line">            <span class="token punctuation">}</span></span>
<span class="line">          <span class="token punctuation">}</span></span>
<span class="line">        <span class="token punctuation">}</span></span>
<span class="line">      <span class="token punctuation">}</span></span>
<span class="line">    <span class="token punctuation">}</span></span>
<span class="line">  <span class="token punctuation">}</span></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h6 id="📁-project-readmap-3" tabindex="-1"><a class="header-anchor" href="#📁-project-readmap-3"><span>📁 Project Readmap</span></a></h6>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">📁Project</span>
<span class="line">┣ 📁 project_docs</span>
<span class="line">┃ ┣ 📂 .github</span>
<span class="line">┃ ┣ 📂 Scripts</span>
<span class="line">┃ ┃ ┣ 📂 docs</span>
<span class="line">┃ ┃ ┃ ┣ 📂 .vuepress</span>
<span class="line">┃ ┃ ┃ ┃ ┣ 📂 .cache</span>
<span class="line">┃ ┃ ┃ ┃ ┣ 📂 .temp</span>
<span class="line">┃ ┃ ┃ ┃ ┣ 📂 styles</span>
<span class="line">┃ ┃ ┃ ┃ ┃ ┣ 📜 index.scss</span>
<span class="line">┃ ┃ ┃ ┃ ┣ 📜 config.js</span>
<span class="line">┃ ┃ ┃ ┣ 📜 get-started.md</span>
<span class="line">┃ ┃ ┃ ┣ 📜 index.md</span>
<span class="line">┃ ┃ ┃ ┣ 📜 README.md</span>
<span class="line">┃ ┣ 📂 node_modules</span>
<span class="line">┃ ┣ 📜 package-lock.json</span>
<span class="line">┃ ┣ 📜 package.json</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h2 id="_0️⃣7️⃣-build-vue-press" tabindex="-1"><a class="header-anchor" href="#_0️⃣7️⃣-build-vue-press"><span>0️⃣7️⃣ Build Vue Press</span></a></h2>
<h6 id="🖥️-build-vue-press" tabindex="-1"><a class="header-anchor" href="#🖥️-build-vue-press"><span>🖥️ Build Vue Press</span></a></h6>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">npm run docs:build</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">📁Project</span>
<span class="line">┣ 📁 project_docs</span>
<span class="line">┃ ┣ 📂 .github</span>
<span class="line">┃ ┣ 📂 Scripts</span>
<span class="line">┃ ┃ ┣ 📂 docs</span>
<span class="line">┃ ┃ ┃ ┣ 📂 .vuepress</span>
<span class="line">┃ ┃ ┃ ┃ ┣ 📂 .cache</span>
<span class="line">┃ ┃ ┃ ┃ ┣ 📂 .temp</span>
<span class="line">┃ ┃ ┃ ┃ ┣ 📂 dist</span>
<span class="line">┃ ┃ ┃ ┃ ┣ 📂 styles</span>
<span class="line">┃ ┃ ┃ ┃ ┃ ┣ 📜 index.scss</span>
<span class="line">┃ ┃ ┃ ┃ ┣ 📜 config.js</span>
<span class="line">┃ ┃ ┃ ┣ 📜 get-started.md</span>
<span class="line">┃ ┃ ┃ ┣ 📜 index.md</span>
<span class="line">┃ ┃ ┃ ┣ 📜 README.md</span>
<span class="line">┃ ┣ 📂 node_modules</span>
<span class="line">┃ ┣ 📜 package-lock.json</span>
<span class="line">┃ ┣ 📜 package.json</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h2 id="_0️⃣-8️⃣-run-vue-press" tabindex="-1"><a class="header-anchor" href="#_0️⃣-8️⃣-run-vue-press"><span>0️⃣ 8️⃣ Run Vue Press</span></a></h2>
<h6 id="🖥️-run-vue-press" tabindex="-1"><a class="header-anchor" href="#🖥️-run-vue-press"><span>🖥️ Run Vue Press</span></a></h6>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">npm run docs:dev</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div></div></template>


