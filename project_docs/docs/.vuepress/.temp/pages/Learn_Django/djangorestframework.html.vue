<template><div><h1 id="🔌-django-rest-framework" tabindex="-1"><a class="header-anchor" href="#🔌-django-rest-framework"><span>🔌 Django REST Framework</span></a></h1>
<blockquote>
<p>مكتبة مبنية فوق Django لإنشاء وبناء Web APIs وREST APIs باستخدام Python وDjango.</p>
</blockquote>
<hr>
<h3 id="_1-🎯-purpose" tabindex="-1"><a class="header-anchor" href="#_1-🎯-purpose"><span>1. 🎯 Purpose</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>Django REST Framework أو DRF هو الـFramework اللي بنستخدمه لبناء الـAPI داخل مشروع Django.</p>
<p>هو مسؤول عن توفير الأدوات اللازمة لإنشاء API، مثل:</p>
<ul>
<li>استقبال HTTP Requests.</li>
<li>إرسال API Responses.</li>
<li>التعامل مع Serializers.</li>
<li>التعامل مع Models.</li>
<li>إنشاء API Views.</li>
<li>بناء CRUD APIs.</li>
<li>التعامل مع Authentication وPermissions.</li>
</ul>
<p>لكن الـDRF نفسه مش معناه إن أي Domain أو User مسموح له يدخل الـAPI؛ التحكم في السماح والمنع بيتم من خلال Authentication وPermissions وطبقات الحماية المناسبة.</p>
</div>
<hr>
<h3 id="_2-🧠-concept" tabindex="-1"><a class="header-anchor" href="#_2-🧠-concept"><span>2. 🧠 Concept</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>الفكرة الأساسية إن Django مسؤول عن بناء الـWeb Application، بينما Django REST Framework بيضيف طبقة متخصصة لبناء الـAPIs.</p>
<p>التدفق الأساسي:</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Client</span>
<span class="line">   │</span>
<span class="line">   │ HTTP Request</span>
<span class="line">   ↓</span>
<span class="line">Django REST Framework</span>
<span class="line">   │</span>
<span class="line">   ├── Authentication</span>
<span class="line">   ├── Permissions</span>
<span class="line">   ├── Views / ViewSets</span>
<span class="line">   ├── Serializers</span>
<span class="line">   │</span>
<span class="line">   ↓</span>
<span class="line">Django Models</span>
<span class="line">   │</span>
<span class="line">   ↓</span>
<span class="line">Database</span>
<span class="line">   │</span>
<span class="line">   ↓</span>
<span class="line">Response</span>
<span class="line">   │</span>
<span class="line">   ↓</span>
<span class="line">Client</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>يعني DRF بيكون حلقة مهمة بين الـClient والـDjango Backend والـDatabase.</p>
</div>
<hr>
<h3 id="_3-🔧-requirements" tabindex="-1"><a class="header-anchor" href="#_3-🔧-requirements"><span>3. 🔧 Requirements</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>قبل تثبيت Django REST Framework، لازم يكون عندك مشروع Django شغال وVirtual Environment مفعلة.</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Python</span>
<span class="line">   ↓</span>
<span class="line">Virtual Environment</span>
<span class="line">   ↓</span>
<span class="line">Django</span>
<span class="line">   ↓</span>
<span class="line">Django Project</span>
<span class="line">   ↓</span>
<span class="line">Django REST Framework</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>في مشروع So_Iam_OS، DRF جزء من Backend Layer.</p>
</div>
<hr>
<h3 id="_4-🛠️-installation-setup" tabindex="-1"><a class="header-anchor" href="#_4-🛠️-installation-setup"><span>4. 🛠️ Installation / Setup</span></a></h3>
<h4 id="📦-install-django-rest-framework" tabindex="-1"><a class="header-anchor" href="#📦-install-django-rest-framework"><span>📦 Install Django REST Framework</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>افتح الـTerminal داخل بيئة المشروع الافتراضية، ثم ثبت Django REST Framework:</p>
</div>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip install djangorestframework</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h4 id="⚙️-add-to-installed-apps" tabindex="-1"><a class="header-anchor" href="#⚙️-add-to-installed-apps"><span>⚙️ Add to <code v-pre>INSTALLED_APPS</code></span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>بعد التثبيت، أضف <code v-pre>rest_framework</code> إلى <code v-pre>INSTALLED_APPS</code> داخل <code v-pre>settings.py</code>.</p>
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">INSTALLED_APPS <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line">    <span class="token comment"># Libraries</span></span>
<span class="line">    <span class="token string">'rest_framework'</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">]</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h4 id="📋-save-dependency" tabindex="-1"><a class="header-anchor" href="#📋-save-dependency"><span>📋 Save Dependency</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>بعد تثبيت المكتبة، لازم يتم تسجيلها ضمن dependencies الخاصة بالمشروع.</p>
</div>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip freeze &gt; requirements.txt</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><hr>
<h3 id="_5-🚀-usage" tabindex="-1"><a class="header-anchor" href="#_5-🚀-usage"><span>5. 🚀 Usage</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>DRF بيوفر أكثر من طريقة لبناء الـAPI.</p>
<p>من أهم الطرق:</p>
<ol>
<li>APIView</li>
<li>Generic Views</li>
<li>ViewSets</li>
<li>Routers</li>
</ol>
</div>
<h4 id="🔹-apiview" tabindex="-1"><a class="header-anchor" href="#🔹-apiview"><span>🔹 APIView</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p><code v-pre>APIView</code> بتديك تحكم كبير جدًا في كل HTTP Method.</p>
<p>مناسبة لما تكون محتاج تتحكم في منطق الـEndpoint بشكل يدوي وواضح.</p>
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">from</span> rest_framework<span class="token punctuation">.</span>views <span class="token keyword">import</span> APIView</span>
<span class="line"><span class="token keyword">from</span> rest_framework<span class="token punctuation">.</span>response <span class="token keyword">import</span> Response</span>
<span class="line"><span class="token keyword">from</span> rest_framework <span class="token keyword">import</span> status</span>
<span class="line"></span>
<span class="line"><span class="token keyword">from</span> <span class="token punctuation">.</span>models <span class="token keyword">import</span> Post</span>
<span class="line"><span class="token keyword">from</span> <span class="token punctuation">.</span>serializers <span class="token keyword">import</span> PostSerializer</span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token keyword">class</span> <span class="token class-name">PostListCreateView</span><span class="token punctuation">(</span>APIView<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line"></span>
<span class="line">    <span class="token keyword">def</span> <span class="token function">get</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> request<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">        posts <span class="token operator">=</span> Post<span class="token punctuation">.</span>objects<span class="token punctuation">.</span><span class="token builtin">all</span><span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">        serializer <span class="token operator">=</span> PostSerializer<span class="token punctuation">(</span></span>
<span class="line">            posts<span class="token punctuation">,</span></span>
<span class="line">            many<span class="token operator">=</span><span class="token boolean">True</span></span>
<span class="line">        <span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">        <span class="token keyword">return</span> Response<span class="token punctuation">(</span>serializer<span class="token punctuation">.</span>data<span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">    <span class="token keyword">def</span> <span class="token function">post</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> request<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">        serializer <span class="token operator">=</span> PostSerializer<span class="token punctuation">(</span></span>
<span class="line">            data<span class="token operator">=</span>request<span class="token punctuation">.</span>data</span>
<span class="line">        <span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">        <span class="token keyword">if</span> serializer<span class="token punctuation">.</span>is_valid<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">            serializer<span class="token punctuation">.</span>save<span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">            <span class="token keyword">return</span> Response<span class="token punctuation">(</span></span>
<span class="line">                serializer<span class="token punctuation">.</span>data<span class="token punctuation">,</span></span>
<span class="line">                status<span class="token operator">=</span>status<span class="token punctuation">.</span>HTTP_201_CREATED</span>
<span class="line">            <span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">        <span class="token keyword">return</span> Response<span class="token punctuation">(</span></span>
<span class="line">            serializer<span class="token punctuation">.</span>errors<span class="token punctuation">,</span></span>
<span class="line">            status<span class="token operator">=</span>status<span class="token punctuation">.</span>HTTP_400_BAD_REQUEST</span>
<span class="line">        <span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>في المثال:</p>
<p><code v-pre>GET</code> بتجيب Posts الموجودة.</p>
<p><code v-pre>POST</code> بتستقبل بيانات جديدة، تعمل Validation، وبعدها تحفظ الـPost.</p>
</div>
<hr>
<h4 id="🔹-viewsets" tabindex="-1"><a class="header-anchor" href="#🔹-viewsets"><span>🔹 ViewSets</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p><code v-pre>ViewSet</code> بتوفر طريقة أكثر اختصارًا وتنظيمًا لبناء CRUD APIs، وخصوصًا لما يكون عندك عدد كبير من الـEndpoints.</p>
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">from</span> rest_framework <span class="token keyword">import</span> viewsets</span>
<span class="line"></span>
<span class="line"><span class="token keyword">from</span> <span class="token punctuation">.</span>models <span class="token keyword">import</span> Post</span>
<span class="line"><span class="token keyword">from</span> <span class="token punctuation">.</span>serializers <span class="token keyword">import</span> PostSerializer</span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token keyword">class</span> <span class="token class-name">PostViewSet</span><span class="token punctuation">(</span>viewsets<span class="token punctuation">.</span>ModelViewSet<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line"></span>
<span class="line">    queryset <span class="token operator">=</span> Post<span class="token punctuation">.</span>objects<span class="token punctuation">.</span><span class="token builtin">all</span><span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">    serializer_class <span class="token operator">=</span> PostSerializer</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p><code v-pre>ModelViewSet</code> بتوفر عمليات CRUD الأساسية مثل:</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">GET     → List</span>
<span class="line">GET     → Detail</span>
<span class="line">POST    → Create</span>
<span class="line">PUT     → Update</span>
<span class="line">PATCH   → Partial Update</span>
<span class="line">DELETE  → Delete</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>وده بيقلل كمية الكود المطلوبة مقارنة بكتابة كل عملية بشكل منفصل.</p>
</div>
<hr>
<h3 id="_6-📁-structure" tabindex="-1"><a class="header-anchor" href="#_6-📁-structure"><span>6. 📁 Structure</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>شكل App بسيطة تستخدم Django REST Framework ممكن يكون:</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">social/</span>
<span class="line">│</span>
<span class="line">├── migrations/</span>
<span class="line">│</span>
<span class="line">├── __init__.py</span>
<span class="line">├── admin.py</span>
<span class="line">├── apps.py</span>
<span class="line">├── models.py</span>
<span class="line">├── serializers.py</span>
<span class="line">├── views.py</span>
<span class="line">├── urls.py</span>
<span class="line">└── tests.py</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>أهم الملفات المرتبطة بالـAPI:</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">models.py</span>
<span class="line">    ↓</span>
<span class="line">serializers.py</span>
<span class="line">    ↓</span>
<span class="line">views.py</span>
<span class="line">    ↓</span>
<span class="line">urls.py</span>
<span class="line">    ↓</span>
<span class="line">API Endpoint</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h3 id="_7-🧩-important-concepts" tabindex="-1"><a class="header-anchor" href="#_7-🧩-important-concepts"><span>7. 🧩 Important Concepts</span></a></h3>
<h4 id="🔹-api" tabindex="-1"><a class="header-anchor" href="#🔹-api"><span>🔹 API</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>واجهة تسمح للـFrontend أو أي Client آخر بالتواصل مع الـBackend من خلال HTTP Requests وResponses.</p>
</div>
<h4 id="🔹-serializer" tabindex="-1"><a class="header-anchor" href="#🔹-serializer"><span>🔹 Serializer</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>الـSerializer مسؤول عن تحويل البيانات بين Python/Django Objects والبيانات المناسبة للإرسال والاستقبال عبر الـAPI، بالإضافة إلى Validation للبيانات المدخلة.</p>
</div>
<h4 id="🔹-apiview-1" tabindex="-1"><a class="header-anchor" href="#🔹-apiview-1"><span>🔹 APIView</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>Class بتسمح لك بكتابة منطق كل HTTP Method بشكل مباشر.</p>
</div>
<h4 id="🔹-viewset" tabindex="-1"><a class="header-anchor" href="#🔹-viewset"><span>🔹 ViewSet</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>طريقة لتنظيم مجموعة من العمليات الخاصة بـResource واحد داخل Class واحدة.</p>
</div>
<h4 id="🔹-modelviewset" tabindex="-1"><a class="header-anchor" href="#🔹-modelviewset"><span>🔹 ModelViewSet</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>ViewSet جاهزة توفر عمليات CRUD الأساسية اعتمادًا على Django Model وSerializer.</p>
</div>
<h4 id="🔹-router" tabindex="-1"><a class="header-anchor" href="#🔹-router"><span>🔹 Router</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>أداة تساعد في إنشاء URLs الخاصة بالـViewSets تلقائيًا بدل كتابة كل Route يدويًا.</p>
</div>
<h4 id="🔹-authentication" tabindex="-1"><a class="header-anchor" href="#🔹-authentication"><span>🔹 Authentication</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>تحديد هوية المستخدم الذي يرسل الـRequest.</p>
</div>
<h4 id="🔹-permissions" tabindex="-1"><a class="header-anchor" href="#🔹-permissions"><span>🔹 Permissions</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>تحديد هل المستخدم الذي تم التعرف عليه مسموح له بتنفيذ العملية أم لا.</p>
</div>
<hr>
<h3 id="_8-💻-examples" tabindex="-1"><a class="header-anchor" href="#_8-💻-examples"><span>8. 💻 Examples</span></a></h3>
<h4 id="example-—-apiview" tabindex="-1"><a class="header-anchor" href="#example-—-apiview"><span>Example — APIView</span></a></h4>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">from</span> rest_framework<span class="token punctuation">.</span>views <span class="token keyword">import</span> APIView</span>
<span class="line"><span class="token keyword">from</span> rest_framework<span class="token punctuation">.</span>response <span class="token keyword">import</span> Response</span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token keyword">class</span> <span class="token class-name">HelloAPIView</span><span class="token punctuation">(</span>APIView<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line"></span>
<span class="line">    <span class="token keyword">def</span> <span class="token function">get</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> request<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">        <span class="token keyword">return</span> Response<span class="token punctuation">(</span><span class="token punctuation">{</span></span>
<span class="line">            <span class="token string">"message"</span><span class="token punctuation">:</span> <span class="token string">"Hello So_Iam_OS"</span></span>
<span class="line">        <span class="token punctuation">}</span><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h4 id="example-—-viewset" tabindex="-1"><a class="header-anchor" href="#example-—-viewset"><span>Example — ViewSet</span></a></h4>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">from</span> rest_framework <span class="token keyword">import</span> viewsets</span>
<span class="line"></span>
<span class="line"><span class="token keyword">from</span> <span class="token punctuation">.</span>models <span class="token keyword">import</span> Post</span>
<span class="line"><span class="token keyword">from</span> <span class="token punctuation">.</span>serializers <span class="token keyword">import</span> PostSerializer</span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token keyword">class</span> <span class="token class-name">PostViewSet</span><span class="token punctuation">(</span>viewsets<span class="token punctuation">.</span>ModelViewSet<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line"></span>
<span class="line">    queryset <span class="token operator">=</span> Post<span class="token punctuation">.</span>objects<span class="token punctuation">.</span><span class="token builtin">all</span><span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line">    serializer_class <span class="token operator">=</span> PostSerializer</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h4 id="example-—-basic-router" tabindex="-1"><a class="header-anchor" href="#example-—-basic-router"><span>Example — Basic Router</span></a></h4>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">from</span> rest_framework<span class="token punctuation">.</span>routers <span class="token keyword">import</span> DefaultRouter</span>
<span class="line"></span>
<span class="line"><span class="token keyword">from</span> <span class="token punctuation">.</span>views <span class="token keyword">import</span> PostViewSet</span>
<span class="line"></span>
<span class="line"></span>
<span class="line">router <span class="token operator">=</span> DefaultRouter<span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">router<span class="token punctuation">.</span>register<span class="token punctuation">(</span></span>
<span class="line">    <span class="token string">r'posts'</span><span class="token punctuation">,</span></span>
<span class="line">    PostViewSet<span class="token punctuation">,</span></span>
<span class="line">    basename<span class="token operator">=</span><span class="token string">'posts'</span></span>
<span class="line"><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">urlpatterns <span class="token operator">=</span> router<span class="token punctuation">.</span>urls</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h3 id="_9-❌-common-mistakes" tabindex="-1"><a class="header-anchor" href="#_9-❌-common-mistakes"><span>9. ❌ Common Mistakes</span></a></h3>
<h4 id="_1-نسيان-إضافة-drf" tabindex="-1"><a class="header-anchor" href="#_1-نسيان-إضافة-drf"><span>1. نسيان إضافة DRF</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>تثبيت المكتبة فقط مش كفاية؛ لازم إضافتها إلى <code v-pre>INSTALLED_APPS</code>.</p>
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">INSTALLED_APPS <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line">    <span class="token string">'rest_framework'</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">]</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h4 id="_2-الخلط-بين-authentication-وpermissions" tabindex="-1"><a class="header-anchor" href="#_2-الخلط-بين-authentication-وpermissions"><span>2. الخلط بين Authentication وPermissions</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>Authentication بتجاوب على سؤال:</p>
<p>مين المستخدم؟</p>
<p>Permissions بتجاوب على سؤال:</p>
<p>هل المستخدم ده مسموح له يعمل العملية دي؟</p>
</div>
<h4 id="_3-استخدام-viewset-بدون-فهم-الـcrud" tabindex="-1"><a class="header-anchor" href="#_3-استخدام-viewset-بدون-فهم-الـcrud"><span>3. استخدام ViewSet بدون فهم الـCRUD</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p><code v-pre>ModelViewSet</code> بتوفر عمليات كثيرة تلقائيًا، لكن لازم تفهم العمليات اللي بيتم توفيرها قبل استخدامها.</p>
</div>
<h4 id="_4-نسيان-serializer" tabindex="-1"><a class="header-anchor" href="#_4-نسيان-serializer"><span>4. نسيان Serializer</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>في أغلب APIs التي تتعامل مع Models، الـSerializer بيكون جزء أساسي من عملية تحويل البيانات والتحقق منها.</p>
</div>
<h4 id="_5-عدم-تحديث-requirements-txt" tabindex="-1"><a class="header-anchor" href="#_5-عدم-تحديث-requirements-txt"><span>5. عدم تحديث <code v-pre>requirements.txt</code></span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>بعد تثبيت DRF، لازم تسجيل dependency الخاصة بالمشروع.</p>
</div>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip freeze &gt; requirements.txt</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><hr>
<h3 id="_10-🧠-why" tabindex="-1"><a class="header-anchor" href="#_10-🧠-why"><span>10. 🧠 Why?</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>بنستخدم Django REST Framework لأن Django الأساسي مش مصمم لوحده لتوفير كل الأدوات المتخصصة اللي محتاجينها لبناء REST APIs بشكل مريح ومنظم.</p>
<p>DRF بيوفر abstraction جاهز للـAPI، وبيخلينا نقدر نبني:</p>
<ul>
<li>CRUD APIs</li>
<li>Serializers</li>
<li>Validation</li>
<li>Authentication</li>
<li>Permissions</li>
<li>API Views</li>
<li>ViewSets</li>
<li>Routers</li>
</ul>
<p>وده بيقلل كمية الـBoilerplate Code وبيخلي بناء الـBackend APIs أكثر تنظيمًا.</p>
</div>
<hr>
<h3 id="_11-🔗-project-usage" tabindex="-1"><a class="header-anchor" href="#_11-🔗-project-usage"><span>11. 🔗 Project Usage</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>داخل مشروع So_Iam_OS، Django REST Framework هو طبقة الـAPI الأساسية التي تسمح للـFrontend وباقي Clients بالتواصل مع الـBackend.</p>
<p>مثال على الـSocial App:</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Vue.js Frontend</span>
<span class="line">       ↓</span>
<span class="line">     HTTP</span>
<span class="line">       ↓</span>
<span class="line">Django REST Framework</span>
<span class="line">       ↓</span>
<span class="line">   View / ViewSet</span>
<span class="line">       ↓</span>
<span class="line">   Serializer</span>
<span class="line">       ↓</span>
<span class="line">    Django Model</span>
<span class="line">       ↓</span>
<span class="line">    Database</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>وبالتالي DRF هي نقطة مهمة جدًا في الاتصال بين Vue.js والـDjango Backend.</p>
</div>
<hr>
<h3 id="_12-🤖-ai-reference" tabindex="-1"><a class="header-anchor" href="#_12-🤖-ai-reference"><span>12. 🤖 AI Reference</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>المعلومات التالية تعتبر مرجع للـAI عند التعامل مع Django REST Framework داخل المشروع.</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Project:</span>
<span class="line">So_Iam_OS</span>
<span class="line"></span>
<span class="line">Technology:</span>
<span class="line">Django REST Framework</span>
<span class="line"></span>
<span class="line">Domain:</span>
<span class="line">Backend / API</span>
<span class="line"></span>
<span class="line">Package:</span>
<span class="line">djangorestframework</span>
<span class="line"></span>
<span class="line">Installed App:</span>
<span class="line">rest_framework</span>
<span class="line"></span>
<span class="line">Primary Usage:</span>
<span class="line">Building REST APIs</span>
<span class="line"></span>
<span class="line">Main Components:</span>
<span class="line">- APIView</span>
<span class="line">- Generic Views</span>
<span class="line">- ViewSets</span>
<span class="line">- ModelViewSet</span>
<span class="line">- Serializers</span>
<span class="line">- Routers</span>
<span class="line">- Authentication</span>
<span class="line">- Permissions</span>
<span class="line"></span>
<span class="line">Project Integration:</span>
<span class="line">Vue.js → DRF → Django → Database</span>
<span class="line"></span>
<span class="line">Rules:</span>
<span class="line">- DRF مسؤول عن بناء API layer.</span>
<span class="line">- Authentication يحدد هوية المستخدم.</span>
<span class="line">- Permissions تحدد صلاحية تنفيذ العملية.</span>
<span class="line">- Serializers مسؤولة عن تحويل/Validation البيانات.</span>
<span class="line">- ModelViewSet مناسب لتقليل Boilerplate في CRUD APIs.</span>
<span class="line">- يجب تسجيل dependency داخل requirements.txt.</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h3 id="_13-📊-current-status" tabindex="-1"><a class="header-anchor" href="#_13-📊-current-status"><span>13. 📊 Current Status</span></a></h3>
<table>
<thead>
<tr>
<th>Task</th>
<th>Status</th>
</tr>
</thead>
<tbody>
<tr>
<td>Django Installed</td>
<td>✅</td>
</tr>
<tr>
<td>Django REST Framework Installed</td>
<td>⬜</td>
</tr>
<tr>
<td><code v-pre>rest_framework</code> Added to <code v-pre>INSTALLED_APPS</code></td>
<td>⬜</td>
</tr>
<tr>
<td>Serializer Setup</td>
<td>⬜</td>
</tr>
<tr>
<td>APIView Setup</td>
<td>⬜</td>
</tr>
<tr>
<td>ViewSet Setup</td>
<td>⬜</td>
</tr>
<tr>
<td>Router Setup</td>
<td>⬜</td>
</tr>
<tr>
<td>Authentication Setup</td>
<td>⬜</td>
</tr>
<tr>
<td>Permissions Setup</td>
<td>⬜</td>
</tr>
<tr>
<td>requirements.txt Updated</td>
<td>⬜</td>
</tr>
</tbody>
</table>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>الحالة هنا بتوصف Knowledge/Setup الخاصة بـDRF. يتم تحديثها بعد تنفيذ الخطوات فعليًا داخل مشروع So_Iam_OS.</p>
</div>
<hr>
<h3 id="_14-✅-checklist" tabindex="-1"><a class="header-anchor" href="#_14-✅-checklist"><span>14. ✅ Checklist</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>قائمة مراجعة إعداد Django REST Framework:</p>
</div>
<ul>
<li>[x] تثبيت <code v-pre>djangorestframework</code></li>
<li>[x] إضافة <code v-pre>rest_framework</code> إلى <code v-pre>INSTALLED_APPS</code></li>
<li>[x] تحديث <code v-pre>requirements.txt</code></li>
<li>[ ] إنشاء <code v-pre>serializers.py</code></li>
<li>[ ] إنشاء API Views</li>
<li>[ ] اختيار APIView أو Generic Views أو ViewSet حسب الحاجة</li>
<li>[ ] إعداد URLs</li>
<li>[ ] إعداد Routers عند استخدام ViewSets</li>
<li>[ ] إعداد Authentication</li>
<li>[ ] إعداد Permissions</li>
<li>[ ] اختبار الـAPI</li>
</ul>
<hr>
<h3 id="_15-🔗-related-documentation" tabindex="-1"><a class="header-anchor" href="#_15-🔗-related-documentation"><span>15. 🔗 Related Documentation</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>التقنيات والملفات المرتبطة:</p>
</div>
<ul>
<li>Python</li>
<li>Virtual Environment</li>
<li>Django</li>
<li>Django Models</li>
<li>Django URLs</li>
<li>Django REST Framework</li>
<li>Serializers</li>
<li>APIView</li>
<li>Generic Views</li>
<li>ViewSets</li>
<li>Routers</li>
<li>Authentication</li>
<li>Permissions</li>
<li>Vue.js</li>
<li>PostgreSQL</li>
<li><code v-pre>requirements.txt</code></li>
</ul>
<hr>
<h3 id="_16-📝-notes" tabindex="-1"><a class="header-anchor" href="#_16-📝-notes"><span>16. 📝 Notes</span></a></h3>
<h4 id="🔹-apiview-vs-viewset" tabindex="-1"><a class="header-anchor" href="#🔹-apiview-vs-viewset"><span>🔹 APIView vs ViewSet</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>استخدم <code v-pre>APIView</code> لما تحتاج تحكم تفصيلي في كل Request وHTTP Method.</p>
<p>استخدم <code v-pre>ViewSet</code> أو <code v-pre>ModelViewSet</code> لما تكون بتبني CRUD API واضحة وممكن تستفيد من العمليات الجاهزة وتقليل الكود.</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Custom / Complex Logic</span>
<span class="line">        ↓</span>
<span class="line">     APIView</span>
<span class="line"></span>
<span class="line"></span>
<span class="line">Standard CRUD</span>
<span class="line">        ↓</span>
<span class="line">   ModelViewSet</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h4 id="🔹-drf-لا-يساوي-authentication" tabindex="-1"><a class="header-anchor" href="#🔹-drf-لا-يساوي-authentication"><span>🔹 DRF لا يساوي Authentication</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>وجود DRF في المشروع لا يعني تلقائيًا إن كل الـAPI محمية.</p>
<p>الحماية لازم يتم تصميمها باستخدام Authentication وPermissions والسياسات المناسبة لكل Endpoint.</p>
</div>
<h4 id="🔹-dependency" tabindex="-1"><a class="header-anchor" href="#🔹-dependency"><span>🔹 Dependency</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>اسم الحزمة التي يتم تثبيتها باستخدام pip هو:</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">djangorestframework</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>بينما الاسم الذي يتم وضعه في <code v-pre>INSTALLED_APPS</code> هو:</p>
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token string">'rest_framework'</span><span class="token punctuation">,</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><hr>
<h2 id="📌-quick-reference" tabindex="-1"><a class="header-anchor" href="#📌-quick-reference"><span>📌 Quick Reference</span></a></h2>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip install djangorestframework</span>
<span class="line"></span>
<span class="line">pip freeze &gt; requirements.txt</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">INSTALLED_APPS <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line">    <span class="token string">'rest_framework'</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">]</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">from</span> rest_framework<span class="token punctuation">.</span>views <span class="token keyword">import</span> APIView</span>
<span class="line"><span class="token keyword">from</span> rest_framework<span class="token punctuation">.</span>response <span class="token keyword">import</span> Response</span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token keyword">class</span> <span class="token class-name">ExampleAPIView</span><span class="token punctuation">(</span>APIView<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line"></span>
<span class="line">    <span class="token keyword">def</span> <span class="token function">get</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> request<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">        <span class="token keyword">return</span> Response<span class="token punctuation">(</span><span class="token punctuation">{</span></span>
<span class="line">            <span class="token string">"message"</span><span class="token punctuation">:</span> <span class="token string">"Hello"</span></span>
<span class="line">        <span class="token punctuation">}</span><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">from</span> rest_framework <span class="token keyword">import</span> viewsets</span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token keyword">class</span> <span class="token class-name">ExampleViewSet</span><span class="token punctuation">(</span>viewsets<span class="token punctuation">.</span>ModelViewSet<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line"></span>
<span class="line">    queryset <span class="token operator">=</span> Model<span class="token punctuation">.</span>objects<span class="token punctuation">.</span><span class="token builtin">all</span><span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line">    serializer_class <span class="token operator">=</span> ModelSerializer</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h2 id="🤖-ai-rules" tabindex="-1"><a class="header-anchor" href="#🤖-ai-rules"><span>🤖 AI Rules</span></a></h2>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<ul>
<li>Django REST Framework هو طبقة بناء الـAPI في Backend المشروع.</li>
<li>لا يتم اعتبار DRF نظام Authentication بحد ذاته.</li>
<li>Authentication لتحديد هوية المستخدم.</li>
<li>Permissions لتحديد صلاحيات المستخدم.</li>
<li>Serializer جزء أساسي من التعامل مع بيانات الـAPI.</li>
<li><code v-pre>APIView</code> تستخدم عند الحاجة لتحكم أكبر في الـRequest Logic.</li>
<li><code v-pre>ModelViewSet</code> مناسبة للـCRUD APIs القياسية.</li>
<li>عند استخدام ViewSets يمكن استخدام Routers لتنظيم الـURLs.</li>
<li>أي Dependency جديدة يتم تثبيتها يجب تسجيلها في <code v-pre>requirements.txt</code>.</li>
<li>عند تصميم API جديدة داخل So_Iam_OS، يجب تحديد Authentication وPermissions المناسبة وعدم الاعتماد على وجود DRF وحده للحماية.</li>
</ul>
</div>
</div></template>


