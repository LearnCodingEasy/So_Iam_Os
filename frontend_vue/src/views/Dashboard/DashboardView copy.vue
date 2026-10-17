<template>
  <div class="dashboard_page">
    <!-- Start Card -->
    <prime_card class="header_control" style="width: 100%; overflow: hidden">
      <template #header>
        <div class="header_control_text">
          <span class="eyebrow"
            >SO IAM OS
            <prime_tag value="LIVE" severity="danger" rounded />
          </span>
          <p>كل الأرقام هنا جاية من Django و Database مباشرة.</p>
          <h1>لوحة التحكم</h1>
        </div>
      </template>

      <template #footer>
        <div class="header_control_btn">
          <prime_button
            label="تحديث"
            icon="pi pi-refresh"
            :loading="loading"
            @click="load"
            class="w-full"
          />
        </div>
      </template>
    </prime_card>
    <!-- End Card -->
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
