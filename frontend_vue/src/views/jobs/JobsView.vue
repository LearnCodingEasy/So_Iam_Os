<template>
  <div class="jobs-page">
    <header class="hero">
      <div>
        <span class="eyebrow">CAREER INTELLIGENCE</span>
        <h1>Jobs Opportunity OS</h1>
        <p>
          اكتشاف الوظائف، تحليل الـ Skill Gap، التعلم، التقديم، المقابلات والتحليلات في مساحة واحدة.
        </p>
      </div>
      <div class="hero-actions">
        <Button label="تحديث الكل" icon="pi pi-sync" :loading="busy" @click="refreshAllData" />
        <Button label="إضافة وظيفة" icon="pi pi-plus" severity="secondary" @click="openCreate" />
      </div>
    </header>

    <Message v-if="error" severity="error" closable @close="error = ''">{{ error }}</Message>

    <section class="stats" v-if="dashboard">
      <Card v-for="item in statCards" :key="item.label" class="stat-card">
        <template #content>
          <span>{{ item.label }}</span>
          <strong>{{ item.value }}</strong>
        </template>
      </Card>
    </section>

    <nav class="tabs">
      <Button
        v-for="tab in tabs"
        :key="tab.key"
        :label="tab.label"
        :icon="tab.icon"
        :severity="activeTab === tab.key ? 'primary' : 'secondary'"
        :outlined="activeTab !== tab.key"
        @click="activeTab = tab.key"
      />
    </nav>

    <!-- JOBS -->
    <section v-if="activeTab === 'jobs'" class="workspace">
      <Card>
        <template #content>
          <div class="section-head">
            <div>
              <h2>Job Discovery</h2>
              <p>بحث متقدم مع Match Score و Readiness.</p>
            </div>
            <Button
              label="تحليل كل الوظائف"
              icon="pi pi-sparkles"
              text
              @click="analyzeVisibleJobs"
            />
          </div>
          <div class="filters">
            <InputText v-model="filters.q" placeholder="عنوان / شركة / وصف" />
            <InputText v-model="filters.skill" placeholder="Skill slug" />
            <InputText v-model="filters.location" placeholder="Location" />
            <Select
              v-model="filters.remote"
              :options="remoteOptions"
              optionLabel="label"
              optionValue="value"
              placeholder="Remote"
              showClear
            />
            <Select
              v-model="filters.job_type"
              :options="jobTypes"
              optionLabel="label"
              optionValue="value"
              placeholder="Job type"
              showClear
            />
            <Select
              v-model="filters.experience"
              :options="experienceLevels"
              optionLabel="label"
              optionValue="value"
              placeholder="Experience"
              showClear
            />
            <Button label="بحث" icon="pi pi-search" @click="loadJobs" />
          </div>
        </template>
      </Card>

      <div class="job-grid" v-if="jobs.length">
        <Card v-for="job in jobs" :key="job.id" class="job-card">
          <template #content>
            <div class="job-top">
              <div>
                <span class="company">{{ job.company || 'Company not specified' }}</span>
                <h3>{{ job.title }}</h3>
              </div>
              <Tag
                :value="job.match ? `${job.match.score}% Match` : '—'"
                :severity="matchSeverity(job.match?.score)"
              />
            </div>
            <div class="chips">
              <Tag v-if="job.location" :value="job.location" severity="secondary" /><Tag
                :value="job.location_type || (job.is_remote ? 'remote' : 'unknown')"
              /><Tag :value="job.job_type" severity="contrast" />
            </div>
            <p class="summary">{{ job.ai_summary || job.description || 'No description.' }}</p>
            <div class="meter"><div :style="{ width: `${job.match?.score || 0}%` }" /></div>
            <div class="split">
              <span
                >Readiness: <b>{{ job.readiness?.level || 'not calculated' }}</b></span
              ><span>Freshness: {{ job.freshness_score }}%</span>
            </div>
            <div v-if="job.match?.missing_skills?.length" class="gaps">
              <b>Skill gaps:</b
              ><span
                v-for="gap in job.match.missing_skills.slice(0, 4)"
                :key="gap.id || gap.name"
                >{{ gap.name }}</span
              >
            </div>
            <div class="actions-row">
              <Button
                icon="pi pi-sparkles"
                label="Analyze"
                text
                @click="analyzeJobNow(job)"
              /><Button icon="pi pi-refresh" label="Match" text @click="matchJob(job)" /><Button
                icon="pi pi-check"
                label="Apply"
                @click="applyJob(job)"
              /><a v-if="job.url" :href="job.url" target="_blank" rel="noopener">Open ↗</a>
            </div>
          </template>
        </Card>
      </div>
      <div v-else class="empty">مفيش وظائف مطابقة حاليًا. أضف وظيفة أو اعمل Sync للمصادر.</div>
    </section>

    <!-- RECOMMENDATIONS -->
    <section v-if="activeTab === 'recommendations'" class="workspace two-col">
      <Card
        ><template #content
          ><div class="section-head">
            <div>
              <h2>For You</h2>
              <p>اقتراحات مبنية على Skills + Goals + Preferences.</p>
            </div>
            <Button label="Refresh" icon="pi pi-refresh" @click="refreshRecs" />
          </div>
          <div class="list" v-if="recommendations.length">
            <article v-for="rec in recommendations" :key="rec.id" class="list-item">
              <div>
                <b>{{ rec.job_detail?.title }}</b
                ><small>{{ rec.job_detail?.company }}</small>
                <p>{{ (rec.reasons || []).join(' • ') }}</p>
              </div>
              <div class="item-actions">
                <Tag :value="`${rec.score}%`" severity="success" /><Button
                  icon="pi pi-bookmark"
                  text
                  @click="saveRec(rec)"
                /><Button icon="pi pi-times" text @click="dismissRec(rec)" />
              </div>
            </article>
          </div>
          <div v-else class="empty">اضغط Refresh لبناء الـ recommendations.</div></template
        ></Card
      >
      <Card
        ><template #content
          ><h2>Readiness</h2>
          <div class="list">
            <article v-for="row in readiness" :key="row.id" class="list-item">
              <div>
                <b>{{ row.job_title }}</b
                ><small>{{ row.level }}</small>
              </div>
              <Tag :value="`${row.score}%`" :severity="matchSeverity(row.score)" />
            </article></div></template
      ></Card>
    </section>

    <!-- GAPS -->
    <section v-if="activeTab === 'gaps'" class="workspace">
      <Card
        ><template #content
          ><div class="section-head">
            <div>
              <h2>Skill Gap → Learning</h2>
              <p>كل Gap ممكن يتحول مباشرة إلى Learning Goal داخل Learning.</p>
            </div>
            <Button label="Refresh readiness" icon="pi pi-sync" @click="refreshReadinessData" />
          </div>
          <DataTable :value="gaps" paginator :rows="10" stripedRows
            ><Column field="name" header="Skill" /><Column field="job_title" header="Job" /><Column
              field="required_level"
              header="Required" /><Column field="current_level" header="Current" /><Column
              field="severity"
              header="Severity"
              ><template #body="s"
                ><Tag
                  :value="s.data.severity"
                  :severity="gapSeverity(s.data.severity)" /></template></Column
            ><Column field="status" header="Status" /><Column header="Action"
              ><template #body="s"
                ><Button
                  v-if="!s.data.learning_goal"
                  label="Start learning"
                  icon="pi pi-book"
                  text
                  @click="startLearning(s.data)" /><Tag
                  v-else
                  value="Linked to Learning"
                  severity="success" /></template></Column></DataTable></template
      ></Card>
    </section>

    <!-- APPLICATIONS -->
    <section v-if="activeTab === 'applications'" class="workspace">
      <Card
        ><template #content
          ><div class="section-head">
            <div>
              <h2>Application Pipeline</h2>
              <p>Saved → Preparing → Applied → Interview → Offer.</p>
            </div>
            <Button label="Refresh" icon="pi pi-refresh" @click="loadApplications" />
          </div>
          <div class="kanban">
            <div v-for="stage in applicationStages" :key="stage.value" class="lane">
              <h3>
                {{ stage.label }} <Badge :value="String(applicationsByStage(stage.value).length)" />
              </h3>
              <article
                v-for="app in applicationsByStage(stage.value)"
                :key="app.id"
                class="kanban-card"
              >
                <b>{{ app.job_title }}</b
                ><small>{{ app.company }}</small
                ><Select
                  v-model="app.status"
                  :options="applicationStages"
                  optionLabel="label"
                  optionValue="value"
                  @change="changeApplication(app)"
                /><Button
                  label="Timeline"
                  icon="pi pi-history"
                  text
                  size="small"
                  @click="showTimeline(app)"
                />
              </article>
            </div></div></template
      ></Card>
    </section>

    <!-- SOURCES -->
    <section v-if="activeTab === 'sources'" class="workspace two-col">
      <Card
        ><template #content
          ><div class="section-head">
            <div>
              <h2>Sources</h2>
              <p>API / RSS / Manual مع health status و background sync.</p>
            </div>
            <Button label="Add source" icon="pi pi-plus" @click="sourceDialog = true" />
          </div>
          <div class="list">
            <article v-for="source in sources" :key="source.id" class="list-item">
              <div>
                <b>{{ source.name }}</b
                ><small>{{ source.source_type }} · {{ source.last_sync_status }}</small>
                <p>
                  {{ source.last_sync_error || `${source.last_sync_count || 0} jobs imported` }}
                </p>
              </div>
              <div class="item-actions">
                <Button icon="pi pi-play" text @click="syncSourceNow(source)" /><Button
                  icon="pi pi-check-circle"
                  text
                  @click="testSourceNow(source)"
                />
              </div>
            </article></div></template
      ></Card>
      <Card
        ><template #content
          ><h2>Career Preferences</h2>
          <div class="form">
            <InputText
              v-model="preferences.target_titlesText"
              placeholder="Titles: Django Developer, Backend Engineer"
            /><InputText v-model="preferences.locationsText" placeholder="Locations" /><InputNumber
              v-model="preferences.min_salary"
              placeholder="Minimum salary"
            /><Select
              v-model="preferences.remote_preference"
              :options="remotePreferenceOptions"
              optionLabel="label"
              optionValue="value"
            /><Button
              label="Save preferences"
              icon="pi pi-save"
              @click="savePreferences"
            /></div></template
      ></Card>
    </section>

    <!-- ANALYTICS -->
    <section v-if="activeTab === 'analytics'" class="workspace two-col">
      <Card
        ><template #content
          ><h2>Career Analytics</h2>
          <div class="metric-grid">
            <div v-for="item in analyticsCards" :key="item.label">
              <span>{{ item.label }}</span
              ><strong>{{ item.value }}</strong>
            </div>
          </div></template
        ></Card
      >
      <Card
        ><template #content
          ><h2>Top Skills in Your Jobs</h2>
          <div class="skill-bars">
            <div v-for="skill in dashboard?.top_skills || []" :key="skill[0]">
              <span>{{ skill[0] }}</span
              ><ProgressBar :value="Math.min(100, skill[1] * 10)" />
            </div></div></template
      ></Card>
    </section>

    <!-- FEATURES -->
    <section v-if="activeTab === 'features'" class="workspace">
      <Card
        ><template #content
          ><div class="section-head">
            <div>
              <h2>150 Features</h2>
              <p>كل الـ150 Feature لها مكان واضح في الـ Jobs Opportunity OS.</p>
            </div>
            <Tag :value="`${features.length}/150`" severity="success" />
          </div>
          <div class="feature-grid">
            <article v-for="feature in features" :key="feature.id">
              <span>#{{ feature.id }}</span>
              <div>
                <b>{{ feature.name }}</b
                ><small>{{ feature.category }}</small>
              </div>
              <Tag value="Available" severity="success" />
            </article></div></template
      ></Card>
    </section>

    <!-- CREATE JOB -->
    <Dialog
      v-model:visible="dialog"
      modal
      header="إضافة فرصة وظيفية"
      :style="{ width: '680px', maxWidth: '95vw' }"
    >
      <div class="form">
        <InputText v-model="form.title" placeholder="Title" /><InputText
          v-model="form.company"
          placeholder="Company"
        /><InputText v-model="form.url" placeholder="https://..." /><InputText
          v-model="form.location"
          placeholder="Location"
        /><Textarea v-model="form.description" rows="8" placeholder="Job description" /><Select
          v-model="form.job_type"
          :options="jobTypes.filter((x) => x.value)"
          optionLabel="label"
          optionValue="value"
        />
        <div class="check"><Checkbox v-model="form.is_remote" binary /> Remote</div>
      </div>
      <template #footer
        ><Button label="إلغاء" text @click="dialog = false" /><Button
          label="حفظ وتحليل"
          :loading="saving"
          @click="saveJob"
      /></template>
    </Dialog>

    <Dialog
      v-model:visible="sourceDialog"
      modal
      header="Job Source"
      :style="{ width: '620px', maxWidth: '95vw' }"
      ><div class="form">
        <InputText v-model="sourceForm.name" placeholder="Source name" /><Select
          v-model="sourceForm.source_type"
          :options="sourceTypes"
          optionLabel="label"
          optionValue="value"
        /><InputText v-model="sourceForm.feed_url" placeholder="Feed/API URL" /><InputText
          v-model="sourceForm.base_url"
          placeholder="Base URL"
        />
      </div>
      <template #footer
        ><Button label="Cancel" text @click="sourceDialog = false" /><Button
          label="Save"
          @click="saveSource" /></template
    ></Dialog>

    <Dialog
      v-model:visible="timelineDialog"
      modal
      header="Application Timeline"
      :style="{ width: '700px', maxWidth: '95vw' }"
      ><div class="timeline">
        <article v-for="event in timeline" :key="event.id">
          <b>{{ event.title }}</b
          ><small>{{ formatDate(event.occurred_at) }}</small>
          <p>{{ event.note }}</p>
        </article>
      </div></Dialog
    >
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import Button from 'primevue/button'
import Card from 'primevue/card'
import Message from 'primevue/message'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import Textarea from 'primevue/textarea'
import Select from 'primevue/select'
import Checkbox from 'primevue/checkbox'
import Dialog from 'primevue/dialog'
import Tag from 'primevue/tag'
import Badge from 'primevue/badge'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import ProgressBar from 'primevue/progressbar'
import {
  listJobs,
  createJob,
  refreshJobMatch,
  analyzeJob,
  refreshAll,
  getDashboard,
  listRecommendations,
  refreshRecommendations,
  saveRecommendation,
  dismissRecommendation,
  listSkillGaps,
  startSkillLearning,
  listReadiness,
  refreshReadiness,
  listApplications,
  updateApplication,
  applicationTimeline,
  listSources,
  createSource,
  syncSource,
  testSource,
  getPreferences,
  updatePreferences,
  getFeatureCatalog,
} from '@/services/jobs'

const activeTab = ref('jobs')
const busy = ref(false)
const loading = ref(false)
const saving = ref(false)
const error = ref('')
const dialog = ref(false)
const sourceDialog = ref(false)
const timelineDialog = ref(false)
const jobs = ref([])
const recommendations = ref([])
const gaps = ref([])
const readiness = ref([])
const applications = ref([])
const sources = ref([])
const features = ref([])
const dashboard = ref(null)
const timeline = ref([])
const preferences = reactive({
  target_titlesText: '',
  locationsText: '',
  min_salary: null,
  remote_preference: 'any',
})
const filters = reactive({
  q: '',
  skill: '',
  location: '',
  remote: null,
  job_type: null,
  experience: null,
})
const form = reactive({
  title: '',
  company: '',
  url: '',
  location: '',
  description: '',
  job_type: 'full_time',
  is_remote: false,
})
const sourceForm = reactive({ name: '', source_type: 'rss', feed_url: '', base_url: '' })

const tabs = [
  { key: 'jobs', label: 'Jobs', icon: 'pi pi-briefcase' },
  { key: 'recommendations', label: 'For You', icon: 'pi pi-sparkles' },
  { key: 'gaps', label: 'Skill Gaps', icon: 'pi pi-bolt' },
  { key: 'applications', label: 'Applications', icon: 'pi pi-send' },
  { key: 'sources', label: 'Sources & Preferences', icon: 'pi pi-sliders-h' },
  { key: 'analytics', label: 'Analytics', icon: 'pi pi-chart-line' },
  { key: 'features', label: '150 Features', icon: 'pi pi-list' },
]
const remoteOptions = [{ label: 'Remote only', value: 'true' }]
const jobTypes = [
  { label: 'Full time', value: 'full_time' },
  { label: 'Part time', value: 'part_time' },
  { label: 'Contract', value: 'contract' },
  { label: 'Freelance', value: 'freelance' },
  { label: 'Internship', value: 'internship' },
  { label: 'Project', value: 'project' },
  { label: 'Temporary', value: 'temporary' },
]
const experienceLevels = [
  { label: 'Entry', value: 'entry' },
  { label: 'Junior', value: 'junior' },
  { label: 'Mid', value: 'mid' },
  { label: 'Senior', value: 'senior' },
  { label: 'Lead', value: 'lead' },
  { label: 'Executive', value: 'executive' },
]
const sourceTypes = [
  { label: 'RSS', value: 'rss' },
  { label: 'API', value: 'api' },
  { label: 'Manual', value: 'manual' },
]
const remotePreferenceOptions = [
  { label: 'Any', value: 'any' },
  { label: 'Remote', value: 'remote' },
  { label: 'Hybrid', value: 'hybrid' },
  { label: 'On-site', value: 'onsite' },
]
const applicationStages = [
  { label: 'Saved', value: 'saved' },
  { label: 'Preparing', value: 'preparing' },
  { label: 'Applied', value: 'applied' },
  { label: 'Screening', value: 'screening' },
  { label: 'Interview', value: 'interview' },
  { label: 'Technical', value: 'technical' },
  { label: 'Final', value: 'final' },
  { label: 'Offer', value: 'offer' },
  { label: 'Accepted', value: 'accepted' },
  { label: 'Rejected', value: 'rejected' },
]

const statCards = computed(() => [
  { label: 'Jobs', value: dashboard.value?.jobs ?? 0 },
  { label: 'Active', value: dashboard.value?.active_jobs ?? 0 },
  { label: 'Applied', value: dashboard.value?.applied ?? 0 },
  { label: 'Interviews', value: dashboard.value?.interviews ?? 0 },
  { label: 'Offers', value: dashboard.value?.offers ?? 0 },
  { label: 'Conversion', value: `${dashboard.value?.application_conversion_rate ?? 0}%` },
])
const analyticsCards = computed(() => [
  {
    label: 'Application conversion',
    value: `${dashboard.value?.application_conversion_rate ?? 0}%`,
  },
  { label: 'Interview rate', value: `${dashboard.value?.interview_rate ?? 0}%` },
  { label: 'Offer rate', value: `${dashboard.value?.offer_rate ?? 0}%` },
  { label: 'Remote jobs', value: dashboard.value?.remote_jobs ?? 0 },
  { label: 'Avg salary min', value: dashboard.value?.avg_salary_min ?? '—' },
  { label: 'Rejected', value: dashboard.value?.rejected ?? 0 },
])

function matchSeverity(score) {
  return score >= 85 ? 'success' : score >= 65 ? 'warn' : score >= 45 ? 'info' : 'danger'
}
function gapSeverity(value) {
  return value === 'critical'
    ? 'danger'
    : value === 'high'
      ? 'warn'
      : value === 'medium'
        ? 'info'
        : 'secondary'
}
function formatDate(value) {
  return value ? new Date(value).toLocaleString() : '—'
}
function applicationsByStage(stage) {
  return applications.value.filter((x) => x.status === stage)
}
function showError(e, fallback) {
  error.value = e?.response?.data?.detail || fallback
}

async function loadJobs() {
  loading.value = true
  try {
    jobs.value = await listJobs(
      Object.fromEntries(Object.entries(filters).filter(([, v]) => v !== null && v !== '')),
    )
  } catch (e) {
    showError(e, 'تعذر تحميل الوظائف.')
  } finally {
    loading.value = false
  }
}
async function loadDashboard() {
  dashboard.value = await getDashboard()
}
async function loadAll() {
  await Promise.all([
    loadJobs(),
    loadDashboard(),
    loadSources(),
    loadPreferences(),
    loadFeatures(),
    loadGaps(),
    loadReadinessData(),
    loadApplications(),
    loadRecommendations(),
  ])
}
async function loadSources() {
  sources.value = await listSources()
}
async function loadPreferences() {
  const p = await getPreferences()
  preferences.target_titlesText = (p.target_titles || []).join(', ')
  preferences.locationsText = (p.locations || []).join(', ')
  preferences.min_salary = p.min_salary
  preferences.remote_preference = p.remote_preference || 'any'
}
async function loadFeatures() {
  const data = await getFeatureCatalog()
  features.value = data.features || []
}
async function loadGaps() {
  gaps.value = await listSkillGaps()
}
async function loadReadinessData() {
  readiness.value = await listReadiness()
}
async function loadApplications() {
  applications.value = await listApplications()
}
async function loadRecommendations() {
  recommendations.value = await listRecommendations()
}

async function refreshAllData() {
  busy.value = true
  try {
    await refreshAll()
    await loadAll()
  } catch (e) {
    showError(e, 'تعذر تحديث مساحة الوظائف.')
  } finally {
    busy.value = false
  }
}
async function refreshRecs() {
  try {
    recommendations.value = await refreshRecommendations()
  } catch (e) {
    showError(e, 'تعذر بناء التوصيات.')
  }
}
async function refreshReadinessData() {
  try {
    readiness.value = await refreshReadiness()
    await loadGaps()
  } catch (e) {
    showError(e, 'تعذر تحديث الجاهزية.')
  }
}
async function matchJob(job) {
  try {
    await refreshJobMatch(job.id)
    await loadJobs()
  } catch (e) {
    showError(e, 'تعذر حساب الـ Match.')
  }
}
async function analyzeJobNow(job) {
  try {
    await analyzeJob(job.id)
    await loadJobs()
  } catch (e) {
    showError(e, 'تعذر تحليل الوظيفة.')
  }
}
async function analyzeVisibleJobs() {
  for (const job of jobs.value) {
    try {
      await analyzeJob(job.id)
    } catch {}
  }
  await loadJobs()
}
async function applyJob(job) {
  try {
    await fetchApply(job.id)
    await loadApplications()
    await loadDashboard()
  } catch (e) {
    showError(e, 'تعذر تسجيل التقديم.')
  }
}
async function fetchApply(id) {
  const { applyToJob } = await import('@/services/jobs')
  return applyToJob(id, { status: 'applied' })
}
async function startLearning(gap) {
  try {
    await startSkillLearning(gap.id)
    await loadGaps()
  } catch (e) {
    showError(e, 'تعذر إنشاء Learning Goal.')
  }
}
async function saveRec(rec) {
  try {
    await saveRecommendation(rec.id)
    rec.is_saved = true
  } catch (e) {
    showError(e, 'تعذر حفظ التوصية.')
  }
}
async function dismissRec(rec) {
  try {
    await dismissRecommendation(rec.id)
    recommendations.value = recommendations.value.filter((x) => x.id !== rec.id)
  } catch (e) {
    showError(e, 'تعذر إخفاء التوصية.')
  }
}
async function changeApplication(app) {
  try {
    await updateApplication(app.id, { status: app.status })
  } catch (e) {
    showError(e, 'تعذر تحديث حالة التقديم.')
  }
}
async function showTimeline(app) {
  try {
    timeline.value = await applicationTimeline(app.id)
    timelineDialog.value = true
  } catch (e) {
    showError(e, 'تعذر تحميل الـ timeline.')
  }
}
async function syncSourceNow(source) {
  try {
    await syncSource(source.id)
    await loadSources()
  } catch (e) {
    showError(e, 'تعذر تشغيل الـ sync.')
  }
}
async function testSourceNow(source) {
  try {
    await testSource(source.id)
  } catch (e) {
    showError(e, 'المصدر غير جاهز.')
  }
}
async function saveSource() {
  try {
    await createSource(sourceForm)
    sourceDialog.value = false
    Object.assign(sourceForm, { name: '', source_type: 'rss', feed_url: '', base_url: '' })
    await loadSources()
  } catch (e) {
    showError(e, 'تعذر حفظ المصدر.')
  }
}
async function savePreferences() {
  try {
    await updatePreferences({
      target_titles: preferences.target_titlesText
        .split(',')
        .map((x) => x.trim())
        .filter(Boolean),
      locations: preferences.locationsText
        .split(',')
        .map((x) => x.trim())
        .filter(Boolean),
      min_salary: preferences.min_salary,
      remote_preference: preferences.remote_preference,
    })
    await refreshAllData()
  } catch (e) {
    showError(e, 'تعذر حفظ التفضيلات.')
  }
}
function openCreate() {
  Object.assign(form, {
    title: '',
    company: '',
    url: '',
    location: '',
    description: '',
    job_type: 'full_time',
    is_remote: false,
  })
  dialog.value = true
}
async function saveJob() {
  saving.value = true
  try {
    await createJob(form)
    dialog.value = false
    await loadJobs()
    await loadDashboard()
  } catch (e) {
    showError(e, 'تعذر إنشاء الوظيفة.')
  } finally {
    saving.value = false
  }
}

onMounted(loadAll)
</script>

<style scoped>
.jobs-page {
  max-width: 1500px;
  margin: auto;
  padding: 28px;
}
.hero {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  align-items: flex-end;
  margin-bottom: 22px;
}
.eyebrow {
  font-size: 11px;
  letter-spacing: 0.18em;
  color: #60a5fa;
}
.hero h1 {
  font-size: 38px;
  margin: 7px 0;
}
.hero p {
  color: #94a3b8;
  margin: 0;
}
.hero-actions,
.tabs,
.filters,
.actions-row,
.chips,
.split,
.item-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}
.stats {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 12px;
  margin-bottom: 18px;
}
.stat-card span,
.metric-grid span,
small {
  display: block;
  color: #94a3b8;
  font-size: 12px;
}
.stat-card strong {
  display: block;
  font-size: 28px;
  margin-top: 5px;
}
.tabs {
  flex-wrap: wrap;
  margin-bottom: 18px;
}
.workspace {
  display: grid;
  gap: 16px;
}
.two-col {
  grid-template-columns: 1.35fr 0.8fr;
}
.section-head {
  display: flex;
  justify-content: space-between;
  gap: 15px;
  align-items: center;
  margin-bottom: 16px;
}
.section-head h2 {
  margin: 0;
}
.section-head p {
  margin: 5px 0 0;
  color: #94a3b8;
}
.filters {
  flex-wrap: wrap;
}
.filters .p-inputtext {
  min-width: 180px;
}
.job-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}
.job-card h3 {
  margin: 5px 0 10px;
}
.company {
  color: #60a5fa;
  font-size: 13px;
}
.job-top {
  display: flex;
  justify-content: space-between;
  gap: 12px;
}
.chips {
  flex-wrap: wrap;
  margin-bottom: 12px;
}
.summary {
  color: #cbd5e1;
  line-height: 1.55;
  min-height: 70px;
}
.meter {
  height: 7px;
  background: #1e293b;
  border-radius: 99px;
  overflow: hidden;
}
.meter div {
  height: 100%;
  background: #60a5fa;
}
.split {
  justify-content: space-between;
  font-size: 12px;
  color: #94a3b8;
  margin: 9px 0;
}
.gaps {
  display: flex;
  gap: 5px;
  flex-wrap: wrap;
  font-size: 11px;
}
.gaps span {
  padding: 3px 7px;
  border-radius: 999px;
  background: #451a1a;
  color: #fecaca;
}
.actions-row {
  flex-wrap: wrap;
  margin-top: 14px;
}
.actions-row a {
  color: #60a5fa;
  text-decoration: none;
}
.list {
  display: grid;
  gap: 8px;
}
.list-item {
  display: flex;
  justify-content: space-between;
  gap: 15px;
  padding: 13px;
  border: 1px solid rgba(148, 163, 184, 0.12);
  border-radius: 12px;
}
.list-item p {
  margin: 6px 0;
  color: #cbd5e1;
}
.metric-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}
.metric-grid > div {
  padding: 16px;
  border-radius: 12px;
  background: rgba(148, 163, 184, 0.06);
}
.metric-grid strong {
  font-size: 25px;
}
.kanban {
  display: grid;
  grid-template-columns: repeat(5, minmax(180px, 1fr));
  gap: 10px;
  overflow: auto;
}
.lane {
  background: rgba(148, 163, 184, 0.05);
  padding: 10px;
  border-radius: 12px;
  min-width: 180px;
}
.lane h3 {
  font-size: 13px;
}
.kanban-card {
  background: var(--surface-card);
  padding: 10px;
  border-radius: 10px;
  margin-bottom: 8px;
  display: grid;
  gap: 7px;
}
.kanban-card .p-select {
  width: 100%;
}
.feature-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}
.feature-grid article {
  display: grid;
  grid-template-columns: 35px 1fr auto;
  gap: 10px;
  align-items: center;
  padding: 11px;
  border: 1px solid rgba(148, 163, 184, 0.12);
  border-radius: 10px;
}
.feature-grid article > span {
  font-size: 11px;
  color: #60a5fa;
}
.feature-grid small {
  margin-top: 2px;
}
.form {
  display: grid;
  gap: 12px;
}
.form .p-inputtext,
.form .p-select,
.form .p-inputnumber,
.form .p-textarea {
  width: 100%;
}
.check {
  display: flex;
  align-items: center;
  gap: 8px;
}
.skill-bars {
  display: grid;
  gap: 13px;
}
.timeline {
  display: grid;
  gap: 10px;
}
.timeline article {
  padding: 12px;
  border-left: 3px solid #60a5fa;
  background: rgba(148, 163, 184, 0.05);
}
.empty {
  text-align: center;
  padding: 60px;
  color: #94a3b8;
  border: 1px dashed rgba(148, 163, 184, 0.25);
  border-radius: 14px;
}
@media (max-width: 1200px) {
  .stats {
    grid-template-columns: repeat(3, 1fr);
  }
  .job-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .feature-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (max-width: 800px) {
  .jobs-page {
    padding: 16px;
  }
  .hero {
    flex-direction: column;
    align-items: stretch;
  }
  .two-col {
    grid-template-columns: 1fr;
  }
  .job-grid,
  .feature-grid {
    grid-template-columns: 1fr;
  }
  .stats {
    grid-template-columns: repeat(2, 1fr);
  }
  .metric-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
