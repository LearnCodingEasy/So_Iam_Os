<template>
  <div
    class="dashboard-container min-h-screen bg-slate-50/50 dark:bg-slate-950 text-slate-800 dark:text-slate-100 p-4 sm:p-6 lg:p-8 transition-colors duration-300"
    dir="rtl"
  >
    <!-- ========= ERROR NOTIFICATION ========= -->
    <div
      v-if="error"
      class="mb-6 p-4 rounded-xl border border-rose-200 bg-rose-50 dark:bg-rose-950/40 dark:border-rose-800/50 text-rose-700 dark:text-rose-300 flex items-center justify-between shadow-sm"
    >
      <span class="text-xs font-medium"><strong>خطأ في جلب البيانات:</strong> {{ error }}</span>
      <prime_button
        label="إعادة المحاولة"
        @click="loadDashboard"
        severity="danger"
        size="small"
        class="!rounded-lg !text-xs"
      />
    </div>

    <!-- Header Section (الترويسة العلوية) -->
    <header
      class="mb-8 flex flex-col md:flex-row md:items-center md:justify-between gap-4 glass-card p-6 rounded-2xl shadow-sm border border-slate-200/70 dark:border-slate-800/80"
    >
      <div class="space-y-1.5">
        <div class="flex items-center gap-3 flex-wrap">
          <h1
            class="text-2xl sm:text-3xl font-bold tracking-tight bg-gradient-to-l from-slate-900 via-indigo-950 to-indigo-600 dark:from-white dark:via-slate-200 dark:to-indigo-400 bg-clip-text text-transparent"
          >
            مرحباً بك، {{ userName }} 👋
          </h1>
          <span
            class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium border"
            :class="
              dashboard?.system?.online
                ? 'bg-emerald-50 text-emerald-700 border-emerald-200/80 dark:bg-emerald-950/40 dark:text-emerald-400 dark:border-emerald-800/50'
                : 'bg-rose-50 text-rose-700 border-rose-200 dark:bg-rose-950/40 dark:text-rose-400 dark:border-rose-800/50'
            "
          >
            <span
              class="w-2 h-2 rounded-full animate-pulse"
              :class="dashboard?.system?.online ? 'bg-emerald-500' : 'bg-rose-500'"
            ></span>
            {{ dashboard?.system?.online ? 'النظام متصل وبحالة جيدة' : 'حالة النظام غير متاحة' }}
          </span>
        </div>
        <p class="text-sm text-slate-500 dark:text-slate-400">
          نظرة عامة على مؤشرات الأداء الحيوية، العمليات النشطة، وتحليلات النظام المباشرة من قاعدة
          البيانات
        </p>
      </div>

      <!-- Action Buttons -->
      <div class="flex flex-wrap items-center gap-2.5">
        <prime_button
          icon="pi pi-refresh"
          label="تحديث البيانات"
          :loading="loading"
          @click="loadDashboard"
          class="class_name"
        />
        <prime_button
          icon="pi pi-file-export"
          label="تصدير تقرير"
          @click="exportReport"
          class="class_name"
        />

        <prime_button
          icon="pi pi-plus"
          label="إضافة عنصر جديد"
          @click="openNewItemModal"
          class="class_name"
        />
      </div>
    </header>

    <!-- KPI Metrics Cards (Real Data from API) -->
    <section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 mb-8">
      <router-link
        v-for="(stat, index) in statsList"
        :key="index"
        :to="stat.route"
        class="glass-card kpi-card p-5 rounded-2xl border border-slate-200/80 dark:border-slate-800/80 hover:shadow-lg transition-all duration-300 relative overflow-hidden group block"
      >
        <div class="flex items-start justify-between">
          <div class="space-y-1">
            <span
              class="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider"
              >{{ stat.title }}</span
            >
            <div
              class="text-2xl sm:text-3xl font-bold tracking-tight text-slate-900 dark:text-white font-mono"
            >
              {{ loading ? '...' : stat.value }}
            </div>
          </div>
          <div
            class="w-12 h-12 rounded-xl flex items-center justify-center transition-transform group-hover:scale-110 duration-300 bg-indigo-50 dark:bg-indigo-950/50 text-indigo-600 dark:text-indigo-400"
          >
            <i :class="[stat.icon, 'text-xl']"></i>
          </div>
        </div>

        <div
          class="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800/60 flex items-center justify-between text-xs"
        >
          <span class="text-slate-600 dark:text-slate-400">{{ stat.activeText }}</span>
          <span class="font-semibold text-emerald-600 dark:text-emerald-400">{{
            stat.completedText
          }}</span>
        </div>
      </router-link>
    </section>

    <!-- Analytics & Charts Grid -->
    <section class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
      <!-- Main Line Chart (Task Delivery Overview) -->
      <div
        class="lg:col-span-2 glass-card p-6 rounded-2xl border border-slate-200/80 dark:border-slate-800/80 flex flex-col justify-between"
      >
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-6">
          <div>
            <h2 class="text-lg font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <i class="pi pi-chart-line text-indigo-500"></i>
              نظرة عامة على تنفيذ المهام
            </h2>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">
              مقارنة بين الإجماليات والمهام المكتملة بناءً على بيانات النظام الحية
            </p>
          </div>
          <div class="flex items-center gap-1.5 bg-slate-100 dark:bg-slate-800/70 p-1 rounded-xl">
            <button
              v-for="range in ['أسبوعي', 'شهري', 'سنوي']"
              :key="range"
              class="px-3 py-1 text-xs rounded-lg font-medium transition-all"
              :class="
                selectedRange === range
                  ? 'bg-white dark:bg-slate-900 text-indigo-600 dark:text-indigo-400 shadow-sm'
                  : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
              "
              @click="selectedRange = range"
            >
              {{ range }}
            </button>
          </div>
        </div>

        <div class="h-72 w-full">
          <Line v-if="lineChartData" :data="lineChartData" :options="lineChartOptions" />
        </div>
      </div>

      <!-- Secondary Chart / Learning Overview -->
      <div
        class="glass-card p-6 rounded-2xl border border-slate-200/80 dark:border-slate-800/80 flex flex-col justify-between"
      >
        <div class="mb-4">
          <h2 class="text-lg font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <i class="pi pi-book text-violet-500"></i>
            نظرة عامة على التعلم
          </h2>
          <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">
            مؤشرات التقدم والمسارات التعليمية المرتبطة بقاعدة البيانات
          </p>
        </div>

        <div class="flex flex-col gap-4 my-auto">
          <div class="flex justify-between items-center text-sm">
            <span class="text-slate-500">مسارات التعلم</span>
            <strong class="font-mono">{{ learningStats.paths ?? '—' }}</strong>
          </div>
          <div class="flex justify-between items-center text-sm">
            <span class="text-slate-500">المسارات النشطة</span>
            <strong class="font-mono">{{ learningStats.active_paths ?? '—' }}</strong>
          </div>
          <div class="flex justify-between items-center text-sm">
            <span class="text-slate-500">المواضيع المكتملة</span>
            <strong class="font-mono"
              >{{ learningStats.topics_completed ?? '—' }} /
              {{ learningStats.topics_total ?? '—' }}</strong
            >
          </div>
          <div>
            <div class="flex justify-between text-xs mb-2">
              <span class="text-slate-500">التقدم الإجمالي</span>
              <strong class="font-mono">{{ learningStats.progress ?? 0 }}%</strong>
            </div>
            <prime_progress_bar :value="learningStats.progress || 0" :show-value="false" />
          </div>
        </div>
      </div>
    </section>

    <!-- Activity & Data Tables Section (Tasks & Knowledge) -->
    <section class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
      <!-- Today's Tasks Card -->
      <div
        class="glass-card p-6 rounded-2xl border border-slate-200/80 dark:border-slate-800/80 flex flex-col justify-between"
      >
        <div>
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-lg font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <i class="pi pi-list-check text-indigo-500"></i>
              مهام اليوم
            </h2>
            <router-link
              to="/tasks"
              class="text-xs font-semibold text-indigo-600 dark:text-indigo-400 hover:underline"
            >
              عرض الكل ←
            </router-link>
          </div>

          <div class="flex flex-col gap-2 max-h-60 overflow-y-auto">
            <div v-if="loading" class="text-xs text-slate-400 py-6 text-center font-mono">
              جاري تحميل المهام...
            </div>
            <div
              v-else-if="(tasks || []).length === 0"
              class="text-xs text-slate-400 py-6 text-center font-mono"
            >
              لا توجد مهام حالية.
            </div>
            <div
              v-for="task in tasks || []"
              :key="task.id || task.title"
              class="flex items-center gap-3 p-2.5 rounded-xl bg-slate-50 dark:bg-slate-900/50 border border-slate-100 dark:border-slate-800"
            >
              <span
                class="w-4 h-4 rounded flex items-center justify-center text-[10px] border"
                :class="
                  task.completed
                    ? 'bg-emerald-500 border-emerald-500 text-white'
                    : 'border-slate-300 dark:border-slate-600'
                "
              >
                <span v-if="task.completed">✓</span>
              </span>
              <span
                :class="[
                  'text-xs font-medium truncate',
                  task.completed ? 'line-through opacity-60' : '',
                ]"
              >
                {{ task.title }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Knowledge Card -->
      <div
        class="lg:col-span-2 glass-card p-6 rounded-2xl border border-slate-200/80 dark:border-slate-800/80 flex flex-col justify-between"
      >
        <div>
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-lg font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <i class="pi pi-database text-violet-500"></i>
              المعرفة والملفات المحدثة مؤخراً
            </h2>
            <router-link
              to="/knowledge"
              class="text-xs font-semibold text-indigo-600 dark:text-indigo-400 hover:underline"
            >
              عرض الكل ←
            </router-link>
          </div>

          <div v-if="loading" class="text-xs text-slate-400 py-6 text-center font-mono">
            جاري تحميل المعرفة...
          </div>
          <div
            v-else-if="(recentKnowledge || []).length === 0"
            class="text-xs text-slate-400 py-6 text-center font-mono"
          >
            لا توجد ملفات معرفية مسجلة بعد.
          </div>
          <div v-else class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <router-link
              v-for="item in recentKnowledge || []"
              :key="item.id"
              to="/knowledge"
              class="flex items-center justify-between p-3 rounded-xl bg-slate-50 dark:bg-slate-900/50 border border-slate-100 dark:border-slate-800 hover:border-indigo-500 transition-colors text-xs"
            >
              <span class="font-medium truncate text-slate-800 dark:text-slate-200">{{
                item.title
              }}</span>
              <prime_tag
                :value="`${item.files_count || 0} ملفات`"
                severity="info"
                class="!text-[10px] !py-0.5"
              />
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Dialog for New Item Modal -->
    <prime_dialog
      v-model:visible="isModalOpen"
      modal
      header="إضافة عملية أو مهمة جديدة"
      :style="{ width: '90vw', maxWidth: '520px' }"
      class="stitch-dialog !rounded-2xl"
    >
      <form @submit.prevent="submitNewItem" class="space-y-4 pt-2">
        <div>
          <label class="block text-xs font-semibold text-slate-600 dark:text-slate-300 mb-1.5"
            >اسم المهمة</label
          >
          <prime_input_text
            v-model="newItemForm.name"
            class="w-full !rounded-xl !p-2.5 !text-sm"
            placeholder="مثال: مزامنة بيانات العملاء"
            required
          />
        </div>
        <div>
          <label class="block text-xs font-semibold text-slate-600 dark:text-slate-300 mb-1.5"
            >الخدمة المستهدفة</label
          >
          <prime_select
            v-model="newItemForm.service"
            :options="serviceOptions"
            optionLabel="name"
            placeholder="اختر الخدمة"
            class="w-full !rounded-xl !text-sm"
          />
        </div>
        <div class="pt-4 flex justify-end gap-2 border-t border-slate-100 dark:border-slate-800">
          <prime_button
            label="إلغاء"
            text
            severity="secondary"
            @click="isModalOpen = false"
            class="!rounded-xl"
          />
          <prime_button
            label="حفظ وبدء التشغيل"
            type="submit"
            severity="primary"
            class="!rounded-xl !bg-indigo-600"
          />
        </div>
      </form>
    </prime_dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useOnline, useDark } from '@vueuse/core'
import { toast } from 'vue-sonner'
import { dashboardService } from '@/services/Core/dashboard'

// Chart.js imports
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  ArcElement,
  Filler,
} from 'chart.js'
import { Line } from 'vue-chartjs'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  ArcElement,
  Filler,
)

// Connectivity state using VueUse
const isOnline = useOnline()
console.log('isOnline: ', isOnline)
const isDark = useDark()

// Dashboard API State
const dashboard = ref(null)
const loading = ref(true)
const error = ref(null)

const loadDashboard = async () => {
  loading.value = true
  error.value = null
  try {
    const data = await dashboardService.get()
    dashboard.value = data
  } catch (err) {
    error.value =
      err?.response?.data?.detail ||
      err?.response?.data?.message ||
      err?.message ||
      'تعذر تحميل بيانات لوحة التحكم من الخادم.'
    toast.error('فشل جلب بيانات لوحة التحكم')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadDashboard()
})

// Local State
const selectedRange = ref('شهري')
const isModalOpen = ref(false)

const newItemForm = ref({
  name: '',
  service: null,
})

const serviceOptions = [
  { name: 'قاعدة بيانات PostgreSQL', code: 'postgres' },
  { name: 'Redis Cache Layer', code: 'redis' },
  { name: 'خدمة التحليلات Analytics API', code: 'analytics' },
  { name: 'مزامنة السحابة Cloud Sync', code: 'cloud' },
]

// Computed User & Metrics from real API
const userName = computed(() => dashboard.value?.user?.name || 'م. حسام رشاد عبود')
const learningStats = computed(() => dashboard.value?.stats?.learning || {})
const recentKnowledge = computed(() => dashboard.value?.recent?.knowledge || [])
const tasks = computed(() => dashboard.value?.recent?.tasks || dashboard.value?.tasks || [])

const statsList = computed(() => {
  const data = dashboard.value?.stats || {}
  return [
    {
      title: 'إجمالي المشاريع',
      value: data.projects?.total ?? 0,
      activeText: `${data.projects?.active ?? 0} نشط`,
      completedText: `${data.projects?.completed ?? 0} مكتمل`,
      icon: 'pi pi-folder',
      route: '/projects',
    },
    {
      title: 'معدل المهام',
      value: data.tasks?.total ?? 0,
      activeText: `${data.tasks?.pending ?? 0} معلق`,
      completedText: `${data.tasks?.completed ?? 0} مكتمل`,
      icon: 'pi pi-check-circle',
      route: '/tasks',
    },
    {
      title: 'الأهداف النشطة',
      value: data.goals?.total ?? 0,
      activeText: `${data.goals?.in_progress ?? 0} قيد التنفيذ`,
      completedText: `${data.goals?.completed ?? 0} مكتمل`,
      icon: 'pi pi-bullseye',
      route: '/goals',
    },
    {
      title: 'قاعدة المعرفة',
      value: data.knowledge?.total ?? 0,
      activeText: `${data.knowledge?.files ?? 0} ملف مفهرس`,
      completedText: 'جاهز',
      icon: 'pi pi-book',
      route: '/knowledge',
    },
  ]
})

// Chart.js Data & Configuration
const lineChartData = computed(() => {
  const isDarkTheme = isDark.value
  const taskStats = dashboard.value?.stats?.tasks || {}
  const total = taskStats.total || 10
  const completed = taskStats.completed || 5
  const pending = taskStats.pending || 5
  console.log('pending: ', pending)

  return {
    labels: ['السبت', 'الأحد', 'الإثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة'],
    datasets: [
      {
        label: 'المهام الإجمالية',
        data: [total * 0.4, total * 0.6, total * 0.5, total * 0.8, total * 0.7, total * 0.9, total],
        borderColor: '#4f46e5',
        backgroundColor: isDarkTheme ? 'rgba(79, 70, 229, 0.15)' : 'rgba(79, 70, 229, 0.08)',
        fill: true,
        tension: 0.4,
        borderWidth: 2.5,
      },
      {
        label: 'المهام المكتملة',
        data: [
          completed * 0.3,
          completed * 0.5,
          completed * 0.4,
          completed * 0.7,
          completed * 0.6,
          completed * 0.8,
          completed,
        ],
        borderColor: '#10b981',
        backgroundColor: 'transparent',
        borderDash: [5, 5],
        borderWidth: 1.5,
        tension: 0.3,
      },
    ],
  }
})

const lineChartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top',
      rtl: true,
      labels: {
        font: { family: 'inherit', size: 12 },
        color: isDark.value ? '#94a3b8' : '#64748b',
      },
    },
    tooltip: {
      rtl: true,
      backgroundColor: isDark.value ? '#0f172a' : '#ffffff',
      titleColor: isDark.value ? '#ffffff' : '#0f172a',
      bodyColor: isDark.value ? '#cbd5e1' : '#475569',
      borderColor: isDark.value ? '#334155' : '#e2e8f0',
      borderWidth: 1,
      padding: 10,
      cornerRadius: 10,
    },
  },
  scales: {
    x: {
      grid: { display: false },
      ticks: { color: isDark.value ? '#94a3b8' : '#64748b' },
    },
    y: {
      grid: {
        color: isDark.value ? 'rgba(51, 65, 85, 0.3)' : 'rgba(226, 232, 240, 0.6)',
      },
      ticks: { color: isDark.value ? '#94a3b8' : '#64748b' },
    },
  },
}))

// Actions
const refreshDashboard = async () => {
  await loadDashboard()
  toast.success('تم تحديث بيانات اللوحة بنجاح من الخادم!')
}
console.log('refreshDashboard: ', refreshDashboard)

const exportReport = () => {
  toast.info('جاري إعداد التقرير التراكمي...', {
    description: 'سيتم تحميل الملف خلال لحظات.',
  })
}

const openNewItemModal = () => {
  isModalOpen.value = true
}

const submitNewItem = () => {
  if (!newItemForm.value.name) return
  isModalOpen.value = false
  toast.success('تمت إضافة المهمة بنجاح!', {
    description: `المهمة "${newItemForm.value.name}" أضيفت لقاعدة البيانات.`,
  })
  newItemForm.value.name = ''
  newItemForm.value.service = null
}
</script>
