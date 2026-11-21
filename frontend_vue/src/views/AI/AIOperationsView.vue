<template>
  <main class="ai-ops-page" :dir="direction">
    <header class="page-head">
      <div>
        <span class="eyebrow">AI MANAGEMENT & OPERATIONS</span>
        <h1>إدارة ومراقبة منصة الذكاء الاصطناعي</h1>
        <p>التنفيذات والاستهلاك والميزانيات وسير العمل والتدقيق والتشخيص.</p>
      </div>
      <Button label="تحديث البيانات" icon="pi pi-refresh" :loading="loading" @click="refresh" />
    </header>

    <Message v-if="errorMessage" severity="error" :closable="true" @close="errorMessage = ''">
      {{ errorMessage }}
    </Message>

    <section class="stats">
      <Card><template #title>الرسائل</template><template #content><strong>{{ usage.message_count ?? 0 }}</strong></template></Card>
      <Card><template #title>ردود المساعد</template><template #content><strong>{{ usage.assistant_message_count ?? 0 }}</strong></template></Card>
      <Card><template #title>التنفيذات</template><template #content><strong>{{ executions.length }}</strong></template></Card>
      <Card><template #title>سير العمل</template><template #content><strong>{{ workflows.length }}</strong></template></Card>
    </section>

    <Tabs v-model:value="activeTab">
      <TabList>
        <Tab value="executions">التنفيذات</Tab>
        <Tab value="usage">الاستهلاك</Tab>
        <Tab value="budgets">الميزانيات</Tab>
        <Tab value="workflows">سير العمل</Tab>
        <Tab value="audit">سجل التدقيق</Tab>
        <Tab value="feedback">التقييمات</Tab>
        <Tab value="diagnostics">التشخيص</Tab>
      </TabList>
      <TabPanels>
        <TabPanel value="executions">
          <DataTable :value="executions" paginator :rows="10" responsiveLayout="scroll" :loading="loading">
            <Column field="created_at" header="الوقت" />
            <Column field="task_type" header="نوع التنفيذ" />
            <Column field="requested_provider" header="المزود المطلوب" />
            <Column field="provider" header="المزود المستخدم" />
            <Column field="model" header="النموذج" />
            <Column header="الحالة"><template #body="{ data }"><Tag :value="data.status" :severity="statusSeverity(data.status)" /></template></Column>
            <Column field="duration_ms" header="المدة (ms)" />
            <Column field="fallback_count" header="Fallback" />
          </DataTable>
        </TabPanel>

        <TabPanel value="usage">
          <div class="usage-grid">
            <Card><template #title>ملخص الاستخدام</template><template #content>
              <dl class="metric-list">
                <div v-for="(value, key) in usage" :key="key"><dt>{{ key }}</dt><dd>{{ displayValue(value) }}</dd></div>
              </dl>
            </template></Card>
            <Card><template #title>الاستخدام حسب المزود</template><template #content>
              <DataTable :value="usage.by_provider || []" responsiveLayout="scroll">
                <Column field="provider" header="المزود" />
                <Column field="count" header="عدد الطلبات" />
                <Column field="tokens" header="Tokens" />
              </DataTable>
              <Message v-if="!usage.by_provider?.length" severity="info">لا توجد بيانات مجمعة حسب المزود في الاستجابة الحالية.</Message>
            </template></Card>
          </div>
        </TabPanel>

        <TabPanel value="budgets">
          <div class="section-toolbar"><h2>سياسات الميزانية</h2><Button label="إضافة سياسة" icon="pi pi-plus" @click="openBudgetCreate" /></div>
          <DataTable :value="budgets" paginator :rows="10" responsiveLayout="scroll">
            <Column field="scope" header="النطاق" />
            <Column field="scope_key" header="مفتاح النطاق" />
            <Column field="daily_cost_limit" header="حد التكلفة اليومي" />
            <Column field="monthly_cost_limit" header="حد التكلفة الشهري" />
            <Column field="daily_token_limit" header="حد Tokens اليومي" />
            <Column field="monthly_token_limit" header="حد Tokens الشهري" />
            <Column header="مفعّل"><template #body="{ data }"><Tag :value="data.enabled ? 'نعم' : 'لا'" :severity="data.enabled ? 'success' : 'secondary'" /></template></Column>
            <Column header="إجراءات"><template #body="{ data }">
              <div class="row-actions"><Button icon="pi pi-pencil" text rounded aria-label="تعديل" @click="editBudget(data)" /><Button icon="pi pi-trash" text rounded severity="danger" aria-label="حذف" @click="removeBudget(data)" /></div>
            </template></Column>
          </DataTable>
          <Message v-if="!budgets.length" severity="info">لا توجد سياسات ميزانية محفوظة.</Message>
        </TabPanel>

        <TabPanel value="workflows">
          <div class="section-toolbar"><div><h2>تعريفات Workflows</h2><p>يمكن إنشاء المخطط والتحقق منه ومراجعة سجل التشغيل؛ التنفيذ غير متاح في API الحالي.</p></div><Button label="إنشاء Workflow" icon="pi pi-plus" @click="openWorkflowCreate" /></div>
          <DataTable :value="workflows" paginator :rows="8" responsiveLayout="scroll">
            <Column field="name" header="الاسم" />
            <Column field="version" header="الإصدار" />
            <Column field="is_active" header="نشط"><template #body="{ data }"><Tag :value="data.is_active ? 'نشط' : 'متوقف'" :severity="data.is_active ? 'success' : 'secondary'" /></template></Column>
            <Column field="updated_at" header="آخر تحديث" />
            <Column header="إجراءات"><template #body="{ data }">
              <div class="row-actions"><Button icon="pi pi-eye" text rounded aria-label="سجل التشغيل" @click="showRuns(data)" /><Button icon="pi pi-pencil" text rounded aria-label="تعديل" @click="editWorkflow(data)" /><Button icon="pi pi-trash" text rounded severity="danger" aria-label="حذف" @click="removeWorkflow(data)" /></div>
            </template></Column>
          </DataTable>
          <Message severity="warn" class="mt-3">لا يوجد endpoint لتشغيل Workflow في إعدادات Django الحالية؛ لذلك لا يوجد زر تنفيذ.</Message>
          <Dialog v-model:visible="workflowDialog" modal :header="workflowForm.id ? 'تعديل Workflow' : 'إنشاء Workflow'" :style="{ width: 'min(760px, 94vw)' }">
            <div class="form-grid">
              <label>الاسم<InputText v-model="workflowForm.name" maxlength="160" /></label>
              <label>الوصف<Textarea v-model="workflowForm.description" rows="2" autoResize /></label>
              <label class="full-span">مخطط JSON (nodes وedges)<Textarea v-model="workflowJson" rows="12" spellcheck="false" /></label>
            </div>
            <Message v-if="workflowValidation" :severity="workflowValidation.valid ? 'success' : 'error'" class="mt-3">
              {{ workflowValidation.valid ? `المخطط صالح: ${workflowValidation.node_count} عقدة و${workflowValidation.edge_count} رابط.` : (workflowValidation.errors || []).join(' · ') }}
            </Message>
            <div class="dialog-actions"><Button label="التحقق من المخطط" severity="secondary" outlined :loading="validatingWorkflow" @click="validateWorkflow" /><Button label="حفظ" icon="pi pi-save" :disabled="!workflowForm.name.trim()" :loading="savingWorkflow" @click="saveWorkflow" /></div>
          </Dialog>
          <Dialog v-model:visible="runsDialog" modal header="سجل تشغيل Workflow" :style="{ width: 'min(900px, 96vw)' }">
            <DataTable :value="workflowRuns" paginator :rows="8" responsiveLayout="scroll">
              <Column field="id" header="#" /><Column field="status" header="الحالة" /><Column field="started_at" header="بدأ" /><Column field="finished_at" header="انتهى" /><Column field="error" header="الخطأ" />
              <Column header="النتيجة"><template #body="{ data }"><Button label="عرض" text size="small" @click="selectedRun = data" /></template></Column>
            </DataTable>
            <pre v-if="selectedRun" class="json-view">{{ JSON.stringify({ input_data: selectedRun.input_data, output_data: selectedRun.output_data, error: selectedRun.error }, null, 2) }}</pre>
            <Message v-if="!workflowRuns.length" severity="info">لا توجد سجلات تشغيل لهذا الـ Workflow.</Message>
          </Dialog>
        </TabPanel>

        <TabPanel value="audit">
          <DataTable :value="audit" paginator :rows="12" responsiveLayout="scroll">
            <Column field="created_at" header="الوقت" /><Column field="action" header="العملية" /><Column field="resource" header="المورد" /><Column field="result" header="النتيجة" />
            <Column header="التفاصيل"><template #body="{ data }"><Button label="عرض" text size="small" @click="selectedAudit = data; auditDialog = true" /></template></Column>
          </DataTable>
          <Message v-if="!audit.length" severity="info">لا توجد أحداث تدقيق متاحة.</Message>
          <Dialog v-model:visible="auditDialog" modal header="تفاصيل حدث التدقيق" :style="{ width: 'min(720px, 94vw)' }"><pre class="json-view">{{ JSON.stringify(selectedAudit, null, 2) }}</pre></Dialog>
        </TabPanel>

        <TabPanel value="feedback">
          <Card><template #title>إرسال تقييم لرسالة مساعد</template><template #content>
            <div class="form-grid">
              <label>معرّف رسالة المساعد<InputNumber v-model="feedback.message_id" :min="1" /></label>
              <label>التقييم<Select v-model="feedback.sentiment" :options="sentimentOptions" optionLabel="label" optionValue="value" /></label>
              <label>التصنيف<InputText v-model="feedback.feedback_category" maxlength="80" /></label>
              <label>السبب<InputText v-model="feedback.reason" maxlength="255" /></label>
              <label class="full-span">تعليق<Textarea v-model="feedback.comment" rows="3" maxlength="5000" autoResize /></label>
              <label>التقييم من 1 إلى 5<InputNumber v-model="feedback.rating" :min="1" :max="5" /></label>
            </div>
            <div class="dialog-actions"><Button label="إرسال التقييم" icon="pi pi-send" :loading="sendingFeedback" :disabled="!feedback.message_id" @click="submitFeedback" /></div>
            <Message v-if="feedbackMessage" :severity="feedbackMessage.severity" class="mt-3">{{ feedbackMessage.text }}</Message>
            <small class="muted">يقبل Backend فقط message_id لرسالة مساعد مملوكة للمستخدم الحالي.</small>
          </template></Card>
        </TabPanel>

        <TabPanel value="diagnostics">
          <div class="usage-grid">
            <Card><template #title>صحة النظام</template><template #content>
              <pre class="json-view">{{ JSON.stringify(health, null, 2) }}</pre>
              <Button label="فحص الصحة" icon="pi pi-heart" severity="secondary" outlined :loading="diagnosticsLoading" @click="loadDiagnostics" />
            </template></Card>
            <Card><template #title>قدرات AI المتاحة</template><template #content>
              <ul class="capability-list"><li v-for="(feature, index) in capabilities" :key="index">{{ typeof feature === 'string' ? feature : JSON.stringify(feature) }}</li></ul>
              <Message v-if="!capabilities.length" severity="info">لم يرجع Backend قائمة قدرات.</Message>
            </template></Card>
          </div>
        </TabPanel>
      </TabPanels>
    </Tabs>

    <Dialog v-model:visible="budgetDialog" modal :header="budgetForm.id ? 'تعديل سياسة الميزانية' : 'إضافة سياسة ميزانية'" :style="{ width: 'min(620px, 94vw)' }">
      <div class="form-grid">
        <label>النطاق<Select v-model="budgetForm.scope" :options="scopeOptions" optionLabel="label" optionValue="value" /></label>
        <label>مفتاح النطاق<InputText v-model="budgetForm.scope_key" maxlength="120" /></label>
        <label>التكلفة اليومية<InputNumber v-model="budgetForm.daily_cost_limit" :min="0" :maxFractionDigits="8" /></label>
        <label>التكلفة الشهرية<InputNumber v-model="budgetForm.monthly_cost_limit" :min="0" :maxFractionDigits="8" /></label>
        <label>حد Tokens اليومي<InputNumber v-model="budgetForm.daily_token_limit" :min="0" /></label>
        <label>حد Tokens الشهري<InputNumber v-model="budgetForm.monthly_token_limit" :min="0" /></label>
        <label class="checkbox-field"><Checkbox v-model="budgetForm.enabled" binary /> السياسة مفعّلة</label>
      </div>
      <div class="dialog-actions"><Button label="إلغاء" severity="secondary" text @click="budgetDialog = false" /><Button label="حفظ" icon="pi pi-save" :loading="savingBudget" @click="saveBudget" /></div>
    </Dialog>
  </main>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { storeToRefs } from 'pinia'
import Button from 'primevue/button'
import Card from 'primevue/card'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Tabs from 'primevue/tabs'
import TabList from 'primevue/tablist'
import Tab from 'primevue/tab'
import TabPanels from 'primevue/tabpanels'
import TabPanel from 'primevue/tabpanel'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import Select from 'primevue/select'
import Textarea from 'primevue/textarea'
import Message from 'primevue/message'
import Tag from 'primevue/tag'
import Dialog from 'primevue/dialog'
import Checkbox from 'primevue/checkbox'
import { useAIStore } from '@/stores/ai/useAIStore'
import aiControl from '@/services/AI/aiControl'

const { locale } = useI18n()
const direction = computed(() => locale.value === 'ar' ? 'rtl' : 'ltr')
const store = useAIStore()
const { executions, usage, budgets, audit, workflows, health, capabilities, loading } = storeToRefs(store)
const activeTab = ref('executions')
const errorMessage = ref('')
const budgetDialog = ref(false), workflowDialog = ref(false), runsDialog = ref(false), auditDialog = ref(false)
const savingBudget = ref(false), savingWorkflow = ref(false), validatingWorkflow = ref(false), diagnosticsLoading = ref(false), sendingFeedback = ref(false)
const workflowRuns = ref([]), selectedRun = ref(null), selectedAudit = ref(null), workflowValidation = ref(null)
const feedbackMessage = ref(null)
const workflowJson = ref('{\n  "nodes": [],\n  "edges": []\n}')
const workflowForm = reactive({ id: null, name: '', description: '' })
const budgetForm = reactive({ id: null, scope: 'user', scope_key: '', daily_cost_limit: null, monthly_cost_limit: null, daily_token_limit: null, monthly_token_limit: null, enabled: true })
const feedback = reactive({ message_id: null, sentiment: 'like', reason: '', comment: '', feedback_category: '', rating: null })
const scopeOptions = [{ label: 'مستخدم', value: 'user' }, { label: 'Agent', value: 'agent' }, { label: 'مزود', value: 'provider' }]
const sentimentOptions = [{ label: 'إيجابي', value: 'like' }, { label: 'سلبي', value: 'dislike' }]

function statusSeverity(status) { return ({ succeeded: 'success', completed: 'success', failed: 'danger', running: 'info', queued: 'warn', pending: 'warn' })[status] || 'secondary' }
function displayValue(value) { return value && typeof value === 'object' ? JSON.stringify(value) : (value ?? '—') }
function messageOf(error, fallback) { return error?.response?.data?.detail || error?.response?.data?.error || error?.message || fallback }
async function refresh() {
  errorMessage.value = ''
  try { await Promise.all([store.refreshOperations(), store.refreshControl()]) }
  catch (error) { errorMessage.value = messageOf(error, 'تعذر تحميل بيانات إدارة AI.') }
}
async function loadDiagnostics() {
  diagnosticsLoading.value = true
  try {
    const [healthResult, capabilityResult] = await Promise.all([aiControl.getAIHealth(), aiControl.getAICapabilities()])
    health.value = healthResult
    capabilities.value = Array.isArray(capabilityResult?.features) ? capabilityResult.features : []
  } catch (error) { errorMessage.value = messageOf(error, 'تعذر تحميل التشخيصات.') }
  finally { diagnosticsLoading.value = false }
}
function openBudgetCreate() {
  Object.assign(budgetForm, { id: null, scope: 'user', scope_key: '', daily_cost_limit: null, monthly_cost_limit: null, daily_token_limit: null, monthly_token_limit: null, enabled: true })
  budgetDialog.value = true
}
function editBudget(item) { Object.assign(budgetForm, { ...item }); budgetDialog.value = true }
async function saveBudget() {
  savingBudget.value = true
  try {
    const payload = { scope: budgetForm.scope, scope_key: budgetForm.scope_key, daily_cost_limit: budgetForm.daily_cost_limit, monthly_cost_limit: budgetForm.monthly_cost_limit, daily_token_limit: budgetForm.daily_token_limit, monthly_token_limit: budgetForm.monthly_token_limit, enabled: budgetForm.enabled }
    if (budgetForm.id) await aiControl.updateAIBudget(budgetForm.id, payload)
    else await aiControl.createAIBudget(payload)
    budgetDialog.value = false
    await store.refreshOperations()
  } catch (error) { errorMessage.value = messageOf(error, 'تعذر حفظ سياسة الميزانية.') }
  finally { savingBudget.value = false }
}
async function removeBudget(item) {
  if (!window.confirm(`حذف سياسة الميزانية ${item.scope}؟`)) return
  try { await aiControl.deleteAIBudget(item.id); await store.refreshOperations() }
  catch (error) { errorMessage.value = messageOf(error, 'تعذر حذف سياسة الميزانية.') }
}
function openWorkflowCreate() {
  Object.assign(workflowForm, { id: null, name: '', description: '' })
  workflowJson.value = '{\n  "nodes": [],\n  "edges": []\n}'
  workflowValidation.value = null
  workflowDialog.value = true
}
async function editWorkflow(item) {
  try {
    const full = await aiControl.getAIWorkflow(item.id)
    Object.assign(workflowForm, { id: full.id, name: full.name || '', description: full.description || '' })
    workflowJson.value = JSON.stringify(full.graph || { nodes: [], edges: [] }, null, 2)
    workflowValidation.value = null
    workflowDialog.value = true
  } catch (error) { errorMessage.value = messageOf(error, 'تعذر تحميل Workflow.') }
}
async function validateWorkflow() {
  validatingWorkflow.value = true
  workflowValidation.value = null
  try {
    const graph = JSON.parse(workflowJson.value)
    workflowValidation.value = await aiControl.validateAIWorkflow(graph)
  } catch (error) {
    workflowValidation.value = error?.response?.data || { valid: false, errors: [error instanceof SyntaxError ? 'JSON غير صالح.' : messageOf(error, 'تعذر التحقق من المخطط.')] }
  } finally { validatingWorkflow.value = false }
}
async function saveWorkflow() {
  savingWorkflow.value = true
  try {
    const graph = JSON.parse(workflowJson.value)
    let validation
    try {
      validation = await aiControl.validateAIWorkflow(graph)
    } catch (validationError) {
      if (validationError?.response?.data?.valid === false) validation = validationError.response.data
      else throw validationError
    }
    workflowValidation.value = validation
    if (!validation.valid) return
    const payload = { name: workflowForm.name.trim(), description: workflowForm.description, graph }
    if (workflowForm.id) await aiControl.updateAIWorkflow(workflowForm.id, payload)
    else await aiControl.createAIWorkflow(payload)
    workflowDialog.value = false
    await store.refreshOperations()
  } catch (error) { errorMessage.value = messageOf(error, 'تعذر حفظ Workflow. راجع المخطط والحقول.') }
  finally { savingWorkflow.value = false }
}
async function removeWorkflow(item) {
  if (!window.confirm(`حذف Workflow: ${item.name}؟`)) return
  try { await aiControl.deleteAIWorkflow(item.id); await store.refreshOperations() }
  catch (error) { errorMessage.value = messageOf(error, 'تعذر حذف Workflow.') }
}
async function showRuns(item) {
  try { workflowRuns.value = await aiControl.getAIWorkflowRuns(item.id); selectedRun.value = null; runsDialog.value = true }
  catch (error) { errorMessage.value = messageOf(error, 'تعذر تحميل سجل التشغيل.') }
}
async function submitFeedback() {
  sendingFeedback.value = true
  feedbackMessage.value = null
  try {
    await aiControl.submitAIFeedback({ ...feedback })
    feedbackMessage.value = { severity: 'success', text: 'تم حفظ التقييم.' }
    Object.assign(feedback, { message_id: null, sentiment: 'like', reason: '', comment: '', feedback_category: '', rating: null })
  } catch (error) { feedbackMessage.value = { severity: 'error', text: messageOf(error, 'تعذر حفظ التقييم.') } }
  finally { sendingFeedback.value = false }
}
onMounted(refresh)
</script>

<style scoped>
.ai-ops-page{padding:clamp(1rem,2vw,2rem);display:grid;gap:1.25rem;color:var(--p-text-color)}
.page-head,.section-toolbar{display:flex;align-items:center;justify-content:space-between;gap:1rem;flex-wrap:wrap}
.page-head h1{margin:.35rem 0;font-size:clamp(1.35rem,2.4vw,2rem)}.page-head p,.section-toolbar p,.muted{color:var(--p-text-muted-color);margin:.3rem 0}
.eyebrow{font-size:.72rem;letter-spacing:.12em;color:var(--p-primary-color);font-weight:700}
.stats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.85rem}.stats strong{font-size:1.7rem;font-variant-numeric:tabular-nums}
.usage-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem}.metric-list{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.5rem 1rem;margin:0}.metric-list div{padding:.55rem;border-bottom:1px solid var(--p-content-border-color);min-width:0}.metric-list dt{font-size:.8rem;color:var(--p-text-muted-color)}.metric-list dd{margin:.25rem 0 0;overflow-wrap:anywhere;font-weight:600}
.section-toolbar h2{font-size:1.1rem;margin:0}.row-actions{display:flex;gap:.2rem}.form-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem}.form-grid label{display:grid;gap:.4rem;font-size:.9rem}.form-grid :deep(.p-inputtext),.form-grid :deep(.p-inputnumber),.form-grid :deep(.p-select){width:100%}.full-span{grid-column:1/-1}.checkbox-field{display:flex!important;align-items:center;gap:.6rem!important}.dialog-actions{display:flex;justify-content:flex-start;gap:.6rem;margin-top:1.1rem;flex-wrap:wrap}.json-view{background:var(--p-surface-100);border-radius:8px;padding:1rem;overflow:auto;max-height:360px;direction:ltr;text-align:left;font-size:.8rem}.capability-list{padding-inline-start:1.25rem;display:grid;gap:.5rem}.mt-3{margin-top:1rem}
@media(max-width:850px){.stats{grid-template-columns:repeat(2,minmax(0,1fr))}.usage-grid{grid-template-columns:1fr}}
@media(max-width:560px){.stats{grid-template-columns:1fr 1fr}.form-grid{grid-template-columns:1fr}.full-span{grid-column:auto}.page-head{align-items:flex-start}}
</style>
