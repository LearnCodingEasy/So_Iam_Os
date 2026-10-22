<template>
  <main class="scraper-page">
    <header class="scraper-header">
      <div>
        <p class="eyebrow">SO_IAM_OS · DATA PIPELINE</p>
        <h1>Scraper Engine</h1>
        <p class="subtitle">Manage public sources, validate connections, and monitor collection runs.</p>
      </div>
      <button class="primary-button" @click="openCreate">＋ Add source</button>
    </header>

    <section class="stats-grid" aria-label="Scraper statistics">
      <article class="stat-card"><span>Sources</span><strong>{{ stats.sources_total ?? '—' }}</strong></article>
      <article class="stat-card"><span>Enabled</span><strong>{{ stats.sources_active ?? '—' }}</strong></article>
      <article class="stat-card"><span>Collected items</span><strong>{{ stats.items_scraped ?? '—' }}</strong></article>
      <article class="stat-card"><span>Failed runs</span><strong>{{ stats.runs_failed ?? '—' }}</strong></article>
    </section>

    <p v-if="error" class="notice error" role="alert">{{ error }}</p>
    <p v-if="message" class="notice success" role="status">{{ message }}</p>

    <section class="panel">
      <div class="panel-heading">
        <div><h2>Sources</h2><p>Only use sources you are authorized to access.</p></div>
        <button class="secondary-button" :disabled="loading" @click="refresh">↻ Refresh</button>
      </div>
      <div v-if="loading" class="empty-state">Loading sources…</div>
      <div v-else-if="sources.length === 0" class="empty-state">No sources yet. Add a public API, RSS feed, or permitted HTML source.</div>
      <div v-else class="table-wrap">
        <table>
          <thead><tr><th>Source</th><th>Type</th><th>Status</th><th>Last run</th><th>Actions</th></tr></thead>
          <tbody>
            <tr v-for="source in sources" :key="source.id">
              <td><strong>{{ source.name }}</strong><a :href="source.base_url" target="_blank" rel="noopener noreferrer">{{ source.base_url }}</a></td>
              <td><span class="type-chip">{{ source.source_type }}</span></td>
              <td><span class="status-chip" :class="source.last_status || 'never'">{{ source.last_status || 'never run' }}</span></td>
              <td>{{ formatDate(source.last_run_at) }}<small v-if="source.last_error" class="row-error">{{ source.last_error }}</small></td>
              <td class="actions">
                <button class="small-button" :disabled="busyId === source.id" @click="testSource(source)">Test</button>
                <button class="small-button" :disabled="busyId === source.id || !source.is_active" @click="runSource(source)">Run</button>
                <button class="small-button" @click="editSource(source)">Edit</button>
                <button class="small-button danger-button" @click="removeSource(source)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <section class="panel">
      <div class="panel-heading"><div><h2>Recent runs</h2><p>Execution history returned by the backend.</p></div></div>
      <div v-if="runs.length === 0" class="empty-state">No collection runs recorded yet.</div>
      <div v-else class="runs-list">
        <article v-for="run in runs" :key="run.id" class="run-row">
          <div><strong>{{ run.website_name }}</strong><span>{{ formatDate(run.started_at) }}</span></div>
          <span class="status-chip" :class="run.status">{{ run.status }}</span>
          <span>{{ run.items_scraped }} items</span>
          <small v-if="run.error_message" class="row-error">{{ run.error_message }}</small>
        </article>
      </div>
    </section>

    <div v-if="dialogOpen" class="modal-backdrop" @click.self="dialogOpen = false">
      <form class="source-dialog" @submit.prevent="saveSource">
        <div class="panel-heading"><div><h2>{{ editingId ? 'Edit source' : 'Add source' }}</h2><p>Credentials are not accepted in source URLs or config.</p></div><button type="button" class="icon-button" @click="dialogOpen = false">×</button></div>
        <label>Source name<input v-model.trim="form.name" required maxlength="200" /></label>
        <label>Public URL<input v-model.trim="form.base_url" required type="url" placeholder="https://example.org/feed.json" /></label>
        <label>Connector type<select v-model="form.source_type"><option value="json">JSON / REST API</option><option value="rss">RSS / Atom</option><option value="html">Public HTML</option></select></label>
        <label>Description<textarea v-model="form.description" rows="2" /></label>
        <label v-if="form.source_type === 'json'">Items path (optional)<input v-model="form.config.items_path" placeholder="data.results" /></label>
        <template v-if="form.source_type === 'html'">
          <label>CSS selector for each item<input v-model="form.config.item_selector" placeholder=".job-card" /></label>
          <p class="form-help">Optional fields map: enter JSON in Advanced config only if you know the source markup.</p>
        </template>
        <label class="checkbox-label"><input v-model="form.is_active" type="checkbox" /> Source enabled</label>
        <div class="dialog-actions"><button type="button" class="secondary-button" @click="dialogOpen = false">Cancel</button><button class="primary-button" type="submit" :disabled="saving">{{ saving ? 'Saving…' : 'Save source' }}</button></div>
      </form>
    </div>
  </main>
</template>

<script setup>
import { onMounted, onUnmounted, reactive, ref } from 'vue'
import { scraperApi } from '@/services/scraperApi'

const sources = ref([])
const runs = ref([])
const stats = ref({})
const loading = ref(false)
const saving = ref(false)
const busyId = ref(null)
const error = ref('')
const message = ref('')
const dialogOpen = ref(false)
const editingId = ref(null)
const form = reactive({ name: '', base_url: '', description: '', source_type: 'json', is_active: true, config: { items_path: '', item_selector: '' } })
let refreshTimer

function normalizeList(data) { return Array.isArray(data) ? data : (data?.results || []) }
function clearMessages() { error.value = ''; message.value = '' }
async function refresh() {
  loading.value = true
  error.value = ''
  try {
    const [sourceData, runData, statData] = await Promise.all([scraperApi.sources(), scraperApi.runs(), scraperApi.stats()])
    sources.value = normalizeList(sourceData)
    runs.value = normalizeList(runData).slice(0, 12)
    stats.value = statData
  } catch (e) {
    error.value = e?.response?.data?.detail || 'Could not load scraper data. Check API availability and your login.'
  } finally { loading.value = false }
}
function openCreate() {
  editingId.value = null
  Object.assign(form, { name: '', base_url: '', description: '', source_type: 'json', is_active: true, config: { items_path: '', item_selector: '' } })
  dialogOpen.value = true
}
function editSource(source) {
  editingId.value = source.id
  Object.assign(form, { ...source, config: { items_path: source.config?.items_path || '', item_selector: source.config?.item_selector || '' } })
  dialogOpen.value = true
}
async function saveSource() {
  saving.value = true; clearMessages()
  const config = {}
  if (form.source_type === 'json' && form.config.items_path.trim()) config.items_path = form.config.items_path.trim()
  if (form.source_type === 'html' && form.config.item_selector.trim()) config.item_selector = form.config.item_selector.trim()
  const payload = { name: form.name, base_url: form.base_url, description: form.description, source_type: form.source_type, is_active: form.is_active, config }
  try {
    if (editingId.value) await scraperApi.updateSource(editingId.value, payload)
    else await scraperApi.createSource(payload)
    dialogOpen.value = false; message.value = editingId.value ? 'Source updated.' : 'Source created.'
    await refresh()
  } catch (e) { error.value = e?.response?.data?.base_url?.[0] || e?.response?.data?.detail || 'Could not save source.' }
  finally { saving.value = false }
}
async function testSource(source) {
  busyId.value = source.id; clearMessages()
  try { const result = await scraperApi.testSource(source.id); message.value = `Connection succeeded (${result.status_code}; ${result.bytes} bytes).` }
  catch (e) { error.value = e?.response?.data?.error || e?.response?.data?.detail || 'Connection test failed.' }
  finally { busyId.value = null }
}
async function runSource(source) {
  busyId.value = source.id; clearMessages()
  try { const result = await scraperApi.runSource(source.id); message.value = result.task_id ? `Collection queued (${result.task_id}).` : 'Collection run submitted.'; await refresh() }
  catch (e) { error.value = e?.response?.data?.detail || 'Could not start collection. Ensure the Celery worker and broker are running.'; await refresh() }
  finally { busyId.value = null }
}
async function removeSource(source) {
  if (!window.confirm(`Delete "${source.name}"? Sources with run history will be disabled instead.`)) return
  clearMessages()
  try { await scraperApi.deleteSource(source.id); message.value = 'Source deleted or disabled.'; await refresh() }
  catch (e) { error.value = e?.response?.data?.detail || 'Could not delete source.' }
}
function formatDate(value) { return value ? new Date(value).toLocaleString() : '—' }
onMounted(() => { refresh(); refreshTimer = window.setInterval(refresh, 20000) })
onUnmounted(() => window.clearInterval(refreshTimer))
</script>

<style src="@/assets/scss/Scraper/ScraperView.scss" lang="scss"></style>
