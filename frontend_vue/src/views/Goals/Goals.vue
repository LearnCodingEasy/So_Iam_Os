<template>
  <main class="goals-page" dir="auto">
    <PageHeader
      eyebrow="SO_IAM_OS · PLANNING"
      title="الأهداف والإنجازات"
      description="حوّل أهدافك إلى مراحل ومهام قابلة للتنفيذ، وتابع التقدم الفعلي من بيانات النظام."
      illustration="goals"
    >
      <template #actions>
        <prime_button
          icon="pi pi-refresh"
          severity="secondary"
          outlined
          :loading="store.loading"
          aria-label="تحديث"
          @click="refresh"
        />
        <prime_button icon="pi pi-plus" label="هدف جديد" @click="openCreate" />
      </template>
    </PageHeader>

    <StateBlock
      v-if="store.error"
      state="error"
      title="تعذر تحميل الأهداف"
      message="حدثت مشكلة أثناء جلب الأهداف من الخادم. حاول تحديث البيانات."
      action-label="إعادة المحاولة"
      action-icon="pi pi-refresh"
      @action="refresh"
    />

    <!-- استخدام مكون الإحصائيات المستقل -->
    <GoalStats :analytics="analytics" />

    <!-- استخدام مكون شريط الأدوات المستقل -->
    <GoalsToolbar
      v-model:search="search"
      v-model:statusFilter="statusFilter"
      v-model:categoryFilter="categoryFilter"
      v-model:sortBy="sortBy"
      :statusOptions="statusOptions"
      :categoryOptions="categoryOptions"
      :sortOptions="sortOptions"
    />

    <section v-if="store.loading" class="goals-grid">
      <prime_card v-for="n in 3" :key="n" class="goal-card">
        <template #content
          ><prime_skeleton height="1.2rem" /><prime_skeleton
            height="5rem"
            class="mt-3" /><prime_skeleton height="0.7rem" class="mt-3"
        /></template>
      </prime_card>
    </section>

    <section v-else-if="visibleGoals.length" ref="gridEl" class="goals-grid">
      <!-- استخدام مكون كارت الهدف -->
      <GoalCard
        v-for="goal in visibleGoals"
        :key="goal.id"
        :goal="goal"
        :statusLabel="statusLabel"
        :categoryLabel="categoryLabel"
        :priorityLabel="priorityLabel"
        :statusSeverity="statusSeverity"
        @details="openDetails"
        @edit="openEdit"
        @action="runAction"
        @duplicate="duplicate"
        @remove="removeGoal"
      />
    </section>

    <prime_paginator
      v-if="!store.loading && store.count > pageSize"
      :first="(page - 1) * pageSize"
      :rows="pageSize"
      :total-records="store.count"
      @page="onPage"
    />

    <StateBlock
      v-if="!store.loading && !store.error && visibleGoals.length === 0"
      state="empty"
      illustration="goals"
      title="لا توجد أهداف مطابقة"
      message="أنشئ هدفًا جديدًا أو غيّر عوامل البحث والتصفية."
      action-label="إنشاء هدف"
      action-icon="pi pi-plus"
      @action="openCreate"
    />

    <!-- النوافذ المنبثقة (Modals) يمكن فصلها أيضاً أو إبقاؤها حسب الرغبة -->
    <!-- (ملاحظة: النوافذ تظل بكامل وظائفها والمنطق الخاص بها في الـ Script أدناه) -->

    <!-- Dialogs restored from the previous template; their state/handlers live in <script setup> -->
    <prime_dialog
      v-model:visible="editorVisible"
      modal
      :header="editingId ? 'تعديل الهدف' : 'إنشاء هدف جديد'"
      :style="{ width: 'min(680px, 94vw)' }"
      :draggable="false"
    >
      <form class="goal-form" @submit.prevent="saveGoal">
        <label class="field full"
          >عنوان الهدف<prime_input_text v-model.trim="form.title" required maxlength="255"
        /></label>
        <label class="field full"
          >الوصف<prime_textarea v-model="form.description" rows="3" auto-resize
        /></label>
        <div class="form-columns">
          <label class="field"
            >التصنيف<prime_select
              v-model="form.category"
              :options="categoryOptions"
              option-label="label"
              option-value="value"
          /></label>
          <label class="field"
            >الأولوية<prime_select
              v-model="form.priority"
              :options="priorityOptions"
              option-label="label"
              option-value="value"
          /></label>
          <label class="field"
            >الحالة<prime_select
              v-model="form.status"
              :options="editableStatusOptions"
              option-label="label"
              option-value="value"
          /></label>
          <label class="field">تاريخ البداية<input v-model="form.start_date" type="date" /></label>
          <label class="field"
            >الموعد المستهدف<input v-model="form.target_date" type="date"
          /></label>
          <label class="field"
            >المدة التقديرية بالدقائق<prime_input_number
              v-model="form.estimated_minutes"
              :min="0"
              :max="1000000"
          /></label>
          <label class="field"
            >وحدة القياس<prime_input_text
              v-model="form.measurement_unit"
              placeholder="مثال: ساعة، كتاب، جنيه"
          /></label>
          <label class="field"
            >القيمة الابتدائية<prime_input_number
              v-model="form.initial_value"
              :min-fraction-digits="0"
              :max-fraction-digits="2"
          /></label>
          <label class="field"
            >القيمة الحالية<prime_input_number
              v-model="form.current_value"
              :min-fraction-digits="0"
              :max-fraction-digits="2"
          /></label>
          <label class="field"
            >القيمة المستهدفة<prime_input_number
              v-model="form.target_value"
              :min-fraction-digits="0"
              :max-fraction-digits="2"
          /></label>
          <label class="field full"
            >التقدم المبلغ عنه (%)<prime_input_number
              v-model="form.progress_percent"
              :min="0"
              :max="100"
              suffix="%"
          /></label>
          <label class="field full"
            >أهداف التعلم المرتبطة<prime_list_box
              v-model="form.learning_goals"
              :options="learningGoalOptions"
              option-label="title"
              option-value="id"
              multiple
              list-style="max-height: 9rem"
          /></label>
        </div>
        <div class="dialog-actions">
          <prime_button
            label="إلغاء"
            severity="secondary"
            text
            type="button"
            @click="editorVisible = false"
          /><prime_button label="حفظ الهدف" icon="pi pi-check" type="submit" :loading="saving" />
        </div>
      </form>
    </prime_dialog>

    <prime_dialog
      v-model:visible="detailsVisible"
      modal
      :header="selectedGoal?.title || 'تفاصيل الهدف'"
      :style="{ width: 'min(980px, 96vw)' }"
      :draggable="false"
      maximizable
    >
      <div v-if="selectedGoal" class="goal-details">
        <div class="detail-summary">
          <div>
            <span class="eyebrow">التقدم الحالي</span
            ><strong>{{ selectedGoal.progress_percent }}%</strong
            ><prime_progress_bar :value="selectedGoal.progress_percent" />
          </div>
          <div class="detail-summary-meta">
            <prime_tag
              :value="statusLabel(selectedGoal.status)"
              :severity="statusSeverity(selectedGoal.status)"
            /><span>الموعد: {{ selectedGoal.target_date || 'غير محدد' }}</span
            ><span
              >المهام: {{ linkedTasks.filter((t) => t.status === 'completed').length }}/{{
                linkedTasks.length
              }}</span
            >
          </div>
        </div>
        <div class="detail-grid">
          <section class="detail-panel">
            <div class="panel-heading">
              <h3>المراحل الرئيسية</h3>
              <prime_button
                label="إضافة مرحلة"
                icon="pi pi-plus"
                text
                size="small"
                @click="openMilestoneEditor"
              />
            </div>
            <div v-if="milestones.length" class="milestone-list">
              <article v-for="milestone in milestones" :key="milestone.id" class="milestone-row">
                <div class="milestone-title">
                  <strong>{{ milestone.sequence + 1 }}. {{ milestone.title }}</strong
                  ><prime_tag
                    :value="statusLabel(milestone.status)"
                    :severity="
                      milestone.status === 'completed'
                        ? 'success'
                        : milestone.status === 'blocked'
                          ? 'danger'
                          : 'info'
                    "
                  />
                </div>
                <p>
                  {{
                    milestone.description ||
                    milestone.completion_criteria ||
                    'لا توجد تفاصيل إضافية.'
                  }}
                </p>
                <prime_progress_bar :value="milestone.progress_percent" :show-value="false" /><small
                  >{{ milestone.progress_percent }}% · {{ milestone.target_date || 'دون موعد' }} ·
                  وزن {{ milestone.weight }}%</small
                >
                <div class="inline-actions">
                  <prime_button
                    v-if="milestone.status !== 'completed'"
                    label="إكمال"
                    icon="pi pi-check"
                    size="small"
                    text
                    @click="completeMilestone(milestone)"
                  /><prime_button
                    icon="pi pi-trash"
                    severity="danger"
                    text
                    size="small"
                    aria-label="حذف المرحلة"
                    @click="removeMilestone(milestone)"
                  />
                </div>
              </article>
            </div>
            <p v-else class="muted-empty">لم تتم إضافة مراحل بعد.</p>
          </section>
          <section class="detail-panel">
            <div class="panel-heading">
              <h3>المهام المرتبطة</h3>
              <prime_button
                label="مهمة جديدة"
                icon="pi pi-plus"
                text
                size="small"
                @click="createGoalTask"
              />
            </div>
            <div v-if="linkedTasks.length" class="task-list">
              <article v-for="task in linkedTasks" :key="task.id">
                <span class="task-status" :class="task.status"></span>
                <div>
                  <strong>{{ task.title }}</strong
                  ><small>{{ task.scheduled_date }} · {{ task.status }}</small>
                </div>
              </article>
            </div>
            <p v-else class="muted-empty">لا توجد مهام مرتبطة بهذا الهدف.</p>
          </section>
          <section class="detail-panel">
            <div class="panel-heading">
              <h3>مدرب الأهداف بالذكاء الاصطناعي</h3>
              <prime_button
                label="اقتراح خطة"
                icon="pi pi-sparkles"
                size="small"
                :loading="planning"
                @click="generatePlan"
              />
            </div>
            <p>
              اسأل عن التقدم أو المخاطر، أو اطلب خطة. أي تغييرات تنفيذية تظل مقترحات حتى تعتمدها.
            </p>
            <prime_textarea
              v-model="coachQuestion"
              rows="2"
              placeholder="اسأل مدرب الأهداف عن هذا الهدف..."
            />
            <div class="inline-actions">
              <prime_button
                label="اسأل المدرب"
                icon="pi pi-send"
                size="small"
                :loading="coachLoading"
                :disabled="!coachQuestion.trim()"
                @click="askCoach"
              />
            </div>
            <article v-if="coachAnswer" class="coach-answer">
              <small>المزود: {{ coachAnswer.provider || 'غير محدد' }}</small>
              <p>{{ coachAnswer.content }}</p>
            </article>
            <prime_textarea
              v-model="planInstructions"
              rows="2"
              placeholder="تعليمات إضافية عند إنشاء الخطة (اختياري)"
            />
          </section>
          <section class="detail-panel">
            <div class="panel-heading">
              <h3>التعلم والمشاريع</h3>
              <prime_button
                label="ربط مشروع"
                icon="pi pi-link"
                text
                size="small"
                @click="linkProject"
              />
            </div>
            <p>أهداف التعلم المرتبطة: {{ selectedGoal.learning_goals?.length || 0 }}</p>
            <div v-if="linkedProjects.length" class="history-list">
              <article v-for="project in linkedProjects" :key="project.id">
                <strong>{{ project.title }}</strong
                ><small>{{ project.status }}</small>
              </article>
            </div>
            <p v-else class="muted-empty">لا توجد مشاريع مرتبطة.</p>
          </section>
          <section class="detail-panel">
            <div class="panel-heading"><h3>سجل النشاط</h3></div>
            <div v-if="history.length" class="history-list">
              <article v-for="event in history" :key="event.id">
                <strong>{{ event.description || event.event_type }}</strong
                ><small>{{ formatDateTime(event.created_at) }}</small>
              </article>
            </div>
            <p v-else class="muted-empty">لا يوجد نشاط مسجل بعد.</p>
            <div class="note-entry">
              <prime_input_text
                v-model="noteText"
                placeholder="أضف ملاحظة أو تحديثًا"
                @keyup.enter="addNote"
              /><prime_button
                icon="pi pi-send"
                size="small"
                :disabled="!noteText.trim()"
                @click="addNote"
              />
            </div>
          </section>
        </div>
      </div>
    </prime_dialog>

    <prime_dialog
      v-model:visible="milestoneVisible"
      modal
      header="إضافة مرحلة"
      :style="{ width: 'min(560px, 94vw)' }"
      :draggable="false"
    >
      <form class="goal-form" @submit.prevent="saveMilestone">
        <label class="field full"
          >اسم المرحلة<prime_input_text v-model.trim="milestoneForm.title" required /></label
        ><label class="field full"
          >الوصف<prime_textarea v-model="milestoneForm.description" rows="2"
        /></label>
        <div class="form-columns">
          <label class="field"
            >تاريخ البداية<input v-model="milestoneForm.start_date" type="date" /></label
          ><label class="field"
            >الموعد المستهدف<input v-model="milestoneForm.target_date" type="date" /></label
          ><label class="field"
            >الوزن في تقدم الهدف (%)<prime_input_number
              v-model="milestoneForm.weight"
              :min="0"
              :max="100"
              suffix="%" /></label
          ><label class="field"
            >معيار الإنجاز<prime_input_text v-model="milestoneForm.completion_criteria" /></label
          ><label class="field full"
            >الأدلة المطلوبة / رابط الإثبات<prime_input_text
              v-model="milestoneForm.completion_evidence" /></label
          ><label class="field full"
            >تعتمد على المراحل السابقة<prime_list_box
              v-model="milestoneForm.depends_on"
              :options="milestones"
              option-label="title"
              option-value="id"
              multiple
              list-style="max-height: 8rem"
          /></label>
        </div>
        <div class="dialog-actions">
          <prime_button
            label="إلغاء"
            severity="secondary"
            text
            type="button"
            @click="milestoneVisible = false"
          /><prime_button label="حفظ المرحلة" type="submit" :loading="savingMilestone" />
        </div>
      </form>
    </prime_dialog>

    <prime_dialog
      v-model:visible="proposalVisible"
      modal
      header="مقترح خطة الهدف — بانتظار موافقتك"
      :style="{ width: 'min(760px, 95vw)' }"
      :draggable="false"
    >
      <div v-if="proposal" class="proposal-content">
        <p>{{ proposal.payload?.summary }}</p>
        <h4>معايير النجاح</h4>
        <ul>
          <li v-for="item in proposal.payload?.success_criteria || []" :key="item">{{ item }}</li>
        </ul>
        <h4>المراحل المقترحة</h4>
        <article
          v-for="(item, index) in proposal.payload?.milestones || []"
          :key="index"
          class="proposal-milestone"
        >
          <strong>{{ index + 1 }}. {{ item.title }}</strong>
          <p>{{ item.description }}</p>
          <small>{{ item.tasks?.length || 0 }} مهام مقترحة · وزن {{ item.weight || 0 }}%</small>
        </article>
        <prime_message severity="warn" :closable="false"
          >لن يتم إنشاء المراحل والمهام إلا بعد الضغط على «اعتماد الخطة».</prime_message
        >
        <div class="dialog-actions">
          <prime_button
            label="رفض المقترح"
            severity="danger"
            text
            :loading="approving"
            @click="rejectPlan"
          /><prime_button
            label="اعتماد الخطة وإنشاء المراحل والمهام"
            icon="pi pi-check"
            :loading="approving"
            @click="approvePlan"
          />
        </div>
      </div>
    </prime_dialog>
  </main>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'
import { useGoalsStore } from '@/stores/goals/goalsStore'
import { useAppToast } from '@/composables/useAppToast'
import * as goalApi from '@/services/Goals/goals'
import { createTask, listTasks } from '@/services/Tasks/tasks'
import { getLearningGoals } from '@/services/Learning/learning'

// استيراد المكونات الجديدة المنفصلة
import GoalStats from '@/components/goals/GoalStats.vue'
import GoalsToolbar from '@/components/goals/GoalsToolbar.vue'
import GoalCard from '@/components/goals/GoalCard.vue'
import PageHeader from '@/components/ui/PageHeader.vue'
import StateBlock from '@/components/ui/StateBlock.vue'
import { revealChildren } from '@/composables/useMotion'

const store = useGoalsStore()
const toast = useAppToast()
// Staggered card entrance when a fresh set of goals finishes loading (GSAP, cleaned up on unmount).
const gridEl = ref(null)
let gridCtx = null
watch(
  () => store.loading,
  async (isLoading, wasLoading) => {
    if (isLoading || !wasLoading) return
    gridCtx?.revert()
    await nextTick()
    if (gridEl.value)
      gridCtx = revealChildren(gridEl.value, { selector: ':scope > *', y: 16, stagger: 0.05 })
  },
)
onBeforeUnmount(() => gridCtx?.revert())

const search = ref('')
const statusFilter = ref(null)
const categoryFilter = ref(null)
const sortBy = ref('-created_at')
const page = ref(1)
const pageSize = 20
const editorVisible = ref(false)
const detailsVisible = ref(false)
const milestoneVisible = ref(false)
const proposalVisible = ref(false)
const saving = ref(false)
const savingMilestone = ref(false)
const planning = ref(false)
const coachLoading = ref(false)
const coachQuestion = ref('')
const coachAnswer = ref(null)
const approving = ref(false)
const editingId = ref(null)
const selectedGoal = ref(null)
const milestones = ref([])
const linkedTasks = ref([])
const history = ref([])
const linkedProjects = ref([])
const learningGoalOptions = ref([])
const noteText = ref('')
const proposal = ref(null)
const planInstructions = ref('')
const form = reactive({
  title: '',
  description: '',
  category: 'personal',
  priority: 'medium',
  status: 'active',
  start_date: new Date().toISOString().slice(0, 10),
  target_date: '',
  estimated_minutes: 0,
  measurement_unit: '',
  initial_value: null,
  current_value: null,
  target_value: null,
  progress_percent: 0,
  learning_goals: [],
})
const milestoneForm = reactive({
  title: '',
  description: '',
  start_date: '',
  target_date: '',
  weight: 0,
  completion_criteria: '',
  completion_evidence: '',
  depends_on: [],
})

const analytics = computed(() => store.analytics)
const statusOptions = [
  { label: 'مسودة', value: 'draft' },
  { label: 'مخطط', value: 'planned' },
  { label: 'نشط', value: 'active' },
  { label: 'متوقف مؤقتًا', value: 'paused' },
  { label: 'معرض للخطر', value: 'at_risk' },
  { label: 'مكتمل', value: 'completed' },
  { label: 'ملغي', value: 'cancelled' },
  { label: 'مؤرشف', value: 'archived' },
]
const statusTransitions = {
  draft: ['planned', 'active', 'cancelled', 'archived'],
  planned: ['active', 'paused', 'cancelled', 'archived'],
  active: ['paused', 'at_risk', 'completed', 'cancelled', 'archived'],
  paused: ['active', 'at_risk', 'cancelled', 'archived'],
  at_risk: ['active', 'paused', 'completed', 'cancelled', 'archived'],
  completed: ['active', 'archived'],
  cancelled: ['archived'],
  archived: [],
}
const editableStatusOptions = computed(() => {
  const current = editingId.value
    ? store.items.find((item) => item.id === editingId.value)?.status
    : null
  if (!current)
    return statusOptions.filter((item) => !['completed', 'archived'].includes(item.value))
  const allowed = new Set([current, ...(statusTransitions[current] || [])])
  return statusOptions.filter((item) => allowed.has(item.value))
})
const categoryOptions = [
  { label: 'شخصي', value: 'personal' },
  { label: 'مهني', value: 'professional' },
  { label: 'تعليمي', value: 'educational' },
  { label: 'مالي', value: 'financial' },
  { label: 'صحة ولياقة', value: 'health' },
  { label: 'أعمال', value: 'business' },
  { label: 'مشروع', value: 'project' },
  { label: 'أخرى', value: 'other' },
]
const priorityOptions = [
  { label: 'منخفضة', value: 'low' },
  { label: 'متوسطة', value: 'medium' },
  { label: 'عالية', value: 'high' },
  { label: 'حرجة', value: 'critical' },
]
const sortOptions = [
  { label: 'الأحدث أولًا', value: '-created_at' },
  { label: 'الأقدم أولًا', value: 'created_at' },
  { label: 'أقرب موعد', value: 'target_date' },
  { label: 'أبعد موعد', value: '-target_date' },
  { label: 'الأعلى تقدمًا', value: '-progress_percent' },
]
const visibleGoals = computed(() =>
  store.items
    .filter(
      (goal) =>
        (!statusFilter.value || goal.status === statusFilter.value) &&
        (!categoryFilter.value || goal.category === categoryFilter.value) &&
        `${goal.title} ${goal.description || ''}`
          .toLowerCase()
          .includes(search.value.toLowerCase()),
    )
    .sort((a, b) => {
      const key = sortBy.value.replace('-', '')
      const factor = sortBy.value.startsWith('-') ? -1 : 1
      const av = a[key] ?? ''
      const bv = b[key] ?? ''
      return av > bv ? factor : av < bv ? -factor : 0
    }),
)

function statusLabel(value) {
  return statusOptions.find((item) => item.value === value)?.label || value
}
function categoryLabel(value) {
  return categoryOptions.find((item) => item.value === value)?.label || value
}
function priorityLabel(value) {
  return priorityOptions.find((item) => item.value === value)?.label || value
}
function statusSeverity(value) {
  return value === 'completed'
    ? 'success'
    : value === 'at_risk' || value === 'cancelled'
      ? 'danger'
      : value === 'paused'
        ? 'warn'
        : 'info'
}
function formatDateTime(value) {
  return new Date(value).toLocaleString('ar-EG')
}
function queryParams() {
  return {
    page: page.value,
    page_size: pageSize,
    ...(search.value.trim() ? { search: search.value.trim() } : {}),
    ...(statusFilter.value ? { status: statusFilter.value } : {}),
    ...(categoryFilter.value ? { category: categoryFilter.value } : {}),
    ordering: sortBy.value,
  }
}
async function loadGoals() {
  try {
    await store.fetchGoals(queryParams())
  } catch (error) {
    toast.error(error, 'تعذر تحميل الأهداف')
  }
}
async function refresh() {
  try {
    await Promise.all([loadGoals(), store.fetchAnalytics()])
  } catch (error) {
    toast.error(error, 'تعذر تحديث الأهداف')
  }
}
function onPage(event) {
  page.value = event.page + 1
  loadGoals()
}
function resetForm() {
  Object.assign(form, {
    title: '',
    description: '',
    category: 'personal',
    priority: 'medium',
    status: 'active',
    start_date: new Date().toISOString().slice(0, 10),
    target_date: '',
    estimated_minutes: 0,
    measurement_unit: '',
    initial_value: null,
    current_value: null,
    target_value: null,
    progress_percent: 0,
    learning_goals: [],
  })
}
function openCreate() {
  editingId.value = null
  resetForm()
  editorVisible.value = true
}
function openEdit(goal) {
  editingId.value = goal.id
  Object.assign(form, {
    title: goal.title,
    description: goal.description || '',
    category: goal.category || 'personal',
    priority: goal.priority,
    status: goal.status,
    start_date: goal.start_date,
    target_date: goal.target_date || '',
    estimated_minutes: goal.estimated_minutes || 0,
    measurement_unit: goal.measurement_unit || '',
    initial_value: goal.initial_value === null ? null : Number(goal.initial_value),
    current_value: goal.current_value === null ? null : Number(goal.current_value),
    target_value: goal.target_value === null ? null : Number(goal.target_value),
    progress_percent: goal.progress_percent || 0,
    learning_goals: goal.learning_goals || [],
  })
  editorVisible.value = true
}
async function saveGoal() {
  saving.value = true
  try {
    const payload = {
      ...form,
      target_date: form.target_date || null,
      initial_value: form.initial_value ?? null,
      current_value: form.current_value ?? null,
      target_value: form.target_value ?? null,
    }
    if (editingId.value) {
      const previous = store.items.find((item) => item.id === editingId.value)
      delete payload.progress_percent
      await goalApi.updateGoal(editingId.value, payload)
      if (previous && Number(previous.progress_percent) !== Number(form.progress_percent))
        await goalApi.updateGoalProgress(editingId.value, form.progress_percent)
      toast.success('تم تحديث الهدف.')
    } else {
      await goalApi.createGoal(payload)
      toast.success('تم إنشاء الهدف.')
    }
    editorVisible.value = false
    await refresh()
  } catch (error) {
    toast.error(error, 'تعذر حفظ الهدف')
  } finally {
    saving.value = false
  }
}
async function runAction(goal, action) {
  try {
    if (action === 'pause') await goalApi.pauseGoal(goal.id)
    else if (action === 'complete') await goalApi.completeGoal(goal.id)
    else if (action === 'archive') await goalApi.archiveGoal(goal.id)
    else await goalApi.resumeGoal(goal.id)
    toast.success('تم تحديث حالة الهدف.')
    await refresh()
  } catch (error) {
    toast.error(error)
  }
}
async function duplicate(goal) {
  try {
    await goalApi.duplicateGoal(goal.id)
    toast.success('تم إنشاء نسخة مسودة من الهدف.')
    await refresh()
  } catch (error) {
    toast.error(error)
  }
}
async function removeGoal(goal) {
  if (
    !window.confirm(
      `حذف الهدف «${goal.title}»؟ سيؤدي ذلك إلى حذف مراحله وسجل نشاطه، مع فك ارتباط المهام وفق إعداد قاعدة البيانات.`,
    )
  )
    return
  try {
    await goalApi.deleteGoal(goal.id)
    toast.success('تم حذف الهدف.')
    await refresh()
  } catch (error) {
    toast.error(error)
  }
}
async function openDetails(goal) {
  selectedGoal.value = goal
  detailsVisible.value = true
  planInstructions.value = ''
  await loadDetails()
}
async function loadDetails() {
  if (!selectedGoal.value) return
  try {
    const [detail, stageData, taskData, historyData, projectsData] = await Promise.all([
      goalApi.getGoal(selectedGoal.value.id),
      goalApi.listGoalMilestones(selectedGoal.value.id),
      listTasks({ goal_id: selectedGoal.value.id }),
      goalApi.getGoalHistory(selectedGoal.value.id),
      goalApi.listGoalProjects(selectedGoal.value.id),
    ])
    selectedGoal.value = detail
    milestones.value = stageData
    linkedTasks.value = taskData
    history.value = historyData
    linkedProjects.value = projectsData
  } catch (error) {
    toast.error(error, 'تعذر تحميل تفاصيل الهدف')
  }
}

watch([search, statusFilter, categoryFilter, sortBy], () => {
  page.value = 1
  loadGoals()
})
onMounted(async () => {
  await refresh()
  try {
    learningGoalOptions.value = await getLearningGoals()
  } catch (error) {
    toast.error(error, 'تعذر تحميل أهداف التعلم')
  }
})
</script>

<style src="@/assets/scss/Goals/GoalsView.scss" lang="scss"></style>
