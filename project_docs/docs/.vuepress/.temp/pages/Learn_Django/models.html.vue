<template><div><h2 id="models-إنشاء-قاعدة-البيانات" tabindex="-1"><a class="header-anchor" href="#models-إنشاء-قاعدة-البيانات"><span>Models =&gt; إنشاء قاعدة البيانات</span></a></h2>
<h2 id="id" tabindex="-1"><a class="header-anchor" href="#id"><span>ID</span></a></h2>
<h3 id="uuidfield-id" tabindex="-1"><a class="header-anchor" href="#uuidfield-id"><span>UUIDField [ id ]</span></a></h3>
<div style="font-size:1.2vw; padding: 2rem 0 0 0; font-weight: 900;">
  📝 UUIDField()
</div>
<div dir="rtl" style="font-size:1.2vw; padding: 1rem 0; font-weight: 900;">
  id مُفتاح أساسي يستخدم كمُعرّف فريد لكل نموذج ويتم إنشاؤه بشكل تلقائي باستخدام
  uuid.uuid4.
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">import</span> uuid</span>
<span class="line"></span>
<span class="line"><span class="token comment"># 🧑 Custom User Form  نموذج المستخدم المخصص</span></span>
<span class="line"><span class="token keyword">class</span> <span class="token class-name">User</span><span class="token punctuation">(</span>AbstractBaseUser<span class="token punctuation">,</span> PermissionsMixin<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">    <span class="token triple-quoted-string string">"""</span>
<span class="line">    # 🆔 معرّف فريد</span>
<span class="line"></span>
<span class="line">    import uuid  # 📦 مكتبة لتوليد UUIDs</span>
<span class="line"></span>
<span class="line">    # 🔑 الحقل هو المفتاح الأساسي للجدول يضمن أن القيم داخل الحقل تكون فريدة وغير مكررة</span>
<span class="line">    primary_key=True,</span>
<span class="line"></span>
<span class="line">    # 🌀 يولد UUID عشوائي تلقائيًا</span>
<span class="line">    default=uuid.uuid4,</span>
<span class="line"></span>
<span class="line">    # 🚫 غير قابل للتعديل</span>
<span class="line">    editable=False,</span>
<span class="line"></span>
<span class="line">    # 📋 الاسم الذي يظهر في لوحة الإدارة</span>
<span class="line">    verbose_name="معرّف فريد 🆔",</span>
<span class="line"></span>
<span class="line">    # 💬 مساعدة لتوضيح الهدف من الحقل</span>
<span class="line">    help_text="معرّف فريد يُستخدم كرقم تسلسلي للعنصر 🎯."</span>
<span class="line"></span>
<span class="line">    """</span></span>
<span class="line"></span>
<span class="line">    <span class="token comment"># ___________________</span></span>
<span class="line">    <span class="token comment"># حقل يتم تعبئة تلقائي</span></span>
<span class="line">    <span class="token comment"># ___________________</span></span>
<span class="line">    <span class="token builtin">id</span> <span class="token operator">=</span> models<span class="token punctuation">.</span>UUIDField<span class="token punctuation">(</span>primary_key<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">,</span> default<span class="token operator">=</span>uuid<span class="token punctuation">.</span>uuid4<span class="token punctuation">,</span> editable<span class="token operator">=</span><span class="token boolean">False</span><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h2 id="text" tabindex="-1"><a class="header-anchor" href="#text"><span>Text</span></a></h2>
<h3 id="charfield-text" tabindex="-1"><a class="header-anchor" href="#charfield-text"><span>CharField [ Text ]</span></a></h3>
<div style="font-size: 2vw; padding: 2rem 0 0 0; font-weight: 900;">
  📝 CharField()
</div>
<div dir="rtl" style="font-size:1.5vw; padding: 0 0 1rem 0; ">
  🌾 حقل النص يُستخدم لتخزين النصوص
<p>[ max_length=255 ]
⚙️ يمكن للخيار تحديد الحد الأقصى لعدد الأحرف في النص بحد أقصى 255 حرفًا</p>
<hr>
<p>📝 [ null=False | null=True ]
أو لا(None) يحدد الحقل ما إذا كان يمكن أن يأخذ قيمة فارغة</p>
<p>📌 False القيمة الافتراضية هي</p>
<p>💭 يعني ذلك أن الحقل لا يمكن أن يكون فارغًا</p>
<p>🌟 True الحقل يمكن أن يكون فارغًا</p>
<p>👍 بمعنى أنه لا يحتوي على أي محتوى</p>
<hr>
<p>📝 [ blank=False | blank=True ]</p>
<p>✔️ يحدد ما إذا كان يمكن ترك الحقل فارغًا عند إنشاء نموذج.</p>
<p>❌ False القيمة الافتراضية هي</p>
<p>💭 True مما يعني أنه يجب توفير قيمة لهذا الحقل</p>
<hr>
<p>[ ... | default=&quot;Name&quot; | default=5 ]</p>
<p>⚙️ يحدد القيمة الافتراضية للحقل عندما لا يتم تقديم قيمة له</p>
<p>⚙️ في هذه الحالة، ليس هناك قيمة افتراضية محددة</p>
<p>📌 في هذه الحالة، القيمة الافتراضية هي &quot;اسم المنتج&quot;</p>
<p>🌟 يمكن أن يكون هناك قيمة افتراضية محددة مثل الارقام</p>
<hr>
<p>[ verbose_name=&quot;Name&quot; ]</p>
<p>🏷️ يحدد الاسم الذي سيظهر في واجهة المستخدم كعنوان للحقل</p>
<p>🤔 يساعد في فهم المستخدم لغرض الحقل</p>
<hr>
<p>[ help_text=&quot;Name&quot; ]</p>
<p>🔍 يوفر نص توضيحي للمستخدمين بجانب الحقل</p>
<p>💡 يساعد في ملء الحقل بشكل صحيح</p>
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># 🧑 Custom User Form  نموذج المستخدم المخصص</span></span>
<span class="line"><span class="token keyword">class</span> <span class="token class-name">User</span><span class="token punctuation">(</span>AbstractBaseUser<span class="token punctuation">,</span> PermissionsMixin<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">    <span class="token comment"># ___________________</span></span>
<span class="line">    <span class="token comment"># حقل يتم تعبئة من المستخدام</span></span>
<span class="line">    <span class="token comment"># ___________________</span></span>
<span class="line">    name <span class="token operator">=</span> models<span class="token punctuation">.</span>CharField<span class="token punctuation">(</span>max_length<span class="token operator">=</span><span class="token number">255</span><span class="token punctuation">)</span></span>
<span class="line">    name <span class="token operator">=</span> models<span class="token punctuation">.</span>CharField<span class="token punctuation">(</span>max_length<span class="token operator">=</span><span class="token number">255</span><span class="token punctuation">,</span> null<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">,</span> blank<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">,</span> default<span class="token operator">=</span><span class="token string">"Name"</span><span class="token punctuation">,</span></span>
<span class="line">        verbose_name<span class="token operator">=</span><span class="token string">"Name"</span><span class="token punctuation">,</span> help_text<span class="token operator">=</span><span class="token string">"Please Enter The Your Name Here"</span><span class="token punctuation">,</span></span>
<span class="line">        choices<span class="token operator">=</span><span class="token punctuation">[</span> <span class="token punctuation">(</span><span class="token string">"available"</span><span class="token punctuation">,</span> <span class="token string">"موجود"</span><span class="token punctuation">)</span><span class="token punctuation">,</span> <span class="token punctuation">(</span><span class="token string">"sold_out"</span><span class="token punctuation">,</span> <span class="token string">"خلص"</span><span class="token punctuation">)</span><span class="token punctuation">,</span> <span class="token punctuation">(</span><span class="token string">"reserved"</span><span class="token punctuation">,</span> <span class="token string">"محجوز"</span><span class="token punctuation">)</span><span class="token punctuation">,</span><span class="token punctuation">]</span><span class="token punctuation">,</span><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h3 id="textfield-text" tabindex="-1"><a class="header-anchor" href="#textfield-text"><span>TextField [ Text ]</span></a></h3>
<div style="font-size:1.5vw; padding: 2rem 0 0 0; font-weight: 900;">
  📝 TextField()
</div>
<div dir="rtl" style="font-size:1.5vw; padding: 0 0 1rem 0; ">
<p>🌾 حقل النص يُستخدم لتخزين النصوص الطويله</p>
<hr>
<p>[ max_length=255 ]</p>
<p>⚙️ يمكن للخيار تحديد الحد الأقصى لعدد الأحرف في النص بحد أقصى 255 حرفًا</p>
<hr>
<p>📝 [ null=False | null=True ]</p>
<p>أو لا(None) يحدد الحقل ما إذا كان يمكن أن يأخذ قيمة فارغة</p>
<p>📌 False القيمة الافتراضية هي</p>
<p>💭 يعني ذلك أن الحقل لا يمكن أن يكون فارغًا</p>
<p>🌟 True الحقل يمكن أن يكون فارغًا</p>
<p>👍 بمعنى أنه لا يحتوي على أي محتوى</p>
<hr>
<p>📝 [ blank=False | blank=True ]
<br>
✔️ يحدد ما إذا كان يمكن ترك الحقل فارغًا عند إنشاء نموذج.</p>
<p>❌ False القيمة الافتراضية هي</p>
<p>💭 True مما يعني أنه يجب توفير قيمة لهذا الحقل</p>
<hr>
<p>[ ... | default=&quot;Name&quot; | default=5 ]</p>
<p>⚙️ يحدد القيمة الافتراضية للحقل عندما لا يتم تقديم قيمة له</p>
<p>⚙️ في هذه الحالة، ليس هناك قيمة افتراضية محددة</p>
<p>📌 في هذه الحالة، القيمة الافتراضية هي &quot;اسم المنتج&quot;</p>
<p>🌟 يمكن أن يكون هناك قيمة افتراضية محددة مثل الارقام</p>
<hr>
<p>[ verbose_name=&quot;Name&quot; ]</p>
<p>🏷️ يحدد الاسم الذي سيظهر في واجهة المستخدم كعنوان للحقل</p>
<p>🤔 يساعد في فهم المستخدم لغرض الحقل</p>
<hr>
<p>[ help_text=&quot;Name&quot; ]</p>
<p>🔍 يوفر نص توضيحي للمستخدمين بجانب الحقل</p>
<p>💡 يساعد في ملء الحقل بشكل صحيح</p>
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token comment"># 🧑 Custom User Form  نموذج المستخدم المخصص</span></span>
<span class="line"><span class="token keyword">class</span> <span class="token class-name">User</span><span class="token punctuation">(</span>AbstractBaseUser<span class="token punctuation">,</span> PermissionsMixin<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">    <span class="token comment"># ___________________</span></span>
<span class="line">    <span class="token comment"># حقل يتم تعبئة من المستخدام</span></span>
<span class="line">    <span class="token comment"># ___________________</span></span>
<span class="line">    long_description <span class="token operator">=</span> models<span class="token punctuation">.</span>TextField<span class="token punctuation">(</span>null<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">,</span> blank<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span></span>
<span class="line">    long_description <span class="token operator">=</span> models<span class="token punctuation">.</span>TextField<span class="token punctuation">(</span>max_length<span class="token operator">=</span><span class="token number">255</span><span class="token punctuation">,</span> null<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">,</span> blank<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">,</span> default<span class="token operator">=</span><span class="token string">"Name"</span><span class="token punctuation">,</span></span>
<span class="line">        verbose_name<span class="token operator">=</span><span class="token string">"Name"</span><span class="token punctuation">,</span> help_text<span class="token operator">=</span><span class="token string">"Please Enter The Your Name Here"</span><span class="token punctuation">,</span></span>
<span class="line">        choices<span class="token operator">=</span><span class="token punctuation">[</span> <span class="token punctuation">(</span><span class="token string">"available"</span><span class="token punctuation">,</span> <span class="token string">"موجود"</span><span class="token punctuation">)</span><span class="token punctuation">,</span> <span class="token punctuation">(</span><span class="token string">"sold_out"</span><span class="token punctuation">,</span> <span class="token string">"خلص"</span><span class="token punctuation">)</span><span class="token punctuation">,</span> <span class="token punctuation">(</span><span class="token string">"reserved"</span><span class="token punctuation">,</span> <span class="token string">"محجوز"</span><span class="token punctuation">)</span><span class="token punctuation">,</span><span class="token punctuation">]</span><span class="token punctuation">,</span><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h3 id="slugfield" tabindex="-1"><a class="header-anchor" href="#slugfield"><span>SlugField</span></a></h3>
<div class="" dir="rtl">
  حقل لتخزين عناوين ال Url 
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">class Product(models.Model)</span>
<span class="line">    slug = models.SlugField(max_length=255, unique=True)</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div></div></div><div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">from</span> django<span class="token punctuation">.</span>utils<span class="token punctuation">.</span>text <span class="token keyword">import</span> slugify</span>
<span class="line"></span>
<span class="line"><span class="token keyword">class</span> <span class="token class-name">Product</span><span class="token punctuation">(</span>models<span class="token punctuation">.</span>Model<span class="token punctuation">)</span></span>
<span class="line">    name <span class="token operator">=</span> models<span class="token punctuation">.</span>CharField<span class="token punctuation">(</span>max_length<span class="token operator">=</span><span class="token number">255</span><span class="token punctuation">,</span> blank<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">,</span> null<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">,</span> default<span class="token operator">=</span><span class="token string">""</span><span class="token punctuation">)</span></span>
<span class="line">    slug <span class="token operator">=</span> models<span class="token punctuation">.</span>SlugField<span class="token punctuation">(</span>max_length<span class="token operator">=</span><span class="token number">255</span><span class="token punctuation">,</span> editable<span class="token operator">=</span><span class="token boolean">False</span><span class="token punctuation">,</span> unique<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">    <span class="token keyword">def</span> <span class="token function">save</span><span class="token punctuation">(</span>self<span class="token punctuation">,</span> <span class="token operator">*</span>args<span class="token punctuation">,</span> <span class="token operator">**</span>kwargs<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">        <span class="token keyword">if</span> <span class="token keyword">not</span> self<span class="token punctuation">.</span>slug<span class="token punctuation">:</span></span>
<span class="line">            base_slug <span class="token operator">=</span> slugify<span class="token punctuation">(</span>self<span class="token punctuation">.</span>name<span class="token punctuation">)</span></span>
<span class="line">            slug <span class="token operator">=</span> base_slug</span>
<span class="line">            counter <span class="token operator">=</span> <span class="token number">1</span></span>
<span class="line">            <span class="token keyword">while</span> Product<span class="token punctuation">.</span>objects<span class="token punctuation">.</span><span class="token builtin">filter</span><span class="token punctuation">(</span>slug<span class="token operator">=</span>slug<span class="token punctuation">)</span><span class="token punctuation">.</span>exists<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">                slug <span class="token operator">=</span> <span class="token string-interpolation"><span class="token string">f"</span><span class="token interpolation"><span class="token punctuation">{</span>base_slug<span class="token punctuation">}</span></span><span class="token string">-</span><span class="token interpolation"><span class="token punctuation">{</span>counter<span class="token punctuation">}</span></span><span class="token string">"</span></span></span>
<span class="line">                counter <span class="token operator">+=</span> <span class="token number">1</span></span>
<span class="line">            self<span class="token punctuation">.</span>slug <span class="token operator">=</span> slug</span>
<span class="line">        <span class="token builtin">super</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span>save<span class="token punctuation">(</span><span class="token operator">*</span>args<span class="token punctuation">,</span> <span class="token operator">**</span>kwargs<span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><hr>
<h2 id="email" tabindex="-1"><a class="header-anchor" href="#email"><span>Email</span></a></h2>
<h3 id="emailfield-email" tabindex="-1"><a class="header-anchor" href="#emailfield-email"><span>EmailField [ Email ]</span></a></h3>
<div class="" dir="rtl">
  حقل لتخذين الريد و التحقق من صحتة 
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">email <span class="token operator">=</span> models<span class="token punctuation">.</span>EmailField<span class="token punctuation">(</span>unique<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><hr>
<h2 id="url" tabindex="-1"><a class="header-anchor" href="#url"><span>Url</span></a></h2>
<h3 id="urlfield-url" tabindex="-1"><a class="header-anchor" href="#urlfield-url"><span>UrlField [ Url ]</span></a></h3>
<div class="" dir="rtl">
  حقل لتخذين  و التحقق من صحتة ال Url
<p>يستخدم لتخزين روابط المواقع</p>
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">website <span class="token operator">=</span> models<span class="token punctuation">.</span>URLField<span class="token punctuation">(</span>max_length<span class="token operator">=</span><span class="token number">255</span><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><hr>
<h2 id="number" tabindex="-1"><a class="header-anchor" href="#number"><span>Number</span></a></h2>
<h3 id="integerfield" tabindex="-1"><a class="header-anchor" href="#integerfield"><span>IntegerField</span></a></h3>
<div class="" dir="rtl">
  حقل تخزين الاعداد الصحيحة فقط
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">price <span class="token operator">=</span> models<span class="token punctuation">.</span>IntegerField<span class="token punctuation">(</span>default<span class="token operator">=</span><span class="token number">0</span><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h3 id="floatfield" tabindex="-1"><a class="header-anchor" href="#floatfield"><span>FloatField</span></a></h3>
<div class="" dir="rtl">
  حقل تخزين الاعداد العشرية 
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">price <span class="token operator">=</span> models<span class="token punctuation">.</span>FloatField<span class="token punctuation">(</span>default<span class="token operator">=</span><span class="token number">0.0</span><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h3 id="decimalfield" tabindex="-1"><a class="header-anchor" href="#decimalfield"><span>DecimalField</span></a></h3>
<div class="" dir="rtl">
  حقل تخزين الاعداد العشرية دقة عالية
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">price <span class="token operator">=</span> models<span class="token punctuation">.</span>DecimalField<span class="token punctuation">(</span>max_digits<span class="token operator">=</span><span class="token number">10</span><span class="token punctuation">,</span> decimal_places<span class="token operator">=</span><span class="token number">2</span><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><hr>
<h2 id="image" tabindex="-1"><a class="header-anchor" href="#image"><span>Image</span></a></h2>
<h3 id="imagefield-image" tabindex="-1"><a class="header-anchor" href="#imagefield-image"><span>ImageField [ Image ]</span></a></h3>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">class</span> <span class="token class-name">User</span><span class="token punctuation">(</span>models<span class="token punctuation">.</span>Model<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">    <span class="token triple-quoted-string string">"""</span>
<span class="line">    # 🖼️ حقل لتحميل صورة</span>
<span class="line"></span>
<span class="line">    # 📁 تحديد مكان حفظ الصور داخل MEDIA_ROOT</span>
<span class="line">    upload_to="avatars",</span>
<span class="line"></span>
<span class="line">    # 🚫 الحقل اختياري في النماذج</span>
<span class="line">    blank=True,</span>
<span class="line"></span>
<span class="line">    # 🚫 الحقل يمكن أن يكون فارغًا في قاعدة البيانات</span>
<span class="line">    null=True,</span>
<span class="line"></span>
<span class="line">    # 📋 الاسم الودي للحقل في لوحة الإدارة</span>
<span class="line">    verbose_name="صورة الملف الشخصي 🖼️",</span>
<span class="line"></span>
<span class="line">    # 💬 نص المساعدة لشرح الحقل</span>
<span class="line">    help_text="اختر صورة لملفك الشخصي 🎨.",</span>
<span class="line">    """</span></span>
<span class="line">    <span class="token comment"># ___________________</span></span>
<span class="line">    <span class="token comment"># حقل يتم تعبئة من المستخدام</span></span>
<span class="line">    <span class="token comment"># ___________________</span></span>
<span class="line">    image <span class="token operator">=</span> models<span class="token punctuation">.</span>ImageField<span class="token punctuation">(</span></span>
<span class="line">        upload_to<span class="token operator">=</span><span class="token string">"avatars"</span><span class="token punctuation">,</span></span>
<span class="line">        blank<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">,</span></span>
<span class="line">        null<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">,</span></span>
<span class="line">    <span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h2 id="date-time" tabindex="-1"><a class="header-anchor" href="#date-time"><span>Date Time</span></a></h2>
<h3 id="timefield" tabindex="-1"><a class="header-anchor" href="#timefield"><span>TimeField</span></a></h3>
<div class="" dir="rtl">
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">created_at <span class="token operator">=</span> models<span class="token punctuation">.</span>TimeField<span class="token punctuation">(</span>auto_now_add<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span></span>
<span class="line">updated_at <span class="token operator">=</span> models<span class="token punctuation">.</span>TimeField<span class="token punctuation">(</span>auto_now<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div></div></div><h3 id="datefield" tabindex="-1"><a class="header-anchor" href="#datefield"><span>DateField</span></a></h3>
<div class="" dir="rtl">
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">created_at <span class="token operator">=</span> models<span class="token punctuation">.</span>DateField<span class="token punctuation">(</span>auto_now_add<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span></span>
<span class="line">updated_at <span class="token operator">=</span> models<span class="token punctuation">.</span>DateField<span class="token punctuation">(</span>auto_now<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div></div></div><h3 id="datetimefield" tabindex="-1"><a class="header-anchor" href="#datetimefield"><span>DateTimeField</span></a></h3>
<div class="" dir="rtl">
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">created_at <span class="token operator">=</span> models<span class="token punctuation">.</span>DateTimeField<span class="token punctuation">(</span>auto_now_add<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span></span>
<span class="line">updated_at <span class="token operator">=</span> models<span class="token punctuation">.</span>DateTimeField<span class="token punctuation">(</span>auto_now<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div></div></div><h2 id="boolean" tabindex="-1"><a class="header-anchor" href="#boolean"><span>Boolean</span></a></h2>
<h3 id="booleanfield" tabindex="-1"><a class="header-anchor" href="#booleanfield"><span>BooleanField</span></a></h3>
<div class="" dir="rtl">
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">is_available <span class="token operator">=</span> models<span class="token punctuation">.</span>BooleanField<span class="token punctuation">(</span>default<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h2 id="file-📂" tabindex="-1"><a class="header-anchor" href="#file-📂"><span>File [📂]</span></a></h2>
<h3 id="filefield" tabindex="-1"><a class="header-anchor" href="#filefield"><span>FileField</span></a></h3>
<div class="" dir="rtl">
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token builtin">file</span> <span class="token operator">=</span> models<span class="token punctuation">.</span>FileField<span class="token punctuation">(</span>upload_to<span class="token operator">=</span><span class="token string">'backgrounds/'</span><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h2 id="relationship" tabindex="-1"><a class="header-anchor" href="#relationship"><span>Relationship</span></a></h2>
<h3 id="foreignkey" tabindex="-1"><a class="header-anchor" href="#foreignkey"><span>ForeignKey</span></a></h3>
<div class="" dir="rtl">
  علاقة الكثير لى واحد
<p>استخدمة فى علاقة مستخدم لية العديد من المقالات</p>
</div>
<div class="language-text line-numbers-mode" data-highlighter="prismjs" data-ext="text"><pre v-pre><code><span class="line">category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)</span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h3 id="onetoonefield" tabindex="-1"><a class="header-anchor" href="#onetoonefield"><span>OneToOneField</span></a></h3>
<div class="" dir="rtl">
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">created_by <span class="token operator">=</span> models<span class="token punctuation">.</span>OneToOneField<span class="token punctuation">(</span> User<span class="token punctuation">,</span> related_name<span class="token operator">=</span><span class="token string">'vendor'</span><span class="token punctuation">,</span> on_delete<span class="token operator">=</span>models<span class="token punctuation">.</span>CASCADE<span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><h3 id="manytomanyfield" tabindex="-1"><a class="header-anchor" href="#manytomanyfield"><span>ManyToManyField</span></a></h3>
<div class="" dir="rtl">
</div>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line">vendor <span class="token operator">=</span> models<span class="token punctuation">.</span>ManyToManyField<span class="token punctuation">(</span>Vendor<span class="token punctuation">,</span>  blank<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">,</span> null<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">,</span> <span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div></div></div><hr>
<h2 id="setting-view" tabindex="-1"><a class="header-anchor" href="#setting-view"><span>Setting &amp; View</span></a></h2>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">class</span> <span class="token class-name">Product</span><span class="token punctuation">(</span>models<span class="token punctuation">.</span>Model<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">    <span class="token comment"># ___________________</span></span>
<span class="line">    <span class="token comment"># اعدادات خاصة بى الترتيب و الظهور</span></span>
<span class="line">    <span class="token comment"># ___________________</span></span>
<span class="line">    <span class="token keyword">class</span> <span class="token class-name">Meta</span><span class="token punctuation">:</span></span>
<span class="line">        verbose_name <span class="token operator">=</span> <span class="token string">"Product"</span></span>
<span class="line">        verbose_name_plural <span class="token operator">=</span> <span class="token string">"Products"</span></span>
<span class="line">        ordering <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token string">'-created_at'</span><span class="token punctuation">]</span></span>
<span class="line"></span>
<span class="line">    <span class="token keyword">def</span> <span class="token function">created_at_formatted</span><span class="token punctuation">(</span>self<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">        <span class="token keyword">return</span> timesince<span class="token punctuation">(</span>self<span class="token punctuation">.</span>created_at<span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">    <span class="token keyword">def</span> <span class="token function">__str__</span><span class="token punctuation">(</span>self<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">        <span class="token keyword">return</span> <span class="token string">'%s'</span> <span class="token operator">%</span> self<span class="token punctuation">.</span>name</span>
<span class="line"></span>
<span class="line">    <span class="token keyword">def</span> <span class="token function">__str__</span><span class="token punctuation">(</span>self<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">        <span class="token keyword">return</span> <span class="token string-interpolation"><span class="token string">f"</span><span class="token interpolation"><span class="token punctuation">{</span>self<span class="token punctuation">.</span>name<span class="token punctuation">}</span></span><span class="token string"> - </span><span class="token interpolation"><span class="token punctuation">{</span><span class="token string">'yes'</span> <span class="token keyword">if</span> self<span class="token punctuation">.</span>is_available <span class="token keyword">else</span> <span class="token string">'no'</span><span class="token punctuation">}</span></span><span class="token string">"</span></span></span>
<span class="line"></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h2 id="all" tabindex="-1"><a class="header-anchor" href="#all"><span>All</span></a></h2>
<h3 id="user" tabindex="-1"><a class="header-anchor" href="#user"><span>User</span></a></h3>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">class</span> <span class="token class-name">User</span><span class="token punctuation">(</span>models<span class="token punctuation">.</span>Model<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">    <span class="token comment"># ___________________</span></span>
<span class="line">    <span class="token comment"># حقل يتم تعبئة تلقائي</span></span>
<span class="line">    <span class="token comment"># ___________________</span></span>
<span class="line">    <span class="token builtin">id</span> <span class="token operator">=</span> models<span class="token punctuation">.</span>UUIDField<span class="token punctuation">(</span>primary_key<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">,</span> default<span class="token operator">=</span>uuid<span class="token punctuation">.</span>uuid4<span class="token punctuation">,</span> editable<span class="token operator">=</span><span class="token boolean">False</span><span class="token punctuation">)</span></span>
<span class="line">    created_at <span class="token operator">=</span> models<span class="token punctuation">.</span>DateTimeField<span class="token punctuation">(</span>auto_now_add<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span></span>
<span class="line">    updated_at <span class="token operator">=</span> models<span class="token punctuation">.</span>DateTimeField<span class="token punctuation">(</span>auto_now<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span></span>
<span class="line">    created_by <span class="token operator">=</span> models<span class="token punctuation">.</span>ForeignKey<span class="token punctuation">(</span></span>
<span class="line">        User<span class="token punctuation">,</span> related_name<span class="token operator">=</span><span class="token string">"word"</span><span class="token punctuation">,</span> on_delete<span class="token operator">=</span>models<span class="token punctuation">.</span>CASCADE</span>
<span class="line">    <span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">    <span class="token comment"># ___________________</span></span>
<span class="line">    <span class="token comment"># حقل يتم تعبئة من المستخدام</span></span>
<span class="line">    <span class="token comment"># ___________________</span></span>
<span class="line">    name <span class="token operator">=</span> models<span class="token punctuation">.</span>CharField<span class="token punctuation">(</span>max_length<span class="token operator">=</span><span class="token number">255</span><span class="token punctuation">)</span></span>
<span class="line">    long_description <span class="token operator">=</span> models<span class="token punctuation">.</span>TextField<span class="token punctuation">(</span>null<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">,</span> blank<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div><h3 id="product" tabindex="-1"><a class="header-anchor" href="#product"><span>Product</span></a></h3>
<div class="language-python line-numbers-mode" data-highlighter="prismjs" data-ext="py"><pre v-pre><code><span class="line"><span class="token keyword">from</span> django<span class="token punctuation">.</span>db <span class="token keyword">import</span> models</span>
<span class="line"><span class="token keyword">import</span> uuid</span>
<span class="line"><span class="token keyword">from</span> django<span class="token punctuation">.</span>utils<span class="token punctuation">.</span>timesince <span class="token keyword">import</span> timesince</span>
<span class="line"><span class="token keyword">from</span> users_accounts<span class="token punctuation">.</span>models <span class="token keyword">import</span> User</span>
<span class="line"></span>
<span class="line"><span class="token keyword">class</span> <span class="token class-name">Product</span><span class="token punctuation">(</span>models<span class="token punctuation">.</span>Model<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">    <span class="token comment"># ___________________</span></span>
<span class="line">    <span class="token comment"># حقل يتم تعبئة تلقائي</span></span>
<span class="line">    <span class="token comment"># ___________________</span></span>
<span class="line">    <span class="token builtin">id</span> <span class="token operator">=</span> models<span class="token punctuation">.</span>UUIDField<span class="token punctuation">(</span>primary_key<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">,</span> default<span class="token operator">=</span>uuid<span class="token punctuation">.</span>uuid4<span class="token punctuation">,</span> editable<span class="token operator">=</span><span class="token boolean">False</span><span class="token punctuation">)</span></span>
<span class="line">    created_at <span class="token operator">=</span> models<span class="token punctuation">.</span>DateTimeField<span class="token punctuation">(</span>auto_now_add<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span></span>
<span class="line">    updated_at <span class="token operator">=</span> models<span class="token punctuation">.</span>DateTimeField<span class="token punctuation">(</span>auto_now<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span></span>
<span class="line">    created_by <span class="token operator">=</span> models<span class="token punctuation">.</span>ForeignKey<span class="token punctuation">(</span></span>
<span class="line">        User<span class="token punctuation">,</span> related_name<span class="token operator">=</span><span class="token string">"product"</span><span class="token punctuation">,</span> on_delete<span class="token operator">=</span>models<span class="token punctuation">.</span>CASCADE</span>
<span class="line">    <span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">    <span class="token comment"># ___________________</span></span>
<span class="line">    <span class="token comment"># حقل يتم تعبئة من المستخدام</span></span>
<span class="line">    <span class="token comment"># ___________________</span></span>
<span class="line">    name <span class="token operator">=</span> models<span class="token punctuation">.</span>CharField<span class="token punctuation">(</span>max_length<span class="token operator">=</span><span class="token number">255</span><span class="token punctuation">,</span> blank<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">,</span> null<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">,</span> default<span class="token operator">=</span><span class="token string">""</span><span class="token punctuation">)</span></span>
<span class="line">    description <span class="token operator">=</span> models<span class="token punctuation">.</span>TextField<span class="token punctuation">(</span>blank<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">,</span> null<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">,</span> default<span class="token operator">=</span><span class="token string">""</span><span class="token punctuation">)</span></span>
<span class="line">    price <span class="token operator">=</span> models<span class="token punctuation">.</span>FloatField<span class="token punctuation">(</span>default<span class="token operator">=</span><span class="token number">0</span><span class="token punctuation">)</span></span>
<span class="line">    is_available <span class="token operator">=</span> models<span class="token punctuation">.</span>BooleanField<span class="token punctuation">(</span>default<span class="token operator">=</span><span class="token boolean">True</span><span class="token punctuation">)</span></span>
<span class="line"></span>
<span class="line">    <span class="token comment"># ___________________</span></span>
<span class="line">    <span class="token comment"># اعدادات خاصة بى الترتيب و الظهور</span></span>
<span class="line">    <span class="token comment"># ___________________</span></span>
<span class="line">    <span class="token keyword">class</span> <span class="token class-name">Meta</span><span class="token punctuation">:</span></span>
<span class="line">        verbose_name <span class="token operator">=</span> <span class="token string">"Product"</span></span>
<span class="line">        verbose_name_plural <span class="token operator">=</span> <span class="token string">"Products"</span></span>
<span class="line">        ordering <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token string">'-created_at'</span><span class="token punctuation">]</span></span>
<span class="line">    <span class="token keyword">def</span> <span class="token function">created_at_formatted</span><span class="token punctuation">(</span>self<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">        <span class="token keyword">return</span> timesince<span class="token punctuation">(</span>self<span class="token punctuation">.</span>created_at<span class="token punctuation">)</span></span>
<span class="line">    <span class="token keyword">def</span> <span class="token function">updated_at_formatted</span><span class="token punctuation">(</span>self<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">        <span class="token keyword">return</span> timesince<span class="token punctuation">(</span>self<span class="token punctuation">.</span>updated_at<span class="token punctuation">)</span></span>
<span class="line">    <span class="token keyword">def</span> <span class="token function">__str__</span><span class="token punctuation">(</span>self<span class="token punctuation">)</span><span class="token punctuation">:</span></span>
<span class="line">        <span class="token comment"># return '%s' % self.name</span></span>
<span class="line">        <span class="token keyword">return</span> <span class="token string-interpolation"><span class="token string">f"</span><span class="token interpolation"><span class="token punctuation">{</span>self<span class="token punctuation">.</span>name<span class="token punctuation">}</span></span><span class="token string"> - </span><span class="token interpolation"><span class="token punctuation">{</span><span class="token string">'yes'</span> <span class="token keyword">if</span> self<span class="token punctuation">.</span>is_available <span class="token keyword">else</span> <span class="token string">'no'</span><span class="token punctuation">}</span></span><span class="token string">"</span></span></span>
<span class="line"></span></code></pre>
<div class="line-numbers" aria-hidden="true" style="counter-reset:line-number 0"><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div><div class="line-number"></div></div></div></div></template>


