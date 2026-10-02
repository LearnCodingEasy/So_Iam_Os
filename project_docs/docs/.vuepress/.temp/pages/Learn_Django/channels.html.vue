<template><div><h2 id="install" tabindex="-1"><a class="header-anchor" href="#install"><span>Install</span></a></h2>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">pip install channels</span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div></div></div><div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">pip show django-celery-results</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">pip show django-celery-beat</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h2 id="setting" tabindex="-1"><a class="header-anchor" href="#setting"><span>Setting</span></a></h2>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">INSTALLED_APPS <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line">    <span class="token punctuation">.</span><span class="token punctuation">.</span><span class="token punctuation">.</span></span>
<span class="line">    <span class="token string">"channels"</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">]</span></span>
<span class="line"></span>
<span class="line">ASGI_APPLICATION <span class="token operator">=</span> <span class="token string">"backend_django.asgi.application"</span></span>
<span class="line"></span>
<span class="line">CHANNEL_LAYERS <span class="token operator">=</span> <span class="token punctuation">{</span></span>
<span class="line">    <span class="token string">"default"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span></span>
<span class="line">        <span class="token string">"BACKEND"</span><span class="token punctuation">:</span> <span class="token string">"channels.layers.InMemoryChannelLayer"</span></span>
<span class="line">    <span class="token punctuation">}</span></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h2 id="consumers" tabindex="-1"><a class="header-anchor" href="#consumers"><span>Consumers</span></a></h2>
<ul>
<li>2️⃣ Create File إنشاء مجلد Debug Console</li>
</ul>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">consumers.py</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">backend_django/</span>
<span class="line">│</span>
<span class="line">├── manage.py</span>
<span class="line">│</span>
<span class="line">├── backend_django/</span>
<span class="line">│   ├── settings.py</span>
<span class="line">│   ├── asgi.py</span>
<span class="line">│   ├── urls.py</span>
<span class="line">│   └── ...</span>
<span class="line">│</span>
<span class="line">├── core/</span>
<span class="line">│   ├── __init__.py</span>
<span class="line">│   │</span>
<span class="line">│   └── debug/</span>
<span class="line">│       ├── __init__.py</span>
<span class="line">│       ├── consumers.py</span>
<span class="line">│       ├── routing.py</span>
<span class="line">│       └── handlers.py</span>
<span class="line">│</span>
<span class="line">├── users_accounts/</span>
<span class="line">│   ├── api.py</span>
<span class="line">│   └── ...</span>
<span class="line">│</span>
<span class="line">└── ...</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">import</span> json</span>
<span class="line"></span>
<span class="line"><span class="token keyword">from</span> channels<span class="token punctuation">.</span>generic<span class="token punctuation">.</span>websocket <span class="token keyword">import</span> AsyncWebsocketConsumer</span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token keyword">class</span> <span class="token class-name">DebugConsoleConsumer</span><span class="token punctuation">(</span>AsyncWebsocketConsumer<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line"></span>
<span class="line">    <span class="token keyword">async</span> <span class="token keyword">def</span> <span class="token function">connect</span><span class="token punctuation">(</span>self<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">        <span class="token triple-quoted-string string">"""</span>
<span class="line">        الاتصال بالـ Live Debug Console</span>
<span class="line">        """</span></span>
<span class="line"></span>
<span class="line">        self<span class="token punctuation">.</span>group_name <span class="token operator">=</span> <span class="token string">"debug_console"</span></span>
<span class="line"></span>
<span class="line">        <span class="token comment"># إضافة المتصفح إلى مجموعة Debug Console</span></span>
<span class="line">        <span class="token keyword">await</span> self<span class="token punctuation">.</span>channel_layer<span class="token punctuation">.</span>group_add<span class="token punctuation">(</span></span>
<span class="line">            self<span class="token punctuation">.</span>group_name<span class="token punctuation">,</span></span>
<span class="line">            self<span class="token punctuation">.</span>channel_name<span class="token punctuation">,</span></span>
<span class="line">        <span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">        <span class="token comment"># قبول WebSocket connection</span></span>
<span class="line">        <span class="token keyword">await</span> self<span class="token punctuation">.</span>accept<span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">        <span class="token comment"># رسالة اتصال أولية</span></span>
<span class="line">        <span class="token keyword">await</span> self<span class="token punctuation">.</span>send<span class="token punctuation">(</span></span>
<span class="line">            text_data<span class="token operator">=</span>json<span class="token punctuation">.</span>dumps<span class="token punctuation">(</span><span class="token punctuation">{</span></span>
<span class="line">                <span class="token string">"type"</span><span class="token punctuation">:</span> <span class="token string">"system"</span><span class="token punctuation">,</span></span>
<span class="line">                <span class="token string">"level"</span><span class="token punctuation">:</span> <span class="token string">"success"</span><span class="token punctuation">,</span></span>
<span class="line">                <span class="token string">"message"</span><span class="token punctuation">:</span> <span class="token string">"🔌 Debug Console connected"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token punctuation">}</span><span class="token punctuation">)</span></span>
<span class="line">        <span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">    <span class="token keyword">async</span> <span class="token keyword">def</span> <span class="token function">disconnect</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> close_code<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">        <span class="token triple-quoted-string string">"""</span>
<span class="line">        إزالة المتصفح من Debug Console</span>
<span class="line">        """</span></span>
<span class="line"></span>
<span class="line">        <span class="token keyword">await</span> self<span class="token punctuation">.</span>channel_layer<span class="token punctuation">.</span>group_discard<span class="token punctuation">(</span></span>
<span class="line">            self<span class="token punctuation">.</span>group_name<span class="token punctuation">,</span></span>
<span class="line">            self<span class="token punctuation">.</span>channel_name<span class="token punctuation">,</span></span>
<span class="line">        <span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">    <span class="token keyword">async</span> <span class="token keyword">def</span> <span class="token function">send_log</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> event<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">        <span class="token triple-quoted-string string">"""</span>
<span class="line">        استقبال Log من Django Logging Handler</span>
<span class="line">        وإرساله للمتصفح</span>
<span class="line">        """</span></span>
<span class="line"></span>
<span class="line">        <span class="token keyword">await</span> self<span class="token punctuation">.</span>send<span class="token punctuation">(</span></span>
<span class="line">            text_data<span class="token operator">=</span>json<span class="token punctuation">.</span>dumps<span class="token punctuation">(</span></span>
<span class="line">                event<span class="token punctuation">[</span><span class="token string">"data"</span><span class="token punctuation">]</span></span>
<span class="line">            <span class="token punctuation">)</span></span>
<span class="line">        <span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h2 id="routing" tabindex="-1"><a class="header-anchor" href="#routing"><span>Routing</span></a></h2>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">routing.py</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">from</span> django<span class="token punctuation">.</span>urls <span class="token keyword">import</span> re_path</span>
<span class="line"></span>
<span class="line"><span class="token keyword">from</span> <span class="token punctuation">.</span>consumers <span class="token keyword">import</span> DebugConsoleConsumer</span>
<span class="line"></span>
<span class="line"></span>
<span class="line">websocket_urlpatterns <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line">    re_path<span class="token punctuation">(</span></span>
<span class="line">        <span class="token string">r"ws/debug/$"</span><span class="token punctuation">,</span></span>
<span class="line">        DebugConsoleConsumer<span class="token punctuation">.</span>as_asgi<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">]</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><ul>
<li>إذن عنوان WebSocket أصبح:</li>
</ul>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">ws://127.0.0.1:8000/ws/debug/</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h2 id="handlers" tabindex="-1"><a class="header-anchor" href="#handlers"><span>Handlers</span></a></h2>
<ul>
<li>
<p>5️⃣ أهم جزء — تحويل Django Logs إلى WebSocket 🔥</p>
</li>
<li>
<p>ده قلب النظام.</p>
</li>
</ul>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">handlers.py</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">import</span> logging</span>
<span class="line"></span>
<span class="line"><span class="token keyword">from</span> asgiref<span class="token punctuation">.</span>sync <span class="token keyword">import</span> async_to_sync</span>
<span class="line"><span class="token keyword">from</span> channels<span class="token punctuation">.</span>layers <span class="token keyword">import</span> get_channel_layer</span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token keyword">class</span> <span class="token class-name">WebSocketLogHandler</span><span class="token punctuation">(</span>logging<span class="token punctuation">.</span>Handler<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line"></span>
<span class="line">    <span class="token keyword">def</span> <span class="token function">emit</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> record<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">        <span class="token triple-quoted-string string">"""</span>
<span class="line">        إرسال أي Django Log إلى Live Debug Console</span>
<span class="line">        """</span></span>
<span class="line"></span>
<span class="line">        <span class="token keyword">try</span><span class="token punctuation">:</span></span>
<span class="line"></span>
<span class="line">            channel_layer <span class="token operator">=</span> get_channel_layer<span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">            <span class="token keyword">if</span> channel_layer <span class="token keyword">is</span> <span class="token boolean">None</span><span class="token punctuation">:</span></span>
<span class="line">                <span class="token keyword">return</span></span>
<span class="line"></span>
<span class="line">            data <span class="token operator">=</span> <span class="token punctuation">{</span></span>
<span class="line">                <span class="token string">"type"</span><span class="token punctuation">:</span> <span class="token string">"log"</span><span class="token punctuation">,</span></span>
<span class="line">                <span class="token string">"level"</span><span class="token punctuation">:</span> self<span class="token punctuation">.</span>get_level<span class="token punctuation">(</span>record<span class="token punctuation">.</span>levelname<span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">                <span class="token string">"message"</span><span class="token punctuation">:</span> self<span class="token punctuation">.</span><span class="token builtin">format</span><span class="token punctuation">(</span>record<span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">                <span class="token string">"logger"</span><span class="token punctuation">:</span> record<span class="token punctuation">.</span>name<span class="token punctuation">,</span></span>
<span class="line">                <span class="token string">"timestamp"</span><span class="token punctuation">:</span> record<span class="token punctuation">.</span>created<span class="token punctuation">,</span></span>
<span class="line">            <span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line">            async_to_sync<span class="token punctuation">(</span></span>
<span class="line">                channel_layer<span class="token punctuation">.</span>group_send</span>
<span class="line">            <span class="token punctuation">)</span><span class="token punctuation">(</span></span>
<span class="line">                <span class="token string">"debug_console"</span><span class="token punctuation">,</span></span>
<span class="line">                <span class="token punctuation">{</span></span>
<span class="line">                    <span class="token string">"type"</span><span class="token punctuation">:</span> <span class="token string">"send_log"</span><span class="token punctuation">,</span></span>
<span class="line">                    <span class="token string">"data"</span><span class="token punctuation">:</span> data<span class="token punctuation">,</span></span>
<span class="line">                <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">        <span class="token keyword">except</span> Exception<span class="token punctuation">:</span></span>
<span class="line">            self<span class="token punctuation">.</span>handleError<span class="token punctuation">(</span>record<span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">    <span class="token decorator annotation punctuation">@staticmethod</span></span>
<span class="line">    <span class="token keyword">def</span> <span class="token function">get_level</span><span class="token punctuation">(</span>level_name<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line"></span>
<span class="line">        mapping <span class="token operator">=</span> <span class="token punctuation">{</span></span>
<span class="line">            <span class="token string">"DEBUG"</span><span class="token punctuation">:</span> <span class="token string">"debug"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">"INFO"</span><span class="token punctuation">:</span> <span class="token string">"info"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">"WARNING"</span><span class="token punctuation">:</span> <span class="token string">"warn"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">"ERROR"</span><span class="token punctuation">:</span> <span class="token string">"error"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">"CRITICAL"</span><span class="token punctuation">:</span> <span class="token string">"error"</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line">        <span class="token keyword">return</span> mapping<span class="token punctuation">.</span>get<span class="token punctuation">(</span></span>
<span class="line">            level_name<span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">"info"</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h2 id="settings" tabindex="-1"><a class="header-anchor" href="#settings"><span>settings</span></a></h2>
<ul>
<li>7️⃣ تعديل settings.py</li>
</ul>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"></span>
<span class="line"><span class="token comment"># 0️⃣ channels</span></span>
<span class="line"></span>
<span class="line">ASGI_APPLICATION <span class="token operator">=</span> <span class="token string">"backend_django.asgi.application"</span></span>
<span class="line"></span>
<span class="line">CHANNEL_LAYERS <span class="token operator">=</span> <span class="token punctuation">{</span></span>
<span class="line">    <span class="token string">"default"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span></span>
<span class="line">        <span class="token string">"BACKEND"</span><span class="token punctuation">:</span> <span class="token string">"channels.layers.InMemoryChannelLayer"</span></span>
<span class="line">    <span class="token punctuation">}</span></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line">SO_IAM_OS_DEBUG_CONSOLE <span class="token operator">=</span> config<span class="token punctuation">(</span></span>
<span class="line">    <span class="token string">"SO_IAM_OS_DEBUG_CONSOLE"</span><span class="token punctuation">,</span></span>
<span class="line">    default<span class="token operator">=</span><span class="token boolean">False</span><span class="token punctuation">,</span></span>
<span class="line">    cast<span class="token operator">=</span><span class="token builtin">bool</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">)</span></span>
<span class="line">LOGGING <span class="token operator">=</span> <span class="token punctuation">{</span></span>
<span class="line">    <span class="token string">"version"</span><span class="token punctuation">:</span> <span class="token number">1</span><span class="token punctuation">,</span></span>
<span class="line"></span>
<span class="line">    <span class="token string">"disable_existing_loggers"</span><span class="token punctuation">:</span> <span class="token boolean">False</span><span class="token punctuation">,</span></span>
<span class="line"></span>
<span class="line">    <span class="token string">"formatters"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span></span>
<span class="line">        <span class="token string">"debug_console"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span></span>
<span class="line">            <span class="token string">"format"</span><span class="token punctuation">:</span> <span class="token punctuation">(</span></span>
<span class="line">                <span class="token string">"{asctime} | "</span></span>
<span class="line">                <span class="token string">"{levelname} | "</span></span>
<span class="line">                <span class="token string">"{name} | "</span></span>
<span class="line">                <span class="token string">"{message}"</span></span>
<span class="line">            <span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">"style"</span><span class="token punctuation">:</span> <span class="token string">"{"</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line"></span>
<span class="line">    <span class="token string">"handlers"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span></span>
<span class="line">        <span class="token string">"console"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span></span>
<span class="line">            <span class="token string">"class"</span><span class="token punctuation">:</span> <span class="token string">"logging.StreamHandler"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">"formatter"</span><span class="token punctuation">:</span> <span class="token string">"debug_console"</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line"></span>
<span class="line">    <span class="token string">"root"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span></span>
<span class="line">        <span class="token string">"handlers"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span><span class="token string">"console"</span><span class="token punctuation">]</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">"level"</span><span class="token punctuation">:</span> <span class="token string">"INFO"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token keyword">if</span> SO_IAM_OS_DEBUG_CONSOLE<span class="token punctuation">:</span></span>
<span class="line"></span>
<span class="line">    LOGGING<span class="token punctuation">[</span><span class="token string">"handlers"</span><span class="token punctuation">]</span><span class="token punctuation">[</span><span class="token string">"websocket"</span><span class="token punctuation">]</span> <span class="token operator">=</span> <span class="token punctuation">{</span></span>
<span class="line">        <span class="token string">"class"</span><span class="token punctuation">:</span> <span class="token string">"core.debug_console.handlers.WebSocketLogHandler"</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">"formatter"</span><span class="token punctuation">:</span> <span class="token string">"debug_console"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line">    LOGGING<span class="token punctuation">[</span><span class="token string">"root"</span><span class="token punctuation">]</span><span class="token punctuation">[</span><span class="token string">"handlers"</span><span class="token punctuation">]</span><span class="token punctuation">.</span>append<span class="token punctuation">(</span></span>
<span class="line">        <span class="token string">"websocket"</span></span>
<span class="line">    <span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token comment"># Application definition</span></span>
<span class="line">INSTALLED_APPS <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line"></span>
<span class="line">    <span class="token comment"># 📚 Libraries</span></span>
<span class="line">    <span class="token comment"># 0️⃣ channels</span></span>
<span class="line">    <span class="token string">"channels"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"django_celery_results"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"django_celery_beat"</span><span class="token punctuation">,</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line">    <span class="token comment"># So_Iam_OS</span></span>
<span class="line">    <span class="token string">"users_accounts"</span><span class="token punctuation">,</span>  <span class="token comment"># ✅</span></span>
<span class="line">    <span class="token comment"># ...</span></span>
<span class="line"><span class="token punctuation">]</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h2 id="asgi" tabindex="-1"><a class="header-anchor" href="#asgi"><span>ASGI</span></a></h2>
<ul>
<li>🔟 تعديل ASGI</li>
</ul>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token triple-quoted-string string">"""</span>
<span class="line">ASGI config for backend_django project.</span>
<span class="line"></span>
<span class="line">It exposes the ASGI callable as a module-level variable named ``application``.</span>
<span class="line"></span>
<span class="line">For more information on this file, see</span>
<span class="line">https://docs.djangoproject.com/en/6.1/howto/deployment/asgi/</span>
<span class="line">"""</span></span>
<span class="line"></span>
<span class="line"><span class="token keyword">from</span> core<span class="token punctuation">.</span>debug_console<span class="token punctuation">.</span>routing <span class="token keyword">import</span> websocket_urlpatterns</span>
<span class="line"><span class="token keyword">from</span> channels<span class="token punctuation">.</span>routing <span class="token keyword">import</span> ProtocolTypeRouter<span class="token punctuation">,</span> URLRouter</span>
<span class="line"><span class="token keyword">import</span> os</span>
<span class="line"></span>
<span class="line"><span class="token keyword">from</span> django<span class="token punctuation">.</span>core<span class="token punctuation">.</span>asgi <span class="token keyword">import</span> get_asgi_application</span>
<span class="line"></span>
<span class="line">os<span class="token punctuation">.</span>environ<span class="token punctuation">.</span>setdefault<span class="token punctuation">(</span><span class="token string">'DJANGO_SETTINGS_MODULE'</span><span class="token punctuation">,</span> <span class="token string">'backend_django.settings'</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line">django_asgi_app <span class="token operator">=</span> get_asgi_application<span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line">application <span class="token operator">=</span> ProtocolTypeRouter<span class="token punctuation">(</span><span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">    <span class="token string">"http"</span><span class="token punctuation">:</span> django_asgi_app<span class="token punctuation">,</span></span>
<span class="line"></span>
<span class="line">    <span class="token string">"websocket"</span><span class="token punctuation">:</span> URLRouter<span class="token punctuation">(</span></span>
<span class="line">        websocket_urlpatterns</span>
<span class="line">    <span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line"></span>
<span class="line"><span class="token punctuation">}</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h2 id="frontend" tabindex="-1"><a class="header-anchor" href="#frontend"><span>Frontend</span></a></h2>
<ul>
<li>1️⃣1️⃣ LiveDebugConsole vue</li>
</ul>
<div class="language-javascript line-numbers-mode" data-highlighter="prismjs" data-ext="js"><pre v-pre><code><span class="line"><span class="token operator">&lt;</span>script setup<span class="token operator">></span></span>
<span class="line"><span class="token keyword">import</span> <span class="token punctuation">{</span></span>
<span class="line">  ref<span class="token punctuation">,</span></span>
<span class="line">  onMounted<span class="token punctuation">,</span></span>
<span class="line">  onBeforeUnmount<span class="token punctuation">,</span></span>
<span class="line">  nextTick<span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">'vue'</span></span>
<span class="line"></span>
<span class="line"><span class="token keyword">const</span> logs <span class="token operator">=</span> <span class="token function">ref</span><span class="token punctuation">(</span><span class="token punctuation">[</span><span class="token punctuation">]</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"><span class="token keyword">const</span> status <span class="token operator">=</span> <span class="token function">ref</span><span class="token punctuation">(</span><span class="token string">'connecting'</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"><span class="token keyword">const</span> consoleEl <span class="token operator">=</span> <span class="token function">ref</span><span class="token punctuation">(</span><span class="token keyword">null</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"><span class="token keyword">const</span> isMinimized <span class="token operator">=</span> <span class="token function">ref</span><span class="token punctuation">(</span><span class="token boolean">false</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"><span class="token keyword">const</span> ws <span class="token operator">=</span> <span class="token function">ref</span><span class="token punctuation">(</span><span class="token keyword">null</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"><span class="token keyword">const</span> maxLines <span class="token operator">=</span> <span class="token number">500</span></span>
<span class="line"></span>
<span class="line"><span class="token keyword">const</span> <span class="token constant">DEBUG_ENABLED</span> <span class="token operator">=</span></span>
<span class="line">  <span class="token keyword">import</span><span class="token punctuation">.</span>meta<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">VITE_DEBUG_CONSOLE</span> <span class="token operator">===</span> <span class="token string">'true'</span></span>
<span class="line"></span>
<span class="line"><span class="token keyword">const</span> <span class="token constant">WS_URL</span> <span class="token operator">=</span></span>
<span class="line">  <span class="token keyword">import</span><span class="token punctuation">.</span>meta<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">VITE_DEBUG_WS_URL</span> <span class="token operator">||</span></span>
<span class="line">  <span class="token string">'ws://127.0.0.1:8000/ws/debug/'</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token comment">// ============================================================</span></span>
<span class="line"><span class="token comment">// Add Log</span></span>
<span class="line"><span class="token comment">// ============================================================</span></span>
<span class="line"></span>
<span class="line"><span class="token keyword">const</span> <span class="token function-variable function">addLog</span> <span class="token operator">=</span> <span class="token punctuation">(</span></span>
<span class="line">  <span class="token parameter">level<span class="token punctuation">,</span></span>
<span class="line">  message<span class="token punctuation">,</span></span>
<span class="line">  logger <span class="token operator">=</span> <span class="token keyword">null</span><span class="token punctuation">,</span></span>
<span class="line">  timestamp <span class="token operator">=</span> <span class="token keyword">null</span><span class="token punctuation">,</span></span></span>
<span class="line"><span class="token punctuation">)</span> <span class="token operator">=></span> <span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">  logs<span class="token punctuation">.</span>value<span class="token punctuation">.</span><span class="token function">push</span><span class="token punctuation">(</span><span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">    <span class="token literal-property property">id</span><span class="token operator">:</span></span>
<span class="line">      Date<span class="token punctuation">.</span><span class="token function">now</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">+</span></span>
<span class="line">      Math<span class="token punctuation">.</span><span class="token function">random</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line"></span>
<span class="line">    level<span class="token punctuation">,</span></span>
<span class="line"></span>
<span class="line">    message<span class="token punctuation">,</span></span>
<span class="line"></span>
<span class="line">    logger<span class="token punctuation">,</span></span>
<span class="line"></span>
<span class="line">    <span class="token literal-property property">timestamp</span><span class="token operator">:</span></span>
<span class="line">      timestamp <span class="token operator">||</span></span>
<span class="line">      Date<span class="token punctuation">.</span><span class="token function">now</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line"></span>
<span class="line">    <span class="token literal-property property">time</span><span class="token operator">:</span></span>
<span class="line">      <span class="token keyword">new</span> <span class="token class-name">Date</span><span class="token punctuation">(</span></span>
<span class="line">        timestamp</span>
<span class="line">          <span class="token operator">?</span> timestamp <span class="token operator">*</span> <span class="token number">1000</span></span>
<span class="line">          <span class="token operator">:</span> Date<span class="token punctuation">.</span><span class="token function">now</span><span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line">      <span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">toLocaleTimeString</span><span class="token punctuation">(</span></span>
<span class="line">        <span class="token string">'ar-EG'</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token punctuation">{</span></span>
<span class="line">          <span class="token literal-property property">hour12</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token punctuation">}</span></span>
<span class="line">      <span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">  <span class="token punctuation">}</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line">  <span class="token keyword">if</span> <span class="token punctuation">(</span></span>
<span class="line">    logs<span class="token punctuation">.</span>value<span class="token punctuation">.</span>length <span class="token operator">></span></span>
<span class="line">    maxLines</span>
<span class="line">  <span class="token punctuation">)</span> <span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">    logs<span class="token punctuation">.</span>value <span class="token operator">=</span></span>
<span class="line">      logs<span class="token punctuation">.</span>value<span class="token punctuation">.</span><span class="token function">slice</span><span class="token punctuation">(</span></span>
<span class="line">        <span class="token operator">-</span>maxLines</span>
<span class="line">      <span class="token punctuation">)</span></span>
<span class="line">  <span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line">  <span class="token function">nextTick</span><span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">=></span> <span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">    <span class="token keyword">if</span> <span class="token punctuation">(</span>consoleEl<span class="token punctuation">.</span>value<span class="token punctuation">)</span> <span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">      consoleEl<span class="token punctuation">.</span>value<span class="token punctuation">.</span>scrollTop <span class="token operator">=</span></span>
<span class="line">        consoleEl<span class="token punctuation">.</span>value<span class="token punctuation">.</span>scrollHeight</span>
<span class="line">    <span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line">  <span class="token punctuation">}</span><span class="token punctuation">)</span></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token comment">// ============================================================</span></span>
<span class="line"><span class="token comment">// Connect WebSocket</span></span>
<span class="line"><span class="token comment">// ============================================================</span></span>
<span class="line"></span>
<span class="line"><span class="token keyword">const</span> <span class="token function-variable function">connect</span> <span class="token operator">=</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">=></span> <span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">  <span class="token keyword">if</span> <span class="token punctuation">(</span><span class="token operator">!</span><span class="token constant">DEBUG_ENABLED</span><span class="token punctuation">)</span> <span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">    status<span class="token punctuation">.</span>value <span class="token operator">=</span> <span class="token string">'disabled'</span></span>
<span class="line"></span>
<span class="line">    <span class="token keyword">return</span></span>
<span class="line">  <span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line">  ws<span class="token punctuation">.</span>value <span class="token operator">=</span></span>
<span class="line">    <span class="token keyword">new</span> <span class="token class-name">WebSocket</span><span class="token punctuation">(</span></span>
<span class="line">      <span class="token constant">WS_URL</span></span>
<span class="line">    <span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line">  ws<span class="token punctuation">.</span>value<span class="token punctuation">.</span><span class="token function-variable function">onopen</span> <span class="token operator">=</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">=></span> <span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">    status<span class="token punctuation">.</span>value <span class="token operator">=</span></span>
<span class="line">      <span class="token string">'connected'</span></span>
<span class="line"></span>
<span class="line">    <span class="token function">addLog</span><span class="token punctuation">(</span></span>
<span class="line">      <span class="token string">'success'</span><span class="token punctuation">,</span></span>
<span class="line">      <span class="token string">'🔌 Debug Console connected'</span></span>
<span class="line">    <span class="token punctuation">)</span></span>
<span class="line">  <span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line">  ws<span class="token punctuation">.</span>value<span class="token punctuation">.</span><span class="token function-variable function">onmessage</span> <span class="token operator">=</span></span>
<span class="line">    <span class="token punctuation">(</span><span class="token parameter">event</span><span class="token punctuation">)</span> <span class="token operator">=></span> <span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">      <span class="token keyword">try</span> <span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">        <span class="token keyword">const</span> data <span class="token operator">=</span></span>
<span class="line">          <span class="token constant">JSON</span><span class="token punctuation">.</span><span class="token function">parse</span><span class="token punctuation">(</span></span>
<span class="line">            event<span class="token punctuation">.</span>data</span>
<span class="line">          <span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line">        <span class="token function">addLog</span><span class="token punctuation">(</span></span>
<span class="line"></span>
<span class="line">          data<span class="token punctuation">.</span>level <span class="token operator">||</span></span>
<span class="line">            <span class="token string">'info'</span><span class="token punctuation">,</span></span>
<span class="line"></span>
<span class="line">          data<span class="token punctuation">.</span>message <span class="token operator">||</span></span>
<span class="line">            <span class="token string">''</span><span class="token punctuation">,</span></span>
<span class="line"></span>
<span class="line">          data<span class="token punctuation">.</span>logger <span class="token operator">||</span></span>
<span class="line">            <span class="token keyword">null</span><span class="token punctuation">,</span></span>
<span class="line"></span>
<span class="line">          data<span class="token punctuation">.</span>timestamp <span class="token operator">||</span></span>
<span class="line">            <span class="token keyword">null</span><span class="token punctuation">,</span></span>
<span class="line"></span>
<span class="line">        <span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">      <span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">        <span class="token function">addLog</span><span class="token punctuation">(</span></span>
<span class="line">          <span class="token string">'info'</span><span class="token punctuation">,</span></span>
<span class="line">          event<span class="token punctuation">.</span>data</span>
<span class="line">        <span class="token punctuation">)</span></span>
<span class="line">      <span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line">    <span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line">  ws<span class="token punctuation">.</span>value<span class="token punctuation">.</span><span class="token function-variable function">onerror</span> <span class="token operator">=</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">=></span> <span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">    status<span class="token punctuation">.</span>value <span class="token operator">=</span></span>
<span class="line">      <span class="token string">'error'</span></span>
<span class="line"></span>
<span class="line">    <span class="token function">addLog</span><span class="token punctuation">(</span></span>
<span class="line">      <span class="token string">'error'</span><span class="token punctuation">,</span></span>
<span class="line">      <span class="token string">'❌ WebSocket connection error'</span></span>
<span class="line">    <span class="token punctuation">)</span></span>
<span class="line">  <span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line">  ws<span class="token punctuation">.</span>value<span class="token punctuation">.</span><span class="token function-variable function">onclose</span> <span class="token operator">=</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">=></span> <span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">    status<span class="token punctuation">.</span>value <span class="token operator">=</span></span>
<span class="line">      <span class="token string">'closed'</span></span>
<span class="line"></span>
<span class="line">    <span class="token function">addLog</span><span class="token punctuation">(</span></span>
<span class="line">      <span class="token string">'warn'</span><span class="token punctuation">,</span></span>
<span class="line">      <span class="token string">'🔌 Debug Console disconnected'</span></span>
<span class="line">    <span class="token punctuation">)</span></span>
<span class="line">  <span class="token punctuation">}</span></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token comment">// ============================================================</span></span>
<span class="line"><span class="token comment">// Close</span></span>
<span class="line"><span class="token comment">// ============================================================</span></span>
<span class="line"></span>
<span class="line"><span class="token keyword">const</span> <span class="token function-variable function">closeConsole</span> <span class="token operator">=</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">=></span> <span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">  ws<span class="token punctuation">.</span>value<span class="token operator">?.</span><span class="token function">close</span><span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token comment">// ============================================================</span></span>
<span class="line"><span class="token comment">// Clear</span></span>
<span class="line"><span class="token comment">// ============================================================</span></span>
<span class="line"></span>
<span class="line"><span class="token keyword">const</span> <span class="token function-variable function">clearLogs</span> <span class="token operator">=</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">=></span> <span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">  logs<span class="token punctuation">.</span>value <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token punctuation">]</span></span>
<span class="line"></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token comment">// ============================================================</span></span>
<span class="line"><span class="token comment">// Level Class</span></span>
<span class="line"><span class="token comment">// ============================================================</span></span>
<span class="line"></span>
<span class="line"><span class="token keyword">const</span> <span class="token function-variable function">levelClass</span> <span class="token operator">=</span> <span class="token punctuation">(</span></span>
<span class="line">  <span class="token parameter">level</span></span>
<span class="line"><span class="token punctuation">)</span> <span class="token operator">=></span> <span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">  <span class="token keyword">return</span> <span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">    <span class="token literal-property property">debug</span><span class="token operator">:</span></span>
<span class="line">      <span class="token string">'log-debug'</span><span class="token punctuation">,</span></span>
<span class="line"></span>
<span class="line">    <span class="token literal-property property">info</span><span class="token operator">:</span></span>
<span class="line">      <span class="token string">'log-info'</span><span class="token punctuation">,</span></span>
<span class="line"></span>
<span class="line">    <span class="token literal-property property">warn</span><span class="token operator">:</span></span>
<span class="line">      <span class="token string">'log-warn'</span><span class="token punctuation">,</span></span>
<span class="line"></span>
<span class="line">    <span class="token literal-property property">error</span><span class="token operator">:</span></span>
<span class="line">      <span class="token string">'log-error'</span><span class="token punctuation">,</span></span>
<span class="line"></span>
<span class="line">    <span class="token literal-property property">success</span><span class="token operator">:</span></span>
<span class="line">      <span class="token string">'log-success'</span><span class="token punctuation">,</span></span>
<span class="line"></span>
<span class="line">  <span class="token punctuation">}</span><span class="token punctuation">[</span>level<span class="token punctuation">]</span> <span class="token operator">||</span></span>
<span class="line">    <span class="token string">'log-info'</span></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token comment">// ============================================================</span></span>
<span class="line"><span class="token comment">// Lifecycle</span></span>
<span class="line"><span class="token comment">// ============================================================</span></span>
<span class="line"></span>
<span class="line"><span class="token function">onMounted</span><span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">=></span> <span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">  <span class="token function">connect</span><span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"><span class="token punctuation">}</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token function">onBeforeUnmount</span><span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">=></span> <span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">  ws<span class="token punctuation">.</span>value<span class="token operator">?.</span><span class="token function">close</span><span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"><span class="token punctuation">}</span><span class="token punctuation">)</span></span>
<span class="line"><span class="token operator">&lt;</span><span class="token operator">/</span>script<span class="token operator">></span></span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div class="language-html line-numbers-mode" data-highlighter="prismjs" data-ext="html"><pre v-pre><code><span class="line"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>template</span><span class="token punctuation">></span></span></span>
<span class="line">  <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>div</span></span>
<span class="line">    <span class="token attr-name">v-if</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>DEBUG_ENABLED<span class="token punctuation">"</span></span></span>
<span class="line">    <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>live-debug-console<span class="token punctuation">"</span></span></span>
<span class="line">    <span class="token attr-name">:class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>{</span>
<span class="line">      minimized:</span>
<span class="line">        isMinimized</span>
<span class="line">    }<span class="token punctuation">"</span></span></span>
<span class="line">  <span class="token punctuation">></span></span></span>
<span class="line">    <span class="token comment">&lt;!-- Header --></span></span>
<span class="line"></span>
<span class="line">    <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>div</span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>console-header<span class="token punctuation">"</span></span><span class="token punctuation">></span></span></span>
<span class="line">      <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>div</span><span class="token punctuation">></span></span></span>
<span class="line">        <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>span</span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>console-title<span class="token punctuation">"</span></span><span class="token punctuation">></span></span></span>
<span class="line">          <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>i</span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>pi pi-terminal<span class="token punctuation">"</span></span> <span class="token punctuation">/></span></span></span>
<span class="line"></span>
<span class="line">          Live Debug Console</span>
<span class="line">        <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>span</span><span class="token punctuation">></span></span></span>
<span class="line"></span>
<span class="line">        <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>span</span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>console-status<span class="token punctuation">"</span></span> <span class="token attr-name">:class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>status<span class="token punctuation">"</span></span><span class="token punctuation">></span></span> ● {{ status }} <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>span</span><span class="token punctuation">></span></span></span>
<span class="line">      <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>div</span><span class="token punctuation">></span></span></span>
<span class="line"></span>
<span class="line">      <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>div</span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>console-actions<span class="token punctuation">"</span></span><span class="token punctuation">></span></span></span>
<span class="line">        <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>button</span> <span class="token attr-name">@click</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>clearLogs<span class="token punctuation">"</span></span><span class="token punctuation">></span></span>Clear<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>button</span><span class="token punctuation">></span></span></span>
<span class="line"></span>
<span class="line">        <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>button</span></span>
<span class="line">          <span class="token attr-name">@click</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span></span>
<span class="line">            isMinimized =</span>
<span class="line">              !isMinimized</span>
<span class="line">          <span class="token punctuation">"</span></span></span>
<span class="line">        <span class="token punctuation">></span></span></span>
<span class="line">          {{ isMinimized ? '▲' : '▼' }}</span>
<span class="line">        <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>button</span><span class="token punctuation">></span></span></span>
<span class="line"></span>
<span class="line">        <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>button</span> <span class="token attr-name">@click</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>closeConsole<span class="token punctuation">"</span></span><span class="token punctuation">></span></span>×<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>button</span><span class="token punctuation">></span></span></span>
<span class="line">      <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>div</span><span class="token punctuation">></span></span></span>
<span class="line">    <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>div</span><span class="token punctuation">></span></span></span>
<span class="line"></span>
<span class="line">    <span class="token comment">&lt;!-- Logs --></span></span>
<span class="line"></span>
<span class="line">    <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>div</span> <span class="token attr-name">v-if</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>!isMinimized<span class="token punctuation">"</span></span> <span class="token attr-name">ref</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>consoleEl<span class="token punctuation">"</span></span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>console-body<span class="token punctuation">"</span></span><span class="token punctuation">></span></span></span>
<span class="line">      <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>div</span> <span class="token attr-name">v-if</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>!logs.length<span class="token punctuation">"</span></span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>console-empty<span class="token punctuation">"</span></span><span class="token punctuation">></span></span></span>
<span class="line">        Waiting for Django logs...</span>
<span class="line">      <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>div</span><span class="token punctuation">></span></span></span>
<span class="line"></span>
<span class="line">      <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>div</span></span>
<span class="line">        <span class="token attr-name">v-for</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>log in logs<span class="token punctuation">"</span></span></span>
<span class="line">        <span class="token attr-name">:key</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>log.id<span class="token punctuation">"</span></span></span>
<span class="line">        <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>log-line<span class="token punctuation">"</span></span></span>
<span class="line">        <span class="token attr-name">:class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span></span>
<span class="line">          levelClass(</span>
<span class="line">            log.level</span>
<span class="line">          )</span>
<span class="line">        <span class="token punctuation">"</span></span></span>
<span class="line">      <span class="token punctuation">></span></span></span>
<span class="line">        <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>span</span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>log-time<span class="token punctuation">"</span></span><span class="token punctuation">></span></span> {{ log.time }} <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>span</span><span class="token punctuation">></span></span></span>
<span class="line"></span>
<span class="line">        <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>span</span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>log-level<span class="token punctuation">"</span></span><span class="token punctuation">></span></span> {{ log.level .toUpperCase() }} <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>span</span><span class="token punctuation">></span></span></span>
<span class="line"></span>
<span class="line">        <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>span</span> <span class="token attr-name">v-if</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>log.logger<span class="token punctuation">"</span></span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>log-logger<span class="token punctuation">"</span></span><span class="token punctuation">></span></span> [{{ log.logger }}] <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>span</span><span class="token punctuation">></span></span></span>
<span class="line"></span>
<span class="line">        <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>span</span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>log-message<span class="token punctuation">"</span></span><span class="token punctuation">></span></span> {{ log.message }} <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>span</span><span class="token punctuation">></span></span></span>
<span class="line">      <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>div</span><span class="token punctuation">></span></span></span>
<span class="line">    <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>div</span><span class="token punctuation">></span></span></span>
<span class="line">  <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>div</span><span class="token punctuation">></span></span></span>
<span class="line"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>template</span><span class="token punctuation">></span></span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><div class="language-css line-numbers-mode" data-highlighter="prismjs" data-ext="css"><pre v-pre><code><span class="line"></span>
<span class="line"><span class="token selector">&lt;style scoped></span>
<span class="line">.live-debug-console</span> <span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">position</span><span class="token punctuation">:</span> fixed<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">left</span><span class="token punctuation">:</span> 20px<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">right</span><span class="token punctuation">:</span> 20px<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">bottom</span><span class="token punctuation">:</span> 20px<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">z-index</span><span class="token punctuation">:</span> 99999<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">background</span><span class="token punctuation">:</span></span>
<span class="line">    #07111f<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">border</span><span class="token punctuation">:</span></span>
<span class="line">    1px solid #1e5eff<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">border-radius</span><span class="token punctuation">:</span></span>
<span class="line">    10px<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">color</span><span class="token punctuation">:</span></span>
<span class="line">    #e5e7eb<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">font-family</span><span class="token punctuation">:</span></span>
<span class="line">    monospace<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">box-shadow</span><span class="token punctuation">:</span></span>
<span class="line">    0 10px 40px</span>
<span class="line">    <span class="token function">rgba</span><span class="token punctuation">(</span>0<span class="token punctuation">,</span> 0<span class="token punctuation">,</span> 0<span class="token punctuation">,</span> .5<span class="token punctuation">)</span><span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token selector">.console-header</span> <span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">display</span><span class="token punctuation">:</span></span>
<span class="line">    flex<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">justify-content</span><span class="token punctuation">:</span></span>
<span class="line">    space-between<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">align-items</span><span class="token punctuation">:</span></span>
<span class="line">    center<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">padding</span><span class="token punctuation">:</span></span>
<span class="line">    12px 16px<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">background</span><span class="token punctuation">:</span></span>
<span class="line">    #0b1728<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">border-bottom</span><span class="token punctuation">:</span></span>
<span class="line">    1px solid #1e293b<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token selector">.console-title</span> <span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">font-weight</span><span class="token punctuation">:</span></span>
<span class="line">    700<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">margin-right</span><span class="token punctuation">:</span></span>
<span class="line">    15px<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token selector">.console-status</span> <span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">font-size</span><span class="token punctuation">:</span></span>
<span class="line">    12px<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token selector">.console-status.connected</span> <span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">color</span><span class="token punctuation">:</span></span>
<span class="line">    #22c55e<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token selector">.console-status.error</span> <span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">color</span><span class="token punctuation">:</span></span>
<span class="line">    #ef4444<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token selector">.console-status.closed</span> <span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">color</span><span class="token punctuation">:</span></span>
<span class="line">    #f59e0b<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token selector">.console-actions</span> <span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">display</span><span class="token punctuation">:</span></span>
<span class="line">    flex<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">gap</span><span class="token punctuation">:</span></span>
<span class="line">    6px<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token selector">.console-actions button</span> <span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">border</span><span class="token punctuation">:</span></span>
<span class="line">    0<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">background</span><span class="token punctuation">:</span></span>
<span class="line">    #17243a<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">color</span><span class="token punctuation">:</span></span>
<span class="line">    white<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">padding</span><span class="token punctuation">:</span></span>
<span class="line">    5px 10px<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">border-radius</span><span class="token punctuation">:</span></span>
<span class="line">    5px<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">cursor</span><span class="token punctuation">:</span></span>
<span class="line">    pointer<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token selector">.console-body</span> <span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">height</span><span class="token punctuation">:</span></span>
<span class="line">    300px<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">overflow-y</span><span class="token punctuation">:</span></span>
<span class="line">    auto<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">padding</span><span class="token punctuation">:</span></span>
<span class="line">    12px<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token selector">.console-empty</span> <span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">color</span><span class="token punctuation">:</span></span>
<span class="line">    #64748b<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">text-align</span><span class="token punctuation">:</span></span>
<span class="line">    center<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">padding</span><span class="token punctuation">:</span></span>
<span class="line">    50px<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token selector">.log-line</span> <span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">display</span><span class="token punctuation">:</span></span>
<span class="line">    flex<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">gap</span><span class="token punctuation">:</span></span>
<span class="line">    10px<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">padding</span><span class="token punctuation">:</span></span>
<span class="line">    4px 0<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">font-size</span><span class="token punctuation">:</span></span>
<span class="line">    13px<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">line-height</span><span class="token punctuation">:</span></span>
<span class="line">    1.5<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token selector">.log-time</span> <span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">color</span><span class="token punctuation">:</span></span>
<span class="line">    #64748b<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">min-width</span><span class="token punctuation">:</span></span>
<span class="line">    75px<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token selector">.log-level</span> <span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">min-width</span><span class="token punctuation">:</span></span>
<span class="line">    65px<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">font-weight</span><span class="token punctuation">:</span></span>
<span class="line">    bold<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token selector">.log-logger</span> <span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">color</span><span class="token punctuation">:</span></span>
<span class="line">    #38bdf8<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token selector">.log-message</span> <span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">white-space</span><span class="token punctuation">:</span></span>
<span class="line">    pre-wrap<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token selector">.log-info</span> <span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">color</span><span class="token punctuation">:</span></span>
<span class="line">    #60a5fa<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token selector">.log-debug</span> <span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">color</span><span class="token punctuation">:</span></span>
<span class="line">    #a78bfa<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token selector">.log-warn</span> <span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">color</span><span class="token punctuation">:</span></span>
<span class="line">    #fbbf24<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token selector">.log-error</span> <span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">color</span><span class="token punctuation">:</span></span>
<span class="line">    #f87171<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token selector">.log-success</span> <span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">color</span><span class="token punctuation">:</span></span>
<span class="line">    #4ade80<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token selector">.minimized</span>
<span class="line">.console-body</span> <span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">  <span class="token property">display</span><span class="token punctuation">:</span></span>
<span class="line">    none<span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line">&lt;/style></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><ul>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
</ul>
<h1 id="so-iam-os-—-live-debug-console" tabindex="-1"><a class="header-anchor" href="#so-iam-os-—-live-debug-console"><span>SO_IAM_OS — Live Debug Console</span></a></h1>
<h2 id="_1-تعريف-المعرفة" tabindex="-1"><a class="header-anchor" href="#_1-تعريف-المعرفة"><span>1. تعريف المعرفة</span></a></h2>
<p><strong>اسم النظام:</strong> Live Debug Console
<strong>المشروع:</strong> SO_IAM_OS
<strong>التقنية:</strong> Django Channels + WebSocket + Vue.js
<strong>الغرض:</strong> عرض Django Logs مباشرة داخل واجهة Vue أثناء تشغيل المشروع.</p>
<hr>
<h1 id="_2-الهدف-من-النظام" tabindex="-1"><a class="header-anchor" href="#_2-الهدف-من-النظام"><span>2. الهدف من النظام</span></a></h1>
<p>Live Debug Console هو نظام Debug داخلي يسمح للمطور بمشاهدة Logs الخاصة بـ Django مباشرة داخل المتصفح.</p>
<p>التدفق الأساسي:</p>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Django Logger</span>
<span class="line">      ↓</span>
<span class="line">WebSocketLogHandler</span>
<span class="line">      ↓</span>
<span class="line">Django Channels</span>
<span class="line">      ↓</span>
<span class="line">WebSocket Group</span>
<span class="line">      ↓</span>
<span class="line">Vue LiveDebugConsole</span>
<span class="line">      ↓</span>
<span class="line">عرض الـ Logs مباشرة</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><p>وبذلك لا يحتاج المطور إلى الاعتماد فقط على Terminal لمتابعة Logs.</p>
<hr>
<h1 id="_3-django-channels" tabindex="-1"><a class="header-anchor" href="#_3-django-channels"><span>3. Django Channels</span></a></h1>
<p>يتم استخدام مكتبة:</p>
<div class="language-bash line-numbers-mode" data-highlighter="prismjs" data-ext="sh"><pre v-pre><code><span class="line">pip <span class="token function">install</span> channels</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><p>ويمكن فحص بعض حزم المشروع باستخدام:</p>
<div class="language-bash line-numbers-mode" data-highlighter="prismjs" data-ext="sh"><pre v-pre><code><span class="line">pip show django-celery-results</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><div class="language-bash line-numbers-mode" data-highlighter="prismjs" data-ext="sh"><pre v-pre><code><span class="line">pip show django-celery-beat</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><hr>
<h1 id="_4-إعداد-django" tabindex="-1"><a class="header-anchor" href="#_4-إعداد-django"><span>4. إعداد Django</span></a></h1>
<p>إضافة Channels إلى:</p>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">INSTALLED_APPS <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line">    <span class="token punctuation">.</span><span class="token punctuation">.</span><span class="token punctuation">.</span></span>
<span class="line">    <span class="token string">"channels"</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">]</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><p>وتحديد ASGI:</p>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">ASGI_APPLICATION <span class="token operator">=</span> <span class="token string">"backend_django.asgi.application"</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><p>ثم إعداد Channel Layer:</p>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">CHANNEL_LAYERS <span class="token operator">=</span> <span class="token punctuation">{</span></span>
<span class="line">    <span class="token string">"default"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span></span>
<span class="line">        <span class="token string">"BACKEND"</span><span class="token punctuation">:</span> <span class="token string">"channels.layers.InMemoryChannelLayer"</span></span>
<span class="line">    <span class="token punctuation">}</span></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><p>في الوضع الحالي يتم استخدام:</p>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">InMemoryChannelLayer</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><hr>
<h1 id="_5-هيكل-ملفات-debug-console" tabindex="-1"><a class="header-anchor" href="#_5-هيكل-ملفات-debug-console"><span>5. هيكل ملفات Debug Console</span></a></h1>
<p>الهيكل المقترح داخل المشروع:</p>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">backend_django/</span>
<span class="line">│</span>
<span class="line">├── manage.py</span>
<span class="line">│</span>
<span class="line">├── backend_django/</span>
<span class="line">│   ├── settings.py</span>
<span class="line">│   ├── asgi.py</span>
<span class="line">│   ├── urls.py</span>
<span class="line">│   └── ...</span>
<span class="line">│</span>
<span class="line">├── core/</span>
<span class="line">│   ├── __init__.py</span>
<span class="line">│   │</span>
<span class="line">│   └── debug/</span>
<span class="line">│       ├── __init__.py</span>
<span class="line">│       ├── consumers.py</span>
<span class="line">│       ├── routing.py</span>
<span class="line">│       └── handlers.py</span>
<span class="line">│</span>
<span class="line">├── users_accounts/</span>
<span class="line">│   ├── api.py</span>
<span class="line">│   └── ...</span>
<span class="line">│</span>
<span class="line">└── ...</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><blockquote>
<p><strong>ملاحظة:</strong> ملف الإعدادات الوارد في المصدر يشير لاحقًا إلى المسار <code v-pre>core.debug_console.handlers.WebSocketLogHandler</code>، بينما الهيكل المعروض يستخدم <code v-pre>core/debug/</code>. هذه نقطة يجب الحفاظ عليها كقرار يحتاج للمراجعة قبل التنفيذ النهائي، وليس تغييرها تلقائيًا.</p>
</blockquote>
<hr>
<h1 id="_6-consumer" tabindex="-1"><a class="header-anchor" href="#_6-consumer"><span>6. Consumer</span></a></h1>
<p>الـ Consumer مسؤول عن إدارة اتصال WebSocket.</p>
<h2 id="consumers-py" tabindex="-1"><a class="header-anchor" href="#consumers-py"><span><code v-pre>consumers.py</code></span></a></h2>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">import</span> json</span>
<span class="line"><span class="token keyword">from</span> channels<span class="token punctuation">.</span>generic<span class="token punctuation">.</span>websocket <span class="token keyword">import</span> AsyncWebsocketConsumer</span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token keyword">class</span> <span class="token class-name">DebugConsoleConsumer</span><span class="token punctuation">(</span>AsyncWebsocketConsumer<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line"></span>
<span class="line">    <span class="token keyword">async</span> <span class="token keyword">def</span> <span class="token function">connect</span><span class="token punctuation">(</span>self<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">        <span class="token triple-quoted-string string">"""</span>
<span class="line">        الاتصال بالـ Live Debug Console</span>
<span class="line">        """</span></span>
<span class="line"></span>
<span class="line">        self<span class="token punctuation">.</span>group_name <span class="token operator">=</span> <span class="token string">"debug_console"</span></span>
<span class="line"></span>
<span class="line">        <span class="token comment"># إضافة المتصفح إلى مجموعة Debug Console</span></span>
<span class="line">        <span class="token keyword">await</span> self<span class="token punctuation">.</span>channel_layer<span class="token punctuation">.</span>group_add<span class="token punctuation">(</span></span>
<span class="line">            self<span class="token punctuation">.</span>group_name<span class="token punctuation">,</span></span>
<span class="line">            self<span class="token punctuation">.</span>channel_name<span class="token punctuation">,</span></span>
<span class="line">        <span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">        <span class="token comment"># قبول WebSocket connection</span></span>
<span class="line">        <span class="token keyword">await</span> self<span class="token punctuation">.</span>accept<span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">        <span class="token comment"># رسالة اتصال أولية</span></span>
<span class="line">        <span class="token keyword">await</span> self<span class="token punctuation">.</span>send<span class="token punctuation">(</span></span>
<span class="line">            text_data<span class="token operator">=</span>json<span class="token punctuation">.</span>dumps<span class="token punctuation">(</span><span class="token punctuation">{</span></span>
<span class="line">                <span class="token string">"type"</span><span class="token punctuation">:</span> <span class="token string">"system"</span><span class="token punctuation">,</span></span>
<span class="line">                <span class="token string">"level"</span><span class="token punctuation">:</span> <span class="token string">"success"</span><span class="token punctuation">,</span></span>
<span class="line">                <span class="token string">"message"</span><span class="token punctuation">:</span> <span class="token string">"🔌 Debug Console connected"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token punctuation">}</span><span class="token punctuation">)</span></span>
<span class="line">        <span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">    <span class="token keyword">async</span> <span class="token keyword">def</span> <span class="token function">disconnect</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> close_code<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">        <span class="token triple-quoted-string string">"""</span>
<span class="line">        إزالة المتصفح من Debug Console</span>
<span class="line">        """</span></span>
<span class="line"></span>
<span class="line">        <span class="token keyword">await</span> self<span class="token punctuation">.</span>channel_layer<span class="token punctuation">.</span>group_discard<span class="token punctuation">(</span></span>
<span class="line">            self<span class="token punctuation">.</span>group_name<span class="token punctuation">,</span></span>
<span class="line">            self<span class="token punctuation">.</span>channel_name<span class="token punctuation">,</span></span>
<span class="line">        <span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">    <span class="token keyword">async</span> <span class="token keyword">def</span> <span class="token function">send_log</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> event<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">        <span class="token triple-quoted-string string">"""</span>
<span class="line">        استقبال Log من Django Logging Handler</span>
<span class="line">        وإرساله للمتصفح</span>
<span class="line">        """</span></span>
<span class="line"></span>
<span class="line">        <span class="token keyword">await</span> self<span class="token punctuation">.</span>send<span class="token punctuation">(</span></span>
<span class="line">            text_data<span class="token operator">=</span>json<span class="token punctuation">.</span>dumps<span class="token punctuation">(</span></span>
<span class="line">                event<span class="token punctuation">[</span><span class="token string">"data"</span><span class="token punctuation">]</span></span>
<span class="line">            <span class="token punctuation">)</span></span>
<span class="line">        <span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h1 id="_7-debug-group" tabindex="-1"><a class="header-anchor" href="#_7-debug-group"><span>7. Debug Group</span></a></h1>
<p>جميع اتصالات Debug Console تستخدم المجموعة:</p>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">debug_console</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><p>عند اتصال المتصفح:</p>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">await</span> self<span class="token punctuation">.</span>channel_layer<span class="token punctuation">.</span>group_add<span class="token punctuation">(</span></span>
<span class="line">    self<span class="token punctuation">.</span>group_name<span class="token punctuation">,</span></span>
<span class="line">    self<span class="token punctuation">.</span>channel_name<span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><p>وعند إغلاق الاتصال:</p>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">await</span> self<span class="token punctuation">.</span>channel_layer<span class="token punctuation">.</span>group_discard<span class="token punctuation">(</span></span>
<span class="line">    self<span class="token punctuation">.</span>group_name<span class="token punctuation">,</span></span>
<span class="line">    self<span class="token punctuation">.</span>channel_name<span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><p>وبالتالي يمكن إرسال Log واحد إلى جميع متصفحات Debug Console المتصلة بالمجموعة.</p>
<hr>
<h1 id="_8-websocket-routing" tabindex="-1"><a class="header-anchor" href="#_8-websocket-routing"><span>8. WebSocket Routing</span></a></h1>
<h2 id="routing-py" tabindex="-1"><a class="header-anchor" href="#routing-py"><span><code v-pre>routing.py</code></span></a></h2>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">from</span> django<span class="token punctuation">.</span>urls <span class="token keyword">import</span> re_path</span>
<span class="line"><span class="token keyword">from</span> <span class="token punctuation">.</span>consumers <span class="token keyword">import</span> DebugConsoleConsumer</span>
<span class="line"></span>
<span class="line"></span>
<span class="line">websocket_urlpatterns <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line">    re_path<span class="token punctuation">(</span></span>
<span class="line">        <span class="token string">r"ws/debug/$"</span><span class="token punctuation">,</span></span>
<span class="line">        DebugConsoleConsumer<span class="token punctuation">.</span>as_asgi<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">]</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><p>عنوان WebSocket المستخدم في النظام:</p>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">ws://127.0.0.1:8000/ws/debug/</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><hr>
<h1 id="_9-websocketloghandler" tabindex="-1"><a class="header-anchor" href="#_9-websocketloghandler"><span>9. WebSocketLogHandler</span></a></h1>
<p>هذا هو الجزء الأساسي الذي يربط Django Logging مع WebSocket.</p>
<p>الفكرة:</p>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">logging.LogRecord</span>
<span class="line">       ↓</span>
<span class="line">WebSocketLogHandler</span>
<span class="line">       ↓</span>
<span class="line">Channel Layer</span>
<span class="line">       ↓</span>
<span class="line">debug_console</span>
<span class="line">       ↓</span>
<span class="line">WebSocket</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h2 id="handlers-py" tabindex="-1"><a class="header-anchor" href="#handlers-py"><span><code v-pre>handlers.py</code></span></a></h2>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">import</span> logging</span>
<span class="line"></span>
<span class="line"><span class="token keyword">from</span> asgiref<span class="token punctuation">.</span>sync <span class="token keyword">import</span> async_to_sync</span>
<span class="line"><span class="token keyword">from</span> channels<span class="token punctuation">.</span>layers <span class="token keyword">import</span> get_channel_layer</span>
<span class="line"></span>
<span class="line"></span>
<span class="line"><span class="token keyword">class</span> <span class="token class-name">WebSocketLogHandler</span><span class="token punctuation">(</span>logging<span class="token punctuation">.</span>Handler<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line"></span>
<span class="line">    <span class="token keyword">def</span> <span class="token function">emit</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> record<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">        <span class="token triple-quoted-string string">"""</span>
<span class="line">        إرسال أي Django Log إلى Live Debug Console</span>
<span class="line">        """</span></span>
<span class="line"></span>
<span class="line">        <span class="token keyword">try</span><span class="token punctuation">:</span></span>
<span class="line">            channel_layer <span class="token operator">=</span> get_channel_layer<span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">            <span class="token keyword">if</span> channel_layer <span class="token keyword">is</span> <span class="token boolean">None</span><span class="token punctuation">:</span></span>
<span class="line">                <span class="token keyword">return</span></span>
<span class="line"></span>
<span class="line">            data <span class="token operator">=</span> <span class="token punctuation">{</span></span>
<span class="line">                <span class="token string">"type"</span><span class="token punctuation">:</span> <span class="token string">"log"</span><span class="token punctuation">,</span></span>
<span class="line">                <span class="token string">"level"</span><span class="token punctuation">:</span> self<span class="token punctuation">.</span>get_level<span class="token punctuation">(</span>record<span class="token punctuation">.</span>levelname<span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">                <span class="token string">"message"</span><span class="token punctuation">:</span> self<span class="token punctuation">.</span><span class="token builtin">format</span><span class="token punctuation">(</span>record<span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">                <span class="token string">"logger"</span><span class="token punctuation">:</span> record<span class="token punctuation">.</span>name<span class="token punctuation">,</span></span>
<span class="line">                <span class="token string">"timestamp"</span><span class="token punctuation">:</span> record<span class="token punctuation">.</span>created<span class="token punctuation">,</span></span>
<span class="line">            <span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line">            async_to_sync<span class="token punctuation">(</span></span>
<span class="line">                channel_layer<span class="token punctuation">.</span>group_send</span>
<span class="line">            <span class="token punctuation">)</span><span class="token punctuation">(</span></span>
<span class="line">                <span class="token string">"debug_console"</span><span class="token punctuation">,</span></span>
<span class="line">                <span class="token punctuation">{</span></span>
<span class="line">                    <span class="token string">"type"</span><span class="token punctuation">:</span> <span class="token string">"send_log"</span><span class="token punctuation">,</span></span>
<span class="line">                    <span class="token string">"data"</span><span class="token punctuation">:</span> data<span class="token punctuation">,</span></span>
<span class="line">                <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">        <span class="token keyword">except</span> Exception<span class="token punctuation">:</span></span>
<span class="line">            self<span class="token punctuation">.</span>handleError<span class="token punctuation">(</span>record<span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">    <span class="token decorator annotation punctuation">@staticmethod</span></span>
<span class="line">    <span class="token keyword">def</span> <span class="token function">get_level</span><span class="token punctuation">(</span>level_name<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line"></span>
<span class="line">        mapping <span class="token operator">=</span> <span class="token punctuation">{</span></span>
<span class="line">            <span class="token string">"DEBUG"</span><span class="token punctuation">:</span> <span class="token string">"debug"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">"INFO"</span><span class="token punctuation">:</span> <span class="token string">"info"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">"WARNING"</span><span class="token punctuation">:</span> <span class="token string">"warn"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">"ERROR"</span><span class="token punctuation">:</span> <span class="token string">"error"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">"CRITICAL"</span><span class="token punctuation">:</span> <span class="token string">"error"</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line">        <span class="token keyword">return</span> mapping<span class="token punctuation">.</span>get<span class="token punctuation">(</span></span>
<span class="line">            level_name<span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">"info"</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h1 id="_10-تحويل-مستويات-logging" tabindex="-1"><a class="header-anchor" href="#_10-تحويل-مستويات-logging"><span>10. تحويل مستويات Logging</span></a></h1>
<p>النظام يحول مستويات Django Logging إلى مستويات مناسبة للواجهة:</p>
<table>
<thead>
<tr>
<th>Django</th>
<th>Vue Console</th>
</tr>
</thead>
<tbody>
<tr>
<td>DEBUG</td>
<td>debug</td>
</tr>
<tr>
<td>INFO</td>
<td>info</td>
</tr>
<tr>
<td>WARNING</td>
<td>warn</td>
</tr>
<tr>
<td>ERROR</td>
<td>error</td>
</tr>
<tr>
<td>CRITICAL</td>
<td>error</td>
</tr>
</tbody>
</table>
<hr>
<h1 id="_11-البيانات-المرسلة-إلى-vue" tabindex="-1"><a class="header-anchor" href="#_11-البيانات-المرسلة-إلى-vue"><span>11. البيانات المرسلة إلى Vue</span></a></h1>
<p>كل Log يتم تحويله إلى Object يحتوي على:</p>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token punctuation">{</span></span>
<span class="line">    <span class="token string">"type"</span><span class="token punctuation">:</span> <span class="token string">"log"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"level"</span><span class="token punctuation">:</span> <span class="token string">"..."</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"message"</span><span class="token punctuation">:</span> <span class="token string">"..."</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"logger"</span><span class="token punctuation">:</span> <span class="token string">"..."</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"timestamp"</span><span class="token punctuation">:</span> <span class="token punctuation">.</span><span class="token punctuation">.</span><span class="token punctuation">.</span></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><p>حيث:</p>
<ul>
<li><code v-pre>type</code>: نوع الرسالة.</li>
<li><code v-pre>level</code>: مستوى الـ Log.</li>
<li><code v-pre>message</code>: نص الرسالة.</li>
<li><code v-pre>logger</code>: اسم الـ Logger.</li>
<li><code v-pre>timestamp</code>: وقت إنشاء الـ Log.</li>
</ul>
<hr>
<h1 id="_12-إعداد-logging-في-settings-py" tabindex="-1"><a class="header-anchor" href="#_12-إعداد-logging-في-settings-py"><span>12. إعداد Logging في settings.py</span></a></h1>
<p>يتم تشغيل Debug Console بناءً على متغير:</p>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">SO_IAM_OS_DEBUG_CONSOLE</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><p>ويتم قراءته من إعدادات المشروع:</p>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">SO_IAM_OS_DEBUG_CONSOLE <span class="token operator">=</span> config<span class="token punctuation">(</span></span>
<span class="line">    <span class="token string">"SO_IAM_OS_DEBUG_CONSOLE"</span><span class="token punctuation">,</span></span>
<span class="line">    default<span class="token operator">=</span><span class="token boolean">False</span><span class="token punctuation">,</span></span>
<span class="line">    cast<span class="token operator">=</span><span class="token builtin">bool</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><p>وهذا يجعل تشغيل Live Debug Console قابلًا للتحكم من إعدادات البيئة.</p>
<hr>
<h1 id="_13-logging-configuration" tabindex="-1"><a class="header-anchor" href="#_13-logging-configuration"><span>13. Logging Configuration</span></a></h1>
<p>الإعداد الأساسي:</p>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">LOGGING <span class="token operator">=</span> <span class="token punctuation">{</span></span>
<span class="line">    <span class="token string">"version"</span><span class="token punctuation">:</span> <span class="token number">1</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"disable_existing_loggers"</span><span class="token punctuation">:</span> <span class="token boolean">False</span><span class="token punctuation">,</span></span>
<span class="line"></span>
<span class="line">    <span class="token string">"formatters"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span></span>
<span class="line">        <span class="token string">"debug_console"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span></span>
<span class="line">            <span class="token string">"format"</span><span class="token punctuation">:</span> <span class="token punctuation">(</span></span>
<span class="line">                <span class="token string">"{asctime} | "</span></span>
<span class="line">                <span class="token string">"{levelname} | "</span></span>
<span class="line">                <span class="token string">"{name} | "</span></span>
<span class="line">                <span class="token string">"{message}"</span></span>
<span class="line">            <span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">"style"</span><span class="token punctuation">:</span> <span class="token string">"{"</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line"></span>
<span class="line">    <span class="token string">"handlers"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span></span>
<span class="line">        <span class="token string">"console"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span></span>
<span class="line">            <span class="token string">"class"</span><span class="token punctuation">:</span> <span class="token string">"logging.StreamHandler"</span><span class="token punctuation">,</span></span>
<span class="line">            <span class="token string">"formatter"</span><span class="token punctuation">:</span> <span class="token string">"debug_console"</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line"></span>
<span class="line">    <span class="token string">"root"</span><span class="token punctuation">:</span> <span class="token punctuation">{</span></span>
<span class="line">        <span class="token string">"handlers"</span><span class="token punctuation">:</span> <span class="token punctuation">[</span><span class="token string">"console"</span><span class="token punctuation">]</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">"level"</span><span class="token punctuation">:</span> <span class="token string">"INFO"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">}</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h1 id="_14-تفعيل-websocket-logging" tabindex="-1"><a class="header-anchor" href="#_14-تفعيل-websocket-logging"><span>14. تفعيل WebSocket Logging</span></a></h1>
<p>إذا كان:</p>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">SO_IAM_OS_DEBUG_CONSOLE <span class="token operator">=</span> <span class="token boolean">True</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><p>يتم إضافة WebSocket Handler:</p>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">if</span> SO_IAM_OS_DEBUG_CONSOLE<span class="token punctuation">:</span></span>
<span class="line"></span>
<span class="line">    LOGGING<span class="token punctuation">[</span><span class="token string">"handlers"</span><span class="token punctuation">]</span><span class="token punctuation">[</span><span class="token string">"websocket"</span><span class="token punctuation">]</span> <span class="token operator">=</span> <span class="token punctuation">{</span></span>
<span class="line">        <span class="token string">"class"</span><span class="token punctuation">:</span> <span class="token string">"core.debug_console.handlers.WebSocketLogHandler"</span><span class="token punctuation">,</span></span>
<span class="line">        <span class="token string">"formatter"</span><span class="token punctuation">:</span> <span class="token string">"debug_console"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">}</span></span>
<span class="line"></span>
<span class="line">    LOGGING<span class="token punctuation">[</span><span class="token string">"root"</span><span class="token punctuation">]</span><span class="token punctuation">[</span><span class="token string">"handlers"</span><span class="token punctuation">]</span><span class="token punctuation">.</span>append<span class="token punctuation">(</span></span>
<span class="line">        <span class="token string">"websocket"</span></span>
<span class="line">    <span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><p>وبالتالي يصبح الـ Root Logger مرتبطًا أيضًا بـ WebSocket.</p>
<blockquote>
<p><strong>ملاحظة:</strong> المسار <code v-pre>core.debug_console.handlers.WebSocketLogHandler</code> يجب أن يتطابق فعليًا مع مكان <code v-pre>handlers.py</code> في المشروع.</p>
</blockquote>
<hr>
<h1 id="_15-installed-apps" tabindex="-1"><a class="header-anchor" href="#_15-installed-apps"><span>15. Installed Apps</span></a></h1>
<p>إضافة Channels:</p>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">INSTALLED_APPS <span class="token operator">=</span> <span class="token punctuation">[</span></span>
<span class="line">    <span class="token comment"># Libraries</span></span>
<span class="line"></span>
<span class="line">    <span class="token string">"channels"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"django_celery_results"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"django_celery_beat"</span><span class="token punctuation">,</span></span>
<span class="line"></span>
<span class="line">    <span class="token comment"># SO_IAM_OS</span></span>
<span class="line"></span>
<span class="line">    <span class="token string">"users_accounts"</span><span class="token punctuation">,</span></span>
<span class="line"></span>
<span class="line">    <span class="token comment"># ...</span></span>
<span class="line"><span class="token punctuation">]</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h1 id="_16-asgi" tabindex="-1"><a class="header-anchor" href="#_16-asgi"><span>16. ASGI</span></a></h1>
<p>ملف:</p>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">backend_django/asgi.py</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><p>هو نقطة الدخول التي تجمع HTTP وWebSocket.</p>
<p>الكود المستخدم:</p>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">from</span> core<span class="token punctuation">.</span>debug_console<span class="token punctuation">.</span>routing <span class="token keyword">import</span> websocket_urlpatterns</span>
<span class="line"></span>
<span class="line"><span class="token keyword">from</span> channels<span class="token punctuation">.</span>routing <span class="token keyword">import</span> <span class="token punctuation">(</span></span>
<span class="line">    ProtocolTypeRouter<span class="token punctuation">,</span></span>
<span class="line">    URLRouter<span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"><span class="token keyword">import</span> os</span>
<span class="line"></span>
<span class="line"><span class="token keyword">from</span> django<span class="token punctuation">.</span>core<span class="token punctuation">.</span>asgi <span class="token keyword">import</span> <span class="token punctuation">(</span></span>
<span class="line">    get_asgi_application<span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line">os<span class="token punctuation">.</span>environ<span class="token punctuation">.</span>setdefault<span class="token punctuation">(</span></span>
<span class="line">    <span class="token string">"DJANGO_SETTINGS_MODULE"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token string">"backend_django.settings"</span><span class="token punctuation">,</span></span>
<span class="line"><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line">django_asgi_app <span class="token operator">=</span> get_asgi_application<span class="token punctuation">(</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"></span>
<span class="line">application <span class="token operator">=</span> ProtocolTypeRouter<span class="token punctuation">(</span><span class="token punctuation">{</span></span>
<span class="line"></span>
<span class="line">    <span class="token string">"http"</span><span class="token punctuation">:</span> django_asgi_app<span class="token punctuation">,</span></span>
<span class="line"></span>
<span class="line">    <span class="token string">"websocket"</span><span class="token punctuation">:</span> URLRouter<span class="token punctuation">(</span></span>
<span class="line">        websocket_urlpatterns</span>
<span class="line">    <span class="token punctuation">)</span><span class="token punctuation">,</span></span>
<span class="line"></span>
<span class="line"><span class="token punctuation">}</span><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h1 id="_17-وظيفة-protocoltyperouter" tabindex="-1"><a class="header-anchor" href="#_17-وظيفة-protocoltyperouter"><span>17. وظيفة ProtocolTypeRouter</span></a></h1>
<p>النظام يفرق بين نوعين من الاتصالات:</p>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">HTTP</span>
<span class="line"> ↓</span>
<span class="line">Django ASGI Application</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><p>و:</p>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">WebSocket</span>
<span class="line"> ↓</span>
<span class="line">URLRouter</span>
<span class="line"> ↓</span>
<span class="line">websocket_urlpatterns</span>
<span class="line"> ↓</span>
<span class="line">DebugConsoleConsumer</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h1 id="_18-frontend-—-livedebugconsole" tabindex="-1"><a class="header-anchor" href="#_18-frontend-—-livedebugconsole"><span>18. Frontend — LiveDebugConsole</span></a></h1>
<p>واجهة Vue مسؤولة عن:</p>
<ul>
<li>إنشاء WebSocket connection.</li>
<li>استقبال Logs.</li>
<li>تخزين Logs.</li>
<li>عرض Logs.</li>
<li>تحديد حالة الاتصال.</li>
<li>مسح Logs.</li>
<li>تصغير Console.</li>
<li>إغلاق الاتصال.</li>
<li>الاحتفاظ بحد أقصى 500 Log.</li>
</ul>
<hr>
<h1 id="_19-إعدادات-frontend" tabindex="-1"><a class="header-anchor" href="#_19-إعدادات-frontend"><span>19. إعدادات Frontend</span></a></h1>
<p>يتم التحكم في تشغيل Debug Console من:</p>
<div class="language-javascript line-numbers-mode" data-highlighter="prismjs" data-ext="js"><pre v-pre><code><span class="line"><span class="token keyword">import</span><span class="token punctuation">.</span>meta<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">VITE_DEBUG_CONSOLE</span><span class="token punctuation">;</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><p>ويتم التحقق من:</p>
<div class="language-javascript line-numbers-mode" data-highlighter="prismjs" data-ext="js"><pre v-pre><code><span class="line"><span class="token keyword">const</span> <span class="token constant">DEBUG_ENABLED</span> <span class="token operator">=</span> <span class="token keyword">import</span><span class="token punctuation">.</span>meta<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">VITE_DEBUG_CONSOLE</span> <span class="token operator">===</span> <span class="token string">"true"</span><span class="token punctuation">;</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><p>عنوان WebSocket:</p>
<div class="language-javascript line-numbers-mode" data-highlighter="prismjs" data-ext="js"><pre v-pre><code><span class="line"><span class="token keyword">const</span> <span class="token constant">WS_URL</span> <span class="token operator">=</span></span>
<span class="line">  <span class="token keyword">import</span><span class="token punctuation">.</span>meta<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">VITE_DEBUG_WS_URL</span> <span class="token operator">||</span> <span class="token string">"ws://127.0.0.1:8000/ws/debug/"</span><span class="token punctuation">;</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div></div></div><p>وبالتالي يمكن تغيير WebSocket URL من Environment Variable.</p>
<hr>
<h1 id="_20-تخزين-logs" tabindex="-1"><a class="header-anchor" href="#_20-تخزين-logs"><span>20. تخزين Logs</span></a></h1>
<p>يتم استخدام:</p>
<div class="language-javascript line-numbers-mode" data-highlighter="prismjs" data-ext="js"><pre v-pre><code><span class="line"><span class="token keyword">const</span> logs <span class="token operator">=</span> <span class="token function">ref</span><span class="token punctuation">(</span><span class="token punctuation">[</span><span class="token punctuation">]</span><span class="token punctuation">)</span><span class="token punctuation">;</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><p>والحد الأقصى:</p>
<div class="language-javascript line-numbers-mode" data-highlighter="prismjs" data-ext="js"><pre v-pre><code><span class="line"><span class="token keyword">const</span> maxLines <span class="token operator">=</span> <span class="token number">500</span><span class="token punctuation">;</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><p>عند تجاوز 500 Log يتم الاحتفاظ بآخر 500 فقط:</p>
<div class="language-javascript line-numbers-mode" data-highlighter="prismjs" data-ext="js"><pre v-pre><code><span class="line"><span class="token keyword">if</span> <span class="token punctuation">(</span>logs<span class="token punctuation">.</span>value<span class="token punctuation">.</span>length <span class="token operator">></span> maxLines<span class="token punctuation">)</span> <span class="token punctuation">{</span></span>
<span class="line">  logs<span class="token punctuation">.</span>value <span class="token operator">=</span> logs<span class="token punctuation">.</span>value<span class="token punctuation">.</span><span class="token function">slice</span><span class="token punctuation">(</span><span class="token operator">-</span>maxLines<span class="token punctuation">)</span><span class="token punctuation">;</span></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h1 id="_21-إضافة-log" tabindex="-1"><a class="header-anchor" href="#_21-إضافة-log"><span>21. إضافة Log</span></a></h1>
<p>الدالة:</p>
<div class="language-javascript line-numbers-mode" data-highlighter="prismjs" data-ext="js"><pre v-pre><code><span class="line"><span class="token keyword">const</span> <span class="token function-variable function">addLog</span> <span class="token operator">=</span> <span class="token punctuation">(</span></span>
<span class="line">  <span class="token parameter">level<span class="token punctuation">,</span></span>
<span class="line">  message<span class="token punctuation">,</span></span>
<span class="line">  logger <span class="token operator">=</span> <span class="token keyword">null</span><span class="token punctuation">,</span></span>
<span class="line">  timestamp <span class="token operator">=</span> <span class="token keyword">null</span><span class="token punctuation">,</span></span></span>
<span class="line"><span class="token punctuation">)</span> <span class="token operator">=></span> <span class="token punctuation">{</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><p>تقوم بإضافة:</p>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">id</span>
<span class="line">level</span>
<span class="line">message</span>
<span class="line">logger</span>
<span class="line">timestamp</span>
<span class="line">time</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><p>إلى Array الخاصة بالـ Logs.</p>
<p>ويتم تحويل Timestamp إلى وقت محلي باستخدام:</p>
<div class="language-javascript line-numbers-mode" data-highlighter="prismjs" data-ext="js"><pre v-pre><code><span class="line"><span class="token keyword">new</span> <span class="token class-name">Date</span><span class="token punctuation">(</span><span class="token operator">...</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">toLocaleTimeString</span><span class="token punctuation">(</span></span>
<span class="line">    <span class="token string">'ar-EG'</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">{</span></span>
<span class="line">        <span class="token literal-property property">hour12</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">}</span></span>
<span class="line"><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h1 id="_22-الاتصال-بـ-websocket" tabindex="-1"><a class="header-anchor" href="#_22-الاتصال-بـ-websocket"><span>22. الاتصال بـ WebSocket</span></a></h1>
<p>يتم الاتصال باستخدام:</p>
<div class="language-javascript line-numbers-mode" data-highlighter="prismjs" data-ext="js"><pre v-pre><code><span class="line">ws<span class="token punctuation">.</span>value <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">WebSocket</span><span class="token punctuation">(</span><span class="token constant">WS_URL</span><span class="token punctuation">)</span><span class="token punctuation">;</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><p>وعند نجاح الاتصال:</p>
<div class="language-javascript line-numbers-mode" data-highlighter="prismjs" data-ext="js"><pre v-pre><code><span class="line">ws<span class="token punctuation">.</span>value<span class="token punctuation">.</span><span class="token function-variable function">onopen</span> <span class="token operator">=</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">=></span> <span class="token punctuation">{</span></span>
<span class="line">  status<span class="token punctuation">.</span>value <span class="token operator">=</span> <span class="token string">"connected"</span><span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line">  <span class="token function">addLog</span><span class="token punctuation">(</span><span class="token string">"success"</span><span class="token punctuation">,</span> <span class="token string">"🔌 Debug Console connected"</span><span class="token punctuation">)</span><span class="token punctuation">;</span></span>
<span class="line"><span class="token punctuation">}</span><span class="token punctuation">;</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h1 id="_23-استقبال-الرسائل" tabindex="-1"><a class="header-anchor" href="#_23-استقبال-الرسائل"><span>23. استقبال الرسائل</span></a></h1>
<p>عند استقبال Message:</p>
<div class="language-javascript line-numbers-mode" data-highlighter="prismjs" data-ext="js"><pre v-pre><code><span class="line">ws<span class="token punctuation">.</span>value<span class="token punctuation">.</span><span class="token function-variable function">onmessage</span> <span class="token operator">=</span></span>
<span class="line">  <span class="token punctuation">(</span><span class="token parameter">event</span><span class="token punctuation">)</span> <span class="token operator">=></span> <span class="token punctuation">{</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div></div></div><p>يتم تحويل البيانات من JSON:</p>
<div class="language-javascript line-numbers-mode" data-highlighter="prismjs" data-ext="js"><pre v-pre><code><span class="line"><span class="token keyword">const</span> data <span class="token operator">=</span> <span class="token constant">JSON</span><span class="token punctuation">.</span><span class="token function">parse</span><span class="token punctuation">(</span>event<span class="token punctuation">.</span>data<span class="token punctuation">)</span><span class="token punctuation">;</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><p>ثم إضافتها إلى Console:</p>
<div class="language-javascript line-numbers-mode" data-highlighter="prismjs" data-ext="js"><pre v-pre><code><span class="line"><span class="token function">addLog</span><span class="token punctuation">(</span></span>
<span class="line">  data<span class="token punctuation">.</span>level <span class="token operator">||</span> <span class="token string">"info"</span><span class="token punctuation">,</span></span>
<span class="line">  data<span class="token punctuation">.</span>message <span class="token operator">||</span> <span class="token string">""</span><span class="token punctuation">,</span></span>
<span class="line">  data<span class="token punctuation">.</span>logger <span class="token operator">||</span> <span class="token keyword">null</span><span class="token punctuation">,</span></span>
<span class="line">  data<span class="token punctuation">.</span>timestamp <span class="token operator">||</span> <span class="token keyword">null</span></span>
<span class="line"><span class="token punctuation">)</span><span class="token punctuation">;</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><p>وفي حالة عدم كون البيانات JSON:</p>
<div class="language-javascript line-numbers-mode" data-highlighter="prismjs" data-ext="js"><pre v-pre><code><span class="line"><span class="token keyword">catch</span> <span class="token punctuation">{</span></span>
<span class="line">    <span class="token function">addLog</span><span class="token punctuation">(</span></span>
<span class="line">        <span class="token string">'info'</span><span class="token punctuation">,</span></span>
<span class="line">        event<span class="token punctuation">.</span>data</span>
<span class="line">    <span class="token punctuation">)</span></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h1 id="_24-حالات-الاتصال" tabindex="-1"><a class="header-anchor" href="#_24-حالات-الاتصال"><span>24. حالات الاتصال</span></a></h1>
<p>النظام يستخدم الحالات:</p>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">connecting</span>
<span class="line">connected</span>
<span class="line">error</span>
<span class="line">closed</span>
<span class="line">disabled</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><p>إذا كان Debug Console غير مفعّل:</p>
<div class="language-javascript line-numbers-mode" data-highlighter="prismjs" data-ext="js"><pre v-pre><code><span class="line"><span class="token keyword">if</span> <span class="token punctuation">(</span><span class="token operator">!</span><span class="token constant">DEBUG_ENABLED</span><span class="token punctuation">)</span> <span class="token punctuation">{</span></span>
<span class="line">  status<span class="token punctuation">.</span>value <span class="token operator">=</span> <span class="token string">"disabled"</span><span class="token punctuation">;</span></span>
<span class="line">  <span class="token keyword">return</span><span class="token punctuation">;</span></span>
<span class="line"><span class="token punctuation">}</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h1 id="_25-websocket-error" tabindex="-1"><a class="header-anchor" href="#_25-websocket-error"><span>25. WebSocket Error</span></a></h1>
<p>عند حدوث خطأ:</p>
<div class="language-javascript line-numbers-mode" data-highlighter="prismjs" data-ext="js"><pre v-pre><code><span class="line">ws<span class="token punctuation">.</span>value<span class="token punctuation">.</span><span class="token function-variable function">onerror</span> <span class="token operator">=</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">=></span> <span class="token punctuation">{</span></span>
<span class="line">  status<span class="token punctuation">.</span>value <span class="token operator">=</span> <span class="token string">"error"</span><span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line">  <span class="token function">addLog</span><span class="token punctuation">(</span><span class="token string">"error"</span><span class="token punctuation">,</span> <span class="token string">"❌ WebSocket connection error"</span><span class="token punctuation">)</span><span class="token punctuation">;</span></span>
<span class="line"><span class="token punctuation">}</span><span class="token punctuation">;</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h1 id="_26-websocket-close" tabindex="-1"><a class="header-anchor" href="#_26-websocket-close"><span>26. WebSocket Close</span></a></h1>
<p>عند إغلاق الاتصال:</p>
<div class="language-javascript line-numbers-mode" data-highlighter="prismjs" data-ext="js"><pre v-pre><code><span class="line">ws<span class="token punctuation">.</span>value<span class="token punctuation">.</span><span class="token function-variable function">onclose</span> <span class="token operator">=</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">=></span> <span class="token punctuation">{</span></span>
<span class="line">  status<span class="token punctuation">.</span>value <span class="token operator">=</span> <span class="token string">"closed"</span><span class="token punctuation">;</span></span>
<span class="line"></span>
<span class="line">  <span class="token function">addLog</span><span class="token punctuation">(</span><span class="token string">"warn"</span><span class="token punctuation">,</span> <span class="token string">"🔌 Debug Console disconnected"</span><span class="token punctuation">)</span><span class="token punctuation">;</span></span>
<span class="line"><span class="token punctuation">}</span><span class="token punctuation">;</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h1 id="_27-إغلاق-console" tabindex="-1"><a class="header-anchor" href="#_27-إغلاق-console"><span>27. إغلاق Console</span></a></h1>
<p>الدالة:</p>
<div class="language-javascript line-numbers-mode" data-highlighter="prismjs" data-ext="js"><pre v-pre><code><span class="line"><span class="token keyword">const</span> <span class="token function-variable function">closeConsole</span> <span class="token operator">=</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">=></span> <span class="token punctuation">{</span></span>
<span class="line">  ws<span class="token punctuation">.</span>value<span class="token operator">?.</span><span class="token function">close</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span></span>
<span class="line"><span class="token punctuation">}</span><span class="token punctuation">;</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h1 id="_28-مسح-logs" tabindex="-1"><a class="header-anchor" href="#_28-مسح-logs"><span>28. مسح Logs</span></a></h1>
<div class="language-javascript line-numbers-mode" data-highlighter="prismjs" data-ext="js"><pre v-pre><code><span class="line"><span class="token keyword">const</span> <span class="token function-variable function">clearLogs</span> <span class="token operator">=</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">=></span> <span class="token punctuation">{</span></span>
<span class="line">  logs<span class="token punctuation">.</span>value <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token punctuation">]</span><span class="token punctuation">;</span></span>
<span class="line"><span class="token punctuation">}</span><span class="token punctuation">;</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h1 id="_29-تصنيف-مستوى-log" tabindex="-1"><a class="header-anchor" href="#_29-تصنيف-مستوى-log"><span>29. تصنيف مستوى Log</span></a></h1>
<p>الدالة:</p>
<div class="language-javascript line-numbers-mode" data-highlighter="prismjs" data-ext="js"><pre v-pre><code><span class="line"><span class="token keyword">const</span> <span class="token function-variable function">levelClass</span> <span class="token operator">=</span> <span class="token punctuation">(</span><span class="token parameter">level</span><span class="token punctuation">)</span> <span class="token operator">=></span> <span class="token punctuation">{</span></span>
<span class="line">  <span class="token keyword">return</span> <span class="token punctuation">(</span></span>
<span class="line">    <span class="token punctuation">{</span></span>
<span class="line">      <span class="token literal-property property">debug</span><span class="token operator">:</span> <span class="token string">"log-debug"</span><span class="token punctuation">,</span></span>
<span class="line">      <span class="token literal-property property">info</span><span class="token operator">:</span> <span class="token string">"log-info"</span><span class="token punctuation">,</span></span>
<span class="line">      <span class="token literal-property property">warn</span><span class="token operator">:</span> <span class="token string">"log-warn"</span><span class="token punctuation">,</span></span>
<span class="line">      <span class="token literal-property property">error</span><span class="token operator">:</span> <span class="token string">"log-error"</span><span class="token punctuation">,</span></span>
<span class="line">      <span class="token literal-property property">success</span><span class="token operator">:</span> <span class="token string">"log-success"</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">}</span><span class="token punctuation">[</span>level<span class="token punctuation">]</span> <span class="token operator">||</span> <span class="token string">"log-info"</span></span>
<span class="line">  <span class="token punctuation">)</span><span class="token punctuation">;</span></span>
<span class="line"><span class="token punctuation">}</span><span class="token punctuation">;</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><p>وتستخدم لتحديد CSS class حسب مستوى الرسالة.</p>
<hr>
<h1 id="_30-lifecycle" tabindex="-1"><a class="header-anchor" href="#_30-lifecycle"><span>30. Lifecycle</span></a></h1>
<p>عند تحميل Component:</p>
<div class="language-javascript line-numbers-mode" data-highlighter="prismjs" data-ext="js"><pre v-pre><code><span class="line"><span class="token function">onMounted</span><span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">=></span> <span class="token punctuation">{</span></span>
<span class="line">  <span class="token function">connect</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span></span>
<span class="line"><span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><p>وعند إزالة Component:</p>
<div class="language-javascript line-numbers-mode" data-highlighter="prismjs" data-ext="js"><pre v-pre><code><span class="line"><span class="token function">onBeforeUnmount</span><span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">=></span> <span class="token punctuation">{</span></span>
<span class="line">  ws<span class="token punctuation">.</span>value<span class="token operator">?.</span><span class="token function">close</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span></span>
<span class="line"><span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><p>وبالتالي يتم فتح WebSocket عند تشغيل الواجهة وإغلاقه عند إزالة Component.</p>
<hr>
<h1 id="_31-واجهة-console" tabindex="-1"><a class="header-anchor" href="#_31-واجهة-console"><span>31. واجهة Console</span></a></h1>
<p>الـ Template يحتوي على:</p>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Live Debug Console</span>
<span class="line">        ↓</span>
<span class="line">Connection Status</span>
<span class="line">        ↓</span>
<span class="line">Clear</span>
<span class="line">Minimize</span>
<span class="line">Close</span>
<span class="line">        ↓</span>
<span class="line">Logs</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><p>العنصر الرئيسي:</p>
<div class="language-html line-numbers-mode" data-highlighter="prismjs" data-ext="html"><pre v-pre><code><span class="line"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>div</span> <span class="token attr-name">v-if</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>DEBUG_ENABLED<span class="token punctuation">"</span></span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>live-debug-console<span class="token punctuation">"</span></span><span class="token punctuation">></span></span><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>div</span><span class="token punctuation">></span></span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><p>وبالتالي لا تظهر الواجهة إذا كان:</p>
<div class="language-javascript line-numbers-mode" data-highlighter="prismjs" data-ext="js"><pre v-pre><code><span class="line"><span class="token constant">DEBUG_ENABLED</span> <span class="token operator">===</span> <span class="token boolean">false</span><span class="token punctuation">;</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><hr>
<h1 id="_32-header" tabindex="-1"><a class="header-anchor" href="#_32-header"><span>32. Header</span></a></h1>
<p>يحتوي Header على:</p>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Terminal Icon</span>
<span class="line">Live Debug Console</span>
<span class="line">Status</span>
<span class="line">Clear</span>
<span class="line">Minimize</span>
<span class="line">Close</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><p>مثال:</p>
<div class="language-html line-numbers-mode" data-highlighter="prismjs" data-ext="html"><pre v-pre><code><span class="line"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>span</span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>console-title<span class="token punctuation">"</span></span><span class="token punctuation">></span></span></span>
<span class="line">  <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>i</span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>pi pi-terminal<span class="token punctuation">"</span></span> <span class="token punctuation">/></span></span></span>
<span class="line">  Live Debug Console</span>
<span class="line"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>span</span><span class="token punctuation">></span></span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h1 id="_33-عرض-logs" tabindex="-1"><a class="header-anchor" href="#_33-عرض-logs"><span>33. عرض Logs</span></a></h1>
<p>يتم عرض كل Log باستخدام:</p>
<div class="language-html line-numbers-mode" data-highlighter="prismjs" data-ext="html"><pre v-pre><code><span class="line"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>div</span> <span class="token attr-name">v-for</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>log in logs<span class="token punctuation">"</span></span> <span class="token attr-name">:key</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>log.id<span class="token punctuation">"</span></span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>log-line<span class="token punctuation">"</span></span><span class="token punctuation">></span></span><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>div</span><span class="token punctuation">></span></span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><p>ويتم عرض:</p>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Time</span>
<span class="line">Level</span>
<span class="line">Logger</span>
<span class="line">Message</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h1 id="_34-empty-state" tabindex="-1"><a class="header-anchor" href="#_34-empty-state"><span>34. Empty State</span></a></h1>
<p>عندما لا توجد Logs:</p>
<div class="language-html line-numbers-mode" data-highlighter="prismjs" data-ext="html"><pre v-pre><code><span class="line"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>div</span> <span class="token attr-name">v-if</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>!logs.length<span class="token punctuation">"</span></span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>console-empty<span class="token punctuation">"</span></span><span class="token punctuation">></span></span>Waiting for Django logs...<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>div</span><span class="token punctuation">></span></span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><hr>
<h1 id="_35-console-ui" tabindex="-1"><a class="header-anchor" href="#_35-console-ui"><span>35. Console UI</span></a></h1>
<p>خصائص الواجهة:</p>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">position: fixed</span>
<span class="line">left: 20px</span>
<span class="line">right: 20px</span>
<span class="line">bottom: 20px</span>
<span class="line">z-index: 99999</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><p>وارتفاع منطقة Logs:</p>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">300px</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><p>مع:</p>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">overflow-y: auto</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><hr>
<h1 id="_36-مستويات-العرض" tabindex="-1"><a class="header-anchor" href="#_36-مستويات-العرض"><span>36. مستويات العرض</span></a></h1>
<p>CSS classes المستخدمة:</p>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">.log-debug</span>
<span class="line">.log-info</span>
<span class="line">.log-warn</span>
<span class="line">.log-error</span>
<span class="line">.log-success</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><p>والغرض منها إعطاء كل مستوى Log مظهرًا مختلفًا داخل Console.</p>
<hr>
<h1 id="_37-تصغير-console" tabindex="-1"><a class="header-anchor" href="#_37-تصغير-console"><span>37. تصغير Console</span></a></h1>
<p>يتم التحكم باستخدام:</p>
<div class="language-javascript line-numbers-mode" data-highlighter="prismjs" data-ext="js"><pre v-pre><code><span class="line"><span class="token keyword">const</span> isMinimized <span class="token operator">=</span> <span class="token function">ref</span><span class="token punctuation">(</span><span class="token boolean">false</span><span class="token punctuation">)</span><span class="token punctuation">;</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><p>والزر:</p>
<div class="language-javascript line-numbers-mode" data-highlighter="prismjs" data-ext="js"><pre v-pre><code><span class="line">isMinimized <span class="token operator">=</span> <span class="token operator">!</span>isMinimized<span class="token punctuation">;</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><p>وعند التصغير يتم إخفاء:</p>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">.console-body</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><hr>
<h1 id="_38-التكامل-الكامل" tabindex="-1"><a class="header-anchor" href="#_38-التكامل-الكامل"><span>38. التكامل الكامل</span></a></h1>
<p>النظام بالكامل يعمل بهذا التسلسل:</p>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">1. Django يقوم بإنشاء Log</span>
<span class="line">          ↓</span>
<span class="line">2. Python Logging</span>
<span class="line">          ↓</span>
<span class="line">3. WebSocketLogHandler</span>
<span class="line">          ↓</span>
<span class="line">4. get_channel_layer()</span>
<span class="line">          ↓</span>
<span class="line">5. group_send()</span>
<span class="line">          ↓</span>
<span class="line">6. debug_console group</span>
<span class="line">          ↓</span>
<span class="line">7. DebugConsoleConsumer</span>
<span class="line">          ↓</span>
<span class="line">8. WebSocket</span>
<span class="line">          ↓</span>
<span class="line">9. Vue LiveDebugConsole</span>
<span class="line">          ↓</span>
<span class="line">10. JSON.parse()</span>
<span class="line">          ↓</span>
<span class="line">11. addLog()</span>
<span class="line">          ↓</span>
<span class="line">12. عرض Log للمطور</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h1 id="_39-environment-variables" tabindex="-1"><a class="header-anchor" href="#_39-environment-variables"><span>39. Environment Variables</span></a></h1>
<p>النظام يعتمد على متغيرين أساسيين للـ Debug Console:</p>
<h3 id="django" tabindex="-1"><a class="header-anchor" href="#django"><span>Django</span></a></h3>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">SO_IAM_OS_DEBUG_CONSOLE</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h3 id="vue" tabindex="-1"><a class="header-anchor" href="#vue"><span>Vue</span></a></h3>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">VITE_DEBUG_CONSOLE</span>
<span class="line">VITE_DEBUG_WS_URL</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div></div></div><p>المبدأ:</p>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Backend</span>
<span class="line">SO_IAM_OS_DEBUG_CONSOLE</span>
<span class="line">        ↓</span>
<span class="line">تشغيل/إيقاف إرسال Logs عبر WebSocket</span>
<span class="line"></span>
<span class="line"></span>
<span class="line">Frontend</span>
<span class="line">VITE_DEBUG_CONSOLE</span>
<span class="line">        ↓</span>
<span class="line">إظهار/إخفاء Live Debug Console</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h1 id="_40-الحالة-الحالية-للمعرفة" tabindex="-1"><a class="header-anchor" href="#_40-الحالة-الحالية-للمعرفة"><span>40. الحالة الحالية للمعرفة</span></a></h1>
<p>تم تعريف المكونات التالية:</p>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">[Django]</span>
<span class="line">├── Channels</span>
<span class="line">├── Channel Layer</span>
<span class="line">├── Consumer</span>
<span class="line">├── Routing</span>
<span class="line">├── Logging Handler</span>
<span class="line">├── LOGGING</span>
<span class="line">└── ASGI</span>
<span class="line"></span>
<span class="line">[Vue]</span>
<span class="line">├── WebSocket</span>
<span class="line">├── Logs State</span>
<span class="line">├── Connection Status</span>
<span class="line">├── Log Renderer</span>
<span class="line">├── Clear</span>
<span class="line">├── Minimize</span>
<span class="line">└── Close</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h1 id="_41-قرارات-المشروع" tabindex="-1"><a class="header-anchor" href="#_41-قرارات-المشروع"><span>41. قرارات المشروع</span></a></h1>
<h2 id="القرار-1" tabindex="-1"><a class="header-anchor" href="#القرار-1"><span>القرار 1</span></a></h2>
<p>استخدام:</p>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Django Channels</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><p>للتعامل مع WebSocket.</p>
<h2 id="القرار-2" tabindex="-1"><a class="header-anchor" href="#القرار-2"><span>القرار 2</span></a></h2>
<p>استخدام:</p>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">WebSocketLogHandler</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><p>لتحويل Django Logs إلى WebSocket.</p>
<h2 id="القرار-3" tabindex="-1"><a class="header-anchor" href="#القرار-3"><span>القرار 3</span></a></h2>
<p>استخدام Group باسم:</p>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">debug_console</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h2 id="القرار-4" tabindex="-1"><a class="header-anchor" href="#القرار-4"><span>القرار 4</span></a></h2>
<p>عنوان WebSocket المحلي:</p>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">ws://127.0.0.1:8000/ws/debug/</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h2 id="القرار-5" tabindex="-1"><a class="header-anchor" href="#القرار-5"><span>القرار 5</span></a></h2>
<p>Vue هو الطرف الذي يعرض Live Debug Console.</p>
<h2 id="القرار-6" tabindex="-1"><a class="header-anchor" href="#القرار-6"><span>القرار 6</span></a></h2>
<p>الحد الأقصى للـ Logs داخل الواجهة:</p>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">500</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h2 id="القرار-7" tabindex="-1"><a class="header-anchor" href="#القرار-7"><span>القرار 7</span></a></h2>
<p>تفعيل Debug Console يتم التحكم فيه من Environment Variables.</p>
<hr>
<h1 id="_42-نقاط-تحتاج-مراجعة-قبل-التنفيذ-النهائي" tabindex="-1"><a class="header-anchor" href="#_42-نقاط-تحتاج-مراجعة-قبل-التنفيذ-النهائي"><span>42. نقاط تحتاج مراجعة قبل التنفيذ النهائي</span></a></h1>
<p>المحتوى الحالي يحتوي على نقطة مسار تحتاج توحيدًا:</p>
<h3 id="الهيكل-المعروض" tabindex="-1"><a class="header-anchor" href="#الهيكل-المعروض"><span>الهيكل المعروض</span></a></h3>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">core/debug/</span>
<span class="line">    consumers.py</span>
<span class="line">    routing.py</span>
<span class="line">    handlers.py</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h3 id="بينما-settings-py-يستخدم" tabindex="-1"><a class="header-anchor" href="#بينما-settings-py-يستخدم"><span>بينما settings.py يستخدم</span></a></h3>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">core<span class="token punctuation">.</span>debug_console<span class="token punctuation">.</span>handlers<span class="token punctuation">.</span>WebSocketLogHandler</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h3 id="وasgi-يستخدم" tabindex="-1"><a class="header-anchor" href="#وasgi-يستخدم"><span>وASGI يستخدم</span></a></h3>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">from</span> core<span class="token punctuation">.</span>debug_console<span class="token punctuation">.</span>routing <span class="token keyword">import</span> websocket_urlpatterns</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><p>لذلك يجب اختيار مسار واحد فعليًا قبل التشغيل.</p>
<hr>
<h1 id="_43-قاعدة-مهمة" tabindex="-1"><a class="header-anchor" href="#_43-قاعدة-مهمة"><span>43. قاعدة مهمة</span></a></h1>
<p>لا يتم تغيير المعمارية الأساسية للنظام لمجرد وجود اختلاف في المسارات.</p>
<p>يجب أولًا تحديد:</p>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">هل المجلد هو:</span>
<span class="line"></span>
<span class="line">core/debug/</span>
<span class="line"></span>
<span class="line">أم:</span>
<span class="line"></span>
<span class="line">core/debug_console/</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><p>ثم جعل:</p>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">consumers.py</span>
<span class="line">routing.py</span>
<span class="line">handlers.py</span>
<span class="line">settings.py</span>
<span class="line">asgi.py</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><p>كلها تستخدم نفس المسار.</p>
<hr>
<h1 id="_44-تعريف-مختصر-للميزة" tabindex="-1"><a class="header-anchor" href="#_44-تعريف-مختصر-للميزة"><span>44. تعريف مختصر للميزة</span></a></h1>
<p><strong>Live Debug Console</strong> في SO_IAM_OS هي طبقة Debug داخلية تقوم بتحويل Django Logs إلى WebSocket Messages ثم عرضها لحظيًا في Vue.</p>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">Django Logs</span>
<span class="line">    ↓</span>
<span class="line">Logging Handler</span>
<span class="line">    ↓</span>
<span class="line">Channels</span>
<span class="line">    ↓</span>
<span class="line">WebSocket</span>
<span class="line">    ↓</span>
<span class="line">Vue</span>
<span class="line">    ↓</span>
<span class="line">Live Debug Console</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><p>هذه الميزة جزء من أدوات التطوير والمراقبة داخل مشروع <strong>SO_IAM_OS</strong> وليست جزءًا من منطق المستخدم الأساسي.</p>
</div></template>


