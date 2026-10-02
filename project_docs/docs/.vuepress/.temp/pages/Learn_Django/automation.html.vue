<template><div><h1 id="automation" tabindex="-1"><a class="header-anchor" href="#automation"><span>automation</span></a></h1>
<h2 id="app" tabindex="-1"><a class="header-anchor" href="#app"><span>app</span></a></h2>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">python manage.py startapp automation</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h2 id="_1️⃣-program" tabindex="-1"><a class="header-anchor" href="#_1️⃣-program"><span>1️⃣ Program</span></a></h2>
<h3 id="models" tabindex="-1"><a class="header-anchor" href="#models"><span>models</span></a></h3>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token triple-quoted-string string">"""</span>
<span class="line">models.py</span>
<span class="line">==========</span>
<span class="line">الملف ده هو عقل الداتابيز كله</span>
<span class="line">أي Automation – Workflow – Node – Action</span>
<span class="line">لازم يعدي من هنا الأول</span>
<span class="line"></span>
<span class="line">اقرأ التعليقات كويس 👇</span>
<span class="line">"""</span></span>
<span class="line"></span>
<span class="line"><span class="token keyword">from</span> django<span class="token punctuation">.</span>db <span class="token keyword">import</span> models</span>
<span class="line"><span class="token keyword">from</span> django<span class="token punctuation">.</span>conf <span class="token keyword">import</span> settings</span>
<span class="line"><span class="token keyword">import</span> uuid</span>
<span class="line"></span>
<span class="line"><span class="token comment"># App User</span></span>
<span class="line"><span class="token keyword">from</span> users_accounts<span class="token punctuation">.</span>models <span class="token keyword">import</span> User</span>
<span class="line"></span>
<span class="line"><span class="token keyword">from</span> django<span class="token punctuation">.</span>utils<span class="token punctuation">.</span>text <span class="token keyword">import</span> slugify</span>
<span class="line"></span>
<span class="line"><span class="token comment"># ==================================================</span></span>
<span class="line"><span class="token comment"># 1️⃣ Program</span></span>
<span class="line"><span class="token comment"># ==================================================</span></span>
<span class="line"><span class="token keyword">class</span> <span class="token class-name">Program</span><span class="token punctuation">(</span>models<span class="token punctuation">.</span>Model<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">    <span class="token triple-quoted-string string">"""</span>
<span class="line">    🖥️ يمثل أي برنامج على جهازك</span>
<span class="line">    (Photoshop – Chrome – Premiere – VSCode)</span>
<span class="line"></span>
<span class="line">    الهدف:</span>
<span class="line">    - السيستم يبقى فاهم البرنامج</span>
<span class="line">    - يعرف يضغط فين</span>
<span class="line">    - يعرف يستخدم الاختصارات</span>
<span class="line">    """</span></span>
<span class="line"></span>
<span class="line">    <span class="token comment"># ====================== 🆔 IDs ======================</span></span>
<span class="line">    <span class="token builtin">id</span> <span class="token operator">=</span> models<span class="token punctuation">.</span>UUIDField<span class="token punctuation">(</span>primary_key<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">,</span> default<span class="token operator">=</span>uuid<span class="token punctuation">.</span>uuid4<span class="token punctuation">,</span> editable<span class="token operator">=</span><span class="token boolean">False</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">    <span class="token comment"># ====================== ℹ️ Basic Info ======================</span></span>
<span class="line">    <span class="token comment"># اسم البرنامج اللي هيظهر في الواجهة</span></span>
<span class="line">    name <span class="token operator">=</span> models<span class="token punctuation">.</span>CharField<span class="token punctuation">(</span>max_length<span class="token operator">=</span><span class="token number">100</span><span class="token punctuation">)</span></span>
<span class="line">    slug <span class="token operator">=</span> models<span class="token punctuation">.</span>SlugField<span class="token punctuation">(</span>unique<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">,</span> blank<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span>  <span class="token comment"># URL-friendly</span></span>
<span class="line">    description <span class="token operator">=</span> models<span class="token punctuation">.</span>TextField<span class="token punctuation">(</span>blank<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span>  <span class="token comment"># وصف اختياري</span></span>
<span class="line"></span>
<span class="line">    <span class="token comment"># ====================== ⚡ Execution ======================</span></span>
<span class="line">    executable_path <span class="token operator">=</span> models<span class="token punctuation">.</span>CharField<span class="token punctuation">(</span>max_length<span class="token operator">=</span><span class="token number">500</span><span class="token punctuation">)</span>  <span class="token comment"># مسار تشغيل البرنامج</span></span>
<span class="line">    project_path <span class="token operator">=</span> models<span class="token punctuation">.</span>CharField<span class="token punctuation">(</span></span>
<span class="line">        max_length<span class="token operator">=</span><span class="token number">500</span><span class="token punctuation">,</span> blank<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">,</span> null<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span>  <span class="token comment"># مشروع مرتبط</span></span>
<span class="line">    working_directory <span class="token operator">=</span> models<span class="token punctuation">.</span>CharField<span class="token punctuation">(</span></span>
<span class="line">        max_length<span class="token operator">=</span><span class="token number">500</span><span class="token punctuation">,</span> blank<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">,</span> null<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span>  <span class="token comment"># فولدر تشغيل</span></span>
<span class="line">    window_title_pattern <span class="token operator">=</span> models<span class="token punctuation">.</span>CharField<span class="token punctuation">(</span></span>
<span class="line">        max_length<span class="token operator">=</span><span class="token number">255</span><span class="token punctuation">,</span> blank<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span>  <span class="token comment"># عنوان الشباك للتأكد</span></span>
<span class="line">    global_shortcuts <span class="token operator">=</span> models<span class="token punctuation">.</span>JSONField<span class="token punctuation">(</span></span>
<span class="line">        default<span class="token operator">=</span><span class="token builtin">dict</span><span class="token punctuation">,</span> blank<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span>  <span class="token comment"># اختصارات عامة</span></span>
<span class="line"></span>
<span class="line">    <span class="token comment"># ====================== 📊 State ======================</span></span>
<span class="line">    is_running <span class="token operator">=</span> models<span class="token punctuation">.</span>BooleanField<span class="token punctuation">(</span>default<span class="token operator">=</span><span class="token boolean">False</span><span class="token punctuation">)</span>  <span class="token comment"># هل البرنامج شغال</span></span>
<span class="line">    last_run_at <span class="token operator">=</span> models<span class="token punctuation">.</span>DateTimeField<span class="token punctuation">(</span>null<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">,</span> blank<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span></span>
<span class="line">    last_status <span class="token operator">=</span> models<span class="token punctuation">.</span>CharField<span class="token punctuation">(</span></span>
<span class="line">        max_length<span class="token operator">=</span><span class="token number">50</span><span class="token punctuation">,</span></span>
<span class="line">        choices<span class="token operator">=</span><span class="token punctuation">[</span></span>
<span class="line">            <span class="token punctuation">(</span><span class="token string">"success"</span><span class="token punctuation">,</span> <span class="token string">"Success"</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token punctuation">(</span><span class="token string">"failed"</span><span class="token punctuation">,</span> <span class="token string">"Failed"</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token punctuation">(</span><span class="token string">"running"</span><span class="token punctuation">,</span> <span class="token string">"Running"</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token punctuation">(</span><span class="token string">"idle"</span><span class="token punctuation">,</span> <span class="token string">"Idle"</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token punctuation">]</span><span class="token punctuation">,</span></span>
<span class="line">        default<span class="token operator">=</span><span class="token string">"idle"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">    <span class="token comment"># ====================== 🎨 UI / Visual ======================</span></span>
<span class="line">    icon <span class="token operator">=</span> models<span class="token punctuation">.</span>CharField<span class="token punctuation">(</span>max_length<span class="token operator">=</span><span class="token number">100</span><span class="token punctuation">,</span> blank<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span></span>
<span class="line">    image <span class="token operator">=</span> models<span class="token punctuation">.</span>ImageField<span class="token punctuation">(</span>upload_to<span class="token operator">=</span><span class="token string">"programs"</span><span class="token punctuation">,</span> blank<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">,</span> null<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span></span>
<span class="line">    is_installed <span class="token operator">=</span> models<span class="token punctuation">.</span>BooleanField<span class="token punctuation">(</span>default<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">    <span class="token comment"># ====================== ⚙️ Configuration ======================</span></span>
<span class="line">    settings <span class="token operator">=</span> models<span class="token punctuation">.</span>JSONField<span class="token punctuation">(</span>default<span class="token operator">=</span><span class="token builtin">dict</span><span class="token punctuation">,</span> blank<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span>  <span class="token comment"># إعدادات مخصصة</span></span>
<span class="line">    env_variables <span class="token operator">=</span> models<span class="token punctuation">.</span>JSONField<span class="token punctuation">(</span></span>
<span class="line">        default<span class="token operator">=</span><span class="token builtin">dict</span><span class="token punctuation">,</span> blank<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span>  <span class="token comment"># متغيرات البيئة</span></span>
<span class="line"></span>
<span class="line">    <span class="token comment"># ====================== 🗂️ Meta ======================</span></span>
<span class="line">    created_at <span class="token operator">=</span> models<span class="token punctuation">.</span>DateTimeField<span class="token punctuation">(</span>auto_now_add<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span></span>
<span class="line">    updated_at <span class="token operator">=</span> models<span class="token punctuation">.</span>DateTimeField<span class="token punctuation">(</span>auto_now<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">    <span class="token comment"># ====================== 🖼️ Helper ======================</span></span>
<span class="line">    <span class="token keyword">def</span> <span class="token function">get_image</span><span class="token punctuation">(</span>self<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">        <span class="token keyword">if</span> self<span class="token punctuation">.</span>image<span class="token punctuation">:</span></span>
<span class="line">            <span class="token keyword">return</span> settings<span class="token punctuation">.</span>WEBSITE_URL <span class="token operator">+</span> self<span class="token punctuation">.</span>image<span class="token punctuation">.</span>url</span>
<span class="line">        <span class="token keyword">return</span> <span class="token string">"https://placehold.co/400x400?text=Program"</span></span>
<span class="line"></span>
<span class="line">    <span class="token comment"># ====================== 💾 Auto Save Slug ======================</span></span>
<span class="line">    <span class="token keyword">def</span> <span class="token function">save</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> <span class="token operator">*</span>args<span class="token punctuation">,</span> <span class="token operator">**</span>kwargs<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">        <span class="token keyword">if</span> <span class="token keyword">not</span> self<span class="token punctuation">.</span>slug<span class="token punctuation">:</span></span>
<span class="line">            base_slug <span class="token operator">=</span> slugify<span class="token punctuation">(</span>self<span class="token punctuation">.</span>name<span class="token punctuation">)</span></span>
<span class="line">            slug <span class="token operator">=</span> base_slug</span>
<span class="line">            counter <span class="token operator">=</span> <span class="token number">1</span></span>
<span class="line">            <span class="token keyword">while</span> Program<span class="token punctuation">.</span>objects<span class="token punctuation">.</span><span class="token builtin">filter</span><span class="token punctuation">(</span>slug<span class="token operator">=</span>slug<span class="token punctuation">)</span><span class="token punctuation">.</span>exists<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">                slug <span class="token operator">=</span> <span class="token string-interpolation"><span class="token string">f"</span><span class="token interpolation"><span class="token punctuation">{</span>base_slug<span class="token punctuation">}</span></span><span class="token string">-</span><span class="token interpolation"><span class="token punctuation">{</span>counter<span class="token punctuation">}</span></span><span class="token string">"</span></span></span>
<span class="line">                counter <span class="token operator">+=</span> <span class="token number">1</span></span>
<span class="line">            self<span class="token punctuation">.</span>slug <span class="token operator">=</span> slug</span>
<span class="line">        <span class="token builtin">super</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span>save<span class="token punctuation">(</span><span class="token operator">*</span>args<span class="token punctuation">,</span> <span class="token operator">**</span>kwargs<span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">    <span class="token keyword">def</span> <span class="token function">__str__</span><span class="token punctuation">(</span>self<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">        <span class="token keyword">return</span> self<span class="token punctuation">.</span>name</span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h3 id="serializers" tabindex="-1"><a class="header-anchor" href="#serializers"><span>serializers</span></a></h3>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># backend_django\automation\serializers.py</span></span>
<span class="line"></span>
<span class="line"><span class="token keyword">from</span> rest_framework <span class="token keyword">import</span> serializers</span>
<span class="line"><span class="token keyword">from</span> <span class="token punctuation">.</span>models <span class="token keyword">import</span> Program</span>
<span class="line"></span>
<span class="line"><span class="token keyword">class</span> <span class="token class-name">ProgramSerializer</span><span class="token punctuation">(</span>serializers<span class="token punctuation">.</span>ModelSerializer<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">    <span class="token keyword">class</span> <span class="token class-name">Meta</span><span class="token punctuation">:</span></span>
<span class="line">        model <span class="token operator">=</span> Program</span>
<span class="line">        fields <span class="token operator">=</span> <span class="token string">"__all__"</span></span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h3 id="views" tabindex="-1"><a class="header-anchor" href="#views"><span>views</span></a></h3>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># backend_django\automation\views.py</span></span>
<span class="line"></span>
<span class="line"><span class="token keyword">from</span> rest_framework <span class="token keyword">import</span> viewsets<span class="token punctuation">,</span> status</span>
<span class="line"><span class="token keyword">from</span> rest_framework<span class="token punctuation">.</span>decorators <span class="token keyword">import</span> action</span>
<span class="line"><span class="token keyword">from</span> rest_framework<span class="token punctuation">.</span>response <span class="token keyword">import</span> Response</span>
<span class="line"><span class="token keyword">from</span> rest_framework<span class="token punctuation">.</span>generics <span class="token keyword">import</span> ListAPIView</span>
<span class="line"><span class="token keyword">from</span> rest_framework<span class="token punctuation">.</span>viewsets <span class="token keyword">import</span> ReadOnlyModelViewSet</span>
<span class="line"></span>
<span class="line"><span class="token keyword">from</span> django<span class="token punctuation">.</span>utils <span class="token keyword">import</span> timezone</span>
<span class="line"></span>
<span class="line"><span class="token keyword">from</span> <span class="token punctuation">.</span>models <span class="token keyword">import</span> Program</span>
<span class="line"><span class="token keyword">from</span> <span class="token punctuation">.</span>serializers <span class="token keyword">import</span> ProgramSerializer</span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token keyword">class</span> <span class="token class-name">ProgramViewSet</span><span class="token punctuation">(</span>viewsets<span class="token punctuation">.</span>ModelViewSet<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">    <span class="token triple-quoted-string string">"""</span>
<span class="line">    🖥️ ViewSet لإدارة البرامج وتشغيلها وتتبع حالتها</span>
<span class="line">    """</span></span>
<span class="line">    queryset <span class="token operator">=</span> Program<span class="token punctuation">.</span>objects<span class="token punctuation">.</span><span class="token builtin">all</span><span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line">    serializer_class <span class="token operator">=</span> ProgramSerializer</span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h3 id="urls" tabindex="-1"><a class="header-anchor" href="#urls"><span>urls</span></a></h3>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"></span>
<span class="line"><span class="token comment"># backend_django\automation\urls.py</span></span>
<span class="line"><span class="token keyword">from</span> rest_framework<span class="token punctuation">.</span>routers <span class="token keyword">import</span> DefaultRouter</span>
<span class="line"><span class="token keyword">from</span> <span class="token punctuation">.</span>views <span class="token keyword">import</span> ProgramViewSet</span>
<span class="line"></span>
<span class="line">router <span class="token operator">=</span> DefaultRouter<span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">router<span class="token punctuation">.</span>register<span class="token punctuation">(</span><span class="token string">"programs"</span><span class="token punctuation">,</span> ProgramViewSet<span class="token punctuation">,</span> basename<span class="token operator">=</span><span class="token string">"programs"</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">urlpatterns <span class="token operator">=</span> router<span class="token punctuation">.</span>urls</span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h3 id="admin" tabindex="-1"><a class="header-anchor" href="#admin"><span>admin</span></a></h3>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># backend_django\automation\admin.py</span></span>
<span class="line"></span>
<span class="line"><span class="token comment"># 🛠️ Django استيراد أدوات إدارة</span></span>
<span class="line"><span class="token keyword">from</span> django<span class="token punctuation">.</span>contrib <span class="token keyword">import</span> admin</span>
<span class="line"></span>
<span class="line"><span class="token comment"># 🌐 (Model) استيراد نموذج</span></span>
<span class="line"><span class="token keyword">from</span> <span class="token punctuation">.</span>models <span class="token keyword">import</span> Program</span>
<span class="line"></span>
<span class="line"><span class="token comment"># 🖥️ في لوحة الإدارة Website تسجيل نموذج</span></span>
<span class="line">admin<span class="token punctuation">.</span>site<span class="token punctuation">.</span>register<span class="token punctuation">(</span>Program<span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h2 id="app-1" tabindex="-1"><a class="header-anchor" href="#app-1"><span>app</span></a></h2>
<h2 id="app-2" tabindex="-1"><a class="header-anchor" href="#app-2"><span>app</span></a></h2>
<h2 id="app-3" tabindex="-1"><a class="header-anchor" href="#app-3"><span>app</span></a></h2>
</div></template>


