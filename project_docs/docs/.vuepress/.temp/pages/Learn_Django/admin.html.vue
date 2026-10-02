<template><div><h1 id="django-page-admin" tabindex="-1"><a class="header-anchor" href="#django-page-admin"><span>Django Page Admin</span></a></h1>
<div dir="rtl" style="font-size:1.2vw; padding: 1rem 0; font-weight: 900;">
  الطريقة الطبيعية 
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># 🛠️ استيراد أدوات إدارة Django</span></span>
<span class="line"><span class="token keyword">from</span> django<span class="token punctuation">.</span>contrib <span class="token keyword">import</span> admin  </span>
<span class="line"></span>
<span class="line"><span class="token comment"># 🌐 استيراد نموذج (Model) موقع الويب</span></span>
<span class="line"><span class="token keyword">from</span> <span class="token punctuation">.</span>models <span class="token keyword">import</span> Website  </span>
<span class="line"></span>
<span class="line"><span class="token comment"># 🖥️ تسجيل نموذج Website في لوحة الإدارة</span></span>
<span class="line">admin<span class="token punctuation">.</span>site<span class="token punctuation">.</span>register<span class="token punctuation">(</span>Website<span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size:1.2vw; padding: 1rem 0; font-weight: 900;">
  تخصيص عرض الحقول وإضافة مميزات مثل البحث، الفلاتر، والترتيب 
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># 🛠️ استيراد أدوات الإدارة</span></span>
<span class="line"><span class="token keyword">from</span> django<span class="token punctuation">.</span>contrib <span class="token keyword">import</span> admin</span>
<span class="line"></span>
<span class="line"><span class="token comment"># 🌐 استيراد نموذج موقع الويب</span></span>
<span class="line"><span class="token keyword">from</span> <span class="token punctuation">.</span>models <span class="token keyword">import</span> User</span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token comment"># 🖥️ تخصيص عرض النموذج في لوحة الإدارة</span></span>
<span class="line"><span class="token decorator annotation punctuation">@admin<span class="token punctuation">.</span>register</span><span class="token punctuation">(</span>User<span class="token punctuation">)</span></span>
<span class="line"><span class="token keyword">class</span> <span class="token class-name">UserAdmin</span><span class="token punctuation">(</span>admin<span class="token punctuation">.</span>ModelAdmin<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">    <span class="token comment"># 🌟 الحقول التي ستظهر في قائمة الإدارة</span></span>
<span class="line">    list_display <span class="token operator">=</span> <span class="token punctuation">(</span></span>
<span class="line">        <span class="token string">"name"</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">"surname"</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">"is_online"</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">"email"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">    <span class="token comment"># 🔍 تمكين البحث عبر الحقول</span></span>
<span class="line">    search_fields <span class="token operator">=</span> <span class="token punctuation">(</span><span class="token string">"name"</span><span class="token punctuation">,</span> <span class="token string">"surname"</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">    <span class="token comment"># 🗂️ إضافة فلاتر حسب اللغة</span></span>
<span class="line">    list_filter <span class="token operator">=</span> <span class="token punctuation">(</span><span class="token string">"is_online"</span><span class="token punctuation">,</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">    <span class="token comment"># 🔃 ترتيب النتائج حسب الاسم</span></span>
<span class="line">    ordering <span class="token operator">=</span> <span class="token punctuation">(</span><span class="token string">"name"</span><span class="token punctuation">,</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">    <span class="token comment"># 📝 تحديد الحقول التي يمكن تعديلها داخل شاشة تحرير المستخدم</span></span>
<span class="line">    fields <span class="token operator">=</span> <span class="token punctuation">(</span><span class="token string">"name"</span><span class="token punctuation">,</span> <span class="token string">"surname"</span><span class="token punctuation">,</span> <span class="token string">"email"</span><span class="token punctuation">,</span> <span class="token string">"is_online"</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div></div></template>


