<template>
  <div class="workspace-page">
    <header class="workspace-header">
      <div>
        <span class="eyebrow">Execution</span>
        <h1>Today's Tasks</h1>
        <p>كل ما تحتاج تنفذه اليوم في مكان واحد.</p>
      </div>
      <div class="header-actions">
        <button class="primary-btn" :disabled="generating" @click="generate">{{ generating ? 'جارٍ التوليد…' : '✦ Generate AI Tasks' }}</button
        ><button class="primary-btn" @click="openCreate">＋ مهمة جديدة</button>
      </div>
    </header>
    <div v-if="error" class="alert error">{{ error }}</div>
    <div v-if="success" class="alert success">{{ success }}</div>
    <section class="task-layout">
      <div class="content-card">
        <div class="task-toolbar">
          <strong>{{ tasks.length }} مهام اليوم</strong
          ><select v-model="filter">
            <option value="all">الكل</option>
            <option value="pending">Pending</option>
            <option value="in_progress">In Progress</option>
            <option value="completed">Completed</option>
            <option value="postponed">Postponed</option>
          </select>
        </div>
        <div v-if="loading" class="loading">جاري التحميل...</div>
        <div v-else-if="tasks.length === 0 && !error" class="empty">
          مفيش مهام لليوم. ممتاز! أو أنشئ مهمة جديدة.
        </div>
        <div v-else class="task-list">
          <article
            v-for="task in visibleTasks"
            :key="task.id"
            class="task-row"
            :class="task.status"
          >
            <button class="check" :disabled="task.status === 'completed' || busyTaskId === task.id" @click="finish(task)">
              {{ task.status === 'completed' ? '✓' : '○' }}
            </button>
            <div class="task-body">
              <div class="task-title">
                <h3>{{ task.title }}</h3>
                <span class="pill">{{ task.priority_display || task.priority }}</span>
              </div>
              <p>{{ task.description || 'بدون وصف' }}</p>
              <div class="task-meta">
                <span v-if="task.scheduled_start">🕒 {{ task.scheduled_start }}</span
                ><span>⏱ {{ task.estimated_minutes || 0 }}m</span
                ><span v-if="task.overdue" class="overdue">متأخرة</span>
              </div>
            </div>
            <div class="task-actions">
              <button v-if="task.status === 'completed'" :disabled="busyTaskId === task.id" @click="reopen(task)">إعادة فتح</button
              ><button v-else :disabled="busyTaskId === task.id" @click="openPostpone(task)">تأجيل</button
              ><button :disabled="busyTaskId === task.id" @click="editTask(task)">تعديل</button
              ><button class="danger" :disabled="busyTaskId === task.id" @click="removeTask(task)">حذف</button>
            </div>
          </article>
        </div>
      </div>
      <aside class="content-card summary">
        <h2>ملخص اليوم</h2>
        <div class="ring">
          <strong>{{ completion }}%</strong><span>إنجاز</span>
        </div>
        <div class="summary-line">
          <span>Completed</span><strong>{{ completed }}</strong>
        </div>
        <div class="summary-line">
          <span>Remaining</span><strong>{{ Math.max(tasks.length - completed, 0) }}</strong>
        </div>
        <div class="summary-line">
          <span>Estimated</span><strong>{{ estimated }}m</strong>
        </div>
      </aside>
    </section>
    <div v-if="dialog" class="modal-backdrop" @click.self="dialog = false">
      <form class="modal-card" @submit.prevent="save">
        <div class="modal-head">
          <h2>{{ editing ? 'تعديل المهمة' : 'مهمة جديدة' }}</h2>
          <button type="button" @click="dialog = false">×</button>
        </div>
        <label>العنوان<input v-model.trim="form.title" required /></label
        ><label>الوصف<textarea v-model="form.description" rows="3"></textarea></label>
        <div class="form-grid">
          <label>التاريخ<input v-model="form.scheduled_date" type="date" required /></label
          ><label>وقت البداية<input v-model="form.scheduled_start" type="time" /></label
          ><label
            >الأولوية<select v-model="form.priority">
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="critical">Critical</option>
            </select></label
          ><label
            >الحالة<select v-model="form.status">
              <option value="pending">Pending</option>
              <option value="in_progress">In Progress</option>
              <option value="postponed">Postponed</option>
              <option value="cancelled">Cancelled</option>
            </select></label
          ><label
            >المدة المتوقعة<input v-model.number="form.estimated_minutes" type="number" min="0"
          /></label>
        </div>
        <div class="modal-actions">
          <button type="button" @click="dialog = false">إلغاء</button
          ><button class="primary-btn">حفظ</button>
        </div>
      </form>
    </div>
    <div v-if="postponeDialog" class="modal-backdrop" @click.self="postponeDialog = false">
      <form class="modal-card small" @submit.prevent="postpone">
        <h2>تأجيل المهمة</h2>
        <label>اليوم الجديد<input v-model="postponeDate" type="date" required /></label>
        <div class="modal-actions">
          <button type="button" @click="postponeDialog = false">إلغاء</button
          ><button class="primary-btn">تأجيل</button>
        </div>
      </form>
    </div>
  </div>
</template>
<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import {
  completeTask,
  createTask,
  deleteTask,
  listTodayTasks,
  postponeTask,
  updateTask,
  generateTodayTasks,
  reopenTask,
} from '@/services/Tasks/tasks'
const tasks = ref([]),
  loading = ref(false),
  dialog = ref(false),
  postponeDialog = ref(false),
  editing = ref(null),
  postponing = ref(null),
  filter = ref('all'),
  error = ref(''),
  success = ref(''),
  postponeDate = ref(''),
  busyTaskId = ref(null),
  generating = ref(false)
const form = reactive({
  title: '',
  description: '',
  scheduled_date: new Date().toISOString().slice(0, 10),
  scheduled_start: '',
  priority: 'medium',
  status: 'pending',
  estimated_minutes: 0,
})
const completed = computed(() => tasks.value.filter((t) => t.status === 'completed').length),
  completion = computed(() =>
    tasks.value.length ? Math.round((completed.value / tasks.value.length) * 100) : 0,
  ),
  estimated = computed(() => tasks.value.reduce((a, t) => a + Number(t.estimated_minutes || 0), 0)),
  visibleTasks = computed(() =>
    filter.value === 'all' ? tasks.value : tasks.value.filter((t) => t.status === filter.value),
  )
const generate = async () => {
  if (generating.value) return
  generating.value = true
  error.value = ''
  try {
    await generateTodayTasks({ async: true })
    success.value = 'تم إرسال توليد المهام إلى الخلفية.'
    setTimeout(load, 1500)
  } catch (e) {
    error.value = e.response?.data?.detail || 'تعذر توليد المهام.'
  } finally { generating.value = false }
}
const load = async () => {
  loading.value = true
  error.value = ''
  try {
    tasks.value = await listTodayTasks()
  } catch (e) {
    error.value = e.response?.data?.detail || 'تعذر تحميل المهام.'
  } finally {
    loading.value = false
  }
}
const reset = () =>
  Object.assign(form, {
    title: '',
    description: '',
    scheduled_date: new Date().toISOString().slice(0, 10),
    scheduled_start: '',
    priority: 'medium',
    status: 'pending',
    estimated_minutes: 0,
  })
const openCreate = () => {
  editing.value = null
  reset()
  dialog.value = true
}
const editTask = (t) => {
  editing.value = t.id
  Object.assign(form, {
    title: t.title,
    description: t.description,
    scheduled_date: t.scheduled_date,
    scheduled_start: t.scheduled_start || '',
    priority: t.priority,
    status: t.status,
    estimated_minutes: t.estimated_minutes || 0,
  })
  dialog.value = true
}
const save = async () => {
  error.value = ''
  try {
    const payload = { ...form, scheduled_start: form.scheduled_start || null }
    editing.value ? await updateTask(editing.value, payload) : await createTask(payload)
    dialog.value = false
    success.value = 'تم حفظ المهمة.'
    await load()
  } catch (e) {
    error.value = e.response?.data?.detail || 'تعذر حفظ المهمة.'
  }
}
const finish = async (t) => {
  if (busyTaskId.value !== null) return
  busyTaskId.value = t.id
  error.value = ''
  try {
    await completeTask(t.id, t.actual_minutes || t.estimated_minutes || 0)
    success.value = 'تم إكمال المهمة.'
    await load()
  } catch (e) {
    error.value = e.response?.data?.detail || 'تعذر إكمال المهمة.'
  } finally { busyTaskId.value = null }
}
const reopen = async (task) => {
  if (busyTaskId.value !== null) return
  busyTaskId.value = task.id
  error.value = ''
  try {
    await reopenTask(task.id)
    success.value = 'تمت إعادة فتح المهمة.'
    await load()
  } catch (e) {
    error.value = e.response?.data?.detail || 'تعذر إعادة فتح المهمة.'
  } finally {
    busyTaskId.value = null
  }
}
const openPostpone = (t) => {
  postponing.value = t.id
  postponeDate.value = new Date(Date.now() + 86400000).toISOString().slice(0, 10)
  postponeDialog.value = true
}
const postpone = async () => {
  busyTaskId.value = postponing.value
  error.value = ''
  try {
    await postponeTask(postponing.value, postponeDate.value)
    postponeDialog.value = false
    success.value = 'تم تأجيل المهمة.'
    await load()
  } catch (e) {
    error.value = e.response?.data?.detail || 'تعذر تأجيل المهمة.'
  } finally { busyTaskId.value = null }
}
const removeTask = async (t) => {
  if (busyTaskId.value !== null) return
  if (!window.confirm(`حذف المهمة "${t.title}"؟`)) return
  busyTaskId.value = t.id
  try {
    await deleteTask(t.id)
    await load()
  } catch (e) {
    error.value = e.response?.data?.detail || 'تعذر حذف المهمة.'
  } finally { busyTaskId.value = null }
}
onMounted(load)
</script>

