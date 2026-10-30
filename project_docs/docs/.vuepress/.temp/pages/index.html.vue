<template><div><h1 id="project-name" tabindex="-1"><a class="header-anchor" href="#project-name"><span>Project Name</span></a></h1>
<h2 id="github" tabindex="-1"><a class="header-anchor" href="#github"><span>Github</span></a></h2>
<ul>
<li><RouteLink to="/Learn_Github/">Github</RouteLink></li>
</ul>
<hr>
<h2 id="license" tabindex="-1"><a class="header-anchor" href="#license"><span>LICENSE</span></a></h2>
<ul>
<li><RouteLink to="/Learn_License/">LICENSE</RouteLink></li>
</ul>
<hr>
<h2 id="vite-press" tabindex="-1"><a class="header-anchor" href="#vite-press"><span>Vite Press</span></a></h2>
<ul>
<li><RouteLink to="/Learn_Vite_Press/">Vite Press</RouteLink></li>
</ul>
<hr>
<h2 id="django" tabindex="-1"><a class="header-anchor" href="#django"><span>Django</span></a></h2>
<ul>
<li><RouteLink to="/Learn_Django/">Django</RouteLink></li>
</ul>
<h3 id="🔧-django" tabindex="-1"><a class="header-anchor" href="#🔧-django"><span>🔧 Django</span></a></h3>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip install python-decouple</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip install lxml</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip install playwright celery redis</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">playwright install</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip install playwright</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip install gspread oauth2client</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip install rich</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h3 id="🕸️-scraper" tabindex="-1"><a class="header-anchor" href="#🕸️-scraper"><span>🕸️ scraper</span></a></h3>
<h4 id="📝-models-py" tabindex="-1"><a class="header-anchor" href="#📝-models-py"><span>📝 [ models.py ]</span></a></h4>
<ul>
<li>
<p>يمثل موقع إلكتروني واحد هتسحب منه البيانات.</p>
</li>
<li>
<p>كل موقع ليه اسم + رابط رئيسي + وصف + حالة التفعيل.</p>
</li>
</ul>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">from</span> django<span class="token punctuation">.</span>db <span class="token keyword">import</span> models</span>
<span class="line"><span class="token keyword">from</span> django<span class="token punctuation">.</span>contrib<span class="token punctuation">.</span>auth<span class="token punctuation">.</span>models <span class="token keyword">import</span> User</span>
<span class="line"><span class="token keyword">import</span> json</span>
<span class="line"></span>
<span class="line"><span class="token keyword">class</span> <span class="token class-name">Website</span><span class="token punctuation">(</span>models<span class="token punctuation">.</span>Model<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">    name <span class="token operator">=</span> models<span class="token punctuation">.</span>CharField<span class="token punctuation">(</span>max_length<span class="token operator">=</span><span class="token number">200</span><span class="token punctuation">)</span></span>
<span class="line">    base_url <span class="token operator">=</span> models<span class="token punctuation">.</span>URLField<span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line">    description <span class="token operator">=</span> models<span class="token punctuation">.</span>TextField<span class="token punctuation">(</span>blank<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span></span>
<span class="line">    is_active <span class="token operator">=</span> models<span class="token punctuation">.</span>BooleanField<span class="token punctuation">(</span>default<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span></span>
<span class="line">    created_at <span class="token operator">=</span> models<span class="token punctuation">.</span>DateTimeField<span class="token punctuation">(</span>auto_now_add<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span></span>
<span class="line">    updated_at <span class="token operator">=</span> models<span class="token punctuation">.</span>DateTimeField<span class="token punctuation">(</span>auto_now<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">    <span class="token keyword">def</span> <span class="token function">__str__</span><span class="token punctuation">(</span>self<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">        <span class="token keyword">return</span> self<span class="token punctuation">.</span>name</span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><ul>
<li>
<p>بيمثل إعدادات السحب (scraping) لموقع معين.</p>
</li>
<li>
<p>بيقولك هتسحب إيه، و منين، و إزاي.</p>
</li>
<li>
<p>Meta يعني ما ينفعش يكون في موقع عنده نفس field_name مرتين.</p>
</li>
</ul>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">class</span> <span class="token class-name">ScrapingConfig</span><span class="token punctuation">(</span>models<span class="token punctuation">.</span>Model<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">    SELECTOR_TYPES <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line">        <span class="token punctuation">(</span><span class="token string">'css'</span><span class="token punctuation">,</span> <span class="token string">'CSS Selector'</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token punctuation">(</span><span class="token string">'xpath'</span><span class="token punctuation">,</span> <span class="token string">'XPath'</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">]</span></span>
<span class="line"></span>
<span class="line">    website <span class="token operator">=</span> models<span class="token punctuation">.</span>ForeignKey<span class="token punctuation">(</span></span>
<span class="line">        Website<span class="token punctuation">,</span> on_delete<span class="token operator">=</span>models<span class="token punctuation">.</span>CASCADE<span class="token punctuation">,</span> related_name<span class="token operator">=</span><span class="token string">'configs'</span><span class="token punctuation">)</span></span>
<span class="line">    <span class="token comment"># e.g., 'product_name', 'price', 'description'</span></span>
<span class="line">    field_name <span class="token operator">=</span> models<span class="token punctuation">.</span>CharField<span class="token punctuation">(</span>max_length<span class="token operator">=</span><span class="token number">100</span><span class="token punctuation">)</span></span>
<span class="line">    selector <span class="token operator">=</span> models<span class="token punctuation">.</span>TextField<span class="token punctuation">(</span><span class="token punctuation">)</span>  <span class="token comment"># The actual CSS selector or XPath</span></span>
<span class="line">    selector_type <span class="token operator">=</span> models<span class="token punctuation">.</span>CharField<span class="token punctuation">(</span></span>
<span class="line">        max_length<span class="token operator">=</span><span class="token number">10</span><span class="token punctuation">,</span> choices<span class="token operator">=</span>SELECTOR_TYPES<span class="token punctuation">,</span> default<span class="token operator">=</span><span class="token string">'css'</span><span class="token punctuation">)</span></span>
<span class="line">    is_required <span class="token operator">=</span> models<span class="token punctuation">.</span>BooleanField<span class="token punctuation">(</span>default<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span></span>
<span class="line">    <span class="token comment"># text, number, url, etc.</span></span>
<span class="line">    data_type <span class="token operator">=</span> models<span class="token punctuation">.</span>CharField<span class="token punctuation">(</span>max_length<span class="token operator">=</span><span class="token number">50</span><span class="token punctuation">,</span> default<span class="token operator">=</span><span class="token string">'text'</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">    <span class="token keyword">class</span> <span class="token class-name">Meta</span><span class="token punctuation">:</span></span>
<span class="line">        unique_together <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token string">'website'</span><span class="token punctuation">,</span> <span class="token string">'field_name'</span><span class="token punctuation">]</span></span>
<span class="line"></span>
<span class="line">    <span class="token keyword">def</span> <span class="token function">__str__</span><span class="token punctuation">(</span>self<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">        <span class="token keyword">return</span> <span class="token string-interpolation"><span class="token string">f"</span><span class="token interpolation"><span class="token punctuation">{</span>self<span class="token punctuation">.</span>website<span class="token punctuation">.</span>name<span class="token punctuation">}</span></span><span class="token string"> - </span><span class="token interpolation"><span class="token punctuation">{</span>self<span class="token punctuation">.</span>field_name<span class="token punctuation">}</span></span><span class="token string">"</span></span></span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><ul>
<li>
<p>كل مهمة (Job) بتمثل محاولة لسحب البيانات من موقع معين.</p>
</li>
<li>
<p>بترصد الحالة (pending - running - completed - failed)</p>
</li>
</ul>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">class</span> <span class="token class-name">ScrapingJob</span><span class="token punctuation">(</span>models<span class="token punctuation">.</span>Model<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">    STATUS_CHOICES <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line">        <span class="token punctuation">(</span><span class="token string">'pending'</span><span class="token punctuation">,</span> <span class="token string">'Pending'</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token punctuation">(</span><span class="token string">'running'</span><span class="token punctuation">,</span> <span class="token string">'Running'</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token punctuation">(</span><span class="token string">'completed'</span><span class="token punctuation">,</span> <span class="token string">'Completed'</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token punctuation">(</span><span class="token string">'failed'</span><span class="token punctuation">,</span> <span class="token string">'Failed'</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">]</span></span>
<span class="line"></span>
<span class="line">    website <span class="token operator">=</span> models<span class="token punctuation">.</span>ForeignKey<span class="token punctuation">(</span>Website<span class="token punctuation">,</span> on_delete<span class="token operator">=</span>models<span class="token punctuation">.</span>CASCADE<span class="token punctuation">)</span></span>
<span class="line">    target_url <span class="token operator">=</span> models<span class="token punctuation">.</span>URLField<span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line">    status <span class="token operator">=</span> models<span class="token punctuation">.</span>CharField<span class="token punctuation">(</span></span>
<span class="line">        max_length<span class="token operator">=</span><span class="token number">20</span><span class="token punctuation">,</span> choices<span class="token operator">=</span>STATUS_CHOICES<span class="token punctuation">,</span> default<span class="token operator">=</span><span class="token string">'pending'</span><span class="token punctuation">)</span></span>
<span class="line">    started_at <span class="token operator">=</span> models<span class="token punctuation">.</span>DateTimeField<span class="token punctuation">(</span>auto_now_add<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span></span>
<span class="line">    completed_at <span class="token operator">=</span> models<span class="token punctuation">.</span>DateTimeField<span class="token punctuation">(</span>null<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">,</span> blank<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span></span>
<span class="line">    error_message <span class="token operator">=</span> models<span class="token punctuation">.</span>TextField<span class="token punctuation">(</span>blank<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span></span>
<span class="line">    items_scraped <span class="token operator">=</span> models<span class="token punctuation">.</span>IntegerField<span class="token punctuation">(</span>default<span class="token operator">=</span><span class="token number">0</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">    <span class="token keyword">def</span> <span class="token function">__str__</span><span class="token punctuation">(</span>self<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">        <span class="token keyword">return</span> <span class="token string-interpolation"><span class="token string">f"</span><span class="token interpolation"><span class="token punctuation">{</span>self<span class="token punctuation">.</span>website<span class="token punctuation">.</span>name<span class="token punctuation">}</span></span><span class="token string"> - </span><span class="token interpolation"><span class="token punctuation">{</span>self<span class="token punctuation">.</span>started_at<span class="token punctuation">.</span>strftime<span class="token punctuation">(</span><span class="token string">'%Y-%m-%d %H:%M'</span><span class="token punctuation">)</span><span class="token punctuation">}</span></span><span class="token string">"</span></span></span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><ul>
<li>
<p>بيمثل عنصر بيانات تم سحبه في نتيجة Job معينة.</p>
</li>
<li>
<p>بيتخزن كـ JSON.</p>
</li>
</ul>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">class</span> <span class="token class-name">ScrapedData</span><span class="token punctuation">(</span>models<span class="token punctuation">.</span>Model<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">    job <span class="token operator">=</span> models<span class="token punctuation">.</span>ForeignKey<span class="token punctuation">(</span></span>
<span class="line">        ScrapingJob<span class="token punctuation">,</span> on_delete<span class="token operator">=</span>models<span class="token punctuation">.</span>CASCADE<span class="token punctuation">,</span> related_name<span class="token operator">=</span><span class="token string">'scraped_items'</span><span class="token punctuation">)</span></span>
<span class="line">    data <span class="token operator">=</span> models<span class="token punctuation">.</span>JSONField<span class="token punctuation">(</span><span class="token punctuation">)</span>  <span class="token comment"># Stores the actual scraped data as JSON</span></span>
<span class="line">    scraped_at <span class="token operator">=</span> models<span class="token punctuation">.</span>DateTimeField<span class="token punctuation">(</span>auto_now_add<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span></span>
<span class="line">    source_url <span class="token operator">=</span> models<span class="token punctuation">.</span>URLField<span class="token punctuation">(</span><span class="token punctuation">)</span>  <span class="token comment"># The specific page this data came from</span></span>
<span class="line"></span>
<span class="line">    <span class="token keyword">def</span> <span class="token function">__str__</span><span class="token punctuation">(</span>self<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">        <span class="token keyword">return</span> <span class="token string-interpolation"><span class="token string">f"Data from </span><span class="token interpolation"><span class="token punctuation">{</span>self<span class="token punctuation">.</span>job<span class="token punctuation">.</span>website<span class="token punctuation">.</span>name<span class="token punctuation">}</span></span><span class="token string"> - </span><span class="token interpolation"><span class="token punctuation">{</span>self<span class="token punctuation">.</span>scraped_at<span class="token punctuation">}</span></span><span class="token string">"</span></span></span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h4 id="📝-views-py" tabindex="-1"><a class="header-anchor" href="#📝-views-py"><span>📝 [ views.py ]</span></a></h4>
<ul>
<li>
<p>API للتحكم في المواقع (Website) – تقدر تعمل:</p>
</li>
<li>
<p>إنشاء موقع</p>
</li>
<li>
<p>تعديل</p>
</li>
<li>
<p>حذف</p>
</li>
<li>
<p>عرض الكل</p>
</li>
<li>
<p>عرض واحد</p>
</li>
</ul>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">class</span> <span class="token class-name">WebsiteViewSet</span><span class="token punctuation">(</span>viewsets<span class="token punctuation">.</span>ModelViewSet<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">    queryset <span class="token operator">=</span> Website<span class="token punctuation">.</span>objects<span class="token punctuation">.</span><span class="token builtin">all</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span>order_by<span class="token punctuation">(</span></span>
<span class="line">        <span class="token string">'-created_at'</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">    serializer_class <span class="token operator">=</span> WebsiteSerializer</span>
<span class="line"></span>
<span class="line">    <span class="token decorator annotation punctuation">@action</span><span class="token punctuation">(</span>detail<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">,</span> methods<span class="token operator">=</span><span class="token punctuation">[</span><span class="token string">'get'</span><span class="token punctuation">]</span><span class="token punctuation">)</span></span>
<span class="line">    <span class="token keyword">def</span> <span class="token function">configs</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> request<span class="token punctuation">,</span> pk<span class="token operator">=</span><span class="token boolean">None</span><span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">        <span class="token triple-quoted-string string">"""Get all scraping configurations for a website"""</span></span>
<span class="line">        website <span class="token operator">=</span> self<span class="token punctuation">.</span>get_object<span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line">        configs <span class="token operator">=</span> website<span class="token punctuation">.</span>configs<span class="token punctuation">.</span><span class="token builtin">all</span><span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line">        serializer <span class="token operator">=</span> ScrapingConfigSerializer<span class="token punctuation">(</span>configs<span class="token punctuation">,</span> many<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span></span>
<span class="line">        <span class="token keyword">return</span> Response<span class="token punctuation">(</span>serializer<span class="token punctuation">.</span>data<span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">    <span class="token decorator annotation punctuation">@action</span><span class="token punctuation">(</span>detail<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">,</span> methods<span class="token operator">=</span><span class="token punctuation">[</span><span class="token string">'get'</span><span class="token punctuation">]</span><span class="token punctuation">)</span></span>
<span class="line">    <span class="token keyword">def</span> <span class="token function">jobs</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> request<span class="token punctuation">,</span> pk<span class="token operator">=</span><span class="token boolean">None</span><span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">        <span class="token triple-quoted-string string">"""Get all scraping jobs for a website"""</span></span>
<span class="line">        website <span class="token operator">=</span> self<span class="token punctuation">.</span>get_object<span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line">        jobs <span class="token operator">=</span> website<span class="token punctuation">.</span>scrapingjob_set<span class="token punctuation">.</span><span class="token builtin">all</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span>order_by<span class="token punctuation">(</span><span class="token string">'-started_at'</span><span class="token punctuation">)</span></span>
<span class="line">        serializer <span class="token operator">=</span> ScrapingJobSerializer<span class="token punctuation">(</span>jobs<span class="token punctuation">,</span> many<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span></span>
<span class="line">        <span class="token keyword">return</span> Response<span class="token punctuation">(</span>serializer<span class="token punctuation">.</span>data<span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><ul>
<li>بيرجع كل إعدادات السحب (ScrapingConfig) الخاصة بالموقع ده.</li>
</ul>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">class</span> <span class="token class-name">ScrapingConfigViewSet</span><span class="token punctuation">(</span>viewsets<span class="token punctuation">.</span>ModelViewSet<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">    serializer_class <span class="token operator">=</span> ScrapingConfigSerializer</span>
<span class="line"></span>
<span class="line">    <span class="token keyword">def</span> <span class="token function">get_queryset</span><span class="token punctuation">(</span>self<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">        website_id <span class="token operator">=</span> self<span class="token punctuation">.</span>request<span class="token punctuation">.</span>query_params<span class="token punctuation">.</span>get<span class="token punctuation">(</span><span class="token string">'website'</span><span class="token punctuation">,</span> <span class="token boolean">None</span><span class="token punctuation">)</span></span>
<span class="line">        <span class="token keyword">if</span> website_id<span class="token punctuation">:</span></span>
<span class="line">            <span class="token keyword">return</span> ScrapingConfig<span class="token punctuation">.</span>objects<span class="token punctuation">.</span><span class="token builtin">filter</span><span class="token punctuation">(</span>website_id<span class="token operator">=</span>website_id<span class="token punctuation">)</span></span>
<span class="line">        <span class="token keyword">return</span> ScrapingConfig<span class="token punctuation">.</span>objects<span class="token punctuation">.</span><span class="token builtin">all</span><span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><ul>
<li>بيرجع كل مهام السحب (ScrapingJob) الخاصة بالموقع ده.</li>
</ul>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"></span>
<span class="line"><span class="token keyword">class</span> <span class="token class-name">ScrapingJobViewSet</span><span class="token punctuation">(</span>viewsets<span class="token punctuation">.</span>ModelViewSet<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">    queryset <span class="token operator">=</span> ScrapingJob<span class="token punctuation">.</span>objects<span class="token punctuation">.</span><span class="token builtin">all</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span>order_by<span class="token punctuation">(</span><span class="token string">'-started_at'</span><span class="token punctuation">)</span></span>
<span class="line">    serializer_class <span class="token operator">=</span> ScrapingJobSerializer</span>
<span class="line"></span>
<span class="line">    <span class="token decorator annotation punctuation">@action</span><span class="token punctuation">(</span>detail<span class="token operator">=</span><span class="token boolean">False</span><span class="token punctuation">,</span> methods<span class="token operator">=</span><span class="token punctuation">[</span><span class="token string">'post'</span><span class="token punctuation">]</span><span class="token punctuation">)</span></span>
<span class="line">    <span class="token keyword">def</span> <span class="token function">start_scraping</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> request<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">        <span class="token triple-quoted-string string">"""Start a new scraping job"""</span></span>
<span class="line">        website_id <span class="token operator">=</span> request<span class="token punctuation">.</span>data<span class="token punctuation">.</span>get<span class="token punctuation">(</span><span class="token string">'website_id'</span><span class="token punctuation">)</span></span>
<span class="line">        target_url <span class="token operator">=</span> request<span class="token punctuation">.</span>data<span class="token punctuation">.</span>get<span class="token punctuation">(</span><span class="token string">'target_url'</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">        <span class="token keyword">if</span> <span class="token keyword">not</span> website_id <span class="token keyword">or</span> <span class="token keyword">not</span> target_url<span class="token punctuation">:</span></span>
<span class="line">            <span class="token keyword">return</span> Response<span class="token punctuation">(</span></span>
<span class="line">                <span class="token punctuation">{</span><span class="token string">'error'</span><span class="token punctuation">:</span> <span class="token string">'website_id and target_url are required'</span><span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">                status<span class="token operator">=</span>status<span class="token punctuation">.</span>HTTP_400_BAD_REQUEST</span>
<span class="line">            <span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">        website <span class="token operator">=</span> get_object_or_404<span class="token punctuation">(</span>Website<span class="token punctuation">,</span> <span class="token builtin">id</span><span class="token operator">=</span>website_id<span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">        <span class="token comment"># Create the job</span></span>
<span class="line">        job <span class="token operator">=</span> ScrapingJob<span class="token punctuation">.</span>objects<span class="token punctuation">.</span>create<span class="token punctuation">(</span></span>
<span class="line">            website<span class="token operator">=</span>website<span class="token punctuation">,</span></span>
<span class="line">            target_url<span class="token operator">=</span>target_url<span class="token punctuation">,</span></span>
<span class="line">            status<span class="token operator">=</span><span class="token string">'pending'</span></span>
<span class="line">        <span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">        <span class="token comment"># TODO: In Step 4, we'll add the actual scraping logic here</span></span>
<span class="line">        <span class="token comment"># For now, just return the created job</span></span>
<span class="line">        serializer <span class="token operator">=</span> ScrapingJobSerializer<span class="token punctuation">(</span>job<span class="token punctuation">)</span></span>
<span class="line">        <span class="token keyword">return</span> Response<span class="token punctuation">(</span>serializer<span class="token punctuation">.</span>data<span class="token punctuation">,</span> status<span class="token operator">=</span>status<span class="token punctuation">.</span>HTTP_201_CREATED<span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">    <span class="token decorator annotation punctuation">@action</span><span class="token punctuation">(</span>detail<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">,</span> methods<span class="token operator">=</span><span class="token punctuation">[</span><span class="token string">'get'</span><span class="token punctuation">]</span><span class="token punctuation">)</span></span>
<span class="line">    <span class="token keyword">def</span> <span class="token function">results</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> request<span class="token punctuation">,</span> pk<span class="token operator">=</span><span class="token boolean">None</span><span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">        <span class="token triple-quoted-string string">"""Get scraped data for a specific job"""</span></span>
<span class="line">        job <span class="token operator">=</span> self<span class="token punctuation">.</span>get_object<span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line">        scraped_data <span class="token operator">=</span> job<span class="token punctuation">.</span>scraped_items<span class="token punctuation">.</span><span class="token builtin">all</span><span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line">        serializer <span class="token operator">=</span> ScrapedDataSerializer<span class="token punctuation">(</span>scraped_data<span class="token punctuation">,</span> many<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span></span>
<span class="line">        <span class="token keyword">return</span> Response<span class="token punctuation">(</span>serializer<span class="token punctuation">.</span>data<span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<hr>
<hr>
<hr>
</div></template>


