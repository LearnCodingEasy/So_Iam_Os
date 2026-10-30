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
    <Message v-if="notice" severity="success" closable @close="notice = ''">{{ notice }}</Message>

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
            <Button label="(?) شرح" icon="pi pi-question-circle" text @click="helpDialog = true" />
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

      <Message v-if="loading" severity="info" :closable="false">جاري تحميل الوظائف...</Message>
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
                icon="pi pi-envelope"
                label="Cover letter"
                text
                :loading="generatingLetterFor === job.id"
                @click="generateLetter(job)"
              /><Button icon="pi pi-check" label="Apply" @click="applyJob(job)" /><a
                v-if="job.url"
                :href="job.url"
                target="_blank"
                rel="noopener"
                >Open ↗</a
              >
            </div>
          </template>
        </Card>
      </div>
      <div v-else-if="!loading" class="empty">
        مفيش وظائف مطابقة حاليًا. أضف وظيفة أو اعمل Sync للمصادر.
      </div>
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
            <Button label="Sync all enabled" icon="pi pi-sync" severity="secondary" @click="syncAllEnabledSources" />
            <Button
              label="Scraper Builder"
              icon="pi pi-code"
              severity="secondary"
              @click="openScraperBuilder"
            />
          </div>
          <div class="list">
            <article v-for="source in sources" :key="source.id" class="list-item">
              <div>
                <b>{{ source.name }}</b
                ><small>{{ source.source_type }} · {{ source.enabled ? 'enabled' : 'disabled' }} · {{ source.last_sync_status }}</small>
                <p>
                  {{ source.last_sync_error || `${source.last_sync_count || 0} jobs imported` }}
                </p>
              </div>
              <div class="item-actions">
                <Button icon="pi pi-pencil" text v-tooltip.top="'Edit source'" @click="editSource(source)" />
                <Button
                  icon="pi pi-play"
                  text
                  v-tooltip.top="'Sync source'"
                  :disabled="!source.enabled"
                  @click="syncSourceNow(source)"
                />
                <Button
                  icon="pi pi-check-circle"
                  text
                  v-tooltip.top="'Test source'"
                  @click="testSourceNow(source)"
                />
                <Button
                  v-if="source.source_type === 'scraper'"
                  icon="pi pi-eye"
                  text
                  v-tooltip.top="'Preview scraper'"
                  @click="previewSourceNow(source)"
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

    <!-- AI COVER LETTER -->
    <Dialog
      v-model:visible="letterDialog"
      modal
      header="AI Cover Letter"
      :style="{ width: '760px', maxWidth: '95vw' }"
    >
      <p v-if="generatedLetter" class="helper-note">
        تم إنشاء الخطاب باستخدام مزود الذكاء الاصطناعي المضبوط في إعدادات AI. راجعه وعدّله قبل
        الإرسال.
      </p>
      <Textarea
        v-model="generatedLetter"
        rows="16"
        autoResize
        class="letter-editor"
        placeholder="سيظهر الخطاب هنا..."
      />
      <template #footer>
        <Button label="نسخ الخطاب" icon="pi pi-copy" text @click="copyLetter" />
        <Button label="إغلاق" @click="letterDialog = false" />
      </template>
    </Dialog>

    <Dialog
      v-model:visible="helpDialog"
      modal
      header="شرح مطابقة الوظائف وخطاب التقديم"
      :style="{ width: '600px', maxWidth: '95vw' }"
    >
      <div class="jobs-help-content">
        <h3>Resume / Job Matching</h3>
        <p>
          يعتمد التوافق على بيانات المهارات والتفضيلات والوظيفة المتاحة في حسابك. النتيجة مؤشر مساعد
          وليست ضمانًا لقبولك.
        </p>
        <h3>Cover Letter</h3>
        <p>
          يتم إرسال وصف الوظيفة ومحتوى السيرة الذاتية المختارة إلى مزود AI الذي ضبطته في إعدادات
          التطبيق. الخطاب الناتج يُحفظ في سجل خطاباتك؛ راجعه للتأكد من دقته قبل استخدامه.
        </p>
        <h3>بيانات الطلب</h3>
        <p>
          المسار يستخدم معرّف الوظيفة، واختياريًا resume_id وcontext. الوصول محصور في الوظائف والسير
          الذاتية التابعة لحسابك.
        </p>
      </div>
    </Dialog>

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
        <div class="check"><Checkbox v-model="sourceForm.enabled" binary /> Enable source after reviewing its URL and terms</div>
        <div class="check"><Checkbox v-model="sourceForm.ai_analyze_on_import" binary /> Analyze each imported job with AI (uses provider quota)</div>
        <div v-if="sourceForm.source_type !== 'scraper'" class="source-config">
          <Textarea v-model="sourceForm.config_json" rows="5" placeholder='{"adapter":"remotive","ai_analyze_on_import":false}' />
          <small>Adapter config JSON. Supported adapters include remotive, arbeitnow, jobicy, greenhouse, and lever.</small>
        </div>
        <div v-if="sourceForm.source_type === 'scraper'" class="scraper-builder">
          <Message severity="warn" :closable="false"
            >لا تستخدم Scraper إلا مع مصادر تسمح بذلك. النظام سيتحقق من robots.txt ولن يتجاوز
            CAPTCHA أو تسجيل الدخول.</Message
          >
          <InputText v-model="scraperForm.card" placeholder="Job card CSS selector" />
          <InputText v-model="scraperForm.title" placeholder="Title CSS selector" />
          <InputText v-model="scraperForm.company" placeholder="Company CSS selector" />
          <InputText v-model="scraperForm.location" placeholder="Location CSS selector" />
          <InputText v-model="scraperForm.description" placeholder="Description CSS selector" />
          <InputText v-model="scraperForm.url" placeholder="URL CSS selector" />
          <InputText v-model="scraperForm.urlAttribute" placeholder="URL attribute (href)" />
          <div class="check">
            <Checkbox v-model="scraperForm.termsConfirmed" binary /> I confirm this source permits
            scraping
          </div>
        </div>
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
import '@/assets/scss/Jobs/JobsView.scss'
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
  updateSource,
  syncSource,
  syncAllSources,
  testSource,
  getPreferences,
  updatePreferences,
  getFeatureCatalog,
  generateCoverLetter,
} from '@/services/jobs'

const activeTab = ref('jobs')
const busy = ref(false)
const loading = ref(false)
const saving = ref(false)
const error = ref('')
const notice = ref('')
const dialog = ref(false)
const sourceDialog = ref(false)
const timelineDialog = ref(false)
const letterDialog = ref(false)
const helpDialog = ref(false)
const generatedLetter = ref('')
const generatingLetterFor = ref(null)
const currentLetterJob = ref(null)
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
const sourceForm = reactive({ id: null, name: '', source_type: 'rss', feed_url: '', base_url: '', enabled: false, ai_analyze_on_import: false, config_json: '{}' })
const scraperForm = reactive({
  card: '',
  title: '',
  company: '',
  location: '',
  description: '',
  url: '',
  urlAttribute: 'href',
  termsConfirmed: false,
})

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
  { label: 'HTML Scraper', value: 'scraper' },
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
  const data = e?.response?.data
  if (typeof data === 'string') {
    error.value = data || fallback
    return
  }
  if (data?.detail) {
    error.value = data.detail
    return
  }
  if (data && typeof data === 'object') {
    const messages = Object.entries(data).flatMap(([field, value]) => {
      const values = Array.isArray(value) ? value : [value]
      return values.map((message) => `${field}: ${String(message)}`)
    })
    error.value = messages.join(' · ') || fallback
    return
  }
  error.value = fallback
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
  const results = await Promise.allSettled([
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
  const failed = results.find((result) => result.status === 'rejected')
  if (failed) showError(failed.reason, 'تعذر تحميل بعض بيانات مساحة الوظائف.')
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
async function generateLetter(job) {
  generatingLetterFor.value = job.id
  currentLetterJob.value = job
  try {
    const letter = await generateCoverLetter(job.id)
    generatedLetter.value = letter.content || ''
    letterDialog.value = true
  } catch (e) {
    showError(e, 'تعذر إنشاء خطاب التقديم. تحقق من إعدادات مزود AI والسيرة الذاتية.')
  } finally {
    generatingLetterFor.value = null
  }
}
async function copyLetter() {
  try {
    await navigator.clipboard.writeText(generatedLetter.value)
  } catch {
    showError(null, 'تعذر النسخ التلقائي؛ يمكنك تحديد النص ونسخه يدويًا.')
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
  if (!jobs.value.length) return
  busy.value = true
  let failedCount = 0
  try {
    for (const job of jobs.value) {
      try {
        await analyzeJob(job.id)
      } catch (e) {
        failedCount += 1
        showError(e, `تعذر تحليل الوظيفة: ${job.title || job.id}`)
      }
    }
    await loadJobs()
    if (failedCount === 0) error.value = ''
    else
      error.value = `تعذر تحليل ${failedCount} من ${jobs.value.length} وظيفة. راجع الأخطاء المعروضة وأعد المحاولة.`
  } finally {
    busy.value = false
  }
}
async function applyJob(job) {
  try {
    await fetchApply(job.id)
    await loadApplications()
    await loadDashboard()
    notice.value = `تم تسجيل التقديم على: ${job.title}.`
    error.value = ''
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
async function syncAllEnabledSources() {
  busy.value = true
  try {
    const result = await syncAllSources()
    notice.value = `تم وضع ${result.queued || 0} مصدر في قائمة المزامنة.`
    if (result.failures?.length) error.value = `تعذر جدولة ${result.failures.length} مصدر.`
    else error.value = ''
    await loadSources()
  } catch (e) { showError(e, 'تعذر تشغيل مزامنة جميع المصادر. تحقق من Celery/Redis وحالة المصادر.') }
  finally { busy.value = false }
}

async function syncSourceNow(source) {
  try {
    const result = await syncSource(source.id)
    notice.value = result.queued
      ? `تم وضع مزامنة ${source.name} في قائمة التنفيذ.`
      : `تم تنفيذ مزامنة ${source.name}.`
    error.value = ''
    await loadSources()
  } catch (e) {
    showError(e, 'تعذر تشغيل الـ sync.')
  }
}
async function previewSourceNow(source) {
  try {
    const { previewSource } = await import('@/services/jobs')
    const result = await previewSource(source.id)
    notice.value = `اكتملت معاينة المصدر ${source.name}: ${result.items?.length || 0} وظيفة.`
    error.value = ''
  } catch (e) {
    showError(e, 'تعذر معاينة المصدر.')
  }
}
async function testSourceNow(source) {
  try {
    const result = await testSource(source.id)
    error.value = result.ok
      ? ''
      : result.detail || result.message || 'فشل اختبار المصدر؛ راجع إعداداته وصلاحية الوصول.'
    notice.value = result.ok ? `اجتاز المصدر ${source.name} اختبار الاتصال؛ ${result.items_found ?? 0} عناصر مكتشفة.` : ''
    if (!result.ok) return
  } catch (e) {
    showError(e, 'المصدر غير جاهز.')
  }
}
function editSource(source) {
  Object.assign(sourceForm, {
    id: source.id, name: source.name || '', source_type: source.source_type || 'rss',
    feed_url: source.feed_url || '', base_url: source.base_url || '',
    enabled: Boolean(source.enabled), ai_analyze_on_import: Boolean(source.config?.ai_analyze_on_import),
    config_json: JSON.stringify(source.config || {}, null, 2),
  })
  const config = source.config || {}
  Object.assign(scraperForm, {
    card: config.card?.selector || '', title: config.title?.selector || '',
    company: config.company?.selector || '', location: config.location?.selector || '',
    description: config.description?.selector || '', url: config.url?.selector || '',
    urlAttribute: config.url?.attribute || 'href', termsConfirmed: Boolean(config.terms_confirmed),
  })
  sourceDialog.value = true
}

async function openScraperBuilder() {
  Object.assign(sourceForm, { id: null, name: '', source_type: 'scraper', feed_url: '', base_url: '', enabled: false, ai_analyze_on_import: false, config_json: '{}' })
  Object.assign(scraperForm, {
    card: '',
    title: '',
    company: '',
    location: '',
    description: '',
    url: '',
    urlAttribute: 'href',
    termsConfirmed: false,
  })
  sourceDialog.value = true
}
async function saveSource() {
  try {
    const payload = {
      name: sourceForm.name.trim(), source_type: sourceForm.source_type,
      base_url: sourceForm.base_url.trim(), feed_url: sourceForm.source_type === 'scraper' ? '' : sourceForm.feed_url.trim(),
      enabled: Boolean(sourceForm.enabled),
    }
    if (sourceForm.source_type === 'scraper') {
      if (!scraperForm.termsConfirmed) throw new Error('Confirm that this source permits scraping before saving it.')
      if (!scraperForm.card.trim() || !scraperForm.title.trim() || !scraperForm.url.trim())
        throw new Error('Card, title, and URL selectors are required for an HTML scraper source.')
      payload.config = {
        terms_confirmed: true, robots_required: true, rate_limit_seconds: 1,
        ai_analyze_on_import: Boolean(sourceForm.ai_analyze_on_import),
        card: { selector: scraperForm.card }, title: { selector: scraperForm.title },
        company: { selector: scraperForm.company }, location: { selector: scraperForm.location },
        description: { selector: scraperForm.description },
        url: { selector: scraperForm.url, attribute: scraperForm.urlAttribute || 'href' },
      }
    } else {
      try {
        payload.config = JSON.parse(sourceForm.config_json || '{}')
        if (!payload.config || Array.isArray(payload.config) || typeof payload.config !== 'object') throw new Error('Source config must be a JSON object.')
        payload.config.ai_analyze_on_import = Boolean(sourceForm.ai_analyze_on_import)
      } catch (e) { throw new Error(e.message || 'Source config JSON is invalid.') }
    }
    if (sourceForm.id) await updateSource(sourceForm.id, payload)
    else await createSource(payload)
    sourceDialog.value = false
    Object.assign(sourceForm, { id: null, name: '', source_type: 'rss', feed_url: '', base_url: '', enabled: false, ai_analyze_on_import: false, config_json: '{}' })
    await loadSources()
    error.value = ''
    notice.value = 'تم حفظ إعدادات المصدر.'
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
    notice.value = 'تمت إضافة الوظيفة بنجاح.'
    error.value = ''
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
