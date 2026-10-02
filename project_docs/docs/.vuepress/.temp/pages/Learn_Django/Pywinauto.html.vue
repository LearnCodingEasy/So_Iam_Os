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
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip install pywinauto</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h2 id="import" tabindex="-1"><a class="header-anchor" href="#import"><span>Import</span></a></h2>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">from</span> pywinauto<span class="token punctuation">.</span>application <span class="token keyword">import</span> Application</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h2 id="open" tabindex="-1"><a class="header-anchor" href="#open"><span>Open</span></a></h2>
<div dir="rtl" >
  <h2>
    🚀 فتح VS Code
  </h2>
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># 🚀 فتح VS Code</span></span>
<span class="line"><span class="token keyword">from</span> pywinauto<span class="token punctuation">.</span>application <span class="token keyword">import</span> Application</span>
<span class="line"></span>
<span class="line">vs_code_path <span class="token operator">=</span> <span class="token string">r"C:\Users\AFAQE\AppData\Local\Programs\Microsoft VS Code\Code.exe"</span></span>
<span class="line"></span>
<span class="line">Application<span class="token punctuation">(</span>backend<span class="token operator">=</span><span class="token string">"uia"</span><span class="token punctuation">)</span><span class="token punctuation">.</span>start<span class="token punctuation">(</span>vs_code_path<span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"><span class="token triple-quoted-string string">"""</span>
<span class="line"># Run</span>
<span class="line">python path\file.py</span>
<span class="line">"""</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" >
  <h2>
    🚀 فتح VS Code وكمان مشروع معين
  </h2>
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># 🚀 فتح VS Code</span></span>
<span class="line"><span class="token keyword">from</span> pywinauto<span class="token punctuation">.</span>application <span class="token keyword">import</span> Application</span>
<span class="line"></span>
<span class="line">vs_code_path <span class="token operator">=</span> <span class="token string">r"C:\Users\AFAQE\AppData\Local\Programs\Microsoft VS Code\Code.exe"</span></span>
<span class="line">project_path <span class="token operator">=</span> <span class="token string">r"D:\Python_Libraries\automation\Pyautogui\automation_examples"</span></span>
<span class="line"></span>
<span class="line">cmd <span class="token operator">=</span> <span class="token string-interpolation"><span class="token string">f'"</span><span class="token interpolation"><span class="token punctuation">{</span>vs_code_path<span class="token punctuation">}</span></span><span class="token string">" "</span><span class="token interpolation"><span class="token punctuation">{</span>project_path<span class="token punctuation">}</span></span><span class="token string">"'</span></span></span>
<span class="line"></span>
<span class="line">Application<span class="token punctuation">(</span>backend<span class="token operator">=</span><span class="token string">"uia"</span><span class="token punctuation">)</span><span class="token punctuation">.</span>start<span class="token punctuation">(</span>cmd<span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"><span class="token triple-quoted-string string">"""</span>
<span class="line"># Run</span>
<span class="line">python path\file.py</span>
<span class="line">"""</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" >
  <h2>
    🚀 فتح VS Code وكمان مشروع معين
  </h2>
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># 🚀 فتح VS Code</span></span>
<span class="line"><span class="token keyword">from</span> pywinauto<span class="token punctuation">.</span>application <span class="token keyword">import</span> Application</span>
<span class="line"></span>
<span class="line">vs_code_path <span class="token operator">=</span> <span class="token string">r"C:\Users\AFAQE\AppData\Local\Programs\Microsoft VS Code\Code.exe"</span></span>
<span class="line">project_path <span class="token operator">=</span> <span class="token string">r"D:\Python_Libraries\automation\Pyautogui\automation_examples"</span></span>
<span class="line"></span>
<span class="line">cmd <span class="token operator">=</span> <span class="token string-interpolation"><span class="token string">f'"</span><span class="token interpolation"><span class="token punctuation">{</span>vs_code_path<span class="token punctuation">}</span></span><span class="token string">" "</span><span class="token interpolation"><span class="token punctuation">{</span>project_path<span class="token punctuation">}</span></span><span class="token string">"'</span></span></span>
<span class="line"></span>
<span class="line">Application<span class="token punctuation">(</span>backend<span class="token operator">=</span><span class="token string">"uia"</span><span class="token punctuation">)</span><span class="token punctuation">.</span>start<span class="token punctuation">(</span>cmd<span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"><span class="token triple-quoted-string string">"""</span>
<span class="line"># Run</span>
<span class="line">python path\file.py</span>
<span class="line">"""</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" >
  <h2>
    🚀 فتح VS Code وكمان مشروع معين وكمان ملف معين
  </h2>
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># 🚀 فتح VS Code</span></span>
<span class="line"><span class="token keyword">from</span> pywinauto<span class="token punctuation">.</span>application <span class="token keyword">import</span> Application</span>
<span class="line"></span>
<span class="line">vs_code_path <span class="token operator">=</span> <span class="token string">r"C:\Users\AFAQE\AppData\Local\Programs\Microsoft VS Code\Code.exe"</span></span>
<span class="line">project_path <span class="token operator">=</span> <span class="token string">r"D:\Python_Libraries\automation\Pyautogui\automation_examples"</span></span>
<span class="line">file_path <span class="token operator">=</span> <span class="token string">r"D:\Python_Libraries\automation\Pyautogui\automation_examples\example_12.py"</span></span>
<span class="line"></span>
<span class="line">cmd <span class="token operator">=</span> <span class="token string-interpolation"><span class="token string">f'"</span><span class="token interpolation"><span class="token punctuation">{</span>vs_code_path<span class="token punctuation">}</span></span><span class="token string">" "</span><span class="token interpolation"><span class="token punctuation">{</span>project_path<span class="token punctuation">}</span></span><span class="token string">" "</span><span class="token interpolation"><span class="token punctuation">{</span>file_path<span class="token punctuation">}</span></span><span class="token string">"'</span></span></span>
<span class="line"></span>
<span class="line">app <span class="token operator">=</span> Application<span class="token punctuation">(</span>backend<span class="token operator">=</span><span class="token string">"uia"</span><span class="token punctuation">)</span><span class="token punctuation">.</span>start<span class="token punctuation">(</span>cmd<span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"><span class="token triple-quoted-string string">"""</span>
<span class="line"># Run</span>
<span class="line">python path\file.py</span>
<span class="line">"""</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div></div></template>


