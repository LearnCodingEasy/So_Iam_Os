<template><div><h3 id="❄️-freeze" tabindex="-1"><a class="header-anchor" href="#❄️-freeze"><span>❄️ freeze</span></a></h3>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">cd backend_django</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div dir="rtl" style="font-size:1.5vw; margin:1.5rem 0">
  الأمر ده بيعمل تصدير لكل المكتبات اللي مثبتها في البيئة الافتراضية بتاعتك (virtual environment) ويحطهم في ملف اسمه requirements.txt.
</div>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip freeze &gt; requirements.txt</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div dir="rtl" style="font-size:1.5vw; margin:1.5rem 0">
  الأمر ده بيعرض قائمة المكتبات المثبتة حاليًا في البيئة الافتراضية مع إصداراتها، لكن مش بيحفظهم في ملف.
</div>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip freeze</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div dir="rtl" style="font-size:1.5vw; margin:1.5rem 0">
  يقدر أي حد يثبت نفس المكتبات بالظبط باستخدام:
</div>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip install -r requirements.txt</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div></div></template>


