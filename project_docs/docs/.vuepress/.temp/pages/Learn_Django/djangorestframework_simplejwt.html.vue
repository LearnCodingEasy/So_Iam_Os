<template><div><h1 id="🔐-django-rest-framework-simplejwt" tabindex="-1"><a class="header-anchor" href="#🔐-django-rest-framework-simplejwt"><span>🔐 Django REST Framework SimpleJWT</span></a></h1>
<blockquote>
<p>مكتبة لإضافة JWT Authentication إلى Django REST Framework، واستخدام Access Token وRefresh Token للتحقق من هوية المستخدم وحماية الـAPI.</p>
</blockquote>
<hr>
<h3 id="_1-🎯-purpose" tabindex="-1"><a class="header-anchor" href="#_1-🎯-purpose"><span>1. 🎯 Purpose</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>SimpleJWT بنستخدمها لإضافة نظام Authentication قائم على JSON Web Tokens داخل Django REST Framework.</p>
<p>الهدف الأساسي هو إن المستخدم بعد تسجيل الدخول يحصل على:</p>
<ul>
<li>Access Token</li>
<li>Refresh Token</li>
</ul>
<p>وبعد كده يستخدم الـAccess Token للوصول إلى الـAPI المحمية.</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">User</span>
<span class="line">  ↓</span>
<span class="line">Login</span>
<span class="line">  ↓</span>
<span class="line">SimpleJWT</span>
<span class="line">  ↓</span>
<span class="line">Access Token + Refresh Token</span>
<span class="line">  ↓</span>
<span class="line">Authenticated API Requests</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>وفي مشروع So_Iam_OS، JWT هي جزء أساسي من نظام Identity &amp; Authentication.</p>
</div>
<hr>
<h3 id="_2-🧠-concept" tabindex="-1"><a class="header-anchor" href="#_2-🧠-concept"><span>2. 🧠 Concept</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>بدل ما الـServer يعتمد فقط على Session لتحديد المستخدم، SimpleJWT بتستخدم Tokens.</p>
<p>عند تسجيل الدخول:</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Username / Email</span>
<span class="line">        +</span>
<span class="line">    Password</span>
<span class="line">        ↓</span>
<span class="line">   Login API</span>
<span class="line">        ↓</span>
<span class="line">   SimpleJWT</span>
<span class="line">        ↓</span>
<span class="line"> ┌─────────────────┐</span>
<span class="line"> │ Access Token    │</span>
<span class="line"> │ Refresh Token   │</span>
<span class="line"> └─────────────────┘</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>الـAccess Token بيستخدم للوصول إلى الـAPI.</p>
<p>والـRefresh Token بيستخدم للحصول على Access Token جديد عند انتهاء صلاحية الـAccess Token.</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Access Token</span>
<span class="line">    ↓</span>
<span class="line">API Request</span>
<span class="line">    ↓</span>
<span class="line">JWTAuthentication</span>
<span class="line">    ↓</span>
<span class="line">Authenticated User</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h3 id="_3-🔧-requirements" tabindex="-1"><a class="header-anchor" href="#_3-🔧-requirements"><span>3. 🔧 Requirements</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>قبل استخدام SimpleJWT، لازم يكون عندك:</p>
<ul>
<li>Python</li>
<li>Virtual Environment</li>
<li>Django</li>
<li>Django REST Framework</li>
<li>User Model</li>
<li>API Layer</li>
</ul>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Python</span>
<span class="line">   ↓</span>
<span class="line">Virtual Environment</span>
<span class="line">   ↓</span>
<span class="line">Django</span>
<span class="line">   ↓</span>
<span class="line">Django REST Framework</span>
<span class="line">   ↓</span>
<span class="line">User Model</span>
<span class="line">   ↓</span>
<span class="line">SimpleJWT</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h3 id="_4-🛠️-installation-setup" tabindex="-1"><a class="header-anchor" href="#_4-🛠️-installation-setup"><span>4. 🛠️ Installation / Setup</span></a></h3>
<h4 id="📦-install-simplejwt" tabindex="-1"><a class="header-anchor" href="#📦-install-simplejwt"><span>📦 Install SimpleJWT</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>داخل Virtual Environment الخاصة بالمشروع:</p>
</div>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip install djangorestframework-simplejwt</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h4 id="⚙️-add-authentication-configuration" tabindex="-1"><a class="header-anchor" href="#⚙️-add-authentication-configuration"><span>⚙️ Add Authentication Configuration</span></a></h4>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">REST_FRAMEWORK <span class="token operator">=</span> <span class="token punctuation">{</span></span>
<span class="line">    <span class="token string">"DEFAULT_AUTHENTICATION_CLASSES"</span><span class="token punctuation">:</span> <span class="token punctuation">(</span></span>
<span class="line">        <span class="token string">"rest_framework_simplejwt.authentication.JWTAuthentication"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"DEFAULT_PERMISSION_CLASSES"</span><span class="token punctuation">:</span> <span class="token punctuation">(</span></span>
<span class="line">        <span class="token string">"rest_framework.permissions.IsAuthenticated"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>الإعداد السابق معناه إن الـAPI بشكل افتراضي هتستخدم JWT للتحقق من هوية المستخدم، والـEndpoints هتحتاج User Authenticated.</p>
</div>
<h4 id="🔐-simplejwt-configuration" tabindex="-1"><a class="header-anchor" href="#🔐-simplejwt-configuration"><span>🔐 SimpleJWT Configuration</span></a></h4>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">from</span> datetime <span class="token keyword">import</span> timedelta</span>
<span class="line"></span>
<span class="line">SIMPLE_JWT <span class="token operator">=</span> <span class="token punctuation">{</span></span>
<span class="line">    <span class="token string">"ACCESS_TOKEN_LIFETIME"</span><span class="token punctuation">:</span> timedelta<span class="token punctuation">(</span>days<span class="token operator">=</span><span class="token number">30</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"REFRESH_TOKEN_LIFETIME"</span><span class="token punctuation">:</span> timedelta<span class="token punctuation">(</span>days<span class="token operator">=</span><span class="token number">180</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"ROTATE_REFRESH_TOKENS"</span><span class="token punctuation">:</span> <span class="token boolean">False</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>الإعدادات الحالية:</p>
<p><code v-pre>ACCESS_TOKEN_LIFETIME</code> → Access Token صالح لمدة 30 يوم.</p>
<p><code v-pre>REFRESH_TOKEN_LIFETIME</code> → Refresh Token صالح لمدة 180 يوم.</p>
<p><code v-pre>ROTATE_REFRESH_TOKENS</code> → عند ضبطها على <code v-pre>False</code>، لا يتم إصدار Refresh Token جديد تلقائيًا عند استخدام Refresh Token.</p>
</div>
<blockquote>
<p>⚠️ ملاحظة أمنية: مدد 30 يوم للـAccess Token و180 يوم للـRefresh Token طويلة نسبيًا، لذلك يجب مراجعتها وفق نموذج الأمان الخاص بالمشروع، خصوصًا لو النظام سيتعامل مع بيانات حساسة.</p>
</blockquote>
<h4 id="📦-token-blacklist" tabindex="-1"><a class="header-anchor" href="#📦-token-blacklist"><span>📦 Token Blacklist</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>لو المشروع محتاج إبطال Refresh Tokens عند Logout، لازم تفعيل تطبيق الـBlacklist الخاص بـSimpleJWT.</p>
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">INSTALLED_APPS <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line">    <span class="token comment"># Libraries</span></span>
<span class="line">    <span class="token string">"rest_framework"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"rest_framework_simplejwt.token_blacklist"</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">]</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>بعد إضافة Blacklist App، يجب تشغيل migrations:</p>
</div>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">python manage.py migrate</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>أما <code v-pre>djangorestframework-simplejwt</code> فهي الحزمة التي يتم تثبيتها باستخدام pip، بينما <code v-pre>rest_framework_simplejwt.token_blacklist</code> هو التطبيق المستخدم لتخزين وإدارة الـBlacklisted Tokens.</p>
</div>
<h4 id="📋-update-dependencies" tabindex="-1"><a class="header-anchor" href="#📋-update-dependencies"><span>📋 Update Dependencies</span></a></h4>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip freeze &gt; requirements.txt</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><hr>
<h3 id="_5-🚀-usage" tabindex="-1"><a class="header-anchor" href="#_5-🚀-usage"><span>5. 🚀 Usage</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>في So_Iam_OS، SimpleJWT مستخدمة في دورة حياة المستخدم الأساسية:</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Login</span>
<span class="line">  ↓</span>
<span class="line">Issue Tokens</span>
<span class="line">  ↓</span>
<span class="line">Authenticated Requests</span>
<span class="line">  ↓</span>
<span class="line">Refresh Access Token</span>
<span class="line">  ↓</span>
<span class="line">Logout</span>
<span class="line">  ↓</span>
<span class="line">Blacklist Refresh Token</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h4 id="🔑-login" tabindex="-1"><a class="header-anchor" href="#🔑-login"><span>🔑 Login</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>بنستخدم <code v-pre>TokenObtainPairView</code> لإنشاء Access Token وRefresh Token.</p>
<p>ولأن المشروع محتاج تحديث <code v-pre>is_online</code> عند تسجيل الدخول، تم إنشاء Serializer مخصص.</p>
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># users_accounts/views.py</span></span>
<span class="line"></span>
<span class="line"><span class="token keyword">from</span> rest_framework_simplejwt<span class="token punctuation">.</span>views <span class="token keyword">import</span> TokenObtainPairView</span>
<span class="line"><span class="token keyword">from</span> rest_framework_simplejwt<span class="token punctuation">.</span>serializers <span class="token keyword">import</span> TokenObtainPairSerializer</span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token keyword">class</span> <span class="token class-name">MyTokenObtainPairSerializer</span><span class="token punctuation">(</span>TokenObtainPairSerializer<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line"></span>
<span class="line">    <span class="token keyword">def</span> <span class="token function">validate</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> attrs<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">        data <span class="token operator">=</span> <span class="token builtin">super</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span>validate<span class="token punctuation">(</span>attrs<span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">        <span class="token comment"># تحديث is_online عند تسجيل الدخول</span></span>
<span class="line">        user <span class="token operator">=</span> self<span class="token punctuation">.</span>user</span>
<span class="line"></span>
<span class="line">        user<span class="token punctuation">.</span>is_online <span class="token operator">=</span> <span class="token boolean">True</span></span>
<span class="line">        user<span class="token punctuation">.</span>save<span class="token punctuation">(</span></span>
<span class="line">            update_fields<span class="token operator">=</span><span class="token punctuation">[</span><span class="token string">"is_online"</span><span class="token punctuation">]</span></span>
<span class="line">        <span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">        <span class="token keyword">return</span> data</span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token keyword">class</span> <span class="token class-name">MyTokenObtainPairView</span><span class="token punctuation">(</span>TokenObtainPairView<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line"></span>
<span class="line">    serializer_class <span class="token operator">=</span> MyTokenObtainPairSerializer</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>عند نجاح Login، الـSerializer بيعمل:</p>
<ol>
<li>تنفيذ عملية JWT الأصلية.</li>
<li>الحصول على المستخدم.</li>
<li>تغيير <code v-pre>is_online</code> إلى <code v-pre>True</code>.</li>
<li>حفظ التغيير.</li>
<li>إرجاع الـTokens.</li>
</ol>
</div>
<hr>
<h4 id="🔄-refresh-token" tabindex="-1"><a class="header-anchor" href="#🔄-refresh-token"><span>🔄 Refresh Token</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>عند انتهاء Access Token، الـClient يقدر يستخدم Refresh Token للحصول على Access Token جديد.</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Refresh Token</span>
<span class="line">      ↓</span>
<span class="line">Refresh API</span>
<span class="line">      ↓</span>
<span class="line">New Access Token</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h4 id="🚪-logout" tabindex="-1"><a class="header-anchor" href="#🚪-logout"><span>🚪 Logout</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>عند تسجيل الخروج، المشروع بيستقبل Refresh Token، ثم يحاول عمل Blacklist له، وبعدها يغير حالة المستخدم إلى Offline.</p>
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># users_accounts/views.py</span></span>
<span class="line"></span>
<span class="line"><span class="token keyword">from</span> rest_framework_simplejwt<span class="token punctuation">.</span>tokens <span class="token keyword">import</span> RefreshToken</span>
<span class="line"><span class="token keyword">from</span> rest_framework<span class="token punctuation">.</span>permissions <span class="token keyword">import</span> IsAuthenticated</span>
<span class="line"><span class="token keyword">from</span> rest_framework<span class="token punctuation">.</span>views <span class="token keyword">import</span> APIView</span>
<span class="line"><span class="token keyword">from</span> rest_framework<span class="token punctuation">.</span>response <span class="token keyword">import</span> Response</span>
<span class="line"><span class="token keyword">from</span> rest_framework <span class="token keyword">import</span> status</span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token keyword">class</span> <span class="token class-name">LogoutAPIView</span><span class="token punctuation">(</span>APIView<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line"></span>
<span class="line">    permission_classes <span class="token operator">=</span> <span class="token punctuation">[</span>IsAuthenticated<span class="token punctuation">]</span></span>
<span class="line"></span>
<span class="line">    <span class="token keyword">def</span> <span class="token function">post</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> request<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line"></span>
<span class="line">        refresh_token <span class="token operator">=</span> request<span class="token punctuation">.</span>data<span class="token punctuation">.</span>get<span class="token punctuation">(</span><span class="token string">"refresh"</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">        <span class="token keyword">if</span> <span class="token keyword">not</span> refresh_token<span class="token punctuation">:</span></span>
<span class="line">            <span class="token keyword">return</span> Response<span class="token punctuation">(</span></span>
<span class="line">                <span class="token punctuation">{</span><span class="token string">"error"</span><span class="token punctuation">:</span> <span class="token string">"Refresh token is required."</span><span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">                status<span class="token operator">=</span>status<span class="token punctuation">.</span>HTTP_400_BAD_REQUEST</span>
<span class="line">            <span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">        <span class="token keyword">try</span><span class="token punctuation">:</span></span>
<span class="line">            <span class="token comment"># Blacklist refresh token</span></span>
<span class="line">            token <span class="token operator">=</span> RefreshToken<span class="token punctuation">(</span>refresh_token<span class="token punctuation">)</span></span>
<span class="line">            token<span class="token punctuation">.</span>blacklist<span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">            <span class="token comment"># تحديث حالة المستخدم</span></span>
<span class="line">            user <span class="token operator">=</span> request<span class="token punctuation">.</span>user</span>
<span class="line"></span>
<span class="line">            <span class="token keyword">if</span> user <span class="token keyword">and</span> user<span class="token punctuation">.</span>is_authenticated<span class="token punctuation">:</span></span>
<span class="line">                user<span class="token punctuation">.</span>is_online <span class="token operator">=</span> <span class="token boolean">False</span></span>
<span class="line">                user<span class="token punctuation">.</span>save<span class="token punctuation">(</span></span>
<span class="line">                    update_fields<span class="token operator">=</span><span class="token punctuation">[</span><span class="token string">"is_online"</span><span class="token punctuation">]</span></span>
<span class="line">                <span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">            <span class="token keyword">return</span> Response<span class="token punctuation">(</span></span>
<span class="line">                <span class="token punctuation">{</span><span class="token string">"message"</span><span class="token punctuation">:</span> <span class="token string">"تم تسجيل الخروج بنجاح"</span><span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">                status<span class="token operator">=</span>status<span class="token punctuation">.</span>HTTP_200_OK</span>
<span class="line">            <span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">        <span class="token keyword">except</span> Exception <span class="token keyword">as</span> e<span class="token punctuation">:</span></span>
<span class="line"></span>
<span class="line">            <span class="token keyword">return</span> Response<span class="token punctuation">(</span></span>
<span class="line">                <span class="token punctuation">{</span><span class="token string">"error"</span><span class="token punctuation">:</span> <span class="token builtin">str</span><span class="token punctuation">(</span>e<span class="token punctuation">)</span><span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">                status<span class="token operator">=</span>status<span class="token punctuation">.</span>HTTP_400_BAD_REQUEST</span>
<span class="line">            <span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>هنا Logout بيعمل حاجتين رئيسيتين:</p>
<ol>
<li>إبطال Refresh Token عن طريق Blacklist.</li>
<li>تحديث حالة المستخدم إلى <code v-pre>is_online = False</code>.</li>
</ol>
</div>
<hr>
<h3 id="_6-📁-structure" tabindex="-1"><a class="header-anchor" href="#_6-📁-structure"><span>6. 📁 Structure</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>الجزء الخاص بـJWT ممكن يكون موزع بالشكل التالي:</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">backend_django/</span>
<span class="line">│</span>
<span class="line">├── settings.py</span>
<span class="line">├── urls.py</span>
<span class="line">│</span>
<span class="line">├── users_accounts/</span>
<span class="line">│   ├── models.py</span>
<span class="line">│   ├── views.py</span>
<span class="line">│   ├── serializers.py</span>
<span class="line">│   ├── signals.py</span>
<span class="line">│   └── ...</span>
<span class="line">│</span>
<span class="line">└── requirements.txt</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h4 id="jwt-architecture" tabindex="-1"><a class="header-anchor" href="#jwt-architecture"><span>JWT Architecture</span></a></h4>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Frontend</span>
<span class="line">   │</span>
<span class="line">   ├── Login</span>
<span class="line">   │</span>
<span class="line">   ↓</span>
<span class="line">users_accounts</span>
<span class="line">   │</span>
<span class="line">   ↓</span>
<span class="line">SimpleJWT</span>
<span class="line">   │</span>
<span class="line">   ├── Access Token</span>
<span class="line">   └── Refresh Token</span>
<span class="line">   │</span>
<span class="line">   ↓</span>
<span class="line">Protected API</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h3 id="_7-🧩-important-concepts" tabindex="-1"><a class="header-anchor" href="#_7-🧩-important-concepts"><span>7. 🧩 Important Concepts</span></a></h3>
<h4 id="🔹-access-token" tabindex="-1"><a class="header-anchor" href="#🔹-access-token"><span>🔹 Access Token</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>Token قصير أو متوسط العمر يستخدمه الـClient للوصول إلى الـProtected APIs.</p>
<p>في الإعداد الحالي مدته 30 يوم.</p>
</div>
<h4 id="🔹-refresh-token" tabindex="-1"><a class="header-anchor" href="#🔹-refresh-token"><span>🔹 Refresh Token</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>Token أطول عمرًا يستخدم للحصول على Access Token جديد.</p>
<p>في الإعداد الحالي مدته 180 يوم.</p>
</div>
<h4 id="🔹-jwt-authentication" tabindex="-1"><a class="header-anchor" href="#🔹-jwt-authentication"><span>🔹 JWT Authentication</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>آلية تستخدم الـJWT Token لتحديد المستخدم الذي يرسل الـRequest.</p>
</div>
<h4 id="🔹-isauthenticated" tabindex="-1"><a class="header-anchor" href="#🔹-isauthenticated"><span>🔹 IsAuthenticated</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>Permission تمنع المستخدم غير المسجل من الوصول إلى الـAPI.</p>
</div>
<h4 id="🔹-token-blacklist" tabindex="-1"><a class="header-anchor" href="#🔹-token-blacklist"><span>🔹 Token Blacklist</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>آلية تسمح بإبطال Refresh Token بحيث لا يمكن استخدامه مرة أخرى بعد تسجيل الخروج.</p>
</div>
<h4 id="🔹-token-rotation" tabindex="-1"><a class="header-anchor" href="#🔹-token-rotation"><span>🔹 Token Rotation</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>عند تفعيل Refresh Token Rotation، يمكن إصدار Refresh Token جديد عند استخدام الـRefresh Token القديم، مع إمكانية إبطال القديم حسب الإعدادات.</p>
<p>في المشروع الحالي:</p>
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token string">"ROTATE_REFRESH_TOKENS"</span><span class="token punctuation">:</span> <span class="token boolean">False</span><span class="token punctuation">,</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h4 id="🔹-is-online" tabindex="-1"><a class="header-anchor" href="#🔹-is-online"><span>🔹 <code v-pre>is_online</code></span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>حقل داخل User Model يستخدمه المشروع لتسجيل حالة المستخدم Online أو Offline.</p>
<p>لكن مهم جدًا: وجود JWT Token صالح لا يعني بالضرورة أن المستخدم Online فعليًا في هذه اللحظة.</p>
</div>
<hr>
<h3 id="_8-💻-examples" tabindex="-1"><a class="header-anchor" href="#_8-💻-examples"><span>8. 💻 Examples</span></a></h3>
<h4 id="example-—-protected-api" tabindex="-1"><a class="header-anchor" href="#example-—-protected-api"><span>Example — Protected API</span></a></h4>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">from</span> rest_framework<span class="token punctuation">.</span>views <span class="token keyword">import</span> APIView</span>
<span class="line"><span class="token keyword">from</span> rest_framework<span class="token punctuation">.</span>permissions <span class="token keyword">import</span> IsAuthenticated</span>
<span class="line"><span class="token keyword">from</span> rest_framework<span class="token punctuation">.</span>response <span class="token keyword">import</span> Response</span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token keyword">class</span> <span class="token class-name">ProfileAPIView</span><span class="token punctuation">(</span>APIView<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line"></span>
<span class="line">    permission_classes <span class="token operator">=</span> <span class="token punctuation">[</span>IsAuthenticated<span class="token punctuation">]</span></span>
<span class="line"></span>
<span class="line">    <span class="token keyword">def</span> <span class="token function">get</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> request<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line"></span>
<span class="line">        <span class="token keyword">return</span> Response<span class="token punctuation">(</span><span class="token punctuation">{</span></span>
<span class="line">            <span class="token string">"user_id"</span><span class="token punctuation">:</span> request<span class="token punctuation">.</span>user<span class="token punctuation">.</span><span class="token builtin">id</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">"username"</span><span class="token punctuation">:</span> request<span class="token punctuation">.</span>user<span class="token punctuation">.</span>username<span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">"is_online"</span><span class="token punctuation">:</span> request<span class="token punctuation">.</span>user<span class="token punctuation">.</span>is_online<span class="token punctuation">,</span></span>
<span class="line">        <span class="token punctuation">}</span><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h4 id="example-—-jwt-urls" tabindex="-1"><a class="header-anchor" href="#example-—-jwt-urls"><span>Example — JWT URLs</span></a></h4>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># backend_django/urls.py</span></span>
<span class="line"></span>
<span class="line"><span class="token keyword">from</span> django<span class="token punctuation">.</span>contrib <span class="token keyword">import</span> admin</span>
<span class="line"><span class="token keyword">from</span> django<span class="token punctuation">.</span>urls <span class="token keyword">import</span> path</span>
<span class="line"></span>
<span class="line"><span class="token keyword">from</span> rest_framework_simplejwt<span class="token punctuation">.</span>views <span class="token keyword">import</span> <span class="token punctuation">(</span></span>
<span class="line">    TokenRefreshView<span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"><span class="token keyword">from</span> users_accounts<span class="token punctuation">.</span>views <span class="token keyword">import</span> <span class="token punctuation">(</span></span>
<span class="line">    MyTokenObtainPairView<span class="token punctuation">,</span></span>
<span class="line">    LogoutAPIView<span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line">urlpatterns <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line"></span>
<span class="line">    <span class="token comment"># JWT</span></span>
<span class="line">    path<span class="token punctuation">(</span></span>
<span class="line">        <span class="token string">"api/login/"</span><span class="token punctuation">,</span></span>
<span class="line">        MyTokenObtainPairView<span class="token punctuation">.</span>as_view<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">        name<span class="token operator">=</span><span class="token string">"token_obtain"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line"></span>
<span class="line">    path<span class="token punctuation">(</span></span>
<span class="line">        <span class="token string">"api/refresh/"</span><span class="token punctuation">,</span></span>
<span class="line">        TokenRefreshView<span class="token punctuation">.</span>as_view<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">        name<span class="token operator">=</span><span class="token string">"token_refresh"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line"></span>
<span class="line">    path<span class="token punctuation">(</span></span>
<span class="line">        <span class="token string">"api/logout/"</span><span class="token punctuation">,</span></span>
<span class="line">        LogoutAPIView<span class="token punctuation">.</span>as_view<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">        name<span class="token operator">=</span><span class="token string">"logout"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line"></span>
<span class="line">    <span class="token comment"># Admin</span></span>
<span class="line">    path<span class="token punctuation">(</span></span>
<span class="line">        <span class="token string">"admin/"</span><span class="token punctuation">,</span></span>
<span class="line">        admin<span class="token punctuation">.</span>site<span class="token punctuation">.</span>urls<span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">]</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h4 id="api-endpoints" tabindex="-1"><a class="header-anchor" href="#api-endpoints"><span>API Endpoints</span></a></h4>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">POST /api/login/</span>
<span class="line">        ↓</span>
<span class="line">Access + Refresh Token</span>
<span class="line"></span>
<span class="line"></span>
<span class="line">POST /api/refresh/</span>
<span class="line">        ↓</span>
<span class="line">New Access Token</span>
<span class="line"></span>
<span class="line"></span>
<span class="line">POST /api/logout/</span>
<span class="line">        ↓</span>
<span class="line">Blacklist Refresh Token</span>
<span class="line">        ↓</span>
<span class="line">is_online = False</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h3 id="_9-❌-common-mistakes" tabindex="-1"><a class="header-anchor" href="#_9-❌-common-mistakes"><span>9. ❌ Common Mistakes</span></a></h3>
<h4 id="_1-نسيان-blacklist-app" tabindex="-1"><a class="header-anchor" href="#_1-نسيان-blacklist-app"><span>1. نسيان Blacklist App</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>لو هتستخدم:</p>
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">token<span class="token punctuation">.</span>blacklist<span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>لازم يكون Token Blacklist App متفعل ومigrations متطبقة.</p>
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token string">"rest_framework_simplejwt.token_blacklist"</span><span class="token punctuation">,</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><p>ثم:</p>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">python manage.py migrate</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><hr>
<h4 id="_2-الاعتقاد-أن-logout-يحذف-jwt-من-كل-مكان" tabindex="-1"><a class="header-anchor" href="#_2-الاعتقاد-أن-logout-يحذف-jwt-من-كل-مكان"><span>2. الاعتقاد أن Logout يحذف JWT من كل مكان</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>JWT مش Session تقليدية.</p>
<p>عمل Logout من الـBackend لا يعني أن Access Token الموجود بالفعل عند الـClient اختفى تلقائيًا.</p>
<p>لذلك تصميم Logout لازم يحدد بوضوح كيفية التعامل مع Access Token وRefresh Token.</p>
</div>
<hr>
<h4 id="_3-استخدام-access-token-طويل-جدًا-بدون-مراجعة-الأمان" tabindex="-1"><a class="header-anchor" href="#_3-استخدام-access-token-طويل-جدًا-بدون-مراجعة-الأمان"><span>3. استخدام Access Token طويل جدًا بدون مراجعة الأمان</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>Access Token لمدة 30 يوم يعتبر طويلًا نسبيًا.</p>
<p>لو الـAccess Token اتسرق، يظل صالحًا لفترة طويلة حسب إعدادات المشروع.</p>
</div>
<hr>
<h4 id="_4-الخلط-بين-authentication-وonline-status" tabindex="-1"><a class="header-anchor" href="#_4-الخلط-بين-authentication-وonline-status"><span>4. الخلط بين Authentication وOnline Status</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>المستخدم ممكن يكون عنده JWT صالح، لكن ده لا يثبت أنه Online حاليًا.</p>
<p><code v-pre>is_online</code> هو Business State وليس بديلًا عن Authentication.</p>
</div>
<hr>
<h4 id="_5-الاعتماد-على-django-login-signals-مع-jwt-بدون-فهم-دورة-التنفيذ" tabindex="-1"><a class="header-anchor" href="#_5-الاعتماد-على-django-login-signals-مع-jwt-بدون-فهم-دورة-التنفيذ"><span>5. الاعتماد على Django Login Signals مع JWT بدون فهم دورة التنفيذ</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p><code v-pre>user_logged_in</code> و<code v-pre>user_logged_out</code> مرتبطة بدورة تسجيل الدخول والخروج الخاصة بـDjango Authentication.</p>
<p>استخدام SimpleJWT لا يعني تلقائيًا أن كل Login أو Logout عبر JWT سيؤدي إلى تشغيل نفس Signals.</p>
<p>لذلك تحديث <code v-pre>is_online</code> في JWT Login/Logout يتم بشكل أوضح داخل منطق الـJWT نفسه، مثل الـCustom Serializer والـLogout API الموجودين في المشروع.</p>
</div>
<hr>
<h3 id="_10-🧠-why" tabindex="-1"><a class="header-anchor" href="#_10-🧠-why"><span>10. 🧠 Why?</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>بنستخدم SimpleJWT لأن So_Iam_OS محتاج نظام Authentication مناسب للـAPI والـFrontend.</p>
<p>الـFrontend مثل Vue.js يقدر يعمل Login، يستلم Tokens، وبعدها يستخدم Access Token في Requests.</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Vue.js</span>
<span class="line">   ↓</span>
<span class="line">Login</span>
<span class="line">   ↓</span>
<span class="line">Django SimpleJWT</span>
<span class="line">   ↓</span>
<span class="line">Access Token</span>
<span class="line">   ↓</span>
<span class="line">Protected API</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>وده مناسب جدًا للـAPI-first architecture لأن الـFrontend والـBackend بيتواصلوا من خلال HTTP APIs.</p>
</div>
<hr>
<h3 id="_11-🔗-project-usage" tabindex="-1"><a class="header-anchor" href="#_11-🔗-project-usage"><span>11. 🔗 Project Usage</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>داخل So_Iam_OS، SimpleJWT موجودة في طبقة Identity &amp; Authentication.</p>
<p>التدفق الأساسي:</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Vue.js Frontend</span>
<span class="line">       │</span>
<span class="line">       ↓</span>
<span class="line">   Login API</span>
<span class="line">       │</span>
<span class="line">       ↓</span>
<span class="line">  SimpleJWT</span>
<span class="line">       │</span>
<span class="line">       ├──────────────┐</span>
<span class="line">       ↓              ↓</span>
<span class="line">Access Token    Refresh Token</span>
<span class="line">       │</span>
<span class="line">       ↓</span>
<span class="line">Protected APIs</span>
<span class="line">       │</span>
<span class="line">       ↓</span>
<span class="line">Django REST Framework</span>
<span class="line">       │</span>
<span class="line">       ↓</span>
<span class="line">Users / Applications</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h4 id="user-online-state" tabindex="-1"><a class="header-anchor" href="#user-online-state"><span>User Online State</span></a></h4>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Login</span>
<span class="line">  ↓</span>
<span class="line">is_online = True</span>
<span class="line">  ↓</span>
<span class="line">Authenticated Session State</span>
<span class="line"></span>
<span class="line"></span>
<span class="line">Logout</span>
<span class="line">  ↓</span>
<span class="line">Blacklist Refresh Token</span>
<span class="line">  ↓</span>
<span class="line">is_online = False</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>المشروع يستخدم <code v-pre>is_online</code> كحالة إضافية للمستخدم، وليس كوسيلة Authentication.</p>
</div>
<hr>
<h3 id="_12-🤖-ai-reference" tabindex="-1"><a class="header-anchor" href="#_12-🤖-ai-reference"><span>12. 🤖 AI Reference</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>المعلومات التالية تعتبر المرجع الأساسي للـAI عند التعامل مع JWT Authentication داخل So_Iam_OS.</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Project:</span>
<span class="line">So_Iam_OS</span>
<span class="line"></span>
<span class="line">Technology:</span>
<span class="line">Django REST Framework</span>
<span class="line"></span>
<span class="line">Authentication:</span>
<span class="line">SimpleJWT</span>
<span class="line"></span>
<span class="line">Package:</span>
<span class="line">djangorestframework-simplejwt</span>
<span class="line"></span>
<span class="line">Domain:</span>
<span class="line">Identity / Authentication / Backend</span>
<span class="line"></span>
<span class="line">Authentication Class:</span>
<span class="line">JWTAuthentication</span>
<span class="line"></span>
<span class="line">Default Permission:</span>
<span class="line">IsAuthenticated</span>
<span class="line"></span>
<span class="line">Tokens:</span>
<span class="line">- Access Token</span>
<span class="line">- Refresh Token</span>
<span class="line"></span>
<span class="line">Current Lifetimes:</span>
<span class="line">- Access Token: 30 days</span>
<span class="line">- Refresh Token: 180 days</span>
<span class="line"></span>
<span class="line">Refresh Rotation:</span>
<span class="line">False</span>
<span class="line"></span>
<span class="line">Blacklist:</span>
<span class="line">Enabled for Refresh Tokens</span>
<span class="line"></span>
<span class="line">User State:</span>
<span class="line">is_online</span>
<span class="line"></span>
<span class="line">Login:</span>
<span class="line">Custom TokenObtainPairSerializer</span>
<span class="line"></span>
<span class="line">Logout:</span>
<span class="line">Custom LogoutAPIView</span>
<span class="line"></span>
<span class="line">Login Endpoint:</span>
<span class="line">POST /api/login/</span>
<span class="line"></span>
<span class="line">Refresh Endpoint:</span>
<span class="line">POST /api/refresh/</span>
<span class="line"></span>
<span class="line">Logout Endpoint:</span>
<span class="line">POST /api/logout/</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h4 id="ai-rules" tabindex="-1"><a class="header-anchor" href="#ai-rules"><span>AI Rules</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<ul>
<li>SimpleJWT هي طبقة JWT Authentication للمشروع.</li>
<li><code v-pre>JWTAuthentication</code> مسؤولة عن التحقق من Access Token.</li>
<li><code v-pre>IsAuthenticated</code> تحمي الـAPI من المستخدم غير المصادق عليه.</li>
<li>Access Token يستخدم للوصول إلى الـProtected APIs.</li>
<li>Refresh Token يستخدم للحصول على Access Token جديد.</li>
<li>Logout يجب أن يتعامل مع Refresh Token بطريقة آمنة.</li>
<li>Blacklist مطلوب عند استخدام <code v-pre>RefreshToken.blacklist()</code>.</li>
<li>لا يتم اعتبار JWT Authentication مساوية لـOnline Status.</li>
<li><code v-pre>is_online</code> حالة Business داخل User Model.</li>
<li>لا يتم الاعتماد على Django Auth Signals وحدها لتحديث حالة المستخدم عند JWT Login/Logout.</li>
<li>أي تغيير في JWT configuration يجب أن يتم توثيقه.</li>
<li>أي تغيير في Token Lifetime يجب مراجعته أمنيًا.</li>
<li>لا يتم تخزين Tokens في أماكن غير آمنة داخل الـFrontend.</li>
<li>يجب التعامل مع Access وRefresh Tokens كبيانات حساسة.</li>
</ul>
</div>
<hr>
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
<td>SimpleJWT Installed</td>
<td>⬜</td>
</tr>
<tr>
<td><code v-pre>JWTAuthentication</code> Configured</td>
<td>⬜</td>
</tr>
<tr>
<td><code v-pre>IsAuthenticated</code> Configured</td>
<td>⬜</td>
</tr>
<tr>
<td>JWT Lifetime Configured</td>
<td>⬜</td>
</tr>
<tr>
<td>Token Blacklist App Enabled</td>
<td>⬜</td>
</tr>
<tr>
<td>Blacklist Migrations Applied</td>
<td>⬜</td>
</tr>
<tr>
<td>Custom Login Serializer</td>
<td>⬜</td>
</tr>
<tr>
<td>Custom Login View</td>
<td>⬜</td>
</tr>
<tr>
<td>Refresh Endpoint</td>
<td>⬜</td>
</tr>
<tr>
<td>Logout Endpoint</td>
<td>⬜</td>
</tr>
<tr>
<td><code v-pre>is_online</code> Login Update</td>
<td>⬜</td>
</tr>
<tr>
<td><code v-pre>is_online</code> Logout Update</td>
<td>⬜</td>
</tr>
<tr>
<td><code v-pre>requirements.txt</code> Updated</td>
<td>⬜</td>
</tr>
<tr>
<td>JWT Flow Tested</td>
<td>⬜</td>
</tr>
</tbody>
</table>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>الحالة هنا يجب تحديثها بناءً على التنفيذ الفعلي داخل المشروع، وليس مجرد وجود الكود في Documentation.</p>
</div>
<hr>
<h3 id="_14-✅-checklist" tabindex="-1"><a class="header-anchor" href="#_14-✅-checklist"><span>14. ✅ Checklist</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>قائمة مراجعة إعداد SimpleJWT:</p>
</div>
<ul>
<li>[x] تثبيت <code v-pre>djangorestframework-simplejwt</code></li>
<li>[x] إضافة <code v-pre>JWTAuthentication</code></li>
<li>[x] إضافة <code v-pre>IsAuthenticated</code></li>
<li>[x] إعداد <code v-pre>SIMPLE_JWT</code></li>
<li>[ ] تحديد Access Token Lifetime</li>
<li>[ ] تحديد Refresh Token Lifetime</li>
<li>[ ] تحديد Refresh Token Rotation</li>
<li>[ ] إضافة Token Blacklist</li>
<li>[ ] تشغيل migrations</li>
<li>[ ] إنشاء Custom Login Serializer</li>
<li>[ ] تحديث <code v-pre>is_online</code> عند Login</li>
<li>[ ] إنشاء Logout API</li>
<li>[ ] Blacklist للـRefresh Token</li>
<li>[ ] تحديث <code v-pre>is_online</code> عند Logout</li>
<li>[ ] إنشاء Refresh Endpoint</li>
<li>[ ] تسجيل dependency في <code v-pre>requirements.txt</code></li>
<li>[ ] اختبار Login</li>
<li>[ ] اختبار Refresh</li>
<li>[ ] اختبار Protected API</li>
<li>[ ] اختبار Logout</li>
<li>[ ] اختبار Blacklisted Refresh Token</li>
</ul>
<hr>
<h3 id="_15-🔗-related-documentation" tabindex="-1"><a class="header-anchor" href="#_15-🔗-related-documentation"><span>15. 🔗 Related Documentation</span></a></h3>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>المواضيع المرتبطة:</p>
</div>
<ul>
<li>Python</li>
<li>Virtual Environment</li>
<li>Django</li>
<li>Django REST Framework</li>
<li>Django Authentication</li>
<li>Custom User Model</li>
<li>JWT</li>
<li>Access Token</li>
<li>Refresh Token</li>
<li>Authentication</li>
<li>Permissions</li>
<li>Token Blacklist</li>
<li>User Online Status</li>
<li>Vue.js</li>
<li>API Security</li>
<li><code v-pre>requirements.txt</code></li>
</ul>
<hr>
<h3 id="_16-📝-notes" tabindex="-1"><a class="header-anchor" href="#_16-📝-notes"><span>16. 📝 Notes</span></a></h3>
<h4 id="🔐-security-note" tabindex="-1"><a class="header-anchor" href="#🔐-security-note"><span>🔐 Security Note</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>الـJWT Tokens تعتبر بيانات حساسة.</p>
<p>لا يجب تسجيلها في Logs أو وضعها داخل Documentation أو Git أو مشاركتها بشكل عام.</p>
</div>
<h4 id="⏱️-token-lifetime" tabindex="-1"><a class="header-anchor" href="#⏱️-token-lifetime"><span>⏱️ Token Lifetime</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>الإعداد الحالي يستخدم:</p>
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token string">"ACCESS_TOKEN_LIFETIME"</span><span class="token punctuation">:</span> timedelta<span class="token punctuation">(</span>days<span class="token operator">=</span><span class="token number">30</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token string">"REFRESH_TOKEN_LIFETIME"</span><span class="token punctuation">:</span> timedelta<span class="token punctuation">(</span>days<span class="token operator">=</span><span class="token number">180</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div></div></div><div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>هذه المدد جزء من Architecture الخاصة بالمشروع ويجب إعادة تقييمها عند الانتقال إلى Production.</p>
</div>
<h4 id="🟢-online-status" tabindex="-1"><a class="header-anchor" href="#🟢-online-status"><span>🟢 Online Status</span></a></h4>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p><code v-pre>is_online = True</code> عند Login و<code v-pre>is_online = False</code> عند Logout لا تعني بالضرورة أن حالة الاتصال الحقيقية للمستخدم دقيقة في كل لحظة.</p>
<p>لو المشروع مستقبلًا محتاج Presence System حقيقي، ممكن يحتاج Heartbeat / Last Seen / Connection Tracking بدل الاعتماد على Boolean فقط.</p>
</div>
<h4 id="🔄-authentication-flow" tabindex="-1"><a class="header-anchor" href="#🔄-authentication-flow"><span>🔄 Authentication Flow</span></a></h4>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">LOGIN</span>
<span class="line">  │</span>
<span class="line">  ↓</span>
<span class="line">Credentials</span>
<span class="line">  │</span>
<span class="line">  ↓</span>
<span class="line">TokenObtainPair</span>
<span class="line">  │</span>
<span class="line">  ├── Access Token</span>
<span class="line">  └── Refresh Token</span>
<span class="line">  │</span>
<span class="line">  ↓</span>
<span class="line">is_online = True</span>
<span class="line"></span>
<span class="line"></span>
<span class="line">API REQUEST</span>
<span class="line">  │</span>
<span class="line">  ↓</span>
<span class="line">Access Token</span>
<span class="line">  │</span>
<span class="line">  ↓</span>
<span class="line">JWTAuthentication</span>
<span class="line">  │</span>
<span class="line">  ↓</span>
<span class="line">IsAuthenticated</span>
<span class="line">  │</span>
<span class="line">  ↓</span>
<span class="line">Protected API</span>
<span class="line"></span>
<span class="line"></span>
<span class="line">REFRESH</span>
<span class="line">  │</span>
<span class="line">  ↓</span>
<span class="line">Refresh Token</span>
<span class="line">  │</span>
<span class="line">  ↓</span>
<span class="line">New Access Token</span>
<span class="line"></span>
<span class="line"></span>
<span class="line">LOGOUT</span>
<span class="line">  │</span>
<span class="line">  ↓</span>
<span class="line">Refresh Token</span>
<span class="line">  │</span>
<span class="line">  ↓</span>
<span class="line">Blacklist</span>
<span class="line">  │</span>
<span class="line">  ↓</span>
<span class="line">is_online = False</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h2 id="📌-quick-reference" tabindex="-1"><a class="header-anchor" href="#📌-quick-reference"><span>📌 Quick Reference</span></a></h2>
<h3 id="install" tabindex="-1"><a class="header-anchor" href="#install"><span>Install</span></a></h3>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip install djangorestframework-simplejwt</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h3 id="authentication" tabindex="-1"><a class="header-anchor" href="#authentication"><span>Authentication</span></a></h3>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">REST_FRAMEWORK <span class="token operator">=</span> <span class="token punctuation">{</span></span>
<span class="line">    <span class="token string">"DEFAULT_AUTHENTICATION_CLASSES"</span><span class="token punctuation">:</span> <span class="token punctuation">(</span></span>
<span class="line">        <span class="token string">"rest_framework_simplejwt.authentication.JWTAuthentication"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"DEFAULT_PERMISSION_CLASSES"</span><span class="token punctuation">:</span> <span class="token punctuation">(</span></span>
<span class="line">        <span class="token string">"rest_framework.permissions.IsAuthenticated"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h3 id="jwt" tabindex="-1"><a class="header-anchor" href="#jwt"><span>JWT</span></a></h3>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">from</span> datetime <span class="token keyword">import</span> timedelta</span>
<span class="line"></span>
<span class="line">SIMPLE_JWT <span class="token operator">=</span> <span class="token punctuation">{</span></span>
<span class="line">    <span class="token string">"ACCESS_TOKEN_LIFETIME"</span><span class="token punctuation">:</span> timedelta<span class="token punctuation">(</span>days<span class="token operator">=</span><span class="token number">30</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"REFRESH_TOKEN_LIFETIME"</span><span class="token punctuation">:</span> timedelta<span class="token punctuation">(</span>days<span class="token operator">=</span><span class="token number">180</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"ROTATE_REFRESH_TOKENS"</span><span class="token punctuation">:</span> <span class="token boolean">False</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h3 id="blacklist" tabindex="-1"><a class="header-anchor" href="#blacklist"><span>Blacklist</span></a></h3>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">INSTALLED_APPS <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line">    <span class="token string">"rest_framework"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"rest_framework_simplejwt.token_blacklist"</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">]</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">python manage.py migrate</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h3 id="dependency" tabindex="-1"><a class="header-anchor" href="#dependency"><span>Dependency</span></a></h3>
<div class="language-cmd line-numbers-mode" data-highlighter="prismjs" data-ext="cmd"><pre v-pre><code><span class="line">pip freeze &gt; requirements.txt</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h3 id="endpoints" tabindex="-1"><a class="header-anchor" href="#endpoints"><span>Endpoints</span></a></h3>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">POST /api/login/</span>
<span class="line">POST /api/refresh/</span>
<span class="line">POST /api/logout/</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h2 id="🧠-ai-rules" tabindex="-1"><a class="header-anchor" href="#🧠-ai-rules"><span>🧠 AI Rules</span></a></h2>
<div dir="rtl" style="font-size: 1.3rem; font-weight: bold;">
<p>SimpleJWT هي المسؤولة عن JWT Authentication داخل Backend مشروع So_Iam_OS.</p>
<p>أي API محمية تستخدم <code v-pre>JWTAuthentication</code> و<code v-pre>IsAuthenticated</code> حسب احتياج الـEndpoint.</p>
<p>Login يتم من خلال Custom <code v-pre>TokenObtainPairSerializer</code> لتحديث <code v-pre>is_online</code>.</p>
<p>Logout يتم من خلال <code v-pre>LogoutAPIView</code> ويجب أن يعمل على إبطال Refresh Token باستخدام Blacklist.</p>
<p><code v-pre>is_online</code> ليست بديلًا عن Authentication.</p>
<p>لا يتم اعتبار وجود JWT صالح دليلًا كافيًا على أن المستخدم Online فعليًا.</p>
<p>أي تعديل على Token Lifetime أو Rotation أو Blacklist يجب اعتباره تعديلًا في Security Architecture ويجب توثيقه.</p>
</div>
</div></template>


