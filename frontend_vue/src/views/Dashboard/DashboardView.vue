<template>
  <div class="dashboard-page">
    <header class="page-head">
      <div>
        <span class="eyebrow">SO_IAM_OS · LIVE</span>
        <h1>لوحة التحكم</h1>
        <p>كل الأرقام هنا جاية من Django و Database مباشرة.</p>
      </div>
      <Button label="تحديث" icon="pi pi-refresh" :loading="loading" @click="load" />
    </header>
    <Message v-if="error" severity="error" :closable="false">{{ error }}</Message>
    <div v-if="loading && !data" class="stats">
      <Skeleton v-for="i in 6" :key="i" height="110px" />
    </div>
    <template v-else-if="data">
      <section class="stats">
        <Card v-for="item in statCards" :key="item.label"
          ><template #content
            ><span>{{ item.label }}</span
            ><strong>{{ item.value }}</strong
            ><small>{{ item.note }}</small></template
          ></Card
        >
      </section>
      <section class="grid">
        <Card
          ><template #title>Today's Tasks</template
          ><template #content
            ><DataTable :value="data.tasks" size="small"
              ><Column field="title" header="Task" /><Column field="status" header="Status"
                ><template #body="slot"><Tag :value="slot.data.status" /></template></Column
              ><Column field="priority" header="Priority" /></DataTable
            ><Message v-if="!data.tasks.length" severity="secondary"
              >مفيش Tasks النهارده.</Message
            ></template
          ></Card
        >
        <Card
          ><template #title>Job Opportunities</template
          ><template #content
            ><div v-for="job in data.recent.jobs" :key="job.id" class="job">
              <div>
                <strong>{{ job.title }}</strong
                ><span>{{ job.company || '—' }}</span>
              </div>
              <Tag v-if="job.is_remote" value="Remote" severity="success" />
            </div>
            <Message v-if="!data.recent.jobs.length" severity="secondary"
              >لا توجد فرص محفوظة بعد.</Message
            ></template
          ></Card
        >
      </section>
      <section class="grid">
        <Card
          ><template #title>Learning</template
          ><template #content
            ><div class="big">{{ data.stats.learning.active_paths }}</div>
            <span>مسارات تعلم نشطة</span></template
          ></Card
        >
        <Card
          ><template #title>Knowledge</template
          ><template #content
            ><div class="big">{{ data.stats.knowledge.total }}</div>
            <span>{{ data.stats.knowledge.files }} ملف مرتبط</span></template
          ></Card
        >
        <Card
          ><template #title>Goals</template
          ><template #content
            ><div class="big">{{ data.stats.goals.in_progress }}</div>
            <span>{{ data.stats.goals.completed }} مكتملة</span></template
          ></Card
        >
      </section>
    </template>
  </div>
</template>
<script setup>
import { computed, onMounted, ref } from 'vue'
import Button from 'primevue/button'
import Card from 'primevue/card'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Tag from 'primevue/tag'
import Message from 'primevue/message'
import Skeleton from 'primevue/skeleton'
import { dashboardService } from '@/services/dashboard'
const data = ref(null),
  loading = ref(false),
  error = ref('')
const statCards = computed(() =>
  data.value
    ? [
        {
          label: 'Tasks Today',
          value: data.value.stats.tasks.today,
          note: `${data.value.stats.tasks.pending} pending`,
        },
        {
          label: 'Goals',
          value: data.value.stats.goals.total,
          note: `${data.value.stats.goals.completed} completed`,
        },
        {
          label: 'Learning Paths',
          value: data.value.stats.learning.paths,
          note: `${data.value.stats.learning.active_paths} active`,
        },
        {
          label: 'Knowledge',
          value: data.value.stats.knowledge.total,
          note: `${data.value.stats.knowledge.files} files`,
        },
        { label: 'Job Matches', value: data.value.stats.jobs.matches, note: '70%+ compatibility' },
        { label: 'Skills', value: data.value.stats.skills.total, note: 'linked learning skills' },
      ]
    : [],
)
async function load() {
  loading.value = true
  error.value = ''
  try {
    data.value = await dashboardService.get()
  } catch (e) {
    error.value = e.response?.data?.detail || 'تعذر تحميل Dashboard.'
  } finally {
    loading.value = false
  }
}
onMounted(load)
</script>

<style scoped>
.dashboard-page {
  max-width: 1440px;
  margin: auto;
  padding: 32px;
}
.page-head {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 24px;
}
.eyebrow {
  font-size: 12px;
  letter-spacing: 0.14em;
  color: #60a5fa;
}
.page-head h1 {
  font-size: 34px;
  margin: 6px 0;
}
.page-head p {
  color: #94a3b8;
}
.stats {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 14px;
  margin-bottom: 18px;
}
.stats :deep(.p-card) {
  height: 100%;
}
.stats span,
.stats small {
  display: block;
  color: #94a3b8;
}
.stats strong {
  display: block;
  font-size: 30px;
  margin: 8px 0;
}
.grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 18px;
  margin-bottom: 18px;
}
.grid:last-child {
  grid-template-columns: repeat(3, 1fr);
}
.job {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 13px 0;
  border-bottom: 1px solid var(--p-content-border-color);
}
.job span {
  display: block;
  color: #94a3b8;
  font-size: 13px;
}
.big {
  font-size: 42px;
  font-weight: 800;
}
@media (max-width: 1000px) {
  .stats {
    grid-template-columns: repeat(3, 1fr);
  }
}
@media (max-width: 700px) {
  .dashboard-page {
    padding: 18px;
  }
  .page-head {
    flex-direction: column;
  }
  .stats,
  .grid,
  .grid:last-child {
    grid-template-columns: 1fr;
  }
}
</style>
