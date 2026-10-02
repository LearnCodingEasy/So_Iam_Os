<template><div><h1 id="🕸️-automation" tabindex="-1"><a class="header-anchor" href="#🕸️-automation"><span>🕸️ Automation</span></a></h1>
<h2 id="intro" tabindex="-1"><a class="header-anchor" href="#intro"><span>Intro</span></a></h2>
<div dir="rtl" >
PyAutoGUI يعني إيه؟
<br/>
مكتبة Python تقدر من خلالها:
<br/>
<p>✅ تحرك الماوس
<br/>
✅ تضغط
<br/>
✅ تكتب
<br/>
✅ تاخد Screenshot
<br/>
✅ تدور على صورة جوة الشاشة
<br/>
✅ تنتظر حدث يحصل
<br/></p>
<p>يعني بتديك القدرة تخلي الكود يتصرف كإنه بني آدم.</p>
</div>
<h2 id="install" tabindex="-1"><a class="header-anchor" href="#install"><span>Install</span></a></h2>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip install pyautogui</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">import</span> pyautogui<span class="token punctuation">,</span> time</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h2 id="mouse" tabindex="-1"><a class="header-anchor" href="#mouse"><span>Mouse</span></a></h2>
<div dir="rtl" >  
  🖱️ تحريك الماوس
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># 🖱️ تحريك الماوس</span></span>
<span class="line"><span class="token keyword">import</span> pyautogui</span>
<span class="line">pyautogui<span class="token punctuation">.</span>moveTo<span class="token punctuation">(</span><span class="token number">500</span><span class="token punctuation">,</span> <span class="token number">300</span><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" >  
الحركة تكون ناعمة؟
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># 🖱️ تحريك الماوس</span></span>
<span class="line"><span class="token keyword">import</span> pyautogui</span>
<span class="line">pyautogui<span class="token punctuation">.</span>moveTo<span class="token punctuation">(</span><span class="token number">100</span><span class="token punctuation">,</span><span class="token number">100</span><span class="token punctuation">,</span>duration<span class="token operator">=</span><span class="token number">1</span><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" >  
  🖱️ مكان الماوس الحالي؟
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># 🖱️ مكان الماوس الحالي؟</span></span>
<span class="line"><span class="token keyword">import</span> pyautogui</span>
<span class="line"><span class="token keyword">print</span><span class="token punctuation">(</span>pyautogui<span class="token punctuation">.</span>position<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" >  
  الضغط بالماوس
  <br/>
كليك عادي 👆 نقرة واحدة
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># 👆 نقرة واحدة</span></span>
<span class="line"><span class="token keyword">import</span> pyautogui</span>
<span class="line">pyautogui<span class="token punctuation">.</span>click<span class="token punctuation">(</span><span class="token number">100</span><span class="token punctuation">,</span><span class="token number">100</span><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" >  
  دبل كليك
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">import</span> pyautogui</span>
<span class="line"></span>
<span class="line">pyautogui<span class="token punctuation">.</span>doubleClick<span class="token punctuation">(</span><span class="token number">500</span><span class="token punctuation">,</span> <span class="token number">300</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" >  
  كليك يمين
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">import</span> pyautogui</span>
<span class="line">pyautogui<span class="token punctuation">.</span>rightClick<span class="token punctuation">(</span><span class="token number">500</span><span class="token punctuation">,</span> <span class="token number">300</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" >  
  ↔️ سحب الماوس
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># ↔️ سحب الماوس</span></span>
<span class="line"><span class="token keyword">import</span> pyautogui</span>
<span class="line">pyautogui<span class="token punctuation">.</span>dragTo<span class="token punctuation">(</span><span class="token number">400</span><span class="token punctuation">,</span><span class="token number">400</span><span class="token punctuation">,</span>duration<span class="token operator">=</span><span class="token number">1</span><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h2 id="keypord" tabindex="-1"><a class="header-anchor" href="#keypord"><span>keypord</span></a></h2>
<div dir="rtl" >
  الكتابة بالكيبورد
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">import</span> pyautogui</span>
<span class="line"></span>
<span class="line">pyautogui<span class="token punctuation">.</span>write<span class="token punctuation">(</span><span class="token string">"Hello World"</span><span class="token punctuation">)</span></span>
<span class="line"><span class="token comment"># ✍️ كتابة النص</span></span>
<span class="line"><span class="token keyword">import</span> pyautogui</span>
<span class="line">pyautogui<span class="token punctuation">.</span>write<span class="token punctuation">(</span><span class="token string">'Hello VS Code!'</span><span class="token punctuation">,</span> interval<span class="token operator">=</span><span class="token number">0.1</span><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" >
  ضغط زر
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># ⏎ الضغط على Enter</span></span>
<span class="line"><span class="token keyword">import</span> pyautogui</span>
<span class="line">pyautogui<span class="token punctuation">.</span>press<span class="token punctuation">(</span><span class="token string">'enter'</span><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" >
  الشورت كات 
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># 💾 حفظ الملف</span></span>
<span class="line"><span class="token keyword">import</span> pyautogui</span>
<span class="line">pyautogui<span class="token punctuation">.</span>hotkey<span class="token punctuation">(</span><span class="token string">'ctrl'</span><span class="token punctuation">,</span><span class="token string">'s'</span><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># 🔍 فتح Command Palette</span></span>
<span class="line"><span class="token keyword">import</span> pyautogui</span>
<span class="line">pyautogui<span class="token punctuation">.</span>hotkey<span class="token punctuation">(</span><span class="token string">'ctrl'</span><span class="token punctuation">,</span><span class="token string">'shift'</span><span class="token punctuation">,</span><span class="token string">'p'</span><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h2 id="screenshot" tabindex="-1"><a class="header-anchor" href="#screenshot"><span>screenshot</span></a></h2>
<div dir="rtl" >
  📸 أخذ سكرين شوت
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># 📸 أخذ سكرين شوت</span></span>
<span class="line"><span class="token keyword">import</span> pyautogui</span>
<span class="line">screenshot <span class="token operator">=</span> pyautogui<span class="token punctuation">.</span>screenshot<span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line"><span class="token comment"># 💾 حفظ الصورة</span></span>
<span class="line">screenshot<span class="token punctuation">.</span>save<span class="token punctuation">(</span><span class="token string">'screenshot.png'</span><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" >
  🔍 البحث عن أيقونة
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># 🔍 البحث عن أيقونة</span></span>
<span class="line"><span class="token keyword">import</span> pyautogui</span>
<span class="line">location <span class="token operator">=</span> pyautogui<span class="token punctuation">.</span>locateOnScreen<span class="token punctuation">(</span><span class="token string">'TogglePanel.png'</span><span class="token punctuation">)</span></span>
<span class="line"><span class="token keyword">print</span><span class="token punctuation">(</span>location<span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" >
<h2>👆 النقر على الصورة</h2>
  <h2>
  </h2>
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># 👆 النقر على الصورة</span></span>
<span class="line"><span class="token keyword">import</span> pyautogui</span>
<span class="line">pyautogui<span class="token punctuation">.</span>click<span class="token punctuation">(</span>pyautogui<span class="token punctuation">.</span>locateCenterOnScreen<span class="token punctuation">(</span></span>
<span class="line">    <span class="token string">'TogglePanel.png'</span><span class="token punctuation">)</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" >
  <h2>
  </h2>
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">import</span> pyautogui</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div dir="rtl" >
  <h2>
  </h2>
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">import</span> pyautogui</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div></div></template>


