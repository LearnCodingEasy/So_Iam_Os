محتاج الى

"knowledge"

---

---

---

---

---

---

---

---

---

"goals",

---

---

---

---

---

---

---

---

---

"tasks",

---

---

---

---

---

---

---

---

---

"learning",

---

---

---

---

---

---

---

---

---

"jobs_opportunity",

---

---

---

---

---

---

---

---

---

# scraper

---

---

---

---

---

---

---

---

---

# Codex

---

---

---

---

---

---

---

---

---


كل الاتى هو تطوير تطبيق ال 

# AI

____________________________________
____________________________________
____________________________________
____________________________________


محتاج استخدام الاضافات الاتية فى [claude ]
taste skill
web design guidelines
awesome design
image to code 
plawrighte cli
superpowers
karpathy skills
claude-Mem
caveman


1. تطبيق agents (الوكلاء الذكيون)المميزات العشر المقترحة في الباك إند (backend_django/agents/)تنفيذ غير متزامن عبر Celery (POST /api/agents/runs/{id}/execute-async/): نقل execute_run إلى مهمة خلفية مع إرجاع task_id فوراً لتجنب انقطاع الاتصال (Timeout) في المهام الطويلة.حلقات التفكير واستدعاء الأدوات (ReAct / Multi-step Loop): تحديث execution_service.py لتنفيذ خطوات متتالية حتى max_steps وتحديث AgentExecution لكل خطوة (step_index).إيقاف مؤقت واستئناف التشغيل (POST /api/agents/runs/{id}/pause/ و resume/): إضافة حالتي paused وwaiting_input في AgentRun.STATUS_CHOICES.إعادة محاولة الخطوة الفاشلة (POST /api/agents/runs/{id}/retry-step/): إعادة تشغيل آخر AgentExecution فاشل دون إعادة التشغيل من البداية.الذاكرة طويلة وقصيرة المدى (AgentMemory Model + /api/agents/agents/{id}/memory/): تخزين الحقائق والملخصات المستخلصة من التشغيلات السابقة وحقنها في _build_messages.تفويض المهام بين الوكلاء (AgentHandoff / Sub-agent Delegation): السماح لوكيل باستدعاء وكيل فرعي آخر وتسجيل parent_run في AgentRun.إسناد الأدوات من المختبر (POST /api/agents/configurations/{id}/bind-tools/): التحقق من وجود الأدوات في ai_tools_laboratory وربط إعداداتها بالوكيل.بث حي لخطوات التنفيذ (GET /api/agents/runs/{id}/stream/ - SSE): بث كل AgentExecution لحظة حدوثه للفرانت إند.تقييم جودة المخرجات (POST /api/agents/runs/{id}/evaluate/): تقييم آلي (LLM-as-a-Judge) أو بشري بنتيجة (1-5) وملاحظات تحسين.استنساخ وتصدير الوكيل (POST /api/agents/agents/{id}/clone/ و export/): نسخ الوكيل مع نسخته النشطة (AgentConfiguration) بصيغة JSON.الاستدعاء والتحسينات في الفرانت إند (Agents.js + agentsStore.js + agentsView.vue)دوال الاستدعاء (Agents.js): إضافة executeRunAsync(id), pauseRun(id), resumeRun(id), retryStep(id), streamRun(id, onEvent), evaluateRun(id, payload), cloneAgent(id), getAgentMemory(id).تحديثات agentsStore.js: إضافة حالة activeStream وagentMemory وrunMetrics مع تحديث تفاعلي لـ executions أثناء البث الحي.عناصر التحكم وسير العمل والاختبار (agentsView.vue):لوحة تتبع حية (Live Execution Timeline): استبدال الجدول الثابت بـ PrimeVue Timeline يعرض كل خطوة (step_index)، المدخلات، المخرجات، والزمن duration_ms لحظياً.أزرار تحكم دورة الحياة: شريط تحكم مباشر لكل تشغيل (Approve / Execute Async / Pause / Resume / Retry Failed Step / Cancel).صندوق اختبار الوكيل (Agent Sandbox Drawer): لوحة جانبية لاختبار الوكيل بمُدخلات تجريبية ومقارنة مخرجات نسختين مختلفتين (v1 مقابل v2) جنبًا إلى جنب.2. تطبيق ai (المنصة المركزية للذكاء الاصطناعي)المميزات العشر المقترحة في الباك إند (backend_django/ai/)محرك تنفيذ فعلي لسير العمل (POST /api/ai/workflows/{id}/execute/): بناء WorkflowExecutor ينفذ عُقد الـ DAG بترتيب طوبولوجي (Topological Sort) ويحفظ النتائج في AIWorkflowRun.التوجيه الذكي حسب التكلفة وزمن الاستجابة (Smart Routing Policy): توسيع AIFallbackChainService للاختيار التلقائي بين المزودين بناءً على task_type (سريع/رخيص مقابل عميق).التخزين المؤقت الدلالي (Semantic / Exact Response Cache): تخزين الردود المتكررة في AICacheEntry لتقليل استهلاك التوكنز وزمن الاستجابة.حارس الأمان وفحص المحتوى (POST /api/ai/guardrails/inspect/): توسيع ai/services/security.py لاكتشاف Prompt Injection وإخفاء البيانات الحساسة (PII Masking) قبل الإرسال للمزود.محاكي الميزانية والتنبؤ بالاستهلاك (GET /api/ai/budgets/forecast/): حساب معدل الحرق اليومي وتوقع تاريخ نفاد الميزانية في AIBudgetPolicy.توجيه التقييمات للتحسين التلقائي (POST /api/ai/feedback/{id}/promote-to-prompt/): تحويل التقييمات الإيجابية/السلبية (AIFeedback) إلى أمثلة Few-Shot داخل AIPromptProfile.إعادة تشغيل تنفيذ فاشل (POST /api/ai/executions/{id}/replay/): إعادة إرسال نفس الحمولة بمزود أو نموذج بديل للمقارنة.نقطة تجميع مجمعة للتشخيص (GET /api/ai/diagnostics/bundle/): تجميع حالة المزودين، الأخطاء الأخيرة، زمن الاستجابة (P95)، وحالة الطوابير في طلب واحد.اختبار مقارنة النماذج (POST /api/ai/playground/compare/): إرسال نفس الـ Prompt إلى 2-3 مزودين بالتوازي وإرجاع الردود والتكلفة والسرعة.التحقق من المخرجات المهيكلة (POST /api/ai/structured-output/validate/): فرض JSON Schema على مخرجات النماذج مع إعادة محاولة تلقائية عند فشل التحقق.الاستدعاء والتحسينات في الفرانت إند (aiControl.js + useAIStore.js + AIControl.vue / AIOperationsView.vue / AgentPlanner.vue)دوال الاستدعاء (aiControl.js): إضافة executeWorkflow(id, inputs), replayExecution(id, overrides), compareModels(payload), getBudgetForecast(), promoteFeedback(id), inspectGuardrails(text).تحديثات useAIStore.js: إضافة playgroundResults, budgetForecast, وactiveWorkflowRun مع تحديث تلقائي لحالة العُقد.عناصر التحكم وسير العمل والاختبار:مقارن النماذج (Multi-Model Arena في AIControl.vue): واجهة مقسمة لاختبار نفس الـ Prompt على مزودين مختلفين (مثل Gemini vs DeepSeek vs Ollama) ومقارنة السرعة والتكلفة.منفذ ومراقب سير العمل (AgentPlanner.vue و AIOperationsView.vue): زر "تشغيل سير العمل" يحول المخطط المقترح إلى AIWorkflowRun فعلي مع تلوين العُقد (رمادي/أزرق/أخضر/أحمر) حسب حالة التنفيذ.زر Replay في جدول التنفيذات (AIOperationsView.vue): إعادة تشغيل أي طلب فاشل بنقرة واحدة مع إمكانية تغيير المزود.3. تطبيق ai_tools_laboratory (مختبر أدوات الذكاء الاصطناعي)المميزات العشر المقترحة في الباك إند (backend_django/ai_tools_laboratory/)منفذ تجارب فعلي (POST /api/ai-tools/tools/{id}/run-test/): ربط ToolExecution بـ AgentExecutor أو Webhook/HTTP runner لتنفيذ الأداة فعلياً بدلاً من الاكتفاء بالتسجيل اليدوي.معيار مقارنة الأدوات (POST /api/ai-tools/tools/benchmark/): تشغيل نفس المدخلات (input_text) على عدة أدوات ومقارنة السرعة ومعدل النجاح والتقييم.إدارة المفاتيح المشفرة للأدوات (POST /api/ai-tools/tools/{id}/credentials/): ربط الأداة بمفتاح مشفر (مماثل لـ AIProviderCredential) مع إبقاء ToolConfiguration للبيانات غير السرية.مصفوفة التقييم الموزونة (ToolEvaluationScore + POST /api/ai-tools/tools/{id}/score/): تقييم الأداة بناءً على معايير محددة (الدقة، السرعة، التكلفة، سهولة التكامل).المخطط القياسي للمدخلات والمخرجات (input_schema / output_schema في Tool): التحقق من المدخلات قبل التنفيذ وتسهيل تصدير الأداة كـ Function Calling Schema للوكلاء.ترقية الأداة إلى وكيل (POST /api/ai-tools/tools/{id}/promote-to-agent/): إنشاء أو تحديث أداة داخل agents جاهزة للاستخدام المباشر.سجل الإصدارات والبدائل (alternatives M2M في Tool): ربط كل أداة بالبدائل المنافسة في نفس الفئة (ToolCategory).حساب التكلفة التقديرية للتجارب (estimated_cost في ToolExecution): تتبع تكلفة كل تجربة وحساب متوسط التكلفة لكل أداة في laboratory_summary.استيراد/تصدير كتالوج الأدوات (POST /api/ai-tools/tools/import-json/ و export/): مشاركة قوالب الأدوات وإعداداتها الافتراضية.فحص الجاهزية الدوري (POST /api/ai-tools/tools/{id}/health-check/): التحقق من توفر رابط الأداة (website_url / endpoint) وتحديث حالة التوافر.الاستدعاء والتحسينات في الفرانت إند (AI_Tools_Laboratory.js + aiToolsLaboratoryStore.js + aiToolsLaboratoryView.vue)دوال الاستدعاء (AI_Tools_Laboratory.js): إضافة runToolTest(id, payload), benchmarkTools(payload), scoreTool(id, scores), promoteTool(id), healthCheckTool(id).تحديثات aiToolsLaboratoryStore.js: إضافة benchmarkResult وselectedComparisonIds وحالة runningTest.عناصر التحكم وسير العمل والاختبار (aiToolsLaboratoryView.vue):مختبر الاختبار المباشر (Live Playground Tab): نموذج لإدخال input_text واختيار ToolConfiguration وتشغيل الأداة فعلياً مع عرض output_text وduration_ms وحفظها تلقائياً في السجل.وضع المقارنة (Side-by-Side Benchmark): تحديد 2 إلى 4 أدوات من الجدول وتشغيل اختبار موحد لمقارنة النتائج والتقييمات ومعدل النجاح.بطاقات KPIs علوية: عرض إجمالي الأدوات، نسبة النجاح success_rate، ومتوسط التقييم من /tools/summary/.4. تطبيق analytics (التحليلات والمقاييس)المميزات العشر المقترحة في الباك إند (backend_django/analytics/)المستمع التلقائي للأحداث (Django Signals / Event Ingestion Hook): تسجيل AnalyticsEvent وMetricSnapshot تلقائياً عند انتهاء AgentRun أو AIExecution أو ToolExecution.التجميع الزمني المتقدم (GET /api/analytics/metrics/{id}/timeseries/?interval=hour|day|week): إرجاع سلاسل زمنية مجمعة (TruncDay, TruncHour) جاهزة للرسوم البيانية.نظام التنبيهات والعتبات (MetricAlertRule + /api/analytics/alerts/): إطلاق تنبيه عند تجاوز مقياس معين لحد أعلى/أدنى (مثل ارتفاع معدل فشل الوكلاء).كشف الشذوذ (GET /api/analytics/metrics/{id}/anomalies/): حساب المتوسط والانحراف المعياري ($Z\text{-score}$) لاكتشاف القفزات غير الطبيعية في البيانات.تحليل مسار التحويل (POST /api/analytics/events/funnel/): قياس نسبة الانتقال بين سلسلة أحداث متتالية (مثل: agent_created $\rightarrow$ run_approved $\rightarrow$ run_succeeded).جدولة التقارير التلقائية (schedule_cron في Report + مهمة Celery): توليد التقارير دورياً وحفظ النسخ التاريخية.تصدير البيانات والتقارير (GET /api/analytics/reports/{id}/export/?format=csv|json): تنزيل التقارير والـ Snapshots كملفات CSV.حساب المقاييس المركبة (Formula Metrics): دعم مقاييس محسوبة من مقاييس أخرى (مثل: success_rate = succeeded_runs / total_runs * 100).التسجيل الدفعي للأحداث (POST /api/analytics/events/bulk-ingest/): استقبال مجموعة أحداث دفعة واحدة لتحسين الأداء.مقارنة الفترات الزمنية (GET /api/analytics/metrics/{id}/compare/?period=7d): مقارنة أداء الفترة الحالية بالفترة السابقة مباشرة (current vs previous).الاستدعاء والتحسينات في الفرانت إند (Analytics.js + analyticsStore.js + analyticsView.vue)دوال الاستدعاء (Analytics.js): إضافة getTimeseries(id, params), getAnomalies(id), computeFunnel(steps), comparePeriods(id, params), exportReport(id, format), listAlerts(), createAlert(payload).تحديثات analyticsStore.js: إضافة timeseries, anomalies, funnelData, alerts, وdateRange موحد لجميع التبويبات.عناصر التحكم وسير العمل والاختبار (analyticsView.vue):شريط تصفية زمني موحد (Global Date Range & Interval Picker): للتحكم في عرض الرسوم البيانية (ساعي/يومي/أسبوعي) ومقارنة الفترات.منشئ مسارات التحويل (Funnel Builder): واجهة لاختيار تسلسل الأحداث ورؤية نسب التسرب بين كل خطوة.مدير التنبيهات (Alert Rules Drawer): إنشاء قواعد تنبيه واختبارها مباشرة مع عرض نقاط الشذوذ باللون الأحمر على الرسم البياني.5. تطبيق architecture (هندسة النظام والقرارات المعمارية)المميزات العشر المقترحة في الباك إند (backend_django/architecture/)تحليل أثر التغيير والأعطال (GET /api/architecture/components/{id}/impact-analysis/): تتبع جميع المكونات المعتمدة (incoming_dependencies) بشكل تكراري لمعرفة ما سيتأثر عند تعطل مكون معين.اكتشاف المعمارية تلقائياً من النظام (POST /api/architecture/architectures/auto-discover/): مسح تطبيقات Django (agents, ai, automation, إلخ) وإنشاء Component وDependency تلقائياً كمخطط حي.التحقق من صحة البنية (GET /api/architecture/architectures/{id}/lint/): فحص المكونات المعزولة (isolated)، الاختناقات (Single Points of Failure)، والقرارات المعلقة.إصدارات المعمارية والمقارنة (POST /api/architecture/architectures/{id}/snapshot-version/ و diff/): أخذ لقطة لمعمارية النظام ومقارنة الفروقات بين إصدارين (v1.0 vs v2.0).تصدير المخطط ككود (GET /api/architecture/architectures/{id}/export-diagram/?format=mermaid|plantuml): توليد كود Mermaid.js أو PlantUML جاهز للتوثيق.تتبع سلسلة القرارات المعمارية (GET /api/architecture/decisions/{id}/lineage/): عرض شجرة القرارات المستبدلة (superseded_by / supersedes).ربط المكونات بالوكلاء والأدوات (linked_agent_id / linked_tool_id في Component): ربط مكونات المعمارية بالكيانات التشغيلية الحقيقية وحالتها.توليد مسودة ADR بالذكاء الاصطناعي (POST /api/architecture/decisions/draft-with-ai/): استدعاء ai لصياغة context وdecision وconsequences بناءً على وصف المشكلة.حساب درجة صحة المعمارية (Health Score في build_graph): مؤشر رقمي (0-100) يقيس الترابط، التوثيق بالقرارات، وخلو البنية من نقاط الفشل الوحيدة.محاكاة السيناريوهات (POST /api/architecture/architectures/{id}/simulate-failure/): محاكاة إيقاف مكون أو أكثر وإرجاع قائمة الخدمات المتوقفة والمتدهورة.الاستدعاء والتحسينات في الفرانت إند (Architecture.js + architectureStore.js + architectureView.vue)دوال الاستدعاء (Architecture.js): إضافة getImpactAnalysis(componentId), autoDiscoverArchitecture(payload), lintArchitecture(id), exportDiagram(id, format), draftDecisionWithAI(payload), simulateFailure(id, componentIds).تحديثات architectureStore.js: إضافة impactReport, lintIssues, simulatedFailedIds, وmermaidCode.عناصر التحكم وسير العمل والاختبار (architectureView.vue):عارض مخطط تفاعلي (Interactive DAG / Mermaid Canvas): تحويل بيانات store.graph إلى رسم بياني تفاعلي قابل للنقر والسحب بدلاً من الاكتفاء بالقوائم.وضع محاكاة الأعطال (Chaos / Failure Simulator Toggle): النقر على أي مكون في الرسم البياني لتلوين جميع المكونات المتأثرة به باللون الأحمر فوراً.زر الاستكشاف التلقائي ومساعد القرارات (Auto-Discover & AI ADR Drafter): توليد خريطة النظام الحالية بضغطة زر، وصياغة قرارات معمارية (ADR) بمساعدة الذكاء الاصطناعي.

محتاج لى الاتى فى كل تطبيق 
انا هشوف الفرانت اند و اقلك انا عاوز ايه و ايه اللى بيحصل 

- http://localhost:5173/dashboard
* محتاج اضيف البيانات فى الكاش او الوكال استورادج لانو لو رحت صفحة تانية البيانات مبتعيد تحميلها 
* محتاج انو كل النعناصر الموجودة حاليان فى الصفحة تجيب البيانات اللى وجودة فى قاعدة البيانات و يكون فية تفاعل فى الصفحة مع البانات اللى بترجع مع الشكل البيانى 


- http://localhost:5173/goals
* بدوس على التفاصيل محجاش بتفتح ولا على التعديل التحكم مش شغال المسح شغال 
* محتاج الى ايكونات الوان و تكون الوان هادية 




حلّل الكود والبنية الحالية للمشروع بدقة، ثم اعتمد على العقود والوظائف المدعومة فعليًا في AppName/urls.py والـ Serializers دون افتراض أو إضافة أي وظيفة لا يدعمها الخادم، ونفّذ الربط والتكامل الكامل بين جميع وظائف الـ Backend والـ Frontend باستخدام Vue 3 + PrimeVue، مع كتابة أو تعديل الكود اللازم لتحقيق النتيجة المطلوبة، واختبار كل زر ونموذج وصفحة وجميع اتصالات API فعليًا، والتأكد من أن جميع الوظائف تعمل بشكل صحيح ومتوافقة مع إمكانيات النظام الحقيقية.

🌟 القاعدة الذهبية للمشروع
الحفاظ على الموجود والتوسعة: يُمنع تماماً إعادة بناء أي شيء من الصفر أو حذف الميزات القائمة، مع دمج الميزات الجديدة بسلاسة ودون أخطاء.
تسليم الملفات: الاعتماد على الملفات المرفوعة كمرجع أساسي، وتقديم ملفات المشروع الناتج بصيغة (ZIP) متكاملة ومحدثة بالكامل وليست تعديلات جزئية (Diffs).



🚀 رابعاً: النشر والفحص النهائي
تنفيذ اختبارات الاستقرار الشاملة لبيئة العمل والتأكد من خلو المشروع من أي روابط وهمية أو عيوب في الاتصال بين Vue 3 و Django.

