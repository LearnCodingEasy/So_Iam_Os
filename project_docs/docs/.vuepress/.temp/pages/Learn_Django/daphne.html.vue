<template><div><h1 id="so-iam-os-—-daphne" tabindex="-1"><a class="header-anchor" href="#so-iam-os-—-daphne"><span>SO_IAM_OS — Daphne</span></a></h1>
<h2 id="_1-تعريف-المعرفة" tabindex="-1"><a class="header-anchor" href="#_1-تعريف-المعرفة"><span>1. تعريف المعرفة</span></a></h2>
<p><strong>Daphne</strong> هو خادم ASGI يتم تثبيته داخل بيئة Python الخاصة بمشروع <strong>SO_IAM_OS</strong>.</p>
<hr>
<h2 id="_2-تثبيت-daphne" tabindex="-1"><a class="header-anchor" href="#_2-تثبيت-daphne"><span>2. تثبيت Daphne</span></a></h2>
<p>يتم تثبيت المكتبة باستخدام:</p>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip install daphne</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><hr>
<h2 id="_3-مكان-التثبيت" tabindex="-1"><a class="header-anchor" href="#_3-مكان-التثبيت"><span>3. مكان التثبيت</span></a></h2>
<p>يجب تنفيذ الأمر داخل بيئة Python الافتراضية الخاصة بالمشروع:</p>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">(venv)</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><p>مثال:</p>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">(venv) D:\So_Iam_Os\backend_django&gt;pip install daphne</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><hr>
<h2 id="_4-دور-daphne-في-المشروع" tabindex="-1"><a class="header-anchor" href="#_4-دور-daphne-في-المشروع"><span>4. دور Daphne في المشروع</span></a></h2>
<p>المعلومة المتوفرة في المصدر تحدد <strong>تثبيت Daphne فقط</strong>:</p>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip install daphne</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><p>ولا يحدد المصدر هنا إعدادًا إضافيًا لـ Daphne أو طريقة تشغيله أو ربطه مع <code v-pre>ASGI_APPLICATION</code>.</p>
<p>لذلك لا يتم اعتبار أي إعدادات أخرى جزءًا من هذه المعرفة إلا بعد إضافتها إلى معرفة المشروع بشكل صريح.</p>
<hr>
<h2 id="_5-حالة-المعرفة" tabindex="-1"><a class="header-anchor" href="#_5-حالة-المعرفة"><span>5. حالة المعرفة</span></a></h2>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Daphne</span>
<span class="line">  ↓</span>
<span class="line">pip install daphne</span>
<span class="line">  ↓</span>
<span class="line">متاح داخل بيئة المشروع</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><p><strong>الحالة:</strong> تم تحديد وتوثيق خطوة تثبيت Daphne فقط.</p>
</div></template>


